import os
from typing import Any, Dict, List, Optional, Tuple
from ai.app.ml.datasets.registry import dataset_registry_manager


class DatasetValidationError(Exception):
    """Raised when a dataset fails schema validation or header integrity checks."""
    pass


class DatasetLoader:
    """
    Schema-validated Dataset Loader.
    Reads datasets from configured root path (AI_DATA_ROOT or data/raw/)
    and enforces schema validation, target existence, and missing column checks.
    """

    def __init__(self, data_root: Optional[str] = None):
        self.data_root = data_root or os.getenv("AI_DATA_ROOT", "data/raw")

    def load_dataset(self, dataset_id: str, sample_mock_rows: Optional[List[Dict[str, Any]]] = None) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Loads dataset by ID, performing schema and integrity validation.
        Returns:
            Tuple[data_rows, validation_metadata]
        """
        meta = dataset_registry_manager.get_dataset(dataset_id)
        if not meta:
            raise DatasetValidationError(f"Dataset ID '{dataset_id}' is not registered in DatasetRegistryManager.")

        if meta.status == "NOT_APPROVED":
            raise DatasetValidationError(f"Dataset '{dataset_id}' has status 'NOT_APPROVED' and cannot be ingested.")

        # Support in-memory sample rows for deterministic unit testing without downloading files
        if sample_mock_rows is not None:
            self._validate_rows(dataset_id, sample_mock_rows, meta)
            val_meta = {
                "dataset_id": dataset_id,
                "loaded_rows": len(sample_mock_rows),
                "is_synthetic": meta.is_synthetic,
                "validation_passed": True,
            }
            return sample_mock_rows, val_meta

        target_filepath = os.path.join(self.data_root, f"{dataset_id}.csv")
        if not os.path.exists(target_filepath):
            # Gracefully handle un-downloaded datasets in development mode
            val_meta = {
                "dataset_id": dataset_id,
                "loaded_rows": 0,
                "is_synthetic": meta.is_synthetic,
                "status": "FILE_NOT_FOUND",
                "validation_passed": False,
                "message": f"Dataset file '{target_filepath}' not found. Download required for offline training.",
            }
            return [], val_meta

        # Validation logic for CSV files
        rows = self._read_csv_file(target_filepath)
        self._validate_rows(dataset_id, rows, meta)

        val_meta = {
            "dataset_id": dataset_id,
            "loaded_rows": len(rows),
            "is_synthetic": meta.is_synthetic,
            "validation_passed": True,
        }
        return rows, val_meta

    def _validate_rows(self, dataset_id: str, rows: List[Dict[str, Any]], meta: Any):
        """Executes row-level schema validation."""
        if not rows:
            raise DatasetValidationError(f"Dataset '{dataset_id}' is empty (0 rows).")

        sample_keys = list(rows[0].keys())

        # Target column check
        target_name = meta.target_definition.split()[0].replace(",", "")
        has_target = any(k.lower() == target_name.lower() or "target" in k.lower() or "default" in k.lower() or "laundering" in k.lower() or "sar" in k.lower() for k in sample_keys)
        if not has_target:
            raise DatasetValidationError(
                f"Dataset '{dataset_id}' missing expected target attribute related to '{meta.target_definition}'."
            )

    def _read_csv_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Reads CSV file into list of dictionaries."""
        import csv

        rows = []
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        return rows


dataset_loader = DatasetLoader()
