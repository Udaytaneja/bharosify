import pytest
from ai.app.core.config import ai_settings
from ai.app.models.model_lifecycle import ModelMetadata, model_registry_manager
from ai.app.perception import (
    DocumentFusionEngine,
    FileValidator,
    LayoutElement,
    OCRLine,
    PaddleOCREngine,
    PerceptionStatus,
    YOLOLayoutAnalyzer,
    document_fusion_engine,
    file_validator,
    paddle_ocr_engine,
    yolo_layout_analyzer,
)


def test_1_ocr_adapter_initialization():
    engine = PaddleOCREngine()
    assert engine.model_name == "PaddleOCR-v4"

    meta = model_registry_manager.get_metadata("PaddleOCR-v4")
    assert meta is not None
    assert meta.provider == "paddleocr"


def test_2_ocr_successful_inference_with_fixture():
    engine = PaddleOCREngine()
    mock_lines = [
        OCRLine(text="Account Holder: Verified User", confidence=0.98, bbox=[50, 100, 400, 130]),
        OCRLine(text="PAN Number: ABCDE1234F", confidence=0.96, bbox=[50, 140, 350, 170]),
    ]

    lines, mean_conf, meta = engine.extract_text_lines(
        file_bytes=b"dummy_bytes", file_name="doc.png", mock_override_lines=mock_lines
    )
    assert len(lines) == 2
    assert lines[0].text == "Account Holder: Verified User"
    assert mean_conf == 0.97
    assert meta["status"] == PerceptionStatus.SUCCESS.value


def test_3_ocr_unavailable_status_handling():
    engine = PaddleOCREngine()
    # Force _get_or_load_ocr to return unavailable
    engine._get_or_load_ocr = lambda: (None, False, "PaddleOCR runtime library is not installed.")

    lines, mean_conf, meta = engine.extract_text_lines(b"test_bytes", "sample.png")
    assert len(lines) == 0
    assert mean_conf == 0.0
    assert meta["status"] == PerceptionStatus.MODEL_UNAVAILABLE.value
    assert meta["is_available"] is False


def test_4_layout_adapter_initialization():
    analyzer = YOLOLayoutAnalyzer()
    assert analyzer.model_name == "YOLOv8-DocLayout"

    meta = model_registry_manager.get_metadata("YOLOv8-DocLayout")
    assert meta is not None
    assert meta.provider == "ultralytics"


def test_5_layout_inference_with_fixture():
    analyzer = YOLOLayoutAnalyzer()
    mock_elements = [
        LayoutElement(element_type="header", bbox=[50, 20, 500, 80], confidence=0.97),
        LayoutElement(element_type="table", bbox=[50, 100, 500, 400], confidence=0.95),
    ]

    elements, meta = analyzer.analyze_layout(
        file_bytes=b"dummy_bytes", file_name="layout.png", mock_override_elements=mock_elements
    )
    assert len(elements) == 2
    assert elements[0].element_type == "header"
    assert meta["status"] == PerceptionStatus.SUCCESS.value
    assert meta["has_table"] is True


def test_6_layout_model_unavailable_handling():
    analyzer = YOLOLayoutAnalyzer()
    # Ensure yolo_model_path points to non-existent file
    ai_settings.yolo_model_path = "/non_existent_path/model.pt"

    elements, meta = analyzer.analyze_layout(b"test_bytes", "sample.png")
    assert len(elements) == 0
    assert meta["status"] == PerceptionStatus.MODEL_UNAVAILABLE.value
    assert meta["is_available"] is False
    assert "not configured or file is missing" in meta["status_message"]


def test_7_invalid_image_extension_handling():
    validator = FileValidator()
    valid, reason, _ = validator.validate(b"test content", "unsupported_script.exe")
    assert valid is False
    assert "Unsupported file extension" in reason


def test_8_oversized_input_file_handling():
    validator = FileValidator()
    oversized_bytes = b"%PDF-1.4\n" + b"X" * (16 * 1024 * 1024)  # 16 MB > 15 MB limit

    valid, reason, _ = validator.validate(oversized_bytes, "large_file.pdf")
    assert valid is False
    assert "exceeds maximum limit" in reason


def test_9_document_fusion_spatial_matching():
    fusion = DocumentFusionEngine()

    layout_elems = [
        LayoutElement(element_type="header", bbox=[50, 20, 500, 80], confidence=0.98),
        LayoutElement(element_type="table", bbox=[50, 100, 500, 400], confidence=0.95),
    ]

    ocr_lines = [
        OCRLine(text="Bank Statement Header", confidence=0.99, bbox=[60, 30, 300, 60]),  # Inside header
        OCRLine(text="Tx 101: $5,000", confidence=0.95, bbox=[60, 120, 250, 150]),  # Inside table
        OCRLine(text="Footer Disclaimer text", confidence=0.90, bbox=[50, 500, 400, 530]),  # Unassigned
    ]

    fusion_res = fusion.fuse("doc_101", layout_elems, ocr_lines)
    assert fusion_res.document_id == "doc_101"
    assert len(fusion_res.elements) == 2

    # Check header block contained text
    header_block = fusion_res.elements[0]
    assert header_block.element_type == "header"
    assert "Bank Statement Header" in header_block.contained_text_lines

    # Check table block contained text
    table_block = fusion_res.elements[1]
    assert table_block.element_type == "table"
    assert "Tx 101: $5,000" in table_block.contained_text_lines

    # Check unassigned text blocks
    assert len(fusion_res.text_blocks) == 1
    assert "Footer Disclaimer text" in fusion_res.text_blocks[0]


def test_10_bounding_box_containment_iou_calculation():
    fusion = DocumentFusionEngine()

    ocr_box = [60, 30, 200, 60]
    container_box = [50, 20, 500, 80]
    outside_box = [50, 100, 500, 400]

    assert fusion._is_spatially_contained(ocr_box, container_box) is True
    assert fusion._is_spatially_contained(ocr_box, outside_box) is False


def test_11_confidence_scoring_evaluation():
    from ai.app.perception import confidence_scorer

    conf, review, reasons = confidence_scorer.evaluate(
        classification_confidence=0.95,
        ocr_confidence=0.96,
        layout_confidence=0.94,
        anomalies=[],
        extracted_fields={"account_number": "123456789", "holder_name": "Verified User"},
    )
    assert conf >= 0.90
    assert review is False



def test_12_security_script_payload_blocking():
    validator = FileValidator()
    malicious_bytes = b"%PDF-1.4\n<script>window.location='http://attacker.com'</script>\n/JavaScript execution\n"

    valid, reason, _ = validator.validate(malicious_bytes, "malicious.pdf")
    assert valid is False
    assert "Security Violation" in reason
