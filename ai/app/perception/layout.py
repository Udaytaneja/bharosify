import os
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from ai.app.core.config import ai_settings
from ai.app.models.model_lifecycle import model_registry_manager
from ai.app.perception.status import PerceptionStatus


class LayoutElement(BaseModel):
    """Representing a structural layout element detected by YOLOv8-DocLayout."""

    element_type: str  # "header" | "table" | "logo" | "stamp" | "signature" | "text_block"
    bbox: List[int] = Field(default_factory=list, description="Bounding box [x1, y1, x2, y2]")
    confidence: float = Field(ge=0.0, le=1.0)
    page: int = Field(default=1, description="Page index (1-based)")
    source_class: Optional[str] = None
    semantic_class: Optional[str] = None


class YOLOLayoutAnalyzer:
    """
    Production YOLO Document Layout Analyzer Adapter using Ultralytics framework.
    Executes real structural layout element detection (Header, Table, Logo, Stamp, Signature).
    If no trained document-layout model artifact is provided, returns explicit status (MODEL_UNAVAILABLE)
    without fabricating hardcoded bounding boxes or fake detections.
    """

    LEGACY_CLASS_MAPPING = {
        0: "header",
        1: "table",
        2: "logo",
        3: "stamp",
        4: "signature",
        5: "text_block",
    }
    SEMANTIC_CLASS_MAPPING = {
        "Page-header": "DOCUMENT_HEADER",
        "PAGE_HEADER": "DOCUMENT_HEADER",
        "Title": "DOCUMENT_TITLE",
        "TITLE": "DOCUMENT_TITLE",
        "Table": "TRANSACTION_TABLE",
        "TABLE": "TRANSACTION_TABLE",
    }

    def __init__(self):
        self.model_name = "YOLOv8-DocLayout"
        self.model_status = "EXPERIMENTAL"

    def _class_name(self, model: Any, class_id: int) -> str:
        names = getattr(model, "names", {})
        if isinstance(names, dict):
            return str(names.get(class_id, self.LEGACY_CLASS_MAPPING.get(class_id, "text_block")))
        if isinstance(names, (list, tuple)) and class_id < len(names):
            return str(names[class_id])
        return self.LEGACY_CLASS_MAPPING.get(class_id, "text_block")

    def _semantic_class(self, source_class: str) -> Optional[str]:
        return self.SEMANTIC_CLASS_MAPPING.get(source_class)

    def _get_or_load_yolo(self) -> Tuple[Optional[Any], bool, str]:
        """
        Retrieves cached YOLO model instance or initializes once safely.
        Returns:
            Tuple[yolo_instance, is_available, status_message]
        """
        model_path = ai_settings.yolo_model_path
        if not model_path or not os.path.exists(model_path):
            return None, False, f"YOLO document-layout model artifact path '{model_path}' is not configured or file is missing."

        cached = model_registry_manager.get_loaded_instance(self.model_name)
        if cached is not None:
            return cached, True, "MODEL-READY"

        try:
            from ultralytics import YOLO
        except ImportError:
            atv_site = r"C:\atv\lib\site-packages"
            if os.path.exists(atv_site) and atv_site not in sys.path:
                sys.path.insert(0, atv_site)
            try:
                from ultralytics import YOLO
            except Exception as e:
                return None, False, f"Failed to import Ultralytics YOLO runtime: {str(e)}"
        except ImportError:
            return None, False, "Ultralytics library is not installed in runtime environment."
        except Exception as e:
            return None, False, f"YOLO model artifact loading failed: {str(e)}"

        try:
            yolo_instance = YOLO(model_path)
            model_registry_manager.set_loaded_instance(self.model_name, yolo_instance, artifact_path=model_path)
            return yolo_instance, True, "MODEL-READY"
        except Exception as e:
            return None, False, f"YOLO model artifact loading failed: {str(e)}"

    def analyze_layout(
        self, file_bytes: bytes, file_name: str, mock_override_elements: Optional[List[LayoutElement]] = None
    ) -> Tuple[List[LayoutElement], Dict[str, Any]]:
        """
        Detects structural layout elements (Header, Table, Logo, Stamp, Signature, Text Block).
        Returns:
            Tuple[layout_elements, layout_metadata]
        """
        start_time = time.time()

        # Support test injection fixture override for deterministic unit testing
        if mock_override_elements is not None:
            latency_ms = (time.time() - start_time) * 1000.0
            meta = {
                "model": self.model_name,
                "model_status": self.model_status,
                "status": PerceptionStatus.SUCCESS.value,
                "detected_elements_count": len(mock_override_elements),
                "latency_ms": round(latency_ms, 2),
                "is_available": True,
                "has_table": any(e.element_type == "table" for e in mock_override_elements),
                "has_signature": any(e.element_type == "signature" for e in mock_override_elements),
                "has_stamp": any(e.element_type == "stamp" for e in mock_override_elements),
            }
            return mock_override_elements, meta

        yolo_instance, is_available, status_msg = self._get_or_load_yolo()
        if not is_available or yolo_instance is None:
            latency_ms = (time.time() - start_time) * 1000.0
            meta = {
                "model": self.model_name,
                "model_status": self.model_status,
                "checkpoint": ai_settings.yolo_model_path,
                "status": PerceptionStatus.MODEL_UNAVAILABLE.value,
                "status_message": status_msg,
                "detected_elements_count": 0,
                "latency_ms": round(latency_ms, 2),
                "is_available": False,
                "has_table": False,
                "has_signature": False,
                "has_stamp": False,
            }
            return [], meta

        tmp_path = None
        try:
            ext = os.path.splitext(file_name.lower())[1] or ".png"
            if ext == ".pdf":
                try:
                    import fitz
                    doc = fitz.open(stream=file_bytes, filetype="pdf")
                    page = doc.load_page(0)
                    pix = page.get_pixmap(dpi=150)
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                        pix.save(tmp.name)
                        tmp_path = tmp.name
                except Exception as pdf_err:
                    print(f"PDF image rendering warning for YOLO: {pdf_err}")
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                        tmp.write(file_bytes)
                        tmp_path = tmp.name
            else:
                with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                    tmp.write(file_bytes)
                    tmp_path = tmp.name

            results = yolo_instance.predict(
                source=tmp_path,
                conf=ai_settings.yolo_confidence_threshold,
                iou=ai_settings.yolo_iou_threshold,
                device=ai_settings.yolo_device,
                imgsz=ai_settings.yolo_image_size,
                verbose=False,
            )

            elements: List[LayoutElement] = []
            for res in results:
                if hasattr(res, "boxes") and res.boxes is not None:
                    for box in res.boxes:
                        xyxy = box.xyxy[0].tolist()
                        conf = round(float(box.conf[0]), 4)
                        cls_id = int(box.cls[0])
                        source_class = self._class_name(yolo_instance, cls_id)
                        elem_type = source_class.lower().replace("-", "_")

                        x1, y1, x2, y2 = [int(v) for v in xyxy]
                        elements.append(
                            LayoutElement(
                                element_type=elem_type,
                                bbox=[x1, y1, x2, y2],
                                confidence=conf,
                                page=1,
                                source_class=source_class,
                                semantic_class=self._semantic_class(source_class),
                            )
                        )

            latency_ms = (time.time() - start_time) * 1000.0
            meta = {
                "model": self.model_name,
                "model_status": self.model_status,
                "checkpoint": ai_settings.yolo_model_path,
                "status": PerceptionStatus.SUCCESS.value,
                "detected_elements_count": len(elements),
                "latency_ms": round(latency_ms, 2),
                "is_available": True,
                "has_table": any(e.element_type == "table" for e in elements),
                "has_signature": any(e.element_type == "signature" for e in elements),
                "has_stamp": any(e.element_type == "stamp" for e in elements),
            }
            return elements, meta

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000.0
            meta = {
                "model": self.model_name,
                "model_status": self.model_status,
                "checkpoint": ai_settings.yolo_model_path,
                "status": PerceptionStatus.LAYOUT_FAILURE.value,
                "status_message": f"YOLO layout inference failed: {str(e)}",
                "detected_elements_count": 0,
                "latency_ms": round(latency_ms, 2),
                "is_available": True,
                "has_table": False,
                "has_signature": False,
                "has_stamp": False,
            }
            return [], meta
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass


yolo_layout_analyzer = YOLOLayoutAnalyzer()
