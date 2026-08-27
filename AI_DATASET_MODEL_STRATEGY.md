# AgentTrust OS — Dataset & Model Selection Strategy (Phase 5A Audit)

**Author**: Member 3 (Lead AI/ML/LLM/Agent Intelligence Lead)  
**Date**: August 26, 2026  
**Scope**: Dataset Licensing, Model Selection Matrix, Data Governance, Fairness Policy & Phase 5 Roadmap

---

## 1. Executive Recommendation

AgentTrust OS requires an evidence-grounded dataset and model strategy across four core AI operational domains:
1. **Document Intelligence**: Adopt **DocLayNet** (CC-BY-4.0) as the primary pre-training layout benchmark for YOLOv8 transfer learning, combined with PaddleOCR for line-level OCR and spatial bounding-box fusion. Document layout pre-training must be augmented with custom domain fine-tuning for Indian bank statements, Aadhaar, PAN, and salary slips.
2. **Credit Risk Modeling**: Use **UCI Default of Credit Card Clients** (30,000 records) as the primary offline benchmark dataset for XGBoost model evaluation, metric calibration (ECE/Brier Score), and contract validation. Benchmark metrics are explicitly tagged `status = "EXPERIMENTAL"` and must NOT be claimed as real-world production accuracy for Indian fintech customers.
3. **Fraud / AML Intelligence**: Use **IBM AMLSim** (multi-agent synthetic transaction graph) as the primary experimentation framework for LightGBM fraud pattern classification.
4. **Transaction Anomaly Detection**: Utilize synthetic transaction volatility logs generated via **IBM AMLSim** graph structures for Isolation Forest anomaly scoring.

> [!IMPORTANT]
> **Production Licensing & Commercial Policy**: All datasets utilized in AgentTrust OS must be independently verified for commercial use (`COMMERCIAL_PERMITTED`). Datasets with restricted or non-commercial licenses (e.g., CC-BY-NC) are strictly prohibited for production deployments.

---

## 2. Dataset Comparison Table

| Domain | Dataset Name | Sample Count | Feature Count | Target Variable | Data Type | Primary Model Target | Strategic Recommendation |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- | :--- |
| **Document Layout** | **DocLayNet** | 80,863 pages | 11 classes | Bounding box layout classes | High-res Page Images | Ultralytics YOLOv8 Nano | **PRIMARY (BENCHMARK)** |
| **Document Layout** | **PubLayNet** | 360,000+ pages | 5 classes | Bounding box layout classes | Academic PDF Images | Ultralytics YOLOv8 | **SECONDARY (BASELINE)** |
| **Credit Risk** | **UCI Default Credit** | 30,000 rows | 23 features | `default.payment.next.month` (0/1) | Tabular Financial Data | XGBoost Classifier | **PRIMARY (BENCHMARK)** |
| **Credit Risk** | **UCI German Credit** | 1,000 rows | 20 features | Good / Bad Credit (1/2) | Small Tabular Data | XGBoost Classifier | **NOT RECOMMENDED** |
| **Credit Risk** | **UCI Credit Approval** | 690 rows | 15 features | Approved / Refused (+/-) | Obfuscated Tabular | Logistic Regression | **NOT RECOMMENDED** |
| **Fraud / AML** | **IBM AMLSim** | 1M+ edges | Graph/Tabular | `is_laundering` (0/1) | Synthetic Graph / Logs | LightGBM Classifier | **PRIMARY (EXPERIMENTATION)** |
| **Anomaly Detection** | **AMLSim Volatility** | 100k+ events | Volatility metrics | Anomaly Score | Synthetic Time Series | Isolation Forest | **PRIMARY (EXPERIMENTATION)** |

---

## 3. Licensing & Commercial Permissibility Matrix

