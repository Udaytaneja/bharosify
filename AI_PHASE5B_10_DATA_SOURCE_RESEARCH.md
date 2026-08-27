# Phase 5B.10 - Real Indian Document Data Source Research

**Date:** 2026-08-27  
**Status:** Research only; acquisition stopped  
**Training:** Not performed  
**Dataset creation/annotation:** Not performed  
**Phase 5C:** Not started  
**Acquisition gate:** **BLOCKED**  
**REAL_AUTHORIZED sources verified:** **0**

## Executive conclusion

No source currently satisfies the `REAL_AUTHORIZED` gate defined by
[AI_PHASE5B_8_REAL_DATASET_ACQUISITION_PLAN.md](AI_PHASE5B_8_REAL_DATASET_ACQUISITION_PLAN.md).
No documents were downloaded, scraped, copied, annotated, or generated.

The strongest practical route is a controlled institutional partnership with
Indian banks, NBFCs, fintechs, payroll providers, employers, or document
processing vendors. That route can plausibly reach 2,500+ documents and
approximately 5,000 pages, but it is only a prospective route until a provider
signs permission covering de-identified source documents, annotation
licensing, model training, commercial use where required, retention, access,
and deletion.

The second practical route is an explicitly consented user-contribution
program operated by a controlled ingestion service. It can produce authentic
varied documents, but it is not authorized merely because a user uploads a
file; informed consent, purpose limitation, irreversible de-identification,
and a valid data-processing agreement are required.

The acquisition gate therefore remains **BLOCKED** and the available pilot is
zero real documents/pages.

## Controlling material and separation rules

The controlling acquisition requirements are in
[AI_PHASE5B_8_REAL_DATASET_ACQUISITION_PLAN.md](AI_PHASE5B_8_REAL_DATASET_ACQUISITION_PLAN.md).
The annotation classes and privacy rules are in
[docs/ai/INDIAN_DOCUMENT_ANNOTATION_SPEC.md](docs/ai/INDIAN_DOCUMENT_ANNOTATION_SPEC.md).
The prior source assessment is in
[AI_INDIAN_DOCUMENT_DATASET_STRATEGY.md](AI_INDIAN_DOCUMENT_DATASET_STRATEGY.md).

The existing `ds_indian_synthetic_bank_statements_5b6` corpus remains
unchanged and is not counted as real data. It is classified `SYNTHETIC`, not
`REAL_AUTHORIZED`, regardless of its Indian-style labels.

## Candidate source evaluation

The classifications below describe the current evidence. `UNKNOWN` means
that a route could become usable after a named provider and written agreement
are obtained; it is not permission to download or process data.

