import pytest

from ai.app.evaluation import (
    EvaluationReportStore,
    ModelEvaluator,
    ProductionPromotionGate,
    RegressionTester,
    model_evaluator,
    promotion_gate,
    regression_tester,
    report_store,
)


@pytest.mark.asyncio
async def test_1_dataset_loading_all_10_domains():
    evaluator = ModelEvaluator()

    datasets = [
        "financial_qa.json",
        "underwriting_explanations.json",
        "fraud_signals.json",
        "document_extraction.json",
        "hindi_queries.json",
        "english_queries.json",
        "hinglish_queries.json",
        "policy_reasoning.json",
        "rag_grounding.json",
        "agent_behaviour_analysis.json",
    ]

    for ds_file in datasets:
        items = evaluator.load_dataset(ds_file)
        assert len(items) >= 1, f"Dataset '{ds_file}' should contain at least 1 test case."


@pytest.mark.asyncio
async def test_2_evaluation_execution_and_11_metrics():
    evaluator = ModelEvaluator()

    eval_result = await evaluator.evaluate_dataset(
        dataset_filename="financial_qa.json",
        model_id="gemini-3.6-flash",
        model_version="v1.0",
        prompt_version="v1.0",
    )

    assert eval_result["dataset"] == "financial_qa.json"
    metrics = eval_result["metrics"]

    # Verify all 11 core metrics are present
    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1" in metrics
    assert "confidence_calibration_ece" in metrics
    assert "avg_latency_ms" in metrics
    assert "p50_latency_ms" in metrics
    assert "p95_latency_ms" in metrics
    assert "cost_usd" in metrics
    assert "hallucination_rate" in metrics
    assert "grounding_rate" in metrics
    assert "structured_output_validity" in metrics
    assert "security_failures" in metrics

    # Accuracy must be high for deterministic engine
    assert metrics["accuracy"] >= 90.0
    assert metrics["hallucination_rate"] <= 2.0
    assert metrics["structured_output_validity"] == 100.0


def test_3_report_store_metadata_persistence():
    store = EvaluationReportStore()
    sample_report = {
        "dataset": "financial_qa.json",
        "metadata": {
            "model_id": "gemini-3.6-flash",
            "model_version": "v1.0",
            "prompt_version": "v1.0",
        },
        "metrics": {"accuracy": 95.0, "f1": 0.95},
    }

    rep_id = store.save_report("run_eval_101", sample_report)
    assert rep_id == "run_eval_101"

    retrieved = store.get_report("run_eval_101")
    assert retrieved is not None
    assert retrieved["metadata"]["model_id"] == "gemini-3.6-flash"


def test_4_production_promotion_gate_enforcement():
    gate = ProductionPromotionGate()

    # Passing evaluation run
    passing_run = {
        "metadata": {"model_id": "gemini-3.6-flash", "model_version": "v1.0"},
        "metrics": {
            "accuracy": 95.0,
            "f1": 0.94,
            "hallucination_rate": 0.0,
            "grounding_rate": 98.0,
            "structured_output_validity": 100.0,
            "security_failures": 0.0,
            "p95_latency_ms": 450.0,
        },
    }

    is_promoted, reasons, summary = gate.evaluate_for_promotion(passing_run)
    assert is_promoted is True
    assert len(reasons) == 0
    assert summary["status"] == "APPROVED_FOR_PRODUCTION"

    # Failing evaluation run (low accuracy & high hallucination)
    failing_run = {
        "metadata": {"model_id": "experimental-llm", "model_version": "v0.1"},
        "metrics": {
            "accuracy": 75.0,  # Below 90%
            "f1": 0.70,
            "hallucination_rate": 8.0,  # Exceeds 2%
            "grounding_rate": 80.0,
            "structured_output_validity": 90.0,
            "security_failures": 5.0,  # Exceeds 0%
            "p95_latency_ms": 3000.0,
        },
    }

    is_promoted_fail, reasons_fail, summary_fail = gate.evaluate_for_promotion(failing_run)
    assert is_promoted_fail is False
    assert len(reasons_fail) >= 4
    assert summary_fail["status"] == "PROMOTION_BLOCKED"


def test_5_regression_tester_degradation_detection():
    tester = RegressionTester()

    baseline = {
        "metrics": {
            "accuracy": 95.0,
            "f1": 0.94,
            "hallucination_rate": 0.0,
            "security_failures": 0.0,
        }
    }

    # Candidate with degraded accuracy (90% vs 95% baseline)
    candidate_degraded = {
        "metrics": {
            "accuracy": 90.0,  # Dropped > 2%
            "f1": 0.88,
            "hallucination_rate": 2.5,  # Increased > 1%
            "security_failures": 0.0,
        }
    }

    is_clean, reg_reasons, summary = tester.compare_runs(candidate_degraded, baseline)
    assert is_clean is False
    assert len(reg_reasons) >= 2
    assert "Accuracy regression" in reg_reasons[0]
    assert summary["status"] == "REGRESSION_FAILURE"
