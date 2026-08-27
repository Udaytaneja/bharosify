# Phase 5B.7A - Synthetic Indian Document Dataset Validation

**Date:** 2026-08-27  
**Final classification:** **NOT_READY**  
**Training executed:** No  
**Phase 5C started:** No

## Scope and conclusion

This audit validates the existing `ds_indian_synthetic_bank_statements_5b6`
dataset without modifying it or starting model training. The files are
internally consistent and privacy-safe as synthetic data, but the dataset is
not suitable as evidence for an Indian-domain fine-tuning run under the stated
requirements. Its manifest explicitly says `real_or_synthetic: synthetic`,
and its visual/domain variation is too narrow for reliable real-document
Indian banking generalization.

The environment is independently **BLOCKED** for YOLO execution because
Ultralytics is not installed. The overall dataset classification remains
**NOT_READY** because the dataset itself fails the required real-data and
realism criteria.

## Dataset provenance and usage

- Dataset ID: `ds_indian_synthetic_bank_statements_5b6`
- Version: `1.0.0`
- Manifest: [data/processed/indian_fin_docs/manifest.json](data/processed/indian_fin_docs/manifest.json)
- Generator: [scratch/acquire_indian_financial_dataset.py](scratch/acquire_indian_financial_dataset.py)
- Provenance: generated locally by the project; public templates were used
  only as layout inspiration
- Manifest status: `real_or_synthetic: synthetic`
- License: synthetic output authored by this project; no external data
  redistributed
- License verified: `true` for the generated output
- Commercial-use status: `NOT_ASSERTED_FOR_EXTERNAL_COMMERCIAL_USE`

The generator contains no download or training entry point. It renders pages
with PIL, writes YOLO labels, and performs fail-closed integrity/privacy/
leakage checks before writing the manifest.

## Size, classes, and distribution

| Measure | Verified result |
|---|---:|
| Documents | 375 |
| Pages/images | 1,500 |
| YOLO label files | 1,500 |
| Annotations | 19,500 |
| Classes | 13 |

All 13 classes are present, with exactly 1,500 annotations per class:

| ID | Class | Count |
|---:|---|---:|
| 0 | `DOCUMENT_HEADER` | 1,500 |
| 1 | `DOCUMENT_TITLE` | 1,500 |
| 2 | `BANK_NAME` | 1,500 |
| 3 | `EMPLOYER_NAME` | 1,500 |
| 4 | `CUSTOMER_NAME` | 1,500 |
| 5 | `ACCOUNT_NUMBER` | 1,500 |
| 6 | `IFSC_CODE` | 1,500 |
| 7 | `DATE_RANGE` | 1,500 |
| 8 | `TRANSACTION_TABLE` | 1,500 |
| 9 | `TABLE_HEADER` | 1,500 |
| 10 | `TOTAL_AMOUNT` | 1,500 |
| 11 | `SIGNATURE` | 1,500 |
| 12 | `STAMP` | 1,500 |

The machine-readable summary is [data/processed/indian_fin_docs/statistics.json](data/processed/indian_fin_docs/statistics.json), and the class mapping is [data/processed/indian_fin_docs/indian_fin_docs.yaml](data/processed/indian_fin_docs/indian_fin_docs.yaml).

## Integrity and annotation audit

An independent read-only audit inspected all 1,500 records:

| Check | Result |
|---|---|
| PNG decoding and dimensions | 1,500/1,500 valid; PNG, RGB, 1200 x 1600 |
| Label files | 1,500/1,500 present |
| Label record count | 13 per page; 19,500 total |
| Class IDs | 19,500/19,500 in range 0-12 |
| Normalized coordinates | 19,500/19,500 valid: centers in [0,1], widths/heights in (0,1] |
| Exact generator-coordinate comparison | 19,500/19,500 match; 0 mismatches |
| Duplicate image content | 0 duplicate SHA-256 values |

The manifest and statistics file agree on document, page, annotation, split,
and class counts.

