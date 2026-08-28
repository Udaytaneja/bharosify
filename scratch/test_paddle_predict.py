import os
import sys
from pathlib import Path

img_path = Path("data/processed/indian_fin_docs/images/test/indbankdoc-0003-p01.png").resolve()

os.environ["FLAGS_enable_pir_api"] = "0"
os.environ["PFLAGS_enable_onednn"] = "0"
os.environ["FLAGS_use_mkldnn"] = "0"

from paddleocr import PaddleOCR

print(f"Testing PaddleOCR predict() on '{img_path.name}'...")
ocr = PaddleOCR(lang="en", device="cpu", enable_mkldnn=False, use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False)
results = ocr.predict(str(img_path))

lines = []
for result in results:
    data = result if isinstance(result, dict) else dict(result)
    texts = data.get("rec_texts", [])
    scores = data.get("rec_scores", [])
    boxes = data.get("rec_boxes", data.get("dt_polys", []))
    for index, text in enumerate(texts):
        lines.append((text, float(scores[index])))

print(f"SUCCESS: Extracted {len(lines)} lines of text from real document image:")
for text, conf in lines[:10]:
    print(f" - [{conf:.2f}] {text}")
