# Phase 5B Step 2 - Institutional Data Request Package

**Date:** 2026-08-27  
**Purpose:** Provider outreach and review only  
**REAL_AUTHORIZED source:** None  
**Documents acquired:** 0  
**Current status:** **BLOCKED** until an actual provider grants permission

This package is a request specification and acceptance checklist. It is not an
agreement, authorization, consent record, or claim that any provider has
approved data use.

## 1. Technical data-request specification

### Requested pilot

Request a small pilot of **100-250 real Indian financial documents or pages**.
The provider may propose the exact split between documents and pages, but must
identify both counts and keep all pages from one source document grouped.
Synthetic documents, public blank templates, scraped files, and unverified
examples do not count toward the pilot.

Preferred pilot coverage:

| Category | Target pilot quantity | Required examples |
|---|---:|---|
| Bank statements | 40-80 | Transaction tables, account summaries, balances, pagination, debit/credit/fee variations |
| Salary slips | 20-40 | Earnings, deductions, net pay, employer and pay-period layouts |
| Loan statements | 20-40 | EMI schedules, principal/interest, outstanding/due amounts, repayment summaries |
| Income/employment documents | 15-30 | Income proof, employment verification, compensation and approval layouts |
| Other supported financial documents | 5-20 | Explicitly named and approved Form 16/ITR, sanction letter, account summary, or equivalent |

The provider should supply multiple institutions/vendors and multiple template
families. The requested pilot is an initial feasibility sample, not the full
2,500-document target.

### Required diversity

The pilot should include, where legally and operationally available:

- at least 3 institutions/vendors;
- at least 2 distinct template families per represented category;
- single-page and multi-page documents;
- varied statement periods and document lengths;
- different table column arrangements, merged cells, subtotals, continuation
  headers, and multiple-table layouts;
- typography, spacing, color, branding, header/footer, stamp, and signature
  placement variation;
- native PDF and rasterized/scan variants, including realistic but non-
  identifying quality variation;
- regional-language or bilingual examples where the provider is authorized to
  supply them.

Near-identical copies with changed identifiers do not satisfy diversity.
The provider must disclose when samples come from the same template family.

### Acceptable formats

Preferred formats are:

- PDF with all embedded OCR/text layers removed after de-identification;
- PNG, JPEG, or TIFF page images;
- lossless or high-quality rasterization at the provider's native resolution.

Each file must be readable without proprietary software in the review
environment. Passwords, encryption keys, or access credentials must be handled
through an approved secure channel and must not be embedded in filenames or
metadata. The provider must disclose whether a file is native, rasterized,
scanned, or transformed.

### Resolution and image requirements

- Prefer native source resolution; target at least 200 DPI and preferably
  300 DPI for scanned pages.
- Rasterized pages should have a minimum short edge of 1,000 pixels where the
  source permits.
- Preserve the complete page boundary, tables, headers, footers, and visible
  marks; do not crop away context needed for layout annotation.
- Do not upscale low-resolution pages solely to meet the target dimension.
- Record pixel dimensions, DPI when available, color mode, orientation, and
  file format for every file.
- Do not apply augmentation or synthetic compositing during delivery.

### Annotation requirements

The provider may supply existing annotations, but they must include their
schema, version, annotator instructions, and quality evidence. Existing labels
are not accepted without review.

The target annotation schema follows
[docs/ai/INDIAN_DOCUMENT_ANNOTATION_SPEC.md](docs/ai/INDIAN_DOCUMENT_ANNOTATION_SPEC.md):

`DOCUMENT_HEADER`, `DOCUMENT_TITLE`, `BANK_NAME`, `EMPLOYER_NAME`,
`CUSTOMER_NAME`, `ACCOUNT_NUMBER`, `IFSC_CODE`, `DATE_RANGE`,
`TRANSACTION_TABLE`, `TABLE_HEADER`, `TOTAL_AMOUNT`, `SIGNATURE`, `STAMP`.

Required annotation properties:

- tight boxes around the complete visible text or graphic region;
- page-level image dimensions and stable image/document IDs;
- COCO JSON and YOLO TXT exports, or source data that can be converted with
  an explicit mapping;
- normalized YOLO coordinates in
  `<class_id> <x_center> <y_center> <width> <height>` format;
- category/document-type metadata separate from layout class labels;
- explicit `not present` handling rather than forced boxes for absent classes;
- annotation version, annotator/reviewer identity or pseudonymous IDs, and
  adjudication status;
