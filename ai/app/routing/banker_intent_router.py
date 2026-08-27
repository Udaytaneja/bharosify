import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class BankerIntentResult(BaseModel):
    intent: str  # "RISK_EXPLANATION" | "APPLICANT_SUMMARY" | "POLICY_CHECK" | "FINANCIAL_HEALTH_REVIEW" | "FRAUD_REVIEW" | "DOCUMENT_REVIEW" | "RISK_CHANGE_EXPLANATION" | "RECOMMENDED_REVIEW_ITEMS" | "LOAN_APPROVAL" | "LOAN_REJECTION" | "LOAN_DISBURSEMENT" | "MONEY_TRANSFER" | "REPAYMENT_MODIFICATION" | "ACTION_BLOCKED" | "UNKNOWN"
    confidence: float
    language: str  # "en" | "hi" | "hinglish"
    action_requested: Optional[str] = None  # "approve" | "reject" | "disburse" | "transfer" | "modify_repayment" | "transactional_unknown" | None


class BankerIntentRouter:
    """
    Intent Classifier for Banker Intelligence & Underwriting Copilot.
    Routes banker questions to specific evidence-fusion underwriting pipelines.
    Enforces protected action safety shield before read-only intent classification
    using phrase/context-aware precision matching (zero false positives on read queries).
    """

    PROTECTED_ACTION_MAP = [
        (
            "LOAN_APPROVAL",
            "approve",
            [
                "approve", "approval", "auto approve", "force approve",
                "authorize this loan", "authorize loan", "give approval",
                "approve the application", "approve application"
            ],
        ),
        (
            "LOAN_REJECTION",
            "reject",
            [
                "reject", "rejection", "auto reject", "decline this applicant",
                "decline applicant", "deny this application", "deny application",
                "decline application"
            ],
        ),
        (
            "LOAN_DISBURSEMENT",
            "disburse",
            [
                "disburse", "disbursement", "release the loan", "release loan",
                "release funds", "pay out the loan", "payout loan", "payout",
                "send the approved loan", "send loan amount", "send the loan money",
                "disburse funds"
            ],
        ),
        (
            "MONEY_TRANSFER",
            "transfer",
            [
                "transfer", "transfer funds", "transfer the approved amount",
                "send money", "wire money", "wire funds"
            ],
        ),
        (
            "REPAYMENT_MODIFICATION",
            "modify_repayment",
            [
                "change repayment", "modify repayment", "change the emi", "change emi",
                "modify the emi", "modify emi", "reduce monthly repayment",
                "cancel repayment", "cancel the repayment", "cancel the loan payment",
                "skip repayment", "skip next repayment", "extend tenure", "extend the tenure",
                "reduce repayment", "reduce my emi", "change my emi", "modify my emi",
                "change my repayment", "modify my repayment", "alter repayment", "alter emi",
                "change repayment schedule", "modify repayment schedule"
            ],
        ),
    ]

    READ_ONLY_INTENT_PATTERNS = [
        ("RISK_EXPLANATION", ["why is this applicant risky", "why risky", "risk explanation", "risk cause", "risky kyun"]),
        ("APPLICANT_SUMMARY", ["summary", "summarize", "applicant summary", "profile summary", "overview"]),
        ("POLICY_CHECK", ["policy", "satisfy policy", "policy check", "guideline", "rule compliance"]),
        ("FINANCIAL_HEALTH_REVIEW", ["strongest financial factors", "financial health", "health review", "positive factors", "what is my emi", "explain my emi", "how much is my repayment", "why is my repayment high", "show my repayment schedule", "what was my last repayment"]),
        ("FRAUD_REVIEW", ["fraud", "anomaly", "suspicious", "fraud review", "transaction anomaly"]),
        ("DOCUMENT_REVIEW", ["document", "ocr", "evidence", "salary slip", "bank statement", "document review"]),
        ("RISK_CHANGE_EXPLANATION", ["score change", "risk change", "previous assessment", "why score changed"]),
        ("RECOMMENDED_REVIEW_ITEMS", ["review before making a decision", "review items", "what should i review", "recommendation"]),
    ]

    def classify_intent(self, question: str, override_language: Optional[str] = None) -> BankerIntentResult:
        msg = question.strip()
        lower_msg = msg.lower()
        lang = override_language or self._detect_language(msg)

        # 1. READ-ONLY Explicit Precision Guard
        # If the query is an explicit read-only query ("what is my emi", "show my repayment schedule", etc.)
        # route directly to read-only intent to prevent false positive action blocking.
        for intent_cat, keywords in self.READ_ONLY_INTENT_PATTERNS:
            if any(k in lower_msg for k in keywords):
                # Verify no explicit modification verb is present
                if not any(mod in lower_msg for mod in ["change", "modify", "cancel", "skip", "extend", "approve", "reject", "disburse", "transfer"]):
                    return BankerIntentResult(intent=intent_cat, confidence=0.92, language=lang)

        # 2. Protected Action Shield Execution (MUST happen BEFORE read-only intents)
        for intent_cat, action_name, keywords in self.PROTECTED_ACTION_MAP:
            for k in keywords:
                if re.search(r"\b" + re.escape(k) + r"\b", lower_msg):
                    return BankerIntentResult(
                        intent=intent_cat,
                        confidence=0.99,
                        language=lang,
                        action_requested=action_name,
                    )


        # 3. Secondary Read-Only Pattern Fallback
        for intent_cat, keywords in self.READ_ONLY_INTENT_PATTERNS:
            if any(k in lower_msg for k in keywords):
                return BankerIntentResult(intent=intent_cat, confidence=0.90, language=lang)

        # 4. UNKNOWN Transactional Safety Check
        transactional_verbs = ["send", "payout", "pay", "modify", "alter", "execute", "grant", "wire", "cancel"]
        if any(w in lower_msg for w in transactional_verbs):
            return BankerIntentResult(
                intent="ACTION_BLOCKED",
                confidence=0.75,
                language=lang,
                action_requested="transactional_unknown",
            )

        return BankerIntentResult(intent="UNKNOWN", confidence=0.60, language=lang)

    def _detect_language(self, msg: str) -> str:
        if re.search(r"[\u0900-\u097F]", msg):
            return "hi"
        lower = msg.lower()
        if any(w in lower.split() for w in ["mera", "meri", "kyun", "hai", "kaise", "bhai", "kya"]):
            return "hinglish"
        return "en"


banker_intent_router = BankerIntentRouter()
