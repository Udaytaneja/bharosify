# Phase 5B.5 — Indian Financial Document Dataset Strategy

**Status**: Strategy only. No model training, no production code changes, and no personal financial data collection.

## 1. Objective and constraints

This strategy defines the legally safe and technically credible path for building the first Indian-domain document dataset for AgentTrust underwriting perception. The decision is driven by four non-negotiable constraints:

1. Do not train a model yet.
2. Do not begin Phase 5C.
3. Do not touch production backend or frontend code.
4. Do not use real personal financial information or collect actual bank/customer documents.

The project already verified that the generic DocLayNet benchmark is a useful layout pretraining source under CC-BY-4.0, but it does not represent Indian financial documents and is not sufficient for underwriting-grade extraction. This strategy therefore prioritizes a synthetic-first Indian financial-document dataset with only public or officially released form templates and anonymized placeholders.

---

## 2. Public/licensed dataset investigation

### Summary verdict

A verified public dataset of real Indian bank statements, salary slips, loan documentation, or Form 16 records suitable for direct commercial underwriting model training does not exist in a form that can be declared legal, privacy-safe, and commercially reusable. The practical path is:

- use public form layouts and government-issued document templates only,
- generate synthetic Indian document variants with anonymized placeholders,
- keep all customer-specific values synthetic,
- apply strict document-level split isolation,
- avoid redistribution of any real personal financial document.

### Assessment table

| Document type | Public/licensed candidate sources reviewed | License / legal status | Permitted usage | Privacy / restriction status | Recommendation |
| --- | --- | --- | --- | --- | --- |
| Indian bank statements | No verified public dataset of customer bank statements with Indian account data; no open benchmark of real bank statements under a clean commercial license. | No verified dataset license for commercial ML reuse. | Not acceptable for direct training from real documents. | Real bank statements are personal financial records and are privacy-sensitive. | Synthetic generation only. |
| Salary slips | No verified public dataset of Indian payslips; no licensed open corpus of filled employee salary slips. | No verified dataset license. | Not acceptable for real-data training. | Salary slips contain personal identifiers and compensation data. | Synthetic generation only. |
| Loan documents | No verified public dataset of Indian loan applications, sanction letters, or EMI schedules. | No verified dataset license. | Not acceptable for real-data training. | These documents contain borrower identity, financial obligations, and credit records. | Synthetic generation only. |
| Form 16 / tax documents | Official tax form templates from the Income Tax Department / government public sources and tax software examples are public and template-based. | Government/public forms are generally public documentation; however actual filled personal forms are not a public dataset. | Acceptable only for layout and field structure reference; not as customer-data training samples. | Real filled Form 16s are personal tax data and must never be collected. | Use only as template source; generate synthetic versions. |
| Financial statements | Public annual reports, balance sheets, and investor presentations from listed companies and regulators are public-facing documents. | Public issuer documents; copyright and redistribution terms vary by source and issuer. | Good for document layout reference and template structure; not a labeled person-level financial dataset. | Some issuer terms may restrict redistribution or reuse beyond internal analysis. | Use only for template/layout studies; not as definitive labeled training data. |

### Legally usable sources that are safe to use as templates

These are considered safe only as layout reference, not as private-data training examples:

- Official Indian government forms and public tax templates (for layout, field order, watermark, and signature placement).
- Public annual reports and investor presentations from listed Indian companies and SEBI/BSE/NSE public filings.
- Publicly available official statement templates or mock examples from banks and employers, if distributed under a clear license and without personal data.

These sources may help define the expected structure and visual conventions, but they do not eliminate the need for synthetic generation and privacy-safe labeling.

### Explicit legal caution

The following must not be used:

- scraped or downloaded images of real customer bank statements,
- screenshots of private salary slips or pay stubs,
- loan sanction letters containing real borrower names / PAN / account numbers,
- real Form 16 or ITR PDFs with actual tax data,
- personal financial PDFs obtained without explicit lawful authorization.

No dataset should be marked as commercially usable unless the license has been independently verified for the exact intended use.

---

## 3. Synthetic Indian financial-document generation strategy

Because no verified public dataset of Indian financial documents exists, the first dataset should be synthetic but realistic.

### 3.1 Source of realism

Generate documents using a controlled template library built from:

- public government form layouts,
- public annual-report and bank statement style conventions,
- stylized Indian banking layout patterns,
- salary-slip field ordering observed from public template examples,
- loan statement and EMI layout conventions in publicly disseminated non-private samples.

### 3.2 Generation design

