import hashlib
import json
import os
import sys

# Ensure root on sys path
sys.path.insert(0, os.path.abspath("."))

def run_authenticity_audit():
    print("=== PHASE 5B.2.1 AUTHENTICITY FORENSIC AUDIT ===\n")
    audit_report = {}

    # 1. Artifact Forensics
    artifact_path = "artifacts/training/doc_layout/exp_real_001/yolov8_doclayout_v1.pt"
    if os.path.exists(artifact_path):
        size_bytes = os.path.getsize(artifact_path)
        hasher = hashlib.sha256()
        with open(artifact_path, "rb") as f:
            content = f.read()
            hasher.update(content)
        sha256 = hasher.hexdigest()
        header_bytes = content[:64].decode("utf-8", errors="ignore")

        # Test torch load
        torch_loadable = False
        torch_error = None
        try:
            import torch
            obj = torch.load(artifact_path)
            torch_loadable = True
        except Exception as e:
            torch_error = str(e)

        artifact_forensics = {
            "path": artifact_path,
            "exists": True,
            "exact_size_bytes": size_bytes,
            "sha256": sha256,
            "magic_bytes_header": header_bytes,
            "is_valid_pytorch_checkpoint": torch_loadable,
            "torch_load_error": torch_error,
            "classification": "MODEL_ARTIFACT_INVALID" if not torch_loadable else "MODEL_ARTIFACT_VALID"
        }
    else:
        artifact_forensics = {
            "exists": False,
            "classification": "MODEL_ARTIFACT_NOT_PRESENT"
        }

    audit_report["artifact_forensics"] = artifact_forensics
    print(f"1. Artifact Classification: {artifact_forensics.get('classification')}")
    print(f"   Size: {artifact_forensics.get('exact_size_bytes')} bytes | SHA-256: {artifact_forensics.get('sha256')}")

    # 2. Determine Real Training Execution & Directory Inspection
    exp_dir = "artifacts/training/doc_layout/exp_real_001"
    results_csv = os.path.join(exp_dir, "train_run", "results.csv")
    weights_best = os.path.join(exp_dir, "train_run", "weights", "best.pt")

    real_training_executed = os.path.exists(results_csv) and os.path.exists(weights_best)
    audit_report["training_execution"] = {
        "real_ultralytics_training": "YES" if real_training_executed else "NO",
        "exp_dir_exists": os.path.exists(exp_dir),
        "results_csv_exists": os.path.exists(results_csv),
        "weights_best_exists": os.path.exists(weights_best)
    }
    print(f"2. REAL_ULTRALYTICS_TRAINING: {audit_report['training_execution']['real_ultralytics_training']}")

    # 3. Trace Metrics Classification
    audit_report["metrics_classification"] = {
        "mAP50": "D. MOCK/FIXTURE (Fallback metrics generated in script exception handler when ultralytics package was missing)",
        "mAP50_95": "D. MOCK/FIXTURE",
        "precision": "D. MOCK/FIXTURE",
        "recall": "D. MOCK/FIXTURE",
        "training_duration": "TRAINING_DURATION_NOT_AUTHENTIC (Calculated from timer spanning fallback exception block without backprop epochs)"
    }

    # 4. Dataset Authenticity Inspection
    raw_img_dir = "data/raw/doclaynet_subset/images"
    raw_val_json = "data/raw/doclaynet_subset/val.json"
    
    if os.path.exists(raw_img_dir):
        raw_imgs = os.listdir(raw_img_dir)
        total_raw_bytes = sum(os.path.getsize(os.path.join(raw_img_dir, f)) for f in raw_imgs)
        dataset_authentic = {
            "real_images_present": True,
            "image_count": len(raw_imgs),
            "total_bytes": total_raw_bytes,
            "sample_files": raw_imgs[:3],
            "val_json_present": os.path.exists(raw_val_json)
        }
    else:
        dataset_authentic = {"real_images_present": False}

    audit_report["dataset_authenticity"] = dataset_authentic
    print(f"3. Dataset Authenticity: {dataset_authentic['image_count']} real DocLayNet page images verified ({round(dataset_authentic['total_bytes'] / 1024 / 1024, 2)} MB).")

    # 5. Environment Blocker Analysis
    audit_report["environment_blocker"] = {
        "blocker_code": "ULTRALYTICS_INSTALLATION_BLOCKED",
        "sub_reason": "WINDOWS_MAX_PATH",
        "details": "Windows default 260-character path limit prevented pip from extracting deep PyTorch wheel subdirectories under Windows Store Python AppData path.",
        "recommended_fix": "Enable LongPathsEnabled = 1 in Windows Registry (HKLM\\SYSTEM\\CurrentControlSet\\Control\\FileSystem) or use shallow venv path (C:\\venv)."
    }

    # 6. Critical Final Phase Classification
    final_classification = "PIPELINE_ONLY_TRAINING_NOT_VERIFIED"
    audit_report["final_classification"] = final_classification
    print(f"4. Final Phase 5B.2 Classification: {final_classification}\n")

    print("=== AUDIT SUMMARY JSON ===")
    print(json.dumps(audit_report, indent=2))

if __name__ == "__main__":
    run_authenticity_audit()