- permission for AgentTrust to create annotation corrections and derivative
  labels.

No annotation or data transformation will be performed as part of this
request package.

### Required metadata

For each document/page, provide only metadata permitted by the agreement:

- opaque document ID and page ID;
- document category;
- source institution/vendor identifier, or an approved pseudonym;
- template-family identifier;
- page number and total page count;
- source format, rasterization status, dimensions, DPI, orientation, and
  language;
- provenance source ID, acquisition date, dataset version, and transformation
  history;
- de-identification version and privacy-review status;
- split-group identifier, kept separate from the file content;
- SHA-256 hash of the delivered file.

Do not provide names, account identifiers, raw OCR, source URLs containing
personal identifiers, or hidden metadata that can re-identify a person.

## 2. Privacy and de-identification specification

The provider must deliver an already de-identified copy whenever possible.
Raw personal documents must not be transferred merely for AgentTrust to
redact later.

### Mandatory removals

The delivered copy must contain no recoverable:

- PAN, Aadhaar, passport, card, bank-account, loan-account, employee, or
  customer numbers;
- names, initials, signatures, photographs, addresses, phone numbers, email
  addresses, QR codes, barcodes, or customer-specific URLs;
- salary, tax, transaction, repayment, or employment values linked to a real
  person;
- handwritten marks or biometric/identity information;
- PDF OCR/text layers, attachments, thumbnails, comments, revision history,
  EXIF, XMP, author fields, filenames, or other metadata containing PII.

Aadhaar and PAN examples are not required for the pilot. If an authorized
use case requires them, they must be permanently masked/anonymized under the
annotation specification before delivery. Account numbers must be removed or
irreversibly masked; last-four display is allowed only when explicitly
approved and not identifying in context. Names and addresses must be replaced
or fully obfuscated.

### Verification requirements

The provider must document:

- the de-identification method, tool/version, date, and responsible reviewer;
- pixel-level review of rendered pages;
- OCR/text-layer and metadata inspection;
- checks for reversibility, hidden layers, source files, and backups in the
  delivered package;
- false-negative handling and escalation for suspected PII;
- deletion of raw files or controlled retention under the agreement.

Redactions must be irreversible: no removable overlays, editable masks,
recoverable PDF objects, or unblurred underlying text are acceptable. AgentTrust
will reject any file that exposes or permits recovery of personal data.

## 3. Data-governance and legal checklist

A provider response is incomplete until every applicable item is answered and
supported by documentation.

### Provenance and authenticity

- [ ] Provider and legal entity are named and verified.
- [ ] Provider confirms custody or lawful authority over each source group.
- [ ] Documents are confirmed as real operational documents, not synthetic,
      mock, blank, or generated replacements.
- [ ] Category, institution/vendor, period, source system, and template family
      are recorded where legally permissible.
- [ ] Acquisition date, transformation history, dataset version, and file
      hashes are recorded.
- [ ] Authenticity limitations and excluded source groups are disclosed.

### Permission and intended use

- [ ] Signed agreement, license, or consent package identifies AgentTrust and
      the exact receiving entity.
- [ ] Permission explicitly covers de-identified document use for layout
      annotation and machine-learning research/development.
- [ ] Permission explicitly covers model training and internal evaluation.
- [ ] Permission covers creation, correction, storage, and use of annotation
      and other derivative data.
- [ ] Intended commercial use is expressly permitted, or the restriction is
      documented and accepted before transfer.
- [ ] The legal basis, consent scope, purpose limitation, and withdrawal terms
      are documented where personal data was originally involved.

### Retention, security, and deletion

- [ ] Permitted retention period and dataset version are stated.
- [ ] Raw-source retention is controlled by the provider and not transferred
      unless separately authorized.
- [ ] Training-copy deletion, correction, withdrawal, and incident procedures
      are defined.
- [ ] Access is limited to named or role-controlled personnel.
- [ ] Transfer and storage protections are documented.
- [ ] Audit, breach-notification, and takedown obligations are defined.

### Redistribution and commercial restrictions

- [ ] Whether files may be redistributed is explicit; default is no public
      redistribution.
- [ ] Whether labels, derived crops, embeddings, and model outputs may be
      retained or shared is explicit.
- [ ] Institution/vendor names and logos may be retained only if permitted.
- [ ] Third-party rights, copyright, confidentiality, and branding restrictions
      have been reviewed.
- [ ] No restriction conflicts with the intended model evaluation or retention
      plan.

No unchecked or ambiguous legal item authorizes acquisition.