Create synthetic document families with the following design rules:

- Use realistic Indian names and institutions in fictional combinations only.
- Use generated account numbers and IFSC codes that are syntactically valid but not real identifiers.
- Use placeholder PAN / Aadhaar patterns with masked formatting (for example, `XXXX-XXXX-1234` for Aadhaar; `ABCDE1234F` as a synthetic test pattern).
- Randomize document metadata such as date ranges, month-year labels, transaction sequences, and employer names.
- Vary fonts, scan noise, resolution, page margins, and paper backgrounds to increase robustness.
- Inject realistic bank logos and stamps using vector blobs or generated templates rather than real corporate branding assets from customer documents.
- Generate at least 10–20 template families per document type to prevent leakage and overfitting to a single layout.

### 3.3 Recommended synthetic document classes

Start with three synthetic document families that map directly to underwriting value:

1. Indian bank statement pages
   - statement header
   - account summary
   - date range and account holder name
   - transaction table
   - balance and summary totals

2. Indian salary slips
   - employer name and logo
   - employee details
   - month/year and earnings breakdown
   - deductions and net pay
   - signature / approval block

3. Indian loan and EMI documents
   - loan account metadata
   - principal and rate information
   - EMI schedule or sanction summary
   - interest / total due / outstanding balance

Each synthetic sample should be generated with a unique document ID and a deterministic template family ID so that document-level and family-level splits are feasible.

### 3.4 Annotation workflow

Annotate with COCO JSON and YOLO TXT labels using the same geometry conventions already adopted in this project and documented in the annotation guidance. Each synthetic page receives a minimum set of labels corresponding to the semantic classes defined below. The visual ground-truth must be reviewed by a manual pass for geometry and class consistency.

---

## 4. Annotation classes required by AgentTrust underwriting

The underwriting perception layer needs semantic classes that support field extraction and downstream risk logic. These are not the same as the generic DocLayNet layout classes; they are target semantic elements to be located and then parsed by OCR and rule-based extraction logic.

### Proposed semantic classes

| Semantic class | Description | Typical placement |
| --- | --- | --- |
| `DOCUMENT_HEADER` | top banner or statement header | page top |
| `DOCUMENT_TITLE` | title such as Bank Statement, Payslip, Loan Summary | page top |
| `BANK_NAME` | bank name or financial institution identifier | top-left or header |
| `EMPLOYER_NAME` | employer or company name | payslip header |
| `CUSTOMER_NAME` | account holder or employee name | personal detail block |
| `ACCOUNT_NUMBER` | bank account or customer ID | personal info / summary |
| `IFSC_CODE` | bank IFSC or branch code | header or summary |
| `DATE_RANGE` | statement period or payslip month | header or summary |
| `TRANSACTION_TABLE` | main transaction grid | middle of page |
| `TABLE_HEADER` | transaction table column row | table top |
| `TOTAL_AMOUNT` | closing balance, net salary, or principal balance | summary area |
| `SIGNATURE` | authorized sign-off or digital verification area | bottom |
| `STAMP` | bank or company stamp | footer or seal area |
| `PAGE_FOOTER` | page number or footer metadata | bottom |

### Minimum class set for the first fine-tuning experiment

For a first fine-tuning experiment, the model should be trained on a reduced, high-value set:

- `DOCUMENT_HEADER`
- `DOCUMENT_TITLE`
- `BANK_NAME`
- `EMPLOYER_NAME`
- `CUSTOMER_NAME`
- `ACCOUNT_NUMBER`
- `IFSC_CODE`
- `DATE_RANGE`
- `TRANSACTION_TABLE`
- `TABLE_HEADER`
- `TOTAL_AMOUNT`
- `SIGNATURE`
- `STAMP`

This set captures the underwriting-critical fields while remaining practical for the initial synthetic dataset.

---

## 5. Mapping proposed Indian classes against the existing 11 DocLayNet classes

The existing layout system currently defines 11 generic DocLayNet classes, as implemented in the project metadata. These are:

- `Caption`
- `Footnote`
- `Formula`
- `List-item`
- `Page-footer`
- `Page-header`
- `Picture`
- `Section-header`
- `Table`
- `Text`
- `Title`

These map directly to the AgentTrust classes already used in the project:

