import pytest
from ai.app.providers import (
    ModelCategory,
    SarvamLLMAdapter,
    DocumentOCRAdapter,
    XGBoostRiskAdapter,
    IsolationForestAnomalyAdapter,
    VectorEmbeddingAdapter,
    OCRResult,
    RiskOutput,
    AnomalyOutput,
)
from ai.app.models import model_registry


@pytest.mark.asyncio
async def test_sarvam_adapter():
    adapter = SarvamLLMAdapter()
    text, meta = await adapter.generate_text("नमस्ते, मेरी बचत स्थिति क्या है?", language="hi")
    assert len(text) > 0
    assert meta["provider"] == "sarvam"


@pytest.mark.asyncio
async def test_ocr_adapter():
    adapter = DocumentOCRAdapter()
    res = await adapter.extract_document(b"fake_pdf_bytes", "bank_statement.pdf")
    assert isinstance(res, OCRResult)
    assert res.document_type == "bank_statement"
    assert res.confidence >= 0.90
    assert "net_monthly_income" in res.key_value_pairs


@pytest.mark.asyncio
async def test_xgboost_risk_adapter():
    adapter = XGBoostRiskAdapter()
    applicant_data = {
        "income": 120000.0,
        "debt": 15000.0,
        "expenses": 30000.0,
        "requested_amount": 25000.0,
    }
    risk_out = await adapter.predict_risk(applicant_data)
    assert isinstance(risk_out, RiskOutput)
    assert 300 <= risk_out.score <= 850
    assert risk_out.risk_level in ["low", "medium", "high", "critical"]
    assert risk_out.recommendation in ["approve", "review", "reject"]


@pytest.mark.asyncio
async def test_isolation_forest_anomaly_adapter():
    adapter = IsolationForestAnomalyAdapter()
    normal_tx = {"amount": 45.0, "tx_count_last_10m": 1}
    baseline = {"average_transaction_amount": 50.0}
    normal_out = await adapter.detect_anomaly(normal_tx, baseline)
    assert normal_out.is_anomaly is False

    anomalous_tx = {"amount": 5000.0, "tx_count_last_10m": 12}
    anomalous_out = await adapter.detect_anomaly(anomalous_tx, baseline)
    assert isinstance(anomalous_out, AnomalyOutput)
    assert anomalous_out.is_anomaly is True
    assert len(anomalous_out.anomalous_features) >= 1


@pytest.mark.asyncio
async def test_vector_embedding_adapter():
    adapter = VectorEmbeddingAdapter(dimension=128)
    embedding = await adapter.embed_text("AgentTrust OS Financial Document")
    assert len(embedding) == 128
    assert isinstance(embedding[0], float)


def test_registry_category_filtering():
    llm_models = model_registry.get_models_by_category(ModelCategory.LLM)
    assert len(llm_models) >= 1

    ocr_models = model_registry.get_models_by_category(ModelCategory.OCR_MODEL)
    assert len(ocr_models) >= 1
    assert any(m.model_id == "paddleocr-v4" for m in ocr_models)
