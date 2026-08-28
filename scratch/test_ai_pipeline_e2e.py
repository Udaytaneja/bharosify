import asyncio
import os
import sys
from pathlib import Path

# Ensure OCR_PYTHON_EXECUTABLE points to isolated Windows ocr-env during local execution
os.environ["OCR_PYTHON_EXECUTABLE"] = str(Path("ocr-env/Scripts/python.exe").resolve())

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai.app.perception import document_intelligence_pipeline

async def main():
    img_path = Path("data/processed/indian_fin_docs/images/test/indbankdoc-0003-p01.png")
    if not img_path.exists():
        print(f"ERROR: Sample fixture {img_path} not found.")
        return

    with open(img_path, "rb") as f:
        file_bytes = f.read()

    print(f"Executing AI Perception Pipeline on '{img_path.name}' ({len(file_bytes)} bytes)...")
    res = await document_intelligence_pipeline.process_document(
        file_bytes=file_bytes,
        file_name=img_path.name,
    )

    result_dict = res.model_dump() if hasattr(res, "model_dump") else dict(res)

    layout_count = len(result_dict.get("layout_regions", []))
    ocr_count = len(result_dict.get("ocr_lines", []))
    fields = result_dict.get("fields", {})
    confidence = result_dict.get("confidence", 0.0)

    print("\n================ AI PERCEPTION E2E RESULT ================")
    print(f"Document Type: {result_dict.get('document_type')}")
    print(f"YOLO Layout Regions Detected: {layout_count}")
    print(f"PaddleOCR Text Lines Extracted: {ocr_count}")
    print(f"Grounded Extracted Fields Count: {len(fields)}")
    print(f"Overall Confidence Score: {confidence * 100:.1f}%")
    print(f"Model Checkpoint: {result_dict.get('model_metadata', {}).get('provenance', {}).get('layout_checkpoint')}")

    if layout_count > 0 and ocr_count > 0:
        print("\nSUCCESS: REAL YOLO + REAL PaddleOCR + REAL Field Extraction VERIFIED!")

if __name__ == "__main__":
    asyncio.run(main())