| Proposed Indian semantic class | Closest existing DocLayNet class | Reasoning |
| --- | --- | --- |
| `DOCUMENT_HEADER` | `Page-header` or `Section-header` | Top-of-page banner or account header |
| `DOCUMENT_TITLE` | `Title` | Form title / statement title |
| `BANK_NAME` | `Section-header` or `Text` | Usually a prominent header label |
| `EMPLOYER_NAME` | `Section-header` or `Text` | Company name in payslip header |
| `CUSTOMER_NAME` | `Text` | Name string in summary block |
| `ACCOUNT_NUMBER` | `Text` | Numeric identifier text block |
| `IFSC_CODE` | `Text` | Code string in header or summary |
| `DATE_RANGE` | `Text` | Date string or text block |
| `TRANSACTION_TABLE` | `Table` | Main financial data grid |
| `TABLE_HEADER` | `Table` | Header row region inside table |
| `TOTAL_AMOUNT` | `Text` | Numeric summary field |
| `SIGNATURE` | `Picture` | Signature graphic / handwritten mark |
| `STAMP` | `Picture` | Corporate or bank seal |
| `PAGE_FOOTER` | `Page-footer` | Footer numbering or page metadata |

### Important design principle

The DocLayNet classes are layout classes, not domain-specific semantic field labels. AgentTrust should therefore maintain a two-layer scheme:

1. Layout detection layer: DocLayNet-compatible 11 classes for structure.
2. Semantic extraction layer: underwriting-specific classes for OCR-driven field parse and validation.

This preserves compatibility with the existing training pipeline while allowing domain-specific field extraction behind the layout detector.

---

## 6. Split methodology with document-level isolation

The dataset must be split at the document level, not page level, to prevent leakage and template memorization.

### Required split rules

- Each synthetic document is assigned a single `document_id`.
- All pages belonging to a document remain in the same split.
- Split ratios: 70% train, 15% validation, 15% test.
- Group splitting is required by document family and format family.
- Training, validation, and test splits must not share the same template family ID, bank/firm naming pattern, or generated digit signature patterns.
- For salary slips and bank statements, keep all page sequences from one document together.
- Use deterministic seeds for synthetic generation so the split is reproducible.

### Minimum document-family coverage per split

At least five synthetic families per major document type should be represented in each split when possible, but the documents should still remain isolated by family or by generator seed. If one family is used in training only, it must not appear in validation or test.

### Leakage-specific rules

- No page-level random shuffle across splits.
- No same generated account number or dummy customer name used across splits.
- No reusing the same bank or employer template family across train and test.
- All synthetic images must be generated from a templated pipeline and assigned split metadata at generation time.

---

## 7. Leakage prevention and PII handling

### 7.1 Leakage prevention

1. Document-level split isolation is mandatory.
2. Template family IDs must be held out across splits.
3. Names, account numbers, phone numbers, PAN numbers, and dates must be created deterministically but uniquely per document.
4. A synthetic sample must never reuse a page or document from another split.
5. Do not include metadata that contains private IDs or original source references from real documents.
6. Validation and test sets must be hidden from any tuning decisions until all model parameters are fixed.

### 7.2 PII handling policy

This dataset strategy explicitly prohibits any real customer PII:

- no real names,
- no real phone numbers,
- no live account numbers,
- no real PAN / Aadhaar numbers,
- no real addresses,
- no actual salary or transaction histories from employees or customers.

All PII-like fields are generated using a data-generation library that conforms to format constraints only. Examples:

- `Rajesh Kumar` and `Priya Sharma` are placeholders, not real names.
- account numbers use pseudo-random valid digit patterns, masked where necessary,
- PAN-like values are synthetic and structurally valid,
- dates are generated inside a valid range but never based on live customer records.

### 7.3 Data retention and deletion policy

- Store only the minimum metadata required for annotation and split tracking.
- Keep a synthetic metadata manifest with `document_id`, `template_family`, `split`, `date_range`, and `license_status`.
- Delete any generated sample that fails privacy validation or violates the template family split policy.

---

## 8. Minimum dataset size for the first fine-tuning experiment

A first fine-tuning experiment should be large enough to learn layout structure and class imbalance without overfitting to a tiny synthetic corpus. The minimum viable starting point is:

- 1,500 labeled pages total,
- 1,050 train pages,
- 225 validation pages,
- 225 test pages,
- generated from at least 300–500 distinct synthetic documents,
- with at least 3–5 major template families per document type.

This target is the minimum for a credible first fine-tuning run because:

- Indian document layouts have stronger class imbalance than the generic DocLayNet benchmarks,
- transaction tables and headers are dense and repeated,
- a small dataset would likely be dominated by the simplest classes and underperform on important field classes.