## Split isolation

The generator assigns documents before rendering pages. The verified split
counts are:

| Split | Documents | Pages | Template families |
|---|---:|---:|---|
| Train | 262 | 1,050 | `bank-statement-family-00` through `04` |
| Validation | 56 | 225 | `bank-statement-family-05` through `09` |
| Test | 57 | 225 | `bank-statement-family-10` through `14` |

Independent checks found:

- 0 document IDs shared by any split pair
- 0 template families shared by any split pair
- all 1,500 manifest records accounted for by the three splits

Isolation therefore passes, although the family holdout is generated from the
same narrow rendering system rather than independent real-world sources.

## Indian banking-layout realism

**Result: insufficient for the requested fine-tuning readiness.** A visual
inspection of a rendered test page and the generator show a clean schematic
bank-statement-like page, but not realistic Indian banking-document diversity.
The corpus has:

- one locally authored synthetic bank-group style;
- fixed 1200 x 1600 white pages and highly regular coordinates;
- literal text such as `SYNTHETIC BANK GROUP`, `SYNTHETIC CUSTOMER`,
  `SYNTHETIC ENTRY`, and `SYNTH`;
- a fixed eight-row transaction table with simple dates and amounts;
- no scan noise, skew, compression artifacts, handwriting, multilingual text,
  varied bank branding, alternate statement formats, or realistic field
  variation;
- `BANK_NAME` and `EMPLOYER_NAME` assigned the same bounding box on every page;
- exactly one instance of every class on every page, which is not a natural
  banking-document class distribution.

It is useful as a deterministic annotation/pipeline fixture or a controlled
smoke-test corpus. It is not sufficient as a representative Indian banking
benchmark or as the sole dataset for domain adaptation.

## PII and privacy

**Result: no real PII found; synthetic markers are intentional.** The generator
creates fictional/masked values and uses project-generated identifiers. Its
privacy scan found no violations, and the manifest records
`privacy_violations: []`. The rendered text contains explicit synthetic
markers, masked account values, and synthetic IFSC-like values; these are not
real customer data. This conclusion is about absence of real PII, not evidence
that the corpus is real.

## Existing checkpoint verification

The requested checkpoint was not modified:

`runs/detect/artifacts/training/doc_layout/real_yolo_002/train_run/weights/best.pt`

- Exists: yes
- Size: 6,248,042 bytes
- SHA-256: `f1bc0e4d6e4b78f40681d93ce8bb4cf5cd34924bf1efb2ceddbc209d1da40250`
- `torch.load()`: failed before deserialization completed because the
  checkpoint references the missing `ultralytics` module
- `YOLO()`: not attempted successfully for the same missing dependency

No copy, rewrite, or replacement checkpoint was made.

## Python environment and dependency blocker

Read-only environment checks found:

- Python: 3.11.9
- PyTorch: `2.13.0+cpu`
- CUDA: unavailable (`torch.cuda.is_available() == False`)
- Ultralytics: not installed (`ModuleNotFoundError: No module named
  'ultralytics'`)
- Repository requirement files inspected: no Ultralytics/PyTorch pins found

Earlier repository training metadata names `Ultralytics 8.4.129 / PyTorch
2.13.0+cpu`, but that metadata is not an active dependency installation or a
verified pin for this environment.

No installation was attempted. Recommended fix: create or select an isolated
Python environment, install the project-approved compatible Ultralytics and
PyTorch versions there, verify `import torch` and `from ultralytics import
YOLO`, then run checkpoint loading as a separate preflight. Do not install into
the current environment without an explicit dependency decision.

## Final classification

**NOT_READY**

The dataset passes technical file, annotation, duplicate, privacy, and split
checks, but fails the required real-data criterion and lacks realistic Indian
banking variation. YOLO execution is additionally **BLOCKED** by the missing
Ultralytics dependency. No training, validation, inference, metrics, or model
artifacts were generated.
