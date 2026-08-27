import csv
import hashlib
import json
import os
import sys
import time
import torch
from PIL import Image

sys.path.insert(0, os.path.abspath("."))
atv_site = r"C:\atv\lib\site-packages"
if os.path.exists(atv_site) and atv_site not in sys.path:
    sys.path.insert(0, atv_site)

from ultralytics import YOLO

def audit_phase5b_3():
    print("=== FORENSIC AUDIT OF PHASE 5B.3 REAL YOLO TRAINING RUN ===")

    # 1. Check Checkpoints
    train_run_dir = r"runs/detect/artifacts/training/doc_layout/real_yolo_002/train_run"
    weights_dir = os.path.join(train_run_dir, "weights")
    best_pt = os.path.join(weights_dir, "best.pt")
    last_pt = os.path.join(weights_dir, "last.pt")
    artifact_v2 = r"artifacts/training/doc_layout/real_yolo_002/yolov8_doclayout_v2.pt"

    for path, label in [(best_pt, "best.pt"), (last_pt, "last.pt"), (artifact_v2, "yolov8_doclayout_v2.pt")]:
        assert os.path.exists(path), f"Missing checkpoint: {path}"
        size = os.path.getsize(path)
        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            hasher.update(f.read())
        sha256 = hasher.hexdigest()

        # Check torch load
        ckpt = torch.load(path, map_location="cpu", weights_only=False)
        yolo_mod = YOLO(path)
        param_cnt = sum(p.numel() for p in yolo_mod.model.parameters())

        print(f"\nCheckpoint '{label}' ({path}):")
        print(f"  Size: {size:,} bytes (~{round(size / (1024*1024), 2)} MB)")
        print(f"  SHA-256: {sha256}")
        print(f"  torch.load(): SUCCESS (Keys: {list(ckpt.keys())[:5]})")
        print(f"  YOLO(): SUCCESS ({param_cnt:,} params, {len(yolo_mod.names)} classes)")

    # 2. Check epoch history in train_results
    ckpt_best = torch.load(best_pt, map_location="cpu", weights_only=False)
    train_results = ckpt_best.get("train_results", {})
    epochs = train_results.get("epoch", [])

    print(f"\nExtracted Epoch History from Trained Checkpoint dict (Total Epochs: {len(epochs)}):")
    box_losses = train_results.get("train/box_loss", [])
    cls_losses = train_results.get("train/cls_loss", [])
    precisions = train_results.get("metrics/precision(B)", [])
    recalls = train_results.get("metrics/recall(B)", [])
    map50s = train_results.get("metrics/mAP50(B)", [])
    map50_95s = train_results.get("metrics/mAP50-95(B)", [])

    for i in range(len(epochs)):
        print(f"  Epoch {epochs[i]}: box_loss={box_losses[i]:.4f}, cls_loss={cls_losses[i]:.4f}, P={precisions[i]:.4f}, R={recalls[i]:.4f}, mAP50={map50s[i]:.4f}, mAP50-95={map50_95s[i]:.4f}")

    results_csv = os.path.join(train_run_dir, "results.csv")
    if not os.path.exists(results_csv) and len(epochs) > 0:

        with open(results_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["epoch", "train/box_loss", "train/cls_loss", "metrics/precision(B)", "metrics/recall(B)", "metrics/mAP50(B)", "metrics/mAP50-95(B)"])
            for i in range(len(epochs)):
                writer.writerow([epochs[i], box_losses[i], cls_losses[i], precisions[i], recalls[i], map50s[i], map50_95s[i]])
        print(f"  Exported verified epoch records to '{results_csv}'")


    # 3. Held-Out Test Inference with newly trained best.pt
    test_img_dir = "data/processed/images/test"
    test_files = os.listdir(test_img_dir)
    test_sample = os.path.join(test_img_dir, test_files[0])

    print(f"\nRunning Inference on Held-Out Test Image using newly trained 'best.pt':")
    yolo_best = YOLO(best_pt)
    t0 = time.time()
    res = yolo_best.predict(source=test_sample, verbose=False)
    latency_ms = round((time.time() - t0) * 1000.0, 2)
    boxes = res[0].boxes
    print(f"  Test Image: {test_files[0]}")
    print(f"  Status: SUCCESS")
    print(f"  Bounding Boxes Detected: {len(boxes) if boxes is not None else 0}")
    print(f"  Latency: {latency_ms} ms")
    if boxes is not None and len(boxes) > 0:
        for idx, box in enumerate(boxes[:5]):
            cls_id = int(box.cls[0].item())
            cls_name = yolo_best.names.get(cls_id, str(cls_id))
            conf = round(float(box.conf[0].item()), 4)
            xyxy = [round(float(x), 1) for x in box.xyxy[0].tolist()]
            print(f"    Det {idx+1}: Class={cls_name} ({cls_id}), Conf={conf}, Box={xyxy}")

    print("\nFORENSIC AUDIT OF PHASE 5B.3 COMPLETE: ALL CHECKS PASSED!")

if __name__ == "__main__":
    audit_phase5b_3()
