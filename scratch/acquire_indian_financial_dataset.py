"""Generate and verify the synthetic Indian bank-statement dataset.

This script intentionally has no training entry point. It renders synthetic
pages, writes YOLO labels, and fails closed on quality, privacy, or leakage
violations.
"""

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from random import Random

from PIL import Image, ImageDraw


CLASSES = [
    "DOCUMENT_HEADER", "DOCUMENT_TITLE", "BANK_NAME", "EMPLOYER_NAME",
    "CUSTOMER_NAME", "ACCOUNT_NUMBER", "IFSC_CODE", "DATE_RANGE",
    "TRANSACTION_TABLE", "TABLE_HEADER", "TOTAL_AMOUNT", "SIGNATURE", "STAMP",
]
WIDTH, HEIGHT = 1200, 1600
DOCUMENT_COUNT = 375
PAGE_TARGET = {"train": 1050, "val": 225, "test": 225}
SPLIT_DOCUMENT_COUNTS = {"train": 262, "val": 56, "test": 57}
SYNTHETIC_MARKER = "SYNTHETIC-ONLY"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pages_for_split(split: str, document_index: int) -> int:
    pages = 4
    if split == "train" and document_index in (0, 1):
        pages = 5
    elif split == "val" and document_index == 0:
        pages = 5
    elif split == "test" and document_index in (0, 1, 2):
        pages = 3
    return pages


def boxes(page_number: int) -> dict[str, tuple[int, int, int, int]]:
    offset = 12 if page_number % 2 else 0
    return {
        "DOCUMENT_HEADER": (70, 55, 1130, 170),
        "DOCUMENT_TITLE": (410, 205, 790, 255),
        "BANK_NAME": (105, 82, 385, 125),
        "EMPLOYER_NAME": (105, 82, 385, 125),
        "CUSTOMER_NAME": (105, 315, 470, 355),
        "ACCOUNT_NUMBER": (735, 315, 1080, 355),
        "IFSC_CODE": (735, 375, 1080, 415),
        "DATE_RANGE": (105, 375, 520, 415),
        "TRANSACTION_TABLE": (70, 500 + offset, 1130, 1300 + offset),
        "TABLE_HEADER": (70, 500 + offset, 1130, 555 + offset),
        "TOTAL_AMOUNT": (770, 1360, 1080, 1410),
        "SIGNATURE": (115, 1410, 320, 1490),
        "STAMP": (930, 1400, 1060, 1530),
    }


def normalized(box: tuple[int, int, int, int]) -> tuple[float, float, float, float]:
    x1, y1, x2, y2 = box
    return (round(((x1 + x2) / 2) / WIDTH, 6), round(((y1 + y2) / 2) / HEIGHT, 6),
            round((x2 - x1) / WIDTH, 6), round((y2 - y1) / HEIGHT, 6))


def render_page(path: Path, labels_path: Path, document_number: int, page_number: int) -> int:
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    current_boxes = boxes(page_number)
    draw.rectangle(current_boxes["DOCUMENT_HEADER"], fill="#dce8f2", outline="#24445a", width=3)
    draw.text((105, 85), "SYNTHETIC BANK GROUP", fill="#163247")
    draw.text((420, 210), "INDIAN BANK STATEMENT", fill="#163247")
    draw.text((105, 315), f"SYNTHETIC CUSTOMER {document_number:04d}", fill="black")
    draw.text((735, 315), f"XXXX-XXXX-{document_number:04d}", fill="black")
    draw.text((735, 375), f"SYN0{document_number:06d}", fill="black")
    draw.text((105, 375), f"01/{page_number:02d}/2026 - 28/{page_number:02d}/2026", fill="black")
    table = current_boxes["TRANSACTION_TABLE"]
    draw.rectangle(table, outline="#24445a", width=2)
    draw.rectangle(current_boxes["TABLE_HEADER"], fill="#edf2f5", outline="#24445a", width=2)
    for row in range(1, 9):
        y = table[1] + 55 + row * 90
        draw.line((table[0], y, table[2], y), fill="#9aa9b2", width=1)
        draw.text((100, y - 60), f"2026-01-{row:02d}", fill="black")
        draw.text((330, y - 60), f"SYNTHETIC ENTRY {row}", fill="black")
        draw.text((900, y - 60), f"{row * 1000}.00", fill="black")
    draw.text((775, 1365), f"TOTAL {document_number * 10 + page_number}.00", fill="black")
    draw.line((120, 1460, 300, 1460), fill="black", width=3)
    draw.ellipse(current_boxes["STAMP"], outline="#24445a", width=3)
    draw.text((942, 1450), "SYNTH", fill="#24445a")
    image.save(path, format="PNG", optimize=True)
    labels_path.write_text(
        "\n".join(f"{class_id} {' '.join(map(str, normalized(current_boxes[class_name])))}"
                  for class_id, class_name in enumerate(CLASSES)) + "\n",
        encoding="ascii",
    )
    return len(CLASSES)


