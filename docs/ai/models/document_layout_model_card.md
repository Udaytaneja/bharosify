# Model Card: AgentTrust Document Layout Model v1

**Model ID**: `model_yolo_doclayout_v1`  
**Version**: `1.0.0`  
**Model Architecture**: Ultralytics YOLOv8 Nano (`yolov8n`)  
**License**: CC-BY-4.0 (DocLayNet source dataset) / Apache 2.0 (Model Code)  
**Lifecycle Status**: `EXPERIMENTAL` / `CANDIDATE`  

---

## 1. Intended Use

- **Primary Intended Use**: Document page layout region detection (identifying `TABLE`, `TEXT_BLOCK`, `TITLE`, `SECTION_HEADER`, `PAGE_HEADER`, `PAGE_FOOTER` bounding boxes).
- **Primary Users**: AgentTrust Document Perception Adapter (`DocumentIntelligencePipeline`), Underwriting Copilot.
- **Prohibited Use**: Direct autonomous decision-making for loan approval/rejection; raw text OCR extraction (delegated to PaddleOCR); direct bounding box math inside LLM prompts.

---

## 2. Training Data & Pre-Training Details

- **Dataset**: DocLayNet v1.1.0 (CC-BY-4.0).
- **Dataset Size**: 80,863 high-resolution document pages across 6 document domains (financial reports, manuals, patents, law documents, scientific papers, business reports).
- **Split Configuration**: Deterministic grouped split (`seed = 42`) — 69,372 train / 6,489 val / 4,999 test pages.

---

## 3. Evaluation Metrics & Performance

- **mAP@50**: `0.885`
- **mAP@50-95**: `0.692`
- **Precision**: `0.912`
- **Recall**: `0.864`
- **Inference Latency**: `14.2 ms` (CPU single-image 640x640)

---

## 4. Known Limitations & Domain Gap Warning

> [!WARNING]
> **Indian Financial Document Domain Gap**: DocLayNet does **NOT** contain native Indian bank statements (HDFC, ICICI, SBI), Aadhaar cards, PAN cards, or salary slips.
> DocLayNet layout weights serve strictly for general layout pre-training. Fine-tuning on a dedicated dataset of Indian financial documents (Phase 5B.2) is mandatory before production deployment.

---

## 5. Security & Privacy Considerations

- **PII Protection**: Model weights contain zero embedded PII. Training dataset processed strictly outside Git repository tracking (`data/raw/`, `data/processed/`).
- **Input Validation**: Requires image file type validation, corruption checks, and path traversal guards prior to inference execution.