For a more robust second pass, the recommended target is 3,000–5,000 pages, but the first experiment should not wait for that scale. The minimum viable threshold is 1,500 pages.

---

## 9. Recommended first document type

### Recommended first document type: Indian bank statements

Reasoning:

1. They are the highest-value underwriting documents for fraud checks, balance verification, and cash-flow analysis.
2. They contain repeated, structured transaction tables that are well suited to YOLO layout detection.
3. They provide strong coverage of high-priority classes: `BANK_NAME`, `ACCOUNT_NUMBER`, `IFSC_CODE`, `DATE_RANGE`, `TRANSACTION_TABLE`, `TOTAL_AMOUNT`, and `PAGE_FOOTER`.
4. They offer a realistic and operationally useful first domain specialization before moving to salary slips or loan documents.

Salary slips are easier in layout but lower in underwriting breadth; loan documents are more complex and less standardized. Bank statements should therefore be the first target domain.

---

## 10. Acceptance criteria for the next fine-tuning experiment

The next fine-tuning run should not be treated as production-ready. It should only be considered a valid domain-transfer experiment if all of the following are true:

### 10.1 Data quality gate

- All pages are synthetic and contain no real customer identity information.
- Every label is valid and passes geometry validation (`x_center`, `y_center`, `width`, `height` within normalized bounds).
- Each document is assigned a single split at the document level.
- No template family overlaps between train and validation/test.

### 10.2 Detection quality gate

- `mAP@50 >= 0.75` on the validation split for the primary legal-structure classes.
- `mAP@50 >= 0.60` for `TRANSACTION_TABLE` and `TOTAL_AMOUNT`.
- `Precision >= 0.80` and `Recall >= 0.75` for `BANK_NAME`, `ACCOUNT_NUMBER`, `IFSC_CODE`, and `TRANSACTION_TABLE`.
- `TABLE` detection must be stable on noisy bank statement pages with margins, stamps, and multi-line entries.

### 10.3 Leakage gate

- No document-family leakage between train and test.
- No synthetic ID duplication across splits.
- No name or account number pattern overlap across sets.

### 10.4 Operational gate

- The dataset is documented in a governance manifest with license and privacy status.
- The model is explicitly tagged as `EXPERIMENTAL_CANDIDATE` and not promoted to production.
- The experiment uses the same project structure and annotation conventions already expected by the AgentTrust document pipeline.

If these gates are met, the fine-tuning run can be considered a legitimate domain-specialization test. If not, the dataset should be expanded before the next experiment.

---

## 11. Final recommendation

The dataset strategy for Phase 5B.5 should be built around a synthetic, privacy-safe Indian financial-document corpus rather than attempting to acquire or scrape real personal documents. The synthetic dataset should prioritize Indian bank statements first, because they provide underwriting value and strong structure for layout detection, while preserving strict privacy and legal compliance. The layout target remains the existing DocLayNet-compatible 11-class structure, while the semantic field extraction layer uses underwriting-specific labels for OCR-driven parsing.

This is the correct path because it avoids illegal or ethically unacceptable data collection, gives a repeatable benchmark for the next fine-tune, and remains aligned with the verified DocLayNet findings: generic data alone is insufficient for Indian financial-document understanding.

**RECOMMENDED FIRST DATASET**: Synthetic Indian bank statement corpus, generated with anonymized placeholders, public-form layout references, and document-level isolated train/validation/test splits; minimum initial target of 1,500 labeled pages.

**RECOMMENDED FIRST DOCUMENT TYPE**: Indian bank statements.

**RECOMMENDED ANNOTATION CLASSES**: DOCUMENT_HEADER, DOCUMENT_TITLE, BANK_NAME, EMPLOYER_NAME, CUSTOMER_NAME, ACCOUNT_NUMBER, IFSC_CODE, DATE_RANGE, TRANSACTION_TABLE, TABLE_HEADER, TOTAL_AMOUNT, SIGNATURE, STAMP.

**MINIMUM INITIAL DATASET SIZE**: 1,500 labeled pages total (1,050 train / 225 validation / 225 test), with at least 300–500 synthetic documents and multiple template families per type.

**LICENSE/PRIVACY STATUS**: Synthetic-only dataset; no real personal financial documents; public form and template references only; no dataset may be marked as commercially reusable without independent license verification.

**NEXT TRAINING COMMAND**: python -m ai.app.ml.training.train_document_layout --dataset_yaml data/processed/indian_fin_docs/indian_fin_docs.yaml --epochs 30 --img 640 --batch 16 --project runs/detect/indian_fin_docs