| Dataset Name | License Type | License Verified | Commercial Use Permitted | Production Status | Strategic Notes |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **DocLayNet** | CC-BY-4.0 | **YES** | **COMMERCIAL_PERMITTED** | Approved for Pre-Training | Requires attribution in documentation. |
| **PubLayNet** | CC-BY-4.0 | **YES** | **COMMERCIAL_PERMITTED** | Secondary Benchmark | PubMed open access source data. |
| **UCI Default Credit** | CC-BY-4.0 | **YES** | **COMMERCIAL_PERMITTED** | Offline Experimentation | Taiwan 2005 dataset. Non-authoritative for India. |
| **UCI German Credit** | Public Domain / CC | **YES** | **COMMERCIAL_PERMITTED** | Legacy Only | Sample size too small (1,000 records). |
| **UCI Credit Approval** | Public Domain | **YES** | **COMMERCIAL_PERMITTED** | Obfuscated Only | Features obfuscated (A1..A15). |
| **IBM AMLSim** | Apache 2.0 | **YES** | **COMMERCIAL_PERMITTED** | Synthetic Benchmark | Open-source generator code & synthetic data. |

---

## 4. Document Intelligence Strategy (DocLayNet vs PubLayNet)

### A. Architectural Pipeline Separation
Document processing is strictly decoupled into three isolated, verifiable pipeline stages:
1. **Layout Detection (YOLOv8)**: Detects page structural bounding boxes (`Header`, `Text`, `Table`, `Title`, `Page-footer`, `Page-header`, `List-item`).
2. **Line OCR Extraction (PaddleOCR)**: Extracts raw text lines, word bounding boxes, and OCR confidence scores from clean image bytes.
3. **Spatial Bounding Box Fusion & Field Parsing**: Fuses spatial YOLO layout regions with PaddleOCR line coordinates to deterministically extract key-value pairs (e.g. `Income = ₹1,00,000.00`) without LLM hallucination.

### B. DocLayNet vs PubLayNet Comparison
- **DocLayNet**: Contains 80,863 pages across 6 document categories (financial reports, manuals, patents, law documents, scientific papers, business reports). Provides 11 layout classes annotated by professional human annotators.
- **PubLayNet**: Contains scientific article PDFs from PubMed. Limited to 5 layout classes (`Text`, `Title`, `List`, `Table`, `Figure`).
- **Recommendation**: DocLayNet is the **PRIMARY** layout benchmark due to its financial document coverage and granular 11-class schema.

### C. Domain Transfer Limitations for Indian Financial Documents
- **Critical Finding**: DocLayNet alone does **NOT** solve Indian bank statement (HDFC, ICICI, SBI) or salary slip understanding.
- **Domain Gap**: Indian bank statements contain dense transaction tables, bank logos, IFSC/MICR stamps, and bilingual text (Hindi/English).
- **Mitigation**: DocLayNet will serve strictly for general layout pre-training (Phase 5B). Custom synthetic and annotated Indian financial document layouts must be introduced in Phase 5B fine-tuning.

---

## 5. Credit Risk Strategy (UCI Default of Credit Card Clients)

### A. Dataset Evaluation
- **Primary Benchmark**: UCI Default of Credit Card Clients (30,000 credit card clients in Taiwan, April–September 2005).
- **Target Variable**: `default.payment.next.month` (Binary 0 = Non-default, 1 = Default). Class ratio: ~22.1% defaults (6,636 default records).
- **Features**: `LIMIT_BAL` (Credit Limit), `SEX`, `EDUCATION`, `MARRIAGE`, `AGE`, `PAY_0`..`PAY_6` (Repayment status), `BILL_AMT1`..`BILL_AMT6` (Bill statements), `PAY_AMT1`..`PAY_AMT6` (Previous payments).

### B. Calibration & Evaluation Metrics
- **Models**: XGBoost Classifier (`status = "EXPERIMENTAL"`).
- **Metrics Standard**:
  - **ROC-AUC**: Evaluates overall ranking capability.
  - **PR-AUC**: Measures precision/recall tradeoff under 22% class imbalance.
  - **Brier Score**: Evaluates probability calibration accuracy ($\text{Brier} = \frac{1}{N}\sum (\hat{p}_i - y_i)^2$).
  - **Expected Calibration Error (ECE)**: Asserts that predicted default probability $p=0.40$ corresponds empirically to a 40% default rate.

