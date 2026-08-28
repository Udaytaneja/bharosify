import os
import sys
from pathlib import Path

img_path = Path("data/processed/indian_fin_docs/images/test/indbankdoc-0003-p01.png").resolve()

os.environ["FLAGS_enable_pir_api"] = "0"
os.environ["PFLAGS_enable_onednn"] = "0"
os.environ["FLAGS_use_mkldnn"] = "0"

from paddleocr import PaddleOCR

print(f"Testing PaddleOCR directly on '{img_path.name}'...")
ocr = PaddleOCR(lang="en", device="cpu", enable_mkldnn=False, use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False)
results = ocr.ocr(str(img_path))

lines = []
if results and isinstance(results, list):
    for page_res in results:
        if not page_res:
            continue
        for box_item in page_res:
            text_str = box_item[1][0].strip()
            conf_val = float(box_item[1][1])
            lines.append((text_str, conf_val))

print(f"Extracted {len(lines)} lines of text:")
for text, conf in lines[:10]:
    print(f" - [{conf:.2f}] {text}")
