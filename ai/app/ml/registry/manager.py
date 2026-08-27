import hashlib
import os
import threading
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ModelManifest(BaseModel):
    """Manifest representing a trained model artifact experiment."""

    model_id: str
    model_name: str
    model_version: str
    model_type: str  # "risk" | "fraud" | "anomaly"
    dataset_id: str
    dataset_version: str
    feature_version: str
    training_timestamp: str = Field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))
    metrics: Dict[str, float] = Field(default_factory=dict)
    hyperparameters: Dict[str, Any] = Field(default_factory=dict)
    framework_version: str = "xgboost/lightgbm/sklearn"
    checksum: Optional[str] = None
    random_seed: int = 42
    status: str = "EXPERIMENTAL"  # "EXPERIMENTAL" | "VALIDATED" | "PRODUCTION_APPROVED" | "RETIRED"


class ExperimentManifestManager:
    """
    Model Registry & Experiment Manifest Manager.
    Tracks trained model artifacts, metrics, checksums, seeds, and lifecycle statuses.
    """

    def __init__(self):
        self._manifests: Dict[str, ModelManifest] = {}
        self._lock = threading.Lock()

    def register_manifest(self, manifest: ModelManifest):
        """Registers a model manifest in the registry."""
        with self._lock:
            self._manifests[manifest.model_id] = manifest

    def get_manifest(self, model_id: str) -> Optional[ModelManifest]:
        """Retrieves model manifest by ID."""
        with self._lock:
            return self._manifests.get(model_id)

    def list_manifests(self) -> List[ModelManifest]:
        """Lists all registered model manifests."""
        with self._lock:
            return list(self._manifests.values())

    def calculate_artifact_checksum(self, filepath: str) -> str:
        """Calculates MD5 checksum for a model artifact file."""
        if not os.path.exists(filepath):
            return "unknown"
        try:
            hasher = hashlib.md5()
            with open(filepath, "rb") as f:
                buf = f.read(65536)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(65536)
            return hasher.hexdigest()
        except Exception:
            return "error"


experiment_manifest_manager = ExperimentManifestManager()
