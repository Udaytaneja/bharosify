import pytest

from ai.app.agents.banker_copilot import banker_underwriting_copilot
from ai.app.perception import DocumentIntelligenceResult, LayoutElement, OCRLine
from ai.app.perception.layout import YOLOLayoutAnalyzer
from ai.app.perception.pipeline import document_intelligence_pipeline
from ai.app.schemas.underwriting import UnderwritingAssessmentRequest


class FakeTensor:
    def __init__(self, value):
        self.value = value

    def __getitem__(self, index):
        return FakeTensor(self.value[index]) if isinstance(self.value, list) else self.value

    def tolist(self):
        return self.value

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)


class FakeBox:
    def __init__(self, cls_id, confidence, coordinates):
        self.cls = FakeTensor([cls_id])
        self.conf = FakeTensor([confidence])
        self.xyxy = FakeTensor([coordinates])


class FakeResult:
    def __init__(self, boxes):
        self.boxes = boxes


class FakeYOLO:
    names = {0: "Page-header", 8: "Table"}

    def predict(self, **kwargs):
        return [FakeResult([
            FakeBox(0, 0.91, [10, 20, 200, 80]),
            FakeBox(8, 0.87, [20, 100, 500, 400]),
        ])]


def test_yolo_regions_map_deterministic_semantics(monkeypatch):
    analyzer = YOLOLayoutAnalyzer()
    monkeypatch.setattr(analyzer, "_get_or_load_yolo", lambda: (FakeYOLO(), True, "MODEL-READY"))

    regions, metadata = analyzer.analyze_layout(b"image-bytes", "statement.png")

    assert [region.source_class for region in regions] == ["Page-header", "Table"]
    assert [region.semantic_class for region in regions] == ["DOCUMENT_HEADER", "TRANSACTION_TABLE"]
    assert metadata["model_status"] == "EXPERIMENTAL"
    assert metadata["checkpoint"].replace("\\", "/").endswith("real_yolo_002/train_run/weights/best.pt")


@pytest.mark.asyncio
async def test_pipeline_returns_fused_regions_ocr_and_provenance():
    result = await document_intelligence_pipeline.process_document(
        b"%PDF-1.4\nBank Statement\n",
        "statement.pdf",
        mock_ocr_lines=[OCRLine(text="Bank Statement", confidence=0.95, bbox=[10, 20, 150, 50])],
        mock_layout_elements=[LayoutElement(
            element_type="page_header",
            source_class="Page-header",
            semantic_class="DOCUMENT_HEADER",
            bbox=[0, 0, 200, 80],
            confidence=0.91,
        )],
    )

    assert len(result.layout_regions) == 1
    assert result.layout_regions[0]["semantic_class"] == "DOCUMENT_HEADER"
    assert result.ocr_lines[0]["text"] == "Bank Statement"
    assert result.model_metadata["provenance"]["layout_model_status"] == "EXPERIMENTAL"
    assert result.model_metadata["provenance"]["indian_domain_validation"] is False


@pytest.mark.asyncio
async def test_copilot_passes_document_evidence_and_requires_review(monkeypatch):
    async def fake_process_document(file_bytes, file_name):
        return DocumentIntelligenceResult(
            document_type="salary_slip",
            fields={"net_pay": 68500.0},
            confidence=0.81,
            evidence=["synthetic fixture only"],
            model_metadata={
                "provenance": {
                    "layout_model_status": "EXPERIMENTAL",
                    "indian_domain_validation": False,
                }
            },
            layout_regions=[{
                "element_type": "table",
                "source_class": "Table",
                "semantic_class": "TRANSACTION_TABLE",
                "bbox": [20, 100, 500, 400],
                "confidence": 0.87,
                "page": 1,
            }],
            ocr_lines=[{"text": "Net Pay", "confidence": 0.94, "bbox": [30, 110, 120, 135], "page": 1}],
            requires_review=True,
        )

    monkeypatch.setattr(
        "ai.app.agents.banker_copilot.document_intelligence_pipeline.process_document",
        fake_process_document,
    )

    assessment = await banker_underwriting_copilot.generate_assessment(
        UnderwritingAssessmentRequest(
            banker_id="banker_01",
            organization_id="org_A",
            applicant_id="101",
            question="What document evidence supports this assessment?",
        ),
        file_bytes=b"synthetic-fixture",
        file_name="salary_slip.png",
    )

    evidence = assessment.document_evidence[0]
    assert evidence.layout_regions[0]["semantic_class"] == "TRANSACTION_TABLE"
    assert evidence.ocr_lines[0]["text"] == "Net Pay"
    assert evidence.provenance["layout_model_status"] == "EXPERIMENTAL"
    assert assessment.requires_human_review is True