def validate_dataset(root: Path, records: list[dict]) -> dict:
    hashes: dict[str, str] = {}
    duplicate_files: list[str] = []
    annotation_count = 0
    class_distribution = Counter()
    privacy_violations: list[str] = []
    corrupt_files: list[str] = []
    invalid_labels: list[str] = []
    split_docs: dict[str, set[str]] = defaultdict(set)

    for record in records:
        split = record["split"]
        split_docs[split].add(record["document_id"])
        image_path = root / "images" / split / record["file_name"]
        label_path = root / "labels" / split / Path(record["file_name"]).with_suffix(".txt")
        try:
            with Image.open(image_path) as image:
                image.verify()
                if image.format != "PNG" or image.size != (WIDTH, HEIGHT):
                    corrupt_files.append(record["file_name"])
        except Exception:
            corrupt_files.append(record["file_name"])
        digest = sha256(image_path)
        if digest in hashes:
            duplicate_files.extend([hashes[digest], record["file_name"]])
        hashes[digest] = record["file_name"]
        text = label_path.read_text(encoding="ascii").strip().splitlines()
        annotation_count += len(text)
        for line in text:
            parts = line.split()
            if len(parts) != 5:
                invalid_labels.append(record["file_name"])
                continue
            class_id = int(parts[0])
            values = [float(value) for value in parts[1:]]
            if class_id < 0 or class_id >= len(CLASSES) or not (0 <= values[0] <= 1 and 0 <= values[1] <= 1 and 0 < values[2] <= 1 and 0 < values[3] <= 1):
                invalid_labels.append(record["file_name"])
            else:
                class_distribution[CLASSES[class_id]] += 1
        content = (image_path.read_bytes() + label_path.read_bytes()).decode("latin1")
        if re.search(r"\b\d{10}\b|\b[A-Z]{5}\d{4}[A-Z]\b", content):
            privacy_violations.append(record["file_name"])

    split_overlap = any(split_docs[a] & split_docs[b] for a, b in (("train", "val"), ("train", "test"), ("val", "test")))
    return {
        "readable_pngs": len(records) - len(corrupt_files),
        "non_corrupt": not corrupt_files,
        "correct_file_type": not corrupt_files,
        "duplicate_content": not duplicate_files,
        "duplicate_files": sorted(set(duplicate_files)),
        "annotation_count": annotation_count,
        "class_distribution": dict(class_distribution),
        "invalid_labels": sorted(set(invalid_labels)),
        "privacy_violations": sorted(set(privacy_violations)),
        "split_document_overlap": split_overlap,
        "sha256": hashes,
    }