### C. Geographic & Temporal Limitations
- **Warning**: Taiwan 2005 credit card data is **NOT** representative of contemporary Indian lending customers.
- **Status**: The dataset is strictly designated as an **OFFLINE ML BENCHMARK** for pipeline verification. Model metrics on this dataset must never be presented as production credit scoring accuracy.

---

## 6. Fraud & AML Strategy (IBM AMLSim)

### A. Dataset & Generator Evaluation
- **Framework**: IBM AMLSim (Multi-Agent Synthetic Banking Transaction Generator).
- **Graph Structure**: Models entities (Bank Accounts) as nodes and financial transactions as directed weighted edges over time.
- **Typologies Simulated**:
  - **Fan-in / Fan-out**: Rapid aggregation of small transfers into a hub account followed by immediate outbound disbursement.
  - **Scatter-Gather**: Layering transactions across multi-hop intermediate accounts.
  - **Cycle / Circular Transfers**: Recycling funds through shell accounts to obscure origin.

### B. Machine Learning Architecture
- **Model**: LightGBM Binary Classifier on engineered tabular transaction features (velocity, amount variance, ratio of incoming/outgoing funds, counterparty fan-out degree).
- **Evaluation Metrics**: PR-AUC, Recall@K (maximizing detection of true laundering streams), Precision@K (minimizing false alert burden on compliance officers).

---

## 7. Transaction Anomaly Strategy

### A. Unsupervised Anomaly Detection Architecture
- **Model**: Isolation Forest (`IsolationForestAnomalyArchitecture`).
- **Feature Set**: Transaction amount volatility, transaction frequency spikes, off-hours transaction ratios, new location/IP jumps.
- **Evaluation Metrics**: Anomaly Score distribution, False Positive Rate (FPR), Precision@Top-1%.

---

## 8. Model Selection & Metric Matrix

| Domain | Task | Primary Model | Input Features | Evaluation Metrics | Runtime Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Document Perception** | Layout Region Bounding Box | Ultralytics YOLOv8 Nano | Page Image (640x640) | mAP@50, mAP@50-95, Precision, Recall | **CODE_VERIFIED** |
| **Document Perception** | OCR Text Line Extraction | PaddleOCR Adapter v2.0 | Clean Image Bytes | Line Confidence, Character Error Rate (CER) | **LIVE_VERIFIED** |
| **Credit Risk** | Binary Default Prediction | XGBoost Classifier | DTI, Income, Debt, Repayment | ROC-AUC, PR-AUC, Brier Score, ECE | **EXPERIMENTAL** |
| **Fraud Detection** | Laundering Pattern Classification | LightGBM Classifier | Transaction Graph Features | PR-AUC, Recall@K, Precision@K, F1 | **EXPERIMENTAL** |
| **Anomaly Detection** | Unsupervised Anomaly Scoring | Isolation Forest | Volatility & Frequency Metrics | FPR, Top-K Precision, Anomaly Score | **EXPERIMENTAL** |

---

## 9. Fairness Considerations & Sensitive Attribute Policy

To comply with regulatory fairness guidelines and ethical AI principles, sensitive attributes are strictly categorized:

| Attribute Name | Category | Rationale & Policy |
| :--- | :---: | :--- |
| **Gender (`SEX`)** | **PROHIBITED** | Strictly prohibited from being used as a model feature for credit risk decisions. |
| **Race / Ethnicity** | **PROHIBITED** | Strictly prohibited in automated underwriting. |
| **Religion / Caste** | **PROHIBITED** | Strictly prohibited by financial regulatory authorities. |
| **Age (`AGE`)** | **AUDIT_ONLY** | Excluded from direct model scoring. Monitored strictly in fairness audit logs for age-bias evaluation (Disparate Impact Ratio). |
| **Education (`EDUCATION`)** | **AUDIT_ONLY** | Monitored for demographic parity; not used as a primary risk driver. |
| **Income (`INCOME`)** | **MODEL_FEATURE** | Direct financial capacity attribute required for DTI calculations. |
| **Debt Obligations** | **MODEL_FEATURE** | Direct financial obligation attribute required for EMI affordability math. |

