import hashlib
import json
import os
import random
from typing import Any, Dict, List, Optional, Tuple
import yaml

from ai.app.ml.datasets.doclaynet_metadata import (
    AGENTTRUST_LAYOUT_CLASSES,
    DOCLAYNET_CLASS_MAPPING,
    DOCLAYNET_GOVERNANCE_METADATA,
)


class DocLayNetYOLOConverter:
    """
    Deterministic Dataset Converter & Validator for DocLayNet -> YOLO Format.
    Validates images, checks bounding box bounds [0.0, 1.0], performs document-level
    deterministic splits (seed=42), and generates dataset.yaml configuration.
    """

    def __init__(self, raw_dir: str = "data/raw", processed_dir: str = "data/processed"):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir

    def validate_bounding_box(self, bbox: List[float]) -> bool:
        """
        Validates normalized bounding box [x_center, y_center, width, height].
        Must satisfy 0.0 <= val <= 1.0 and width > 0, height > 0.
        """
        if len(bbox) != 4:
            return False
        xc, yc, w, h = bbox
        if not (0.0 <= xc <= 1.0 and 0.0 <= yc <= 1.0 and 0.0 < w <= 1.0 and 0.0 < h <= 1.0):
            return False
        return True

    def convert_coco_bbox_to_yolo(self, bbox: List[float], img_w: int, img_h: int) -> Optional[List[float]]:
        """
        Converts COCO bbox [x_min, y_min, width, height] in pixels to normalized YOLO [x_center, y_center, width, height].
        """
        if img_w <= 0 or img_h <= 0:
            return None
        x_min, y_min, w, h = bbox
        xc = (x_min + w / 2.0) / img_w
        yc = (y_min + h / 2.0) / img_h
        norm_w = w / img_w
        norm_h = h / img_h

        # Clip values to valid [0.0, 1.0] range
        xc = min(max(xc, 0.0), 1.0)
        yc = min(max(yc, 0.0), 1.0)
        norm_w = min(max(norm_w, 0.0), 1.0)
        norm_h = min(max(norm_h, 0.0), 1.0)

        res = [round(xc, 6), round(yc, 6), round(norm_w, 6), round(norm_h, 6)]
        return res if self.validate_bounding_box(res) else None

    def compute_file_hash(self, filepath: str) -> str:
        """Computes SHA-256 hash of a file for duplicate detection."""
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    def deterministic_split_documents(
        self, document_ids: List[str], train_ratio: float = 0.8, val_ratio: float = 0.1, seed: int = 42
    ) -> Dict[str, str]:
        """
        Splits document IDs deterministically into train/val/test splits preserving document-level grouping.
        """
        unique_docs = sorted(list(set(document_ids)))
        rng = random.Random(seed)
        rng.shuffle(unique_docs)

        n = len(unique_docs)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)

        doc_splits = {}
        for idx, doc_id in enumerate(unique_docs):
            if idx < n_train:
                doc_splits[doc_id] = "train"
            elif idx < n_train + n_val:
                doc_splits[doc_id] = "val"
            else:
                doc_splits[doc_id] = "test"

        return doc_splits

    def generate_dataset_yaml(self, output_path: str) -> str:
        """Generates dataset.yaml configuration file for Ultralytics YOLO training."""
        yaml_content = {
            "path": os.path.abspath(self.processed_dir),
            "train": "images/train",
            "val": "images/val",
            "test": "images/test",
            "names": {idx: name for idx, name in enumerate(AGENTTRUST_LAYOUT_CLASSES)},
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            yaml.dump(yaml_content, f, default_flow_style=False)

        return output_path


doclaynet_converter = DocLayNetYOLOConverter()
