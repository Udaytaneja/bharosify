# AI Dataset Registry & Research Inventory - AgentTrust OS

**Author**: Member 3 (AI/ML/LLM/Agent Intelligence Subsystem Lead)  
**Date**: August 25, 2026  
**Scope**: Dataset Inventory, Licenses, Citations, and Research Approvals

---

> [!WARNING]
> **RESEARCH & EXPERIMENTAL SCOPE**:
> Proprietary bank/customer data is currently NOT authorized or used in model training. All datasets listed below are public or synthetic benchmark datasets used strictly for experimentation, benchmarking, and feature pipeline research.

---

## Dataset Inventory Matrix

| Dataset ID | Name | Source | Version | License | Citation | Row Count | Target Definition | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`uci_credit_default`** | UCI Default of Credit Card Clients | UCI ML Repository | `v1.0.0` | **CC BY 4.0** | Yeh & Lien (2009) | 30,000 | `default payment next month` (1/0) | `APPROVED_FOR_RESEARCH` |
| **`uci_german_credit`** | UCI Statlog German Credit | UCI ML Repository | `v1.0.0` | **CC BY 4.0** | Hofmann (1994) | 1,000 | `credit risk` (1 Good, 2 Bad) | `APPROVED_FOR_RESEARCH` |
| **`uci_credit_approval`** | UCI Credit Approval | UCI ML Repository | `v1.0.0` | **CC BY 4.0** | Quinlan (1987) | 690 | `approval status` (+/-) | `APPROVED_FOR_RESEARCH` |
| **`ibm_aml_synthetic`** | IBM Anti-Money Laundering Synthetic | IBM / Kaggle | `v1.0.0` | **CDLA-Sharing-1.0** | Altman (2023) | 500,000 | `Is Laundering` (1/0) | `APPROVED_FOR_RESEARCH` *(Synthetic)* |
| **`ibm_amlsim_graph`** | IBM AMLSim Transaction Graph | IBM GitHub | `v1.0.0` | **Apache-2.0** | Suzumura et al. (2021) | 100,000 | `is_sar` (1/0) | `APPROVED_FOR_RESEARCH` *(Synthetic Graph)* |

---

## Sensitive Attribute Audit

The following protected attributes are recorded in dataset metadata for **fairness auditing ONLY** and are **strictly excluded from model training feature vectors**:
- `SEX`, `AGE`, `MARRIAGE`, `EDUCATION` (`uci_credit_default`)
- `personal_status_sex`, `age`, `foreign_worker` (`uci_german_credit`)
