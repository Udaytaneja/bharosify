# Specification: Indian Financial Document Annotation Standard (Phase 5B)

**Author**: Member 3 (Lead AI/ML/LLM/Agent Intelligence Lead)  
**Date**: August 26, 2026  
**Scope**: Bounding Box Annotation Rules & PII Privacy Standards for Indian Bank Statements and Salary Slips

---

## 1. Objective & Scope

This specification defines the annotation guidelines for building future authorized datasets of Indian financial documents (bank statements, salary slips, Aadhaar, PAN, ITR forms).

> [!IMPORTANT]
> **Strict Privacy & Anti-Scraping Directive**: Scraping private bank documents or collecting real customer documents containing live PII is **STRICTLY PROHIBITED**. Synthetic document generation (using approved templates) or authorized anonymized document datasets with mandatory de-identification MUST be used.

---

## 2. Target Annotation Classes

| Class Name | Definition | Bounding Box Boundary Rule |
| :--- | :--- | :--- |
| `DOCUMENT_HEADER` | Top banner of statement/payslip containing bank/employer logo and title. | Tight bounding box around entire top banner region. |
| `BANK_NAME` | Name/Logo of bank (e.g. HDFC Bank, ICICI Bank, State Bank of India). | Tight box enclosing bank name text/logo. |
| `EMPLOYER_NAME` | Employer name on salary slip. | Tight box enclosing company name. |
| `CUSTOMER_NAME` | Account holder or employee name. | Tight box around customer name line. Must be anonymized. |
| `ACCOUNT_NUMBER` | Bank account number or Employee ID. | Encloses account number digits. Must be masked/redacted. |
| `IFSC_CODE` | 11-digit IFSC code (e.g. `HDFC0001234`). | Tight box around IFSC string. |
| `DATE_RANGE` | Statement period date range or payslip month/year. | Encloses date string. |
| `TRANSACTION_TABLE` | Main transaction grid containing Date, Particulars, Chq, Debit, Credit, Balance. | Outer bounding box enclosing entire table grid. |
| `TABLE_HEADER` | Column header row of transaction table. | Single rectangle enclosing header row (`Date | Description | Amount | Balance`). |
| `TOTAL_AMOUNT` | Net salary, total deposit, or closing balance figure. | Tight box around total numerical value. |
| `SIGNATURE` | Authorized signature or digital verification mark. | Rectangle enclosing signature graphic. |
| `STAMP` | Official bank/company stamp or seal. | Circle/Rectangle enclosing stamp graphic. |

---

## 3. Privacy & De-Identification Requirements

1. **Aadhaar / PAN Redaction**: All 12-digit Aadhaar numbers must have the first 8 digits permanently masked (`XXXX-XXXX-1234`). PAN numbers must be anonymized.
2. **Account Number Masking**: Account numbers must display only the last 4 digits (`XXXX-XXXX-5678`).
3. **Name Anonymization**: Real customer names must be replaced with synthetic placeholders (e.g., `Rajesh Kumar`, `Priya Sharma`).
4. **Address Redaction**: Personal residential address lines must be obfuscated.

---

## 4. Quality Control & Labeling Verification

- **Format**: Export annotations in COCO JSON format and YOLO TXT format (`<class_id> <x_center> <y_center> <width> <height>`).
- **Overlap Protocol**: Bounding boxes must not cut off character ascenders/descenders.
- **Verification**: 100% of annotated images must pass automated bounding box validation checks ($0.0 \le (x_c, y_c, w, h) \le 1.0$) using `DocLayNetYOLOConverter.validate_bounding_box()`.
