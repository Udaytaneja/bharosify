import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from ai.app.perception.layout import LayoutElement
from ai.app.perception.ocr_engine import OCRLine


class FusedLayoutBlock(BaseModel):
    """Representing a structural layout element merged with contained OCR text lines."""

    element_type: str
    bbox: List[int]
    confidence: float
    contained_text_lines: List[str] = Field(default_factory=list)
    line_confidences: List[float] = Field(default_factory=list)


class DocumentFusionResult(BaseModel):
    """Deterministic spatial fusion document representation."""

    document_id: str
    pages_count: int = 1
    elements: List[FusedLayoutBlock] = Field(default_factory=list)
    text_blocks: List[str] = Field(default_factory=list)
    overall_confidence: float = Field(ge=0.0, le=1.0)
    model_versions: Dict[str, str] = Field(default_factory=dict)
    telemetry: Dict[str, Any] = Field(default_factory=dict)


class DocumentFusionEngine:
    """
    Deterministic Document Spatial Fusion Layer.
    Merges YOLO structural layout element bounding boxes with OCR text line coordinates
    using 2D geometric spatial overlap algorithms (no LLMs).
    """

    def fuse(
        self,
        document_id: str,
        layout_elements: List[LayoutElement],
        ocr_lines: List[OCRLine],
        ocr_meta: Optional[Dict[str, Any]] = None,
        layout_meta: Optional[Dict[str, Any]] = None,
    ) -> DocumentFusionResult:
        """
        Executes spatial fusion matching.
        """
        start_time = time.time()
        fused_elements: List[FusedLayoutBlock] = []
        assigned_line_indices = set()

        # 1. Match OCR text lines to YOLO layout element bounding boxes
        for elem in layout_elements:
            contained_texts = []
            contained_confs = []

            for idx, line in enumerate(ocr_lines):
                if self._is_spatially_contained(line.bbox, elem.bbox):
                    contained_texts.append(line.text)
                    contained_confs.append(line.confidence)
                    assigned_line_indices.add(idx)

            fused_elements.append(
                FusedLayoutBlock(
                    element_type=elem.element_type,
                    bbox=elem.bbox,
                    confidence=elem.confidence,
                    contained_text_lines=contained_texts,
                    line_confidences=contained_confs,
                )
            )

        # 2. Collect unassigned text lines as standalone text blocks
        unassigned_text_blocks = [
            ocr_lines[idx].text for idx in range(len(ocr_lines)) if idx not in assigned_line_indices
        ]

        # 3. Overall confidence calculation
        all_confs = [e.confidence for e in layout_elements] + [l.confidence for l in ocr_lines]
        overall_conf = round(sum(all_confs) / max(len(all_confs), 1), 2) if all_confs else 0.0

        fusion_latency_ms = (time.time() - start_time) * 1000.0

        ocr_meta_data = ocr_meta or {}
        layout_meta_data = layout_meta or {}

        model_versions = {
            "ocr": ocr_meta_data.get("engine", "PaddleOCR-v4"),
            "layout": layout_meta_data.get("model", "YOLOv8-DocLayout"),
        }

        telemetry = {
            "ocr_latency_ms": ocr_meta_data.get("latency_ms", 0.0),
            "layout_latency_ms": layout_meta_data.get("latency_ms", 0.0),
            "fusion_latency_ms": round(fusion_latency_ms, 2),
            "total_lines_count": len(ocr_lines),
            "total_elements_count": len(layout_elements),
            "assigned_lines_count": len(assigned_line_indices),
            "unassigned_lines_count": len(unassigned_text_blocks),
        }

        return DocumentFusionResult(
            document_id=document_id,
            pages_count=max(1, max((l.page for l in ocr_lines), default=1)),
            elements=fused_elements,
            text_blocks=unassigned_text_blocks,
            overall_confidence=overall_conf,
            model_versions=model_versions,
            telemetry=telemetry,
        )

    def _is_spatially_contained(self, ocr_bbox: List[int], layout_bbox: List[int], min_overlap_ratio: float = 0.4) -> bool:
        """
        Calculates 2D bounding box intersection area over OCR line area.
        ocr_bbox: [ox1, oy1, ox2, oy2]
        layout_bbox: [lx1, ly1, lx2, ly2]
        """
        if len(ocr_bbox) < 4 or len(layout_bbox) < 4:
            return False

        ox1, oy1, ox2, oy2 = ocr_bbox
        lx1, ly1, lx2, ly2 = layout_bbox

        # Calculate intersection rectangle
        ix1 = max(ox1, lx1)
        iy1 = max(oy1, ly1)
        ix2 = min(ox2, lx2)
        iy2 = min(oy2, ly2)

        if ix2 <= ix1 or iy2 <= iy1:
            return False

        intersection_area = (ix2 - ix1) * (iy2 - iy1)
        ocr_area = max((ox2 - ox1) * (oy2 - oy1), 1)

        overlap_ratio = intersection_area / ocr_area
        return overlap_ratio >= min_overlap_ratio


document_fusion_engine = DocumentFusionEngine()