| Source name / route | Document types | Indian relevance and authenticity | Provenance | License / permission and commercial compatibility | Redistribution restrictions | PII/privacy requirements | Expected scale and diversity | Acquisition method | Classification / confidence |
|---|---|---|---|---|---|---|---|---|---|
| Named Indian bank or NBFC partnership | Bank statements, loan statements, sanction/repayment schedules, account summaries | Highest relevance; authentic operational documents from multiple products and institutions | Provider can supply source system, institution, product, period, and chain-of-custody records | Must be a signed data-sharing/DPA or license explicitly permitting de-identified document use, annotation derivatives, ML training, and intended commercial use | Usually provider-controlled; likely no public redistribution; model/output rights must be explicit | Provider-side de-identification preferred; scan pixels, OCR, metadata, filenames, identifiers, signatures, and account/loan details before training copy | Strongest path to 1,500+ bank/loan documents and multiple layouts; practical contribution toward 2,500+ total | Business development and legal review; receive an already-de-identified, access-controlled pilot | **UNKNOWN** until contract; **REAL_AUTHORIZED** only after approval. Confidence in route practicality: High |
| Fintech, account-aggregator, or document-processing vendor partnership | Bank statements, KYC-adjacent financial proofs, loan documents, income proofs | High relevance and potentially broad institution/vendor coverage; source authenticity depends on vendor chain of custody | Vendor must identify originating institutions, consent/legal basis, transformations, and sample provenance | Contract must cover onward processing, ML training, labels, commercial deployment, retention, and audit rights | Likely restricted to internal use; no redistribution without written permission | Must exclude raw KYC/PII, preserve only irreversible de-identified training copies, and document consent and deletion | Potentially 500-2,000 documents with strong vendor/layout diversity | Qualified vendor agreement and secure transfer; no public scraping | **UNKNOWN** until contract; confidence: Medium-High |
| Payroll provider or employer consortium | Salary slips, employment/income proofs, Form 16-like employer documents | High relevance for salary/employment categories; authentic and likely diverse across payroll systems | Provider/employer must document source employers, periods, document generation system, and authorization | Written permission must include employee-data processing, annotation, model training, commercial use, and retention | Usually no redistribution; institution/vendor identity may need aggregation or pseudonymization | Employer and employee identifiers, salary, tax, bank, address, and signature data require controlled de-identification and review | Practical route to 500-1,000 salary/employment documents across many vendors | Consortium agreement or payroll vendor partnership; receive redacted export | **UNKNOWN** until contract; confidence: Medium-High |
| Controlled user-contributed document program | Bank statements, salary slips, loan statements, income/employment documents, other supported forms | Authentic user-provided Indian documents with potentially broad layout diversity | Consent record must bind contributor, document, purpose, processing scope, and withdrawal/deletion process | Explicit informed consent must cover de-identification, annotation, ML training, intended commercial use, and retention; incentive terms must be clear | Public redistribution should be prohibited unless separately consented; access must be restricted | Collect only through secure upload; reject raw PII where possible, irreversibly de-identify, scan rendered and embedded content, and honor deletion requests | Could reach 100-250 pilot documents in months; 2,500+ requires sustained recruitment and multiple channels | Ethics/privacy-approved recruitment, secure upload, consent ledger, quarantine, de-identification, review | **UNKNOWN** before consent program approval; confidence: Medium |
| Authorized research/academic partnership with Indian institution | Bank statements, salary slips, loan documents, income proofs, or curated subsets depending on partner | Potentially authentic and domain-relevant; academic collection may have strong annotation expertise | University/partner must prove collection authority, participant consent or lawful basis, and dataset custody | Research-only terms often exclude commercial training or redistribution; commercial compatibility is unverified until negotiated | Ethics approval, de-identification, access controls, and purpose limitation required | Potentially 100-1,000 documents; diversity depends on partner and may be limited to one institution/study | Sponsored research/data-use agreement and ethics review | **UNKNOWN** until terms; confidence: Medium |
| Government/official blank forms and templates | Form 16/ITR layouts, public financial forms, blank institutional templates | Authentic layout references but not authentic filled customer documents | Issuing authority and version can be recorded from official publication | Public availability does not prove permission for commercial derivative datasets or filled-record collection | Terms vary; redistribution and logo/branding use require review | Usually no PII in blank forms; still inspect metadata and embedded content | Good structural reference, but no real filled-document diversity or transaction variation | Use only as documented layout reference after terms review | **REAL_RESTRICTED**; confidence: High |
| Indian public company annual reports, investor filings, regulatory PDFs | Annual reports, financial statements, filings | Real Indian corporate financial documents, but not the target person-level bank/salary/loan corpus | Issuer or regulator publication provides source identity and date | Copyright and database/website terms vary; public viewing is not blanket ML or commercial redistribution permission | Usually source-specific and potentially restrictive | Lower personal PII risk, but inspect metadata and named-person content | High PDF/layout diversity but poor category fit; not a substitute for target documents | Evaluate individually; do not bulk download for this phase | **REAL_RESTRICTED**; confidence: High |
| IBM DocLayNet / local DocLayNet subset | Generic document-layout pages | Real documents and useful generic pretraining, but not Indian financial-domain documents | Existing repository metadata identifies IBM Research/Hugging Face source | Prior metadata records CC-BY-4.0; this does not make it an Indian financial dataset or authorize unrelated source use | Follow source license and local data governance; not a candidate for the Indian pilot | Apply source privacy checks, though it is not a person-level Indian financial source | Generic layout variation; does not cover required category/institution targets | Already present; no new acquisition permitted or needed | **REAL_RESTRICTED** for this phase; confidence: High |
| Unnamed public Kaggle/GitHub/web collections or scraped private documents | Any apparent financial document type | Authenticity, Indian origin, and chain of custody cannot be established | Provider and source lineage unclear | License, ML permission, commercial use, and derivative rights unclear | Redistribution and takedown exposure unknown | High risk of exposed PII, embedded OCR, account/PAN/Aadhaar data, and leakage | Apparent scale is not credible without provenance and duplicate audit | Do not scrape or download | **UNSUITABLE**; confidence: High |
| `ds_indian_synthetic_bank_statements_5b6` | Synthetic bank-statement-like pages | Not authentic real documents; locally generated schematic pages | [scratch/acquire_indian_financial_dataset.py](scratch/acquire_indian_financial_dataset.py) | Project-authored synthetic output; not real-source permission | Keep in its existing separate directory and manifest | Synthetic markers and masked/generated values; not evidence of real-data privacy clearance | 375 documents / 1,500 pages but narrow fixed layout families | Existing local data only; preserve unchanged | **SYNTHETIC**; confidence: High |

No source is classified `REAL_AUTHORIZED` at this time.

## Route analysis against the target

