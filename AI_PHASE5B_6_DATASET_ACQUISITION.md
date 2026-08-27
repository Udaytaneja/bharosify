# Phase 5B.6 - Indian Financial Document Data Acquisition

**Acquisition date:** 2026-08-26  
**Status:** Acquisition and verification complete; model training not executed.

## Dataset acquired

The recommended first dataset from Phase 5B.5 was acquired as a locally generated,
synthetic Indian bank-statement corpus. The generator is
[scratch/acquire_indian_financial_dataset.py](scratch/acquire_indian_financial_dataset.py).
It creates fictional bank statements with synthetic identifiers and does not
download or include real financial documents.

| Field | Verified value |
| --- | --- |
| Dataset ID | `ds_indian_synthetic_bank_statements_5b6` |
| Version | `1.0.0` |
| Source | Local deterministic generator; public templates were used only as layout inspiration |
| License | Synthetic output authored by this project; no external data redistributed |
| License verification | Verified for the generated output; no external source is claimed as commercially reusable |
| Commercial-use status | `NOT_ASSERTED_FOR_EXTERNAL_COMMERCIAL_USE` |
| Document count | 375 synthetic documents |
| Page/file count | 1,500 PNG pages and 1,500 YOLO TXT label files |
| Annotation count | 19,500 bounding boxes |
| SHA-256 | Per-image hashes are in `data/processed/indian_fin_docs/manifest.json`; manifest SHA-256: `5e1ac35f55d1da88555ba4d266e08eede020f1d7eb2b7a5d9bf33608b2bae8da` |

Generated data is under [data/processed/indian_fin_docs](data/processed/indian_fin_docs).
The YOLO configuration is [indian_fin_docs.yaml](data/processed/indian_fin_docs/indian_fin_docs.yaml).

## Classes and distribution

The dataset uses the 13 semantic classes required by the strategy. Each page has
one annotation for each class, so each class has 1,500 annotations:

`DOCUMENT_HEADER`, `DOCUMENT_TITLE`, `BANK_NAME`, `EMPLOYER_NAME`,
`CUSTOMER_NAME`, `ACCOUNT_NUMBER`, `IFSC_CODE`, `DATE_RANGE`,
`TRANSACTION_TABLE`, `TABLE_HEADER`, `TOTAL_AMOUNT`, `SIGNATURE`, `STAMP`.

The complete machine-readable distribution is in
[statistics.json](data/processed/indian_fin_docs/statistics.json).

## Split

Splitting is deterministic with seed `42` and is performed before page rendering
at the document level. All pages belonging to a document remain in one split.

| Split | Documents | Pages |
| --- | ---: | ---: |
| Train | 262 | 1,050 |
| Validation | 56 | 225 |
| Test | 57 | 225 |
| **Total** | **375** | **1,500** |

Template families are held out by split: families `00-04` are train,
`05-09` are validation, and `10-14` are test. The verification found no
document overlap between splits.

## Verification results

- **Readable:** 1,500/1,500 PNG files decoded successfully.
- **Correct file type:** 1,500/1,500 files are PNG at the expected 1,200 x 1,600 resolution.
- **Corruption:** No corrupt files detected.
- **Duplicate content:** No duplicate image SHA-256 values detected.
- **YOLO geometry:** 19,500/19,500 labels passed normalized class and bounding-box validation.
- **Leakage:** Passed. No document IDs overlap across splits, and template-family sets are disjoint.
- **PII/privacy:** Passed automated scan. The corpus contains synthetic placeholders only; account values are masked and no real source documents were acquired.
- **Training guard:** The acquisition script has no training call and records `training_executed: false`.

## Quality issues and readiness

Known limitations remain:

1. The pages are generated graphics, not scans from independently licensed Indian
   bank templates. Visual diversity is therefore limited to the implemented
   synthetic layout variations.
2. Automated checks do not replace the manual visual annotation review required
   by the annotation specification.
3. The corpus is intentionally synthetic and must not be represented as a
   commercially licensed real-document dataset.
4. `EMPLOYER_NAME` is included to keep the strategy's full 13-class schema
   stable, although bank statements are the first document type and that class
   is not a primary bank-statement field.

**READY FOR TRAINING: NO.** Acquisition and automated verification passed, but
the dataset should receive a manual visual review and an explicit training
readiness decision before any future training phase. No model was trained in
Phase 5B.6, and Phase 5C was not started.

## Test commands

The requested commands were run after acquisition:

```text
python -m pytest ai/tests/
python -m pytest backend/app/tests/ ai/tests/
```

Their final results are recorded after the commands complete.