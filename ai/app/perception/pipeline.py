import uuid
from typing import Any, Dict, List, Optional
from ai.app.core.config import ai_settings
from ai.app.core.exceptions import SafetyViolationError, ValidationException
from ai.app.perception.validation import file_validator
from ai.app.perception.classification import document_classifier
from ai.app.perception.preprocessing import image_preprocessor
from ai.app.perception.ocr_engine import OCRLine, paddle_ocr_engine
from ai.app.perception.layout import LayoutElement, yolo_layout_analyzer
from ai.app.perception.fusion import document_fusion_engine
from ai.app.perception.extraction import layout_field_extractor
from ai.app.perception.tampering import tampering_detector
from ai.app.perception.confidence import confidence_scorer
from ai.app.perception.backend_adapter import document_backend_adapter, DocumentIntelligenceResult


class DocumentIntelligencePipeline:
    """
    Full AgentTrust Document Intelligence Pipeline:
    Document -> File validation -> Malware/security -> Preprocessing ->
    OCR (PaddleOCR Adapter) -> YOLO Layout Analysis -> Spatial Fusion ->
    Field Extraction -> Confidence Scoring -> Tampering Detection -> Backend DTO
    """

    async def process_document(
        self,
        file_bytes: bytes,
        file_name: str,
        mock_ocr_lines: Optional[List[OCRLine]] = None,
        mock_layout_elements: Optional[List[LayoutElement]] = None,
    ) -> DocumentIntelligenceResult:
        # Stage 1 & 2: File Validation and Security / Malware Checks
        is_valid, err_msg, val_meta = file_validator.validate(file_bytes, file_name)
        if not is_valid:
            if "Security Violation" in err_msg:
                raise SafetyViolationError("MALWARE_FILE_SCANNER", err_msg)
            raise ValidationException(err_msg)

        # Stage 3: Image Preprocessing (Deskew, contrast, noise reduction)
        clean_bytes, prep_meta = image_preprocessor.process(file_bytes, file_name)

        # Stage 4: OCR Engine Execution (PaddleOCR Adapter)
        ocr_lines, ocr_conf, ocr_meta = paddle_ocr_engine.extract_text_lines(
            clean_bytes, file_name, mock_override_lines=mock_ocr_lines
        )
        sample_text = "\n".join([line.text for line in ocr_lines])

        # Stage 5: Document Classification
        doc_type, class_conf, class_meta = document_classifier.classify(sample_text, file_name)

        # Stage 6: YOLO Document Layout Analysis
        layout_elements, layout_meta = yolo_layout_analyzer.analyze_layout(
            clean_bytes, file_name, mock_override_elements=mock_layout_elements
        )
        layout_conf = 0.94 if layout_elements else 0.50

        # Stage 7: Deterministic Bounding Box Spatial Fusion Layer
        doc_id = f"doc_{uuid.uuid4().hex[:10]}"
        fusion_result = document_fusion_engine.fuse(
            document_id=doc_id,
            layout_elements=layout_elements,
            ocr_lines=ocr_lines,
            ocr_meta=ocr_meta,
            layout_meta=layout_meta,
        )

        # Stage 8: Field Extraction (Layout-aware key-values)
        if not ocr_lines and ocr_meta.get("status") == "MODEL_UNAVAILABLE":
            extracted_fields = {}
            evidence = ["OCR unavailable; no document fields extracted."]
        else:
            extracted_fields, evidence = layout_field_extractor.extract_fields(
                document_type=doc_type,
                ocr_lines=ocr_lines,
                layout_elements=layout_elements,
            )

        # Stage 9: Tampering & Anomaly Signals
        anomalies = tampering_detector.detect_tampering(file_bytes, file_name, extracted_fields)

        # Stage 10: Confidence Scoring & Review Router
        overall_confidence, requires_review, review_reasons = confidence_scorer.evaluate(
            classification_confidence=class_conf,
            ocr_confidence=ocr_conf,
            layout_confidence=layout_conf,
            anomalies=anomalies,
            extracted_fields=extracted_fields,
        )

        for reason in review_reasons:
            evidence.append(f"Review Flag: {reason}")

        # Aggregated Model Metadata
        model_metadata = {
            "validation": val_meta,
            "classifier": class_meta,
            "preprocessing": prep_meta,
            "ocr": ocr_meta,
            "layout": layout_meta,
            "fusion": fusion_result.model_dump(),
            "pipeline_version": "v2.0.0",
            "provenance": {
                "layout_model_status": layout_meta.get("model_status", "EXPERIMENTAL"),
                "layout_checkpoint": layout_meta.get("checkpoint", ai_settings.yolo_model_path),
                "indian_domain_validation": False,
            },
        }

        # Stage 11: Backend DTO Formatting
        return document_backend_adapter.format_result(
            document_type=doc_type,
            fields=extracted_fields,
            confidence=overall_confidence,
            anomalies=anomalies,
            evidence=evidence,
            model_metadata=model_metadata,
            layout_regions=[element.model_dump() for element in layout_elements],
            ocr_lines=[line.model_dump() for line in ocr_lines],
            requires_review=requires_review,
        )


document_intelligence_pipeline = DocumentIntelligencePipeline()