---

## 10. Data Leakage Risks & Mitigation Controls

| Leakage Risk Type | Identified Vulnerability | Mitigation Control |
| :--- | :--- | :--- |
| **Post-Outcome Feature Leakage** | Including post-default collection notes or post-chargeoff flags in credit model inputs. | Strict temporal cutoff boundary: Features must strictly precede the loan origination date $T_0$. |
| **Target Leakage in Tabular Datasets** | Including `PAY_AMT` recorded after default event $T_{default}$. | Feature isolation audit checking feature timestamps against label determination windows. |
| **Train / Test Contamination** | Splitting multi-transaction accounts across both train and validation splits. | Group-based splitting (`GroupKFold` on `account_id` / `user_id`). |
| **Temporal Data Leakage** | Random K-Fold cross-validation on time-series transaction graphs. | Time-based splitting (`TimeSeriesSplit`): Train on $T_{0}..T_{k}$, validate strictly on $T_{k+1}..T_{n}$. |

---

## 11. Dataset Governance Schema Standard

All datasets integrated into AgentTrust OS must record a formal `dataset_governance.json` metadata file:

```json
{
  "dataset_id": "ds_uci_default_credit_v1",
  "name": "UCI Default of Credit Card Clients Dataset",
  "source": "UCI Machine Learning Repository",
  "version": "1.0.0",
  "license": "CC-BY-4.0",
  "license_verified": true,
  "commercial_use_status": "COMMERCIAL_PERMITTED",
  "data_type": "tabular",
  "real_or_synthetic": "real",
  "target": "default.payment.next.month",
  "sample_count": 30000,
  "feature_count": 23,
  "sensitive_attributes": ["SEX", "EDUCATION", "MARRIAGE", "AGE"],
  "known_biases": "Taiwan credit card population from 2005. Regional and temporal bias.",
  "approved_use": "Offline benchmark evaluation and contract validation.",
  "prohibited_use": "Production credit decisions for Indian lending customers."
}
```

---

## 12. Recommended Phase 5B–5E Roadmap

- **Phase 5B — Document Layout Fine-Tuning**:
  - Pre-train YOLOv8 on DocLayNet (CC-BY-4.0).
  - Annotate a domain-specific dataset of Indian bank statements, salary slips, and tax forms.
  - Fine-tune YOLOv8 layout model weights and package into `models/yolov8_doclayout_v1.pt`.
- **Phase 5C — Credit Risk Model Calibration**:
  - Execute offline XGBoost training pipeline on verified dataset.
  - Implement Platt Scaling / Isotonic Regression for probability calibration.
  - Export model artifact and update experiment registry.
- **Phase 5D — Fraud / AML Pattern Classification**:
  - Generate synthetic transaction graphs using IBM AMLSim.
  - Train LightGBM classifier on graph-extracted features.
- **Phase 5E — Isolation Forest Anomaly Detection**:
  - Calibrate Isolation Forest contamination thresholds using volatility log streams.

---

## 13. Explicitly Rejected Candidates & Architectural Rationale

| Candidate | Status | Reason for Rejection |
| :--- | :---: | :--- |
| **UCI German Credit** | **REJECTED** | Dataset sample size is too small (1,000 records) and features from 1994 are obsolete for modern fintech risk modeling. |
| **UCI Credit Approval** | **REJECTED** | All 15 feature names and values are obfuscated (`A1`..`A15`), rendering explainable AI reasoning impossible. |
| **Generic COCO YOLO Weights (`yolov8n.pt`) as Document Layout Model** | **REJECTED FOR PRODUCTION** | Generic COCO weights detect general objects (dogs, cars) and cannot reliably identify financial document layout regions. |
| **Uncalibrated Raw Model Probabilities for Underwriting Decisions** | **REJECTED** | Raw tree-based output scores lack probability calibration. Must pass through ECE evaluation and human banker review. |
