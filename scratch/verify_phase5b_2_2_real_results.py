import hashlib
import json
import os
import sys
import torch
from ultralytics import YOLO

def verify_real_training_output():
    print("=== STEP 7-10: VERIFY GENUINE TRAINED CHECKPOINT & INFERENCE ===")
    
    artifact_path = "artifacts/training/doc_layout/real_yolo_001/yolov8_doclayout_v1.pt"
    assert os.path.exists(artifact_path), f"Artifact missing at {artifact_path}"
    
    # 1. Artifact Checkpoint Verification
    byte_size = os.path.getsize(artifact_path)
    hasher = hashlib.sha256()
    with open(artifact_path, "rb") as f:
        hasher.update(f.read())
    sha256 = hasher.hexdigest()
    
    print(f"Artifact Size: {byte_size:,} bytes | SHA-256: {sha256}")
    assert byte_size > 1_000_000, f"Artifact size {byte_size} is too small to be genuine YOLO model!"

    # 2. PyTorch Load Test
    ckpt = torch.load(artifact_path, map_location="cpu", weights_only=False)
    assert isinstance(ckpt, dict), "Loaded checkpoint is not a valid PyTorch dictionary!"
    assert "model" in ckpt or "state_dict" in ckpt or "ema" in ckpt, "Checkpoint missing PyTorch model weights state_dict!"
    print("PyTorch torch.load() succeeded: Valid binary PyTorch checkpoint!")

    # 3. Ultralytics Load Test
    yolo_model = YOLO(artifact_path)
    model_obj = yolo_model.model
    param_count = sum(p.numel() for p in model_obj.parameters())
    class_names = yolo_model.names
    class_count = len(class_names)

    print(f"Ultralytics YOLO() loaded successfully:")
    print(f"  Parameter Count: {param_count:,}")
    print(f"  Class Count: {class_count}")
    print(f"  Class Names: {class_names}")

    # 4. Results.csv Check
    runs_dir = "runs/detect/artifacts/training/doc_layout/real_yolo_001/train_run"
    results_csv = os.path.join(runs_dir, "results.csv")
    assert os.path.exists(results_csv), f"results.csv missing in {runs_dir}"
    with open(results_csv, "r") as f:
        csv_lines = f.readlines()
    print(f"results.csv exists: {len(csv_lines) - 1} epoch rows logged.")

    # 5. Real Inference Verification on Held-Out Test Image
    test_img_dir = "data/processed/images/test"
    test_imgs = os.listdir(test_img_dir)
    assert len(test_imgs) > 0, "No held-out test images found!"
    sample_img = os.path.join(test_img_dir, test_imgs[0])

    import time
    start_t = time.time()
    results = yolo_model.predict(source=sample_img, verbose=False)
    latency_ms = round((time.time() - start_t) * 1000.0, 2)

    boxes = results[0].boxes
    box_count = len(boxes) if boxes is not None else 0
    print(f"Real Inference on '{test_imgs[0]}':")
    print(f"  Detections: {box_count} bounding boxes detected")
    print(f"  Inference Latency: {latency_ms} ms")
    if box_count > 0:
        for idx, box in enumerate(boxes):
            cls_id = int(box.cls[0].item())
            conf = round(float(box.conf[0].item()), 4)
            print(f"    Box {idx+1}: class '{class_names[cls_id]}' (ID {cls_id}), confidence = {conf}")

    print("\nSUCCESS: All Genuine Training and Inference Verification Steps Passed!")

if __name__ == "__main__":
    verify_real_training_output()