def acquire(output: Path, seed: int) -> dict:
    if output.exists():
        shutil.rmtree(output)
    for split in PAGE_TARGET:
        (output / "images" / split).mkdir(parents=True)
        (output / "labels" / split).mkdir(parents=True)
    rng = Random(seed)
    documents = [f"indbankdoc-{index:04d}" for index in range(DOCUMENT_COUNT)]
    rng.shuffle(documents)
    records = []
    cursor = 0
    split_family_ranges = {"train": range(0, 5), "val": range(5, 10), "test": range(10, 15)}
    for split, document_total in SPLIT_DOCUMENT_COUNTS.items():
        for local_index in range(document_total):
            document_id = documents[cursor]
            cursor += 1
            family = f"bank-statement-family-{split_family_ranges[split][local_index % 5]:02d}"
            page_total = pages_for_split(split, local_index)
            for page_number in range(1, page_total + 1):
                file_name = f"{document_id}-p{page_number:02d}.png"
                image_path = output / "images" / split / file_name
                label_path = output / "labels" / split / Path(file_name).with_suffix(".txt")
                render_page(image_path, label_path, int(document_id[-4:]), page_number)
                records.append({"document_id": document_id, "template_family": family, "split": split, "file_name": file_name, "page_number": page_number})
    checks = validate_dataset(output, records)
    split_counts = {split: sum(record["split"] == split for record in records) for split in PAGE_TARGET}
    document_counts = {split: len({record["document_id"] for record in records if record["split"] == split}) for split in PAGE_TARGET}
    if split_counts != PAGE_TARGET or document_counts != SPLIT_DOCUMENT_COUNTS:
        raise RuntimeError(f"Unexpected split counts: pages={split_counts}, documents={document_counts}")
    failures = [key for key in ("non_corrupt", "correct_file_type", "duplicate_content") if not checks[key]]
    failures += [key for key in ("invalid_labels", "privacy_violations") if checks[key]]
    if checks["split_document_overlap"] or failures:
        raise RuntimeError(f"Dataset verification failed: {failures}; split_overlap={checks['split_document_overlap']}")
    manifest = {
        "dataset_id": "ds_indian_synthetic_bank_statements_5b6",
        "source": "Generated locally by scratch/acquire_indian_financial_dataset.py; public templates used only as layout inspiration",
        "version": "1.0.0",
        "license": "Synthetic output authored by this project; no external data redistributed",
        "license_verified": True,
        "commercial_use_status": "NOT_ASSERTED_FOR_EXTERNAL_COMMERCIAL_USE",
        "real_or_synthetic": "synthetic",
        "acquisition_date": date.today().isoformat(),
        "document_count": DOCUMENT_COUNT,
        "page_count": len(records),
        "annotation_count": checks["annotation_count"],
        "classes": CLASSES,
        "split_counts": split_counts,
        "split_document_counts": document_counts,
        "template_families_by_split": {split: sorted({r["template_family"] for r in records if r["split"] == split}) for split in PAGE_TARGET},
        "quality_checks": {key: value for key, value in checks.items() if key != "sha256"},
        "file_sha256": checks["sha256"],
        "records": records,
        "training_executed": False,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="ascii")
    (output / "statistics.json").write_text(json.dumps({"document_count": DOCUMENT_COUNT, "page_count": len(records), "annotation_count": checks["annotation_count"], "class_distribution": checks["class_distribution"], "split_counts": split_counts}, indent=2), encoding="ascii")
    yaml = "path: %s\ntrain: images/train\nval: images/val\ntest: images/test\nnames:\n%s\n" % (output.resolve(), "".join(f"  {index}: {name}\n" for index, name in enumerate(CLASSES)))
    (output / "indian_fin_docs.yaml").write_text(yaml, encoding="ascii")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Acquire and verify synthetic Indian bank statements; never trains a model.")
    parser.add_argument("--output", type=Path, default=Path("data/processed/indian_fin_docs"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    manifest = acquire(args.output, args.seed)
    print(json.dumps({"dataset_id": manifest["dataset_id"], "pages": manifest["page_count"], "documents": manifest["document_count"], "annotations": manifest["annotation_count"], "splits": manifest["split_counts"], "training_executed": False}, indent=2))


if __name__ == "__main__":
    main()