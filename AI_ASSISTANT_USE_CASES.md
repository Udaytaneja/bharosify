# Financial Intelligence Assistant Use Cases Specification - AgentTrust OS

**Author**: Member 3 (AI/ML/LLM/Agent Intelligence Subsystem Lead)  
**Date**: August 25, 2026  
**Scope**: 5 Core User-Facing Financial Use Cases

---

## Supported Use Cases Matrix

| Use Case | Example Query (EN / HI / Hinglish) | Pipeline & Calculations Executed | Primary Output Data |
| :--- | :--- | :--- | :--- |
| **1. Loan Affordability** | *"Can I afford a ₹5 lakh loan?"* / *"क्या मैं ₹5 लाख का लोन ले सकता हूँ?"* / *"Mera income dekh ke kya main 5 lakh ka loan afford kar sakta hoon?"* | Intent classification $\rightarrow$ Minimum data fetch $\rightarrow$ Deterministic EMI & DTI calculation $\rightarrow$ Risk signal $\rightarrow$ Explanation. | EMI, Max Allowed EMI, New DTI%, Disposable Income, Risk Score (EXPERIMENTAL). |
| **2. Repayment Query** | *"How much do I have to repay next month?"* / *"Mera next month repayment kitna hoga?"* | Fetch authoritative Member 1 repayment record. | Authoritative Repayment Due Amount & Due Date. |
| **3. Financial Health** | *"Why did my financial health score decrease?"* / *"Meri financial health kyun kam hui?"* | Fetch income, expenses, debt obligations, health score (74/100) $\rightarrow$ Explain drivers. | Health score drivers, expense-to-income ratio. |
| **4. Loan Scenario** | *"What happens if I take a ₹5 lakh loan for 3 years?"* | Deterministic loan scenario engine (principal, EMI, total interest, total repayment, post-EMI cash flow). | EMI, Total Interest, Total Repayment, Disposable Cash Flow. |
| **5. Risk Explanation** | *"Why is this applicant considered high risk?"* | Combine facts (DTI 52%) + ML risk score (0.72) + RAG policy evidence $\rightarrow$ Fact/Inference separation. | DTI fact, ML score & reason codes, RAG policy citation, `requires_human_review = True`. |
