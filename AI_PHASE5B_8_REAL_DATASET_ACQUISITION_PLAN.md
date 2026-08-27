# Phase 5B.8 - Real Indian Document Dataset Acquisition Plan

**Date:** 2026-08-27  
**Status:** Planning only  
**Training executed:** No  
**Phase 5C started:** No  
**Current classification:** **NOT_READY**

## 1. Purpose and constraints

This document defines the acquisition, governance, privacy, annotation, and
acceptance requirements for a future real Indian financial-document dataset.
It does not acquire data, download candidate datasets, install packages, train
YOLO, generate metrics, or modify production code.

The existing synthetic dataset remains unchanged at
[data/processed/indian_fin_docs](data/processed/indian_fin_docs). It must not be
presented as real data, merged silently with real data, or used to claim
real-domain validation.

The source annotation standard is
[docs/ai/INDIAN_DOCUMENT_ANNOTATION_SPEC.md](docs/ai/INDIAN_DOCUMENT_ANNOTATION_SPEC.md).
The related strategy is
[AI_INDIAN_DOCUMENT_DATASET_STRATEGY.md](AI_INDIAN_DOCUMENT_DATASET_STRATEGY.md).

## 2. Dataset provenance decision

The project must acquire real documents only through an explicitly authorized,
traceable channel. Candidate data is acceptable only when the provider can
identify the source, collection authority, consent/legal basis, intended ML
use, retention period, and redistribution restrictions.

No scraped private documents, leaked datasets, screenshots of personal
financial records, or sources with unclear licensing may be used. Public forms,
blank templates, annual reports, and mock examples may be used as layout
reference, but they are not substitutes for the required real-document set.

Each source package must include a provenance record with:

- source/provider identity and contact;
- acquisition date and jurisdiction;
- document category and institution/vendor;
- lawful collection or authorization basis;
- license text or agreement identifier and permitted ML/commercial use;
- whether redistribution, derivative labels, and model training are allowed;
- anonymization/de-identification method and verification owner;
- source file hashes and immutable dataset version;
- retention, deletion, and access-control requirements;
- known exclusions, transformations, and quality limitations.

A missing or ambiguous provenance or license record is a rejection, not a
conditional approval.

## 3. Required document categories

The first real-domain corpus should cover the following categories. Category
labels must be recorded independently from layout labels.

| Category | Minimum real documents | Required structural coverage |
|---|---:|---|
| Bank statements | 1,000 | account header, statement period, transaction tables, balances, pagination, fees/credits/debits, varied account-summary placement |
| Salary slips | 500 | employer header, employee details, pay period, earnings, deductions, net pay, approval/signature areas |
| Loan statements | 400 | lender header, borrower/loan identifiers, principal, interest, EMI schedule, due/outstanding totals, notices |
| Income/employment documents | 300 | employment/income proof, employer identity, period, compensation or income fields, verification/signature areas |
| Other supported financial documents | 300 | authorized examples from Form 16, ITR acknowledgements/forms, account summaries, sanction letters, or equivalent supported types |
| **Total** | **2,500 documents minimum** | All categories represented in train, validation, and test subject to group isolation |

The minimum target is 2,500 documents and approximately 5,000 pages, with at
least 20,000 annotated instances overall. These are acquisition gates, not
claims about data currently available. If a category cannot meet its minimum,
the corpus is not ready for the initial domain experiment.

The `other` category must be explicitly enumerated before acquisition. PAN and
Aadhaar may be represented only by authorized, permanently de-identified
examples if their inclusion is legally necessary; they are not required for
the first fine-tuning corpus.

## 4. Diversity requirements

Counts alone are insufficient. The real corpus must contain independent visual
and structural variation.

### Institution and vendor diversity

Across the corpus, include at least:

- 8 independent bank/lender institutions or vendors for bank and loan
  documents combined;
- 8 independent employers/payroll vendors for salary and employment documents;
- no institution contributing more than 25% of the total corpus or 35% of any
  single category;
- institution identities recorded as provenance metadata, but never leaked
  through unauthorized PII.

### Layout and template diversity

Each major category must contain at least 12 independently authored template
families, with at least 8 families represented in training and at least 2
unseen families reserved for validation and 2 unseen families reserved for
held-out test. A template family means a distinct visual structure, not a
renamed copy with changed values.

Vary all of the following where naturally present:

- single-page and multi-page documents, including 1, 2-3, and 4+ page cases;
- portrait and landscape orientation where used in practice;
- table column order, merged cells, subtotals, continuation headers, and
  multi-table pages;
- dense and sparse pages, whitespace, margins, headers, footers, and sidebars;
- typography, font size, weight, line spacing, colors, logos, stamps, and
  signature placement;
