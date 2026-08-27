# Phase 5B.9 - Real Indian Financial Dataset Acquisition

**Date:** 2026-08-27  
**Status:** Acquisition stopped before download  
**Training:** Not performed  
**Phase 5C:** Not started  
**Dataset status:** **BLOCKED**  
**READY_FOR_ANNOTATION:** **No**

## Executive decision

No legally usable, clearly authorized real Indian financial-document dataset is
available in this workspace for the requested pilot. The acquisition was
stopped before downloading any candidate source. No questionable dataset was
accepted, no synthetic replacement was generated, and the existing synthetic
corpus was not modified.

The Phase 5B.8 requirements therefore cannot be satisfied. The real pilot
contains **0 documents/pages acquired** and is not ready for annotation.

## Controlling requirements

The controlling plan is
[AI_PHASE5B_8_REAL_DATASET_ACQUISITION_PLAN.md](AI_PHASE5B_8_REAL_DATASET_ACQUISITION_PLAN.md).
It requires authorized real Indian documents, source-level provenance and
permission, privacy-safe training copies, hash and integrity records, and
split-safe document/template groups. It also requires a 100-250 real-document
pilot before the 2,500-document target.

The annotation source is
[docs/ai/INDIAN_DOCUMENT_ANNOTATION_SPEC.md](docs/ai/INDIAN_DOCUMENT_ANNOTATION_SPEC.md).
The existing synthetic data remains separate and unchanged at
[data/processed/indian_fin_docs](data/processed/indian_fin_docs).

## Sources evaluated

Evaluation is based on the repository's existing source assessment and local
availability. No source was downloaded during this phase.

| Candidate/source | Classification | Provenance | License/permission | Authenticity and Indian relevance | Privacy/diversity | Decision |
|---|---|---|---|---|---|---|
| Local `data/raw/doclaynet_subset` / IBM DocLayNet subset | **REAL_RESTRICTED** | Existing project metadata identifies IBM Research/Hugging Face / DocLayNet and a public archive; source files are real document pages | Prior metadata records CC-BY-4.0, but the local package does not establish permission for Indian financial-domain use or unrestricted redistribution of a derived dataset | Real document-layout pages, but not Indian bank statements, salary slips, loan statements, or Indian income documents | Generic layout diversity; not the required Indian financial diversity; no authorization for person-level Indian financial data | Do not use as the Phase 5B.9 real pilot; retain only as generic pretraining/evaluation material |
| Official Indian government blank forms/templates, including tax-form layouts | **REAL_RESTRICTED** | Public official layout sources may be identifiable by issuing authority and URL/version | Public availability does not itself grant permission to create a redistributed commercial training dataset from filled personal records | Authentic forms/layouts, but blank templates are not filled real financial-document examples and do not supply the required categories/diversity | No customer PII in blank forms, but insufficient as real-domain samples | Layout reference only; not acquired as real training data |
| Public Indian bank statement mock examples or officially published statement templates | **REAL_RESTRICTED** | Would require a named institution, exact source URL/version, and provider confirmation | Public access and a bank brand do not prove ML-training, derivative-label, or commercial permission | Potentially relevant layout reference; mock/blank material is not evidence of authentic customer documents | Usually low PII risk if blank, but insufficient category and template coverage | Do not download without written permission and provenance package |
| Public Indian annual reports, investor statements, and regulatory filings | **REAL_RESTRICTED** | Issuer/regulator source can be recorded, but each document has separate ownership/terms | Copyright, database, and redistribution terms vary; public viewing is not a blanket commercial ML license | Real Indian financial-domain documents, but generally corporate reports rather than bank statements, payslips, loan statements, or person-level income documents | Low personal-PII value for the target task; layout diversity may help but does not meet the required categories | Layout/reference material only unless source-specific rights are verified |
| Publicly posted filled salary slips, loan documents, Form 16/ITR, or bank statements | **UNSUITABLE** | Usually no lawful chain of custody or subject authorization | No verified permission for collection, ML training, labeling, redistribution, or commercial use | May be Indian and authentic, but authenticity cannot cure missing authorization | High personal, employment, tax, account, and credit-data risk | Reject; do not scrape or download |
| Unnamed repositories, scraped collections, social-media images, or datasets with unclear terms | **UNSUITABLE** | Provenance and custodianship cannot be established | License and intended-use permission unclear | Authenticity, category, and geographic relevance cannot be independently established | Unbounded PII and leakage risk | Reject; classify blocked rather than infer permission |
| `ds_indian_synthetic_bank_statements_5b6` at [data/processed/indian_fin_docs](data/processed/indian_fin_docs) | **SYNTHETIC** | Locally generated by [scratch/acquire_indian_financial_dataset.py](scratch/acquire_indian_financial_dataset.py) | Project-authored synthetic output; not real-document provenance | Indian-styled schematic pages, not authentic financial records; narrow fixed layout variation | Synthetic placeholders and masked values; no real customer PII claimed | Keep unchanged and separate; never count as real pilot data |

