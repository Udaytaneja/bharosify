import pytest
from ai.app.perception import document_intelligence_pipeline, DocumentIntelligenceResult
from ai.app.core.exceptions import SafetyViolationError, ValidationException


@pytest.mark.asyncio
async def test_identity_document_processing():
    synthetic_pdf = b"%PDF-1.4\nGovernment of India\nPAN Card\nHolder Name: Test User\nPAN Number: ABCDE1234F\nDOB: 15/08/1990\n"
    from ai.app.perception.layout import LayoutElement
    mock_layout = [LayoutElement(element_type="text_block", bbox=[50, 50, 400, 300], confidence=0.95)]
    result = await document_intelligence_pipeline.process_document(synthetic_pdf, "identity_pan.pdf", mock_layout_elements=mock_layout)



    assert isinstance(result, DocumentIntelligenceResult)
    assert result.document_type == "identity_document"
    assert "pan_number" in result.fields
    assert result.fields["pan_number"] == "ABCDE1234F"
    assert result.confidence >= 0.85
    assert isinstance(result.requires_review, bool)


@pytest.mark.asyncio
async def test_bank_statement_processing():
    synthetic_pdf = b"%PDF-1.4\nState Financial Bank\nBank Account Statement\nAccount Number: 987654321012\nOpening Balance: $20,000\nClosing Balance: $125,450.00\n"
    result = await document_intelligence_pipeline.process_document(synthetic_pdf, "bank_statement_aug.pdf")

    assert result.document_type == "bank_statement"
    assert "closing_balance" in result.fields
    assert result.fields["closing_balance"] == 125450.00
    assert "YOLOv8" in result.model_metadata["layout"]["model"]



@pytest.mark.asyncio
async def test_salary_slip_processing():
    synthetic_pdf = b"%PDF-1.4\nEnterprise Tech Corp\nSalary Slip for August 2026\nBasic Pay: $50,000\nHRA: $25,000\nGross Salary: $75,000\n"
    result = await document_intelligence_pipeline.process_document(synthetic_pdf, "salary_slip.pdf")

    assert result.document_type == "salary_slip"
    assert "gross_salary" in result.fields
    assert result.fields["gross_salary"] == 75000.00


@pytest.mark.asyncio
async def test_tampered_document_requires_review():
    synthetic_edited_pdf = b"%PDF-1.4 Photoshop edit tags\nBank Statement edited balance\nClosing Balance: $999,999.00\n"
    result = await document_intelligence_pipeline.process_document(synthetic_edited_pdf, "tampered_statement.pdf")

    assert len(result.anomalies) >= 1
    assert result.requires_review is True
    assert any("Tampering Anomaly" in ev or "Review Flag" in ev for ev in result.evidence)


@pytest.mark.asyncio
async def test_malicious_script_file_blocked():
    malicious_bytes = b"%PDF-1.4\n<script>alert('malware');</script>\n/JavaScript execution\n"
    with pytest.raises(SafetyViolationError):
        await document_intelligence_pipeline.process_document(malicious_bytes, "malicious.pdf")


@pytest.mark.asyncio
async def test_empty_file_rejected():
    with pytest.raises(ValidationException):
        await document_intelligence_pipeline.process_document(b"", "empty.pdf")