- native PDFs, rasterized PDFs, scans, compression, skew, lighting, and
  moderate capture noise when legally present in the source;
- regional language or bilingual text where the authorized corpus supports it.

The data card must report category-by-category counts for institutions,
template families, page counts, orientations, and table structures. Near
identical pages with changed identifiers do not satisfy diversity.

## 5. Privacy and security requirements

Real PII is prohibited unless there is documented legal authorization and a
verified anonymization process approved for this dataset. The preferred rule
is to acquire already de-identified documents and reject raw personal records.

The released training copy must contain:

- no exposed PAN, Aadhaar, bank account, card, loan, employee, phone, email, or
  residential-address identifiers;
- no live names or signatures that can identify a person;
- no unredacted salary, transaction, tax, or repayment history linked to a
  person;
- no metadata, filenames, OCR layers, embedded PDF properties, or thumbnails
  that retain source PII;
- no reversible redactions or recoverable original text.

Account numbers must be masked to the approved last-four format or fully
redacted. Aadhaar must have the first eight digits permanently masked when an
authorized example is required. PAN must be anonymized. Names and addresses
must be replaced or obfuscated. Privacy scanning must cover both rendered
pixels and all file/container metadata.

Access to any controlled raw source must be isolated from the training copy,
logged, least-privilege, encrypted at rest, and deleted according to the
provenance agreement. The training manifest must record the de-identification
version and reviewer sign-off.

## 6. Real, synthetic, augmentation, and validation data

These sources must remain physically and logically distinct, with separate
manifests, hashes, licenses, and split assignments.

| Source type | Permitted role | Required treatment |
|---|---|---|
| **REAL DATA** | Primary domain fine-tuning evidence | Authorized, anonymized Indian documents only; immutable provenance and license; contributes to the real-data training/validation/test counts |
| **SYNTHETIC DATA** | Pipeline tests, controlled preflight, coverage analysis, or optional supplemental training | Keep `ds_indian_synthetic_bank_statements_5b6` unchanged and separately identified; never describe it as real or use it as real test evidence |
| **AUGMENTATION DATA** | Derived transformations of an explicitly identified source image | Store source ID, transform parameters, and parent hash; augmentation must remain in the parent split and never create new independent test evidence |
| **VALIDATION DATA** | Held-out model selection and final reporting | Use untouched authorized real documents; keep a separately governed final test subset unavailable during tuning |

Augmentations include only documented transformations such as scale, mild
rotation, blur, compression, or illumination changes. They cannot change
semantic content, invent labels, or cross a split boundary. Synthetic pages
and public templates are not counted toward the minimum real-data requirement.

## 7. Annotation taxonomy and mapping

The current Indian annotation specification defines these 13 semantic classes:

`DOCUMENT_HEADER`, `DOCUMENT_TITLE`, `BANK_NAME`, `EMPLOYER_NAME`,
`CUSTOMER_NAME`, `ACCOUNT_NUMBER`, `IFSC_CODE`, `DATE_RANGE`,
`TRANSACTION_TABLE`, `TABLE_HEADER`, `TOTAL_AMOUNT`, `SIGNATURE`, `STAMP`.

All applicable instances must be annotated with tight, visible-region boxes.
Class definitions and boundary rules must follow the specification. Optional
category-specific fields must be documented before annotation begins rather
than silently adding incompatible classes.

Exports are required in both formats:

- COCO JSON with image dimensions, category IDs, provenance/split metadata, and
  annotation IDs;
- YOLO TXT using `<class_id> <x_center> <y_center> <width> <height>` normalized
  coordinates, plus the matching YAML class mapping.

The current 13-class Indian semantic taxonomy is not identical to the existing
11-class generic DocLayNet layout taxonomy. Preserve both layers:

| Indian semantic class | Closest generic layout class |
|---|---|
| `DOCUMENT_HEADER` | `PAGE_HEADER` / `SECTION_HEADER` |
| `DOCUMENT_TITLE` | `TITLE` |
| `BANK_NAME`, `EMPLOYER_NAME` | `SECTION_HEADER` / `TEXT_BLOCK` |
| `CUSTOMER_NAME`, `ACCOUNT_NUMBER`, `IFSC_CODE`, `DATE_RANGE`, `TOTAL_AMOUNT` | `TEXT_BLOCK` |
| `TRANSACTION_TABLE`, `TABLE_HEADER` | `TABLE` |
| `SIGNATURE`, `STAMP` | `FIGURE` / `PICTURE` |

This mapping is a compatibility reference, not permission to collapse semantic
labels during annotation. The model configuration for a future experiment
must state whether it uses the 13-class semantic head, a generic 11-class
layout head, or a deliberately documented multi-task mapping.