No candidate met all required conditions for `REAL_AUTHORIZED`.

## REAL_AUTHORIZED result

**None identified or acquired.** A source may enter this class only after a
provider supplies a signed authorization or license that explicitly permits
collection/use for document-layout ML, annotation derivatives, model training,
commercial use where required, and the planned retention/access model. It must
also pass de-identification, provenance, integrity, authenticity, and diversity
review.

There are therefore:

- Real authorized documents acquired: **0**
- Real authorized pages acquired: **0**
- Real authorized categories acquired: **none**
- Pilot SHA-256 manifest: **not created because no source was acquired**
- Pilot integrity/duplicate results: **not applicable**

## REAL_RESTRICTED result

The local DocLayNet material and public official/corporate layouts are useful
reference candidates, but their available evidence does not establish a
legally usable real Indian financial-document corpus under the Phase 5B.8
rules. In particular, blank forms and public corporate documents cannot be
counted toward the 100-250 real pilot because they do not represent the
required filled document categories and subject to layout variation.

No restricted source was downloaded, copied into the Indian dataset, or
reclassified as authorized.

## SYNTHETIC result

The existing dataset is explicitly synthetic and remains unchanged:

- Dataset ID: `ds_indian_synthetic_bank_statements_5b6`
- 375 documents and 1,500 pages
- 19,500 annotations across 13 classes
- Source: local deterministic generator
- Role: separate pipeline/fixture or optional synthetic supplemental data only

These values are recorded for separation and are not real acquisition counts.
No augmentation data was created in this phase.

## Required pilot versus acquired result

| Requirement | Target | Acquired |
|---|---:|---:|
| Real documents/pages pilot | 100-250 | 0 |
| Bank statements | Pilot representation required | 0 |
| Salary slips | Pilot representation required | 0 |
| Loan statements | Pilot representation required | 0 |
| Income/employment documents | Pilot representation required | 0 |
| Other approved financial documents | Explicitly enumerated and authorized | 0 |
| Institutions/vendors | Multiple, source-verified | 0 |
| Template families | Source-verified diverse families | 0 |
| SHA-256 source manifest | Required after acquisition | Not applicable |
| Annotation files | Future step after acquisition approval | 0 |

## Why acquisition stopped

The repository's documented assessment says no verified public dataset of real
Indian bank statements, salary slips, loan documents, or filled tax documents
is available with a clean, privacy-safe, commercially reusable license. The
only locally present Indian corpus is synthetic. Public forms and corporate
filings may be authentic public documents, but they are not an authorized
filled personal-financial dataset for the target pilot and their exact reuse
rights would need source-by-source confirmation.

Treating any restricted or unclear source as authorized would violate the
controlling plan and the privacy requirements. Consequently, the correct
action is to stop, not to download a source and resolve its legality later.

## Blockers and recommended next gate

Current blockers are:

1. No provider-authorized real Indian financial-document source is available in
   the workspace.
2. No source-specific license or permission package covers ML training,
   annotations, commercial use, and redistribution/retention requirements.
3. No 100-250-document real pilot exists across the required categories.
4. No real pilot provenance, de-identification sign-off, SHA-256 manifest,
   duplicate audit, or integrity report can be produced without acquiring a
   permitted source.
5. The local Ultralytics environment remains irrelevant to this acquisition
   phase and was not changed; no packages were installed.

The next permissible acquisition path is a direct provider agreement or a
lawfully governed research/industry data-sharing package that supplies
already-anonymized documents and explicit written ML permission. Only after
that package is reviewed should a 100-250-document pilot be acquired into a
separate REAL directory.

## Completion report

- **Sources evaluated:** local DocLayNet subset; official government blank
  forms/templates; public bank/template examples; public corporate/regulatory
  filings; publicly posted filled financial documents; unclear/scraped sources;
  existing synthetic corpus.
- **Licensing/provenance:** no candidate met the required complete
  authorization/provenance gate; restricted sources were not acquired.
- **Real documents actually acquired:** **0**
- **Document categories acquired:** **none**
- **Diversity:** no real pilot exists; requirements are unmet.
- **Privacy status:** no new source was downloaded or processed; existing
  synthetic data remains separate. Public/private candidate PII risks remain
  unresolved and are not accepted.
- **Duplicate/integrity results:** not applicable to a zero-document pilot;
  no source files were acquired.
- **Blockers:** authorization, license/provenance, privacy-safe source access,
  and the missing 100-250-document pilot.
- **READY_FOR_ANNOTATION:** **No**

No model artifacts, training metrics, annotations, packages, or replacement
data were created. Backend/frontend code and Phase 5C remain untouched.