## 4. Institutional outreach brief

### About AgentTrust

AgentTrust is building an underwriting-support system that uses document
perception to locate financial-document structures and fields. The requested
materials are for a controlled experimental dataset, not for customer
servicing, credit decisions, identity verification, or production deployment.

### Why the documents are needed

Existing project data is synthetic and cannot establish performance on real
Indian financial-document layouts. A small, authorized pilot is needed to
understand real variation across institutions, vendors, page lengths, tables,
typography, and document categories before any later annotation or model
work.

### What will be done

Subject to a signed agreement and successful privacy review, AgentTrust will:

- receive only an approved de-identified copy;
- preserve provider provenance and file hashes;
- restrict access to approved project personnel;
- use the documents for document-layout annotation, research/development, and
  controlled evaluation within the agreed scope;
- retain and delete the files according to the agreed schedule;
- report any suspected privacy or integrity issue to the provider.

### What will not be done

AgentTrust will not scrape documents, seek customer identity, use the files
for credit decisions or customer profiling, bypass access controls, combine
them with unauthorized sources, or publicly redistribute the documents. No
model training or evaluation is authorized by this brief alone; those actions
require the provider agreement to state them explicitly.

### Requested pilot

We request 100-250 real Indian documents/pages across bank statements, salary
slips, loan statements, income/employment documents, and explicitly approved
other financial documents, with multiple institutions/vendors and template
families. The provider may propose a safer category mix, but must identify the
resulting scope and limitations.

## 5. Provider acceptance checklist

The pilot is accepted only when every mandatory criterion passes.

| Criterion | PASS condition | FAIL condition |
|---|---|---|
| Provider identity | Named legal provider and verified authority | Anonymous, intermediary without authority, or unclear custody |
| Authenticity | Provider confirms real operational documents | Synthetic, mock, blank, or authenticity not established |
| Indian relevance | Documents are Indian financial-domain examples | Generic or unrelated documents |
| Scope | 100-250 real documents/pages proposed and counted | No reliable count or below pilot scope without approval |
| Categories | Required categories and exact counts identified | Categories missing or unidentifiable |
| Diversity | Multiple institutions/vendors and template families documented | Single source or near-duplicate layout only |
| Provenance | Source, date, version, transformations, and hashes provided | Missing or unverifiable lineage |
| Permission | Written permission covers ML training, evaluation, annotation derivatives, and intended use | Public availability or verbal permission only |
| Commercial use | Commercial compatibility explicitly granted or formally excluded and accepted | Silent or ambiguous commercial rights |
| Privacy | De-identified copy passes pixel, OCR, metadata, and reversibility review | Any exposed or recoverable PII |
| Security | Transfer, storage, access, incident, and deletion controls agreed | Uncontrolled transfer or undefined access |
| Retention | Retention period and deletion/withdrawal process documented | No retention or deletion terms |
| Redistribution | Document, label, output, and institution restrictions explicit | Redistribution/derivative rights unclear |
| File integrity | Supported formats, dimensions, and SHA-256 manifest provided | Corrupt, unreadable, or unhashed files |
| Split readiness | Source document/template groups can be isolated later | Group identity unavailable or leakage risk unresolved |
| Provider sign-off | Authorized representative signs the final scope | Draft-only response or no accountable signatory |

A single mandatory FAIL means the pilot is rejected or remains **BLOCKED**.
Passing this checklist authorizes only the acquisition step covered by the
signed agreement; it does not authorize annotation or training by itself.

## Completion status

- **Package created:** Yes, this file only.
- **Required document types:** Bank statements, salary slips, loan statements,
  income/employment documents, and explicitly approved other financial
  documents.
- **Pilot size:** 100-250 real documents/pages.
- **Privacy requirements:** Mandatory irreversible de-identification, complete
  PAN/Aadhaar/account/name/address/contact/signature/OCR-layer/metadata removal,
  and verification that redactions cannot be recovered.
- **Legal/data-use requirements:** Verified provenance, written permission for
  ML training/evaluation and annotation derivatives, retention/deletion,
  access, redistribution, and commercial-use terms.
- **Provider acceptance criteria:** Every mandatory checklist item must PASS.
- **Current status:** **BLOCKED** until an actual provider grants permission
  and supplies the required provenance and de-identified pilot.

No provider has agreed, no data is authorized, no documents were acquired, and
no annotation, evaluation, training, package installation, dataset
modification, backend/frontend change, or Phase 5C work was performed.
