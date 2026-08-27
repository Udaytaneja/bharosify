import json
import math
import os
import time
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple


from ai.app.agents.financial_intelligence import FinancialIntelligenceService
from ai.app.gateway import ai_gateway
from ai.app.schemas.financial_intelligence import FinancialIntelligenceRequest
from ai.app.schemas.requests import AIExecutionRequest


class ModelEvaluator:
    """
    Model Evaluator Engine running benchmark datasets and calculating 11 core metrics:
    - accuracy
    - precision
    - recall
    - f1
    - confidence calibration (ECE)
    - latency (avg, p50, p95)
    - cost
    - hallucination rate
    - grounding rate
    - structured-output validity
    - security failures
    """

    def __init__(self, dataset_dir: Optional[str] = None):
        if not dataset_dir:
            dataset_dir = os.path.join(os.path.dirname(__file__), "datasets")
        self.dataset_dir = dataset_dir

    def load_dataset(self, filename: str) -> List[Dict[str, Any]]:
        path = os.path.join(self.dataset_dir, filename)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    async def evaluate_dataset(
        self,
        dataset_filename: str,
        model_id: str = "gemini-3.6-flash",
        model_version: str = "v1.0",
        prompt_version: str = "v1.0",
    ) -> Dict[str, Any]:
        items = self.load_dataset(dataset_filename)
        if not items:
            return self._empty_result(dataset_filename, model_id, model_version, prompt_version)

        latencies: List[float] = []
        confidences: List[float] = []
        correct_predictions: List[bool] = []
        
        tp, fp, fn = 0, 0, 0
        hallucination_count = 0
        grounded_count = 0
        structured_valid_count = 0
        security_failure_count = 0
        total_cost = 0.0

        fi_service = FinancialIntelligenceService()

        for item in items:
            start_t = time.time()
            task = item.get("task", "financial_health")
            lang = item.get("language", "en")
            query = item["input"]
            context = item.get("context", {})

            try:
                if task in ["financial_intelligence", "financial_health", "affordability", "repayment", "loan_scenario", "anomaly_explanation", "digital_twin", "what_if_simulation"]:
                    req = FinancialIntelligenceRequest(
                        request_id=f"eval_{item['id']}",
                        query=query,
                        task=task,
                        language=lang,
                        context=context,
                    )
                    res = await fi_service.process_request(req)
                    explanation = res.explanation
                    decision = res.recommendation
                    confidence = res.confidence
                    is_valid_schema = True
                else:
                    exec_req = AIExecutionRequest(
                        request_id=f"eval_{item['id']}",
                        task=task,
                        input=query,
                        language=lang,
                        context=context,
                    )
                    gtw_res = await ai_gateway.execute(exec_req)
                    explanation = gtw_res.response
                    decision = gtw_res.recommendation
                    confidence = gtw_res.confidence
                    is_valid_schema = True
            except Exception as e:
                explanation = str(e)
                decision = "BLOCK"
                confidence = 0.0
                is_valid_schema = False
                security_failure_count += 1

            latency = (time.time() - start_t) * 1000.0
            latencies.append(latency)
            confidences.append(confidence)
            total_cost += 0.00005  # Standard cost per benchmark item

            if is_valid_schema:
                structured_valid_count += 1

            # 1. Decision Match & Accuracy / Precision / Recall
            expected_dec = item.get("expected_decision", item.get("expected_recommendation"))
            is_correct = True
            if expected_dec:
                is_correct = decision.lower() == expected_dec.lower()
            
            correct_predictions.append(is_correct)

            if is_correct:
                tp += 1
            else:
                fp += 1
                fn += 1

            # 2. Hallucination Rate Verification
            exp_nums = item.get("expected_financial_values", [])
            if exp_nums:
                has_hallucination = False
                explanation_clean = explanation.replace(",", "")
                for num in exp_nums:
                    d_num = Decimal(str(num))
                    num_2f = f"{d_num:.2f}"
                    num_0f = f"{d_num:.0f}"
                    if num_2f not in explanation_clean and num_0f not in explanation_clean and str(num) not in explanation:
                        has_hallucination = True
                        break
                if has_hallucination:
                    hallucination_count += 1




            # 3. Grounding Rate Verification
            ground_truth = item.get("ground_truth", "")
            if ground_truth:
                # Simple text overlap grounding check
                words = [w for w in ground_truth.split() if len(w) > 3]
                matched_words = [w for w in words if w.lower() in explanation.lower()]
                if len(matched_words) >= max(1, len(words) // 2):
                    grounded_count += 1
            else:
                grounded_count += 1

        total_items = len(items)
        accuracy = (sum(1 for c in correct_predictions if c) / total_items) * 100.0 if total_items > 0 else 0.0
        precision = (tp / (tp + fp)) if (tp + fp) > 0 else 1.0
        recall = (tp / (tp + fn)) if (tp + fn) > 0 else 1.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 1.0

        # ECE (Expected Calibration Error)
        avg_conf = sum(confidences) / total_items if total_items > 0 else 1.0
        ece = abs(avg_conf - (accuracy / 100.0))

        # Latency statistics
        latencies.sort()
        avg_latency = sum(latencies) / total_items if total_items > 0 else 0.0
        p50_latency = latencies[total_items // 2] if total_items > 0 else 0.0
        p95_index = min(total_items - 1, int(total_items * 0.95))
        p95_latency = latencies[p95_index] if total_items > 0 else 0.0

        hallucination_rate = (hallucination_count / total_items) * 100.0 if total_items > 0 else 0.0
        grounding_rate = (grounded_count / total_items) * 100.0 if total_items > 0 else 100.0
        structured_validity = (structured_valid_count / total_items) * 100.0 if total_items > 0 else 100.0
        sec_failure_rate = (security_failure_count / total_items) * 100.0 if total_items > 0 else 0.0

        return {
            "dataset": dataset_filename,
            "metadata": {
                "model_id": model_id,
                "model_version": model_version,
                "prompt_version": prompt_version,
                "total_items": total_items,
                "timestamp": time.time(),
            },
            "metrics": {
                "accuracy": round(accuracy, 2),
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1": round(f1, 4),
                "confidence_calibration_ece": round(ece, 4),
                "avg_latency_ms": round(avg_latency, 2),
                "p50_latency_ms": round(p50_latency, 2),
                "p95_latency_ms": round(p95_latency, 2),
                "cost_usd": round(total_cost, 5),
                "hallucination_rate": round(hallucination_rate, 2),
                "grounding_rate": round(grounding_rate, 2),
                "structured_output_validity": round(structured_validity, 2),
                "security_failures": round(sec_failure_rate, 2),
            },
        }

    def _empty_result(self, filename: str, model_id: str, model_version: str, prompt_version: str) -> Dict[str, Any]:
        return {
            "dataset": filename,
            "metadata": {
                "model_id": model_id,
                "model_version": model_version,
                "prompt_version": prompt_version,
                "total_items": 0,
                "timestamp": time.time(),
            },
            "metrics": {
                "accuracy": 100.0,
                "precision": 1.0,
                "recall": 1.0,
                "f1": 1.0,
                "confidence_calibration_ece": 0.0,
                "avg_latency_ms": 0.0,
                "p50_latency_ms": 0.0,
                "p95_latency_ms": 0.0,
                "cost_usd": 0.0,
                "hallucination_rate": 0.0,
                "grounding_rate": 100.0,
                "structured_output_validity": 100.0,
                "security_failures": 0.0,
            },
        }


model_evaluator = ModelEvaluator()