Annotation QA must include double annotation for a representative sample,
reviewer adjudication, class-definition checks, tight-box review, missing and
extra-object review, and automated validation of every label. Every normalized
coordinate must satisfy the specification bounds; boxes must remain within the
image and preserve the complete visible text/graphic region.

## 8. Split and leakage strategy

Split assignment occurs at the highest available source-group level before
annotation tuning:

1. group all pages from one source document together;
2. group related revisions, statement periods, and duplicate exports together;
3. keep template family, institution/vendor, and generator/source signature
   groups disjoint whenever feasible;
4. assign groups deterministically after the group inventory is frozen.

Target split proportions are 70% train, 15% validation, and 15% final test by
document, stratified by category. The final test set must contain at least 375
real documents, including at least 75 bank statements, 40 salary slips, 30 loan
statements, 20 income/employment documents, and 20 other supported documents.

No page-level random split is allowed. No document, template family, source
PDF, institution-specific layout, identifier pattern, near-duplicate image,
or augmentation may appear in more than one split. Validation and test files
must be access-controlled and excluded from annotation-tuning decisions as
appropriate. A duplicate/perceptual-similarity audit must run across all
splits, and any collision is a release blocker.

## 9. Acceptance criteria: READY_FOR_FINE_TUNING

The real dataset may be declared `READY_FOR_FINE_TUNING` only when every item
below is evidenced in a versioned manifest and signed validation report:

- at least 2,500 authorized real documents and approximately 5,000 pages;
- all five required category groups meet their minimum counts;
- provenance, license, legal basis, intended ML use, and retention terms are
  complete for every source;
- privacy review finds no exposed PII, recoverable redaction, or sensitive
  metadata, with human sign-off and automated scan results;
- at least 8 institutions/vendors overall and the specified per-category
  template-family coverage are met;
- document lengths, table structures, typography, orientations, and visual
  conditions meet the diversity requirements;
- COCO and YOLO exports agree on image dimensions, class IDs, and annotation
  geometry;
- 100% of labels pass coordinate, class-range, image-existence, and box
  containment checks;
- annotation QA and adjudication meet the agreed error threshold, with no
  unresolved critical class or privacy defects;
- train/validation/test manifests are frozen, hashed, and prove document,
  template, source, duplicate, and augmentation isolation;
- the current synthetic corpus is still separately identified and unchanged;
- the dataset card identifies real, synthetic, augmentation, and validation
  sources without mixing their counts;
- an independent reviewer approves the release package.

Failure of any mandatory item yields `NOT_READY`. `BLOCKED` is reserved for a
missing required tool/access path that prevents completing an otherwise
specified audit; it must not be used to conceal missing provenance or failed
privacy/domain requirements.

## 10. Current blockers

- No authorized real Indian financial-document corpus is present in the
  workspace.
- The existing Indian corpus is synthetic and intentionally remains unsuitable
  as the required real-data fine-tuning set.
- No source-specific license/provenance packages have been approved for the
  required categories and diversity targets.
- The existing specification requires a manual visual annotation review that
  has not been completed for a future real corpus.
- The existing model taxonomy requires an explicit decision on the 13-class
  semantic head versus compatibility with the generic 11-class layout head.
- Ultralytics is not installed in the current Python environment; this plan
  intentionally performs no installation. This is a future execution blocker,
  separate from dataset readiness.

## End-state summary

- **Required dataset size:** 2,500 authorized real documents, approximately
  5,000 pages, and at least 20,000 annotations.
- **Required document categories:** bank statements, salary slips, loan
  statements, income/employment documents, and other explicitly approved
  supported financial documents.
- **Required layout diversity:** at least 8 institutions/vendors overall, 12
  template families per major category, unseen families in validation/test,
  varied lengths, tables, typography, orientations, and capture conditions.
- **Licensing/provenance:** documented lawful source, license/permission for ML
  use, anonymization, hashes, retention, access, and deletion terms for every
  source.
- **Annotation requirements:** current 13 semantic classes, COCO and YOLO
  exports, tight boxes, automated validation, double annotation, adjudication,
  and explicit taxonomy mapping.
- **Split strategy:** document/group-level 70/15/15 split with institution,
  template, duplicate, source, and augmentation isolation.
- **Acceptance criteria:** every provenance, privacy, diversity, annotation,
  integrity, split, and independent-review gate passes in a frozen manifest.
- **Current blockers:** no approved real corpus, no completed real-data
  annotation package, unresolved taxonomy-head decision, and missing
  Ultralytics runtime for future execution.

No model was trained, no metrics were generated, no packages were installed,
and Phase 5C remains untouched.