| Route | 2,500+ documents | Approximately 5,000 pages | Multiple institutions/vendors | Required categories | Overall assessment |
|---|---:|---:|---:|---|---|
| Institutional bank/NBFC/fintech/payroll consortium | Plausible | Plausible | Strongest | Bank, loan, salary, income/employment; other categories by agreement | **Strongest route**, pending legal partnership |
| Consented users | Possible but operationally slower | Possible | Depends on recruitment | Broadest if recruitment is stratified | Strong pilot route after privacy/consent approval |
| Public licensed datasets | Not currently verified | Not currently verified | Unknown | No verified public source identified | Do not rely on this route without a named license |
| Academic/research dataset | Possible for a restricted study | Possible | Usually limited | Depends on partner | Viable only after commercial-use compatibility review |

## Privacy and provenance requirements for the first pilot

Before accepting even one real document, the provider package must include:

- named provider, institution/vendor, category, source date, and document ID;
- lawful basis or explicit consent and a signed agreement for the exact ML use;
- permission for de-identification, annotation, derivative labels, model
  training, evaluation, retention, and any intended commercial use;
- source and transformed-file SHA-256 hashes, immutable version, and custody
  log;
- documented de-identification method and independent privacy review;
- no exposed PAN, Aadhaar, account/card/loan numbers, names, addresses,
  phones, emails, salaries, transactions, or live signatures;
- removal of OCR layers, thumbnails, PDF properties, filenames, and hidden
  metadata that can retain PII;
- secure transfer, quarantine, access control, deletion/withdrawal process,
  and incident procedure;
- category, institution/vendor, template family, page count, orientation,
  document length, and table-structure metadata where legally permissible;
- explicit separation from `data/processed/indian_fin_docs`, which remains
  synthetic.

## Strongest acquisition route

The strongest route is a **multi-party institutional consortium**:

1. one or more banks/NBFCs for authentic statements and loan documents;
2. a fintech or document-processing vendor for additional institution and
   format diversity; and
3. payroll providers or employers for salary and income/employment documents.

A consortium is more likely than a single source to meet the Phase 5B.8
requirements for eight institutions/vendors, twelve template families per
major category, varied lengths, table structures, and multiple typography and
capture conditions. It also gives the provider a controlled path to
pre-anonymize data before delivery.

This is a route recommendation, not evidence that an agreement exists.

## Exact next action for the first 100-250 documents

Appoint an authorized data owner and send a written request for a **100-250
document de-identified pilot** to a named institutional consortium. The
request must ask for:

- 40-80 bank statements;
- 20-40 salary slips;
- 20-40 loan statements;
- 15-30 income/employment documents; and
- 5-20 other explicitly named supported financial documents;
- at least three institutions/vendors and multiple unseen template families;
- 100% provider-side de-identification before transfer;
- a signed data-use agreement covering document-layout annotation, ML training,
  commercial compatibility, access, retention, deletion, and no unauthorized
  redistribution;
- a provenance manifest and source/license evidence for every delivered file.

Do not receive or download the pilot until legal/privacy review signs the
agreement and confirms that the delivered copy contains no recoverable PII.
After approval, place the files in a new REAL-only directory, hash every file,
verify format/integrity, detect exact and perceptual duplicates, record source
metadata, and then stop for a separate readiness review. Do not annotate or
train as part of this action.

## Final completion report

- **Sources evaluated:** institutional bank/NBFC/fintech partnerships;
  payroll/employer partnerships; controlled user contributions; academic or
  research partnerships; official blank forms/templates; public corporate and
  regulatory PDFs; IBM DocLayNet; unclear public/scraped collections; existing
  synthetic corpus.
- **Strongest acquisition route:** controlled multi-party institutional
  consortium with bank/NBFC/fintech and payroll/employer providers.
- **Legal/provenance status:** no source is currently `REAL_AUTHORIZED`; all
  practical routes require signed source-specific permission and provenance.
- **Estimated achievable scale:** institutional consortium plausibly reaches
  2,500+ documents and approximately 5,000 pages; user and academic routes are
  plausible for the pilot but scale is unverified.
- **Real documents actually acquired:** **0**.
- **Document categories acquired:** none.
- **Diversity acquired:** none; no real pilot exists.
- **Privacy status:** no new documents were downloaded or processed; the
  existing synthetic corpus remains separate.
- **Duplicate/integrity results:** not applicable to a zero-document pilot.
- **Current blocker:** absence of a named provider with verified permission,
  de-identification evidence, and a signed ML/commercial-use agreement.
- **READY_FOR_ANNOTATION:** **No**.

No data was downloaded, no dataset was created, no annotation or metrics were
produced, no packages were installed, no model artifact was created, and Phase
5C remains untouched.
