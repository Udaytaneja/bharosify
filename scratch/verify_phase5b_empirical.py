import hashlib
import json
import os
import sys

# Ensure root on python path
sys.path.insert(0, os.path.abspath("."))

results = {}

def compute_sha256(filepath):
    if not os.path.exists(filepath):
        return None
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def verify_phase5b():
    print("=== PHASE 5B.1 EMPIRICAL VERIFICATION ===\n")

    # 1. Dataset Verification
    raw_dir = "data/raw"
    processed_dir = "data/processed"
    dataset_yaml = os.path.join(processed_dir, "dataset.yaml")

    raw_exists = os.path.exists(raw_dir) and len(os.listdir(raw_dir)) > 0 if os.path.exists(raw_dir) else False
    processed_exists = os.path.exists(processed_dir) and len(os.listdir(processed_dir)) > 0 if os.path.exists(processed_dir) else False
    yaml_exists = os.path.exists(dataset_yaml)

    if not (raw_exists or processed_exists or yaml_exists):
        dataset_status = "DATASET_NOT_PRESENT"
        dataset_details = {
            "status": "DATASET_NOT_PRESENT",
            "message": "The full raw 80,863 page DocLayNet dataset is not stored locally in source tree (gitignored data/raw and data/processed).",
            "raw_dir_exists": raw_exists,
            "processed_dir_exists": processed_exists,
            "dataset_yaml_exists": yaml_exists
        }
    else:
        dataset_status = "DATASET_PRESENT"
        dataset_details = {"dataset_yaml": dataset_yaml}

    results["dataset_verification"] = dataset_details
    print(f"1. Dataset Status: {dataset_status}")

    # 2. Model Artifact Verification
    artifact_path = "artifacts/training/doc_layout/yolov8_doclayout_v1.pt"
    artifact_exists = os.path.exists(artifact_path)

    if artifact_exists:
        stat = os.stat(artifact_path)
        sha256 = compute_sha256(artifact_path)
        artifact_details = {
            "status": "MODEL_ARTIFACT_PRESENT",
            "path": artifact_path,
            "size_bytes": stat.st_size,
            "sha256": sha256,
            "modified_time": stat.st_mtime,
        }
    else:
        artifact_details = {
            "status": "MODEL_ARTIFACT_NOT_PRESENT",
            "path": artifact_path
        }

    results["model_artifact_verification"] = artifact_details
    print(f"2. Artifact Status: {artifact_details['status']}")

    # 3. Training Run & Manifest Verification
    manifest_dir = "artifacts/training/doc_layout"
    manifest_files = [f for f in os.listdir(manifest_dir) if f.endswith("_manifest.json")] if os.path.exists(manifest_dir) else []

    if manifest_files:
        manifest_path = os.path.join(manifest_dir, manifest_files[0])
        with open(manifest_path, "r") as f:
            manifest_data = json.load(f)
        manifest_details = {
            "status": "EXPERIMENT_MANIFEST_FOUND",
            "manifest_file": manifest_path,
            "experiment_id": manifest_data.get("experiment_id"),
            "dataset_id": manifest_data.get("dataset_id"),
            "reported_metrics": manifest_data.get("metrics"),
            "empirical_verification": "METRICS_NOT_EMPIRICALLY_VERIFIED (Metrics generated during offline infrastructure dry-run manifest logging without full Ultralytics CUDA execution against full 80,863 page dataset)"
        }
    else:
        manifest_details = {
            "status": "MANIFEST_NOT_FOUND",
            "empirical_verification": "METRICS_NOT_EMPIRICALLY_VERIFIED"
        }

    results["training_run_verification"] = manifest_details
    print(f"3. Training Run Verification: {manifest_details['empirical_verification']}")

    # 4. Class Mapping Verification
    from ai.app.ml.datasets.doclaynet_metadata import AGENTTRUST_LAYOUT_CLASSES, DOCLAYNET_CLASS_MAPPING
    results["class_verification"] = {
        "class_count": len(AGENTTRUST_LAYOUT_CLASSES),
        "classes": AGENTTRUST_LAYOUT_CLASSES,
        "mapping": DOCLAYNET_CLASS_MAPPING
    }

    # 5. Integration Readiness Check
    from ai.app.core.config import ai_settings
    integration_status = "INTEGRATION_REQUIRES_CONFIGURATION"
    results["integration_check"] = {
        "status": integration_status,
        "yolo_model_path_configured": ai_settings.yolo_model_path,
        "artifact_file_exists": os.path.exists(ai_settings.yolo_model_path or ""),
        "notes": f"Production perception currently configured to '{ai_settings.yolo_model_path}'. Updating to 'artifacts/training/doc_layout/yolov8_doclayout_v1.pt' requires configuration update."
    }
    print(f"4. Production Integration Readiness: {integration_status}")

    print("\n=== VERIFICATION SUMMARY JSON ===")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    verify_phase5b()
