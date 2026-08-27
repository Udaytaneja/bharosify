import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class IntentClassificationResult(BaseModel):
    """Structured Intent Classification Output."""

    intent: str  # "LOAN_AFFORDABILITY" | "REPAYMENT_QUERY" | "FINANCIAL_HEALTH_EXPLANATION" | "LOAN_SCENARIO" | "RISK_EXPLANATION" | "GENERAL_FINANCIAL_QUESTION" | "UNKNOWN"
    confidence: float
    language: str  # "en" | "hi" | "hinglish"
    requires_financial_data: bool = True
    requires_rag: bool = False
    requires_ml: bool = False
    extracted_amount: Optional[float] = None
    extracted_tenure_years: Optional[int] = None
    action_requested: Optional[str] = None  # "approve" | "transfer" | "change_repayment" | None


class IntentRouter:
    """
    Explicit Intent Classification & Routing Layer for Financial Intelligence Assistant.
    Detects intent, language (English, Hindi, Hinglish), extracted parameters, and requested actions.
    """

    def classify_intent(self, message: str, override_language: Optional[str] = None) -> IntentClassificationResult:
        msg = message.strip()
        lower_msg = msg.lower()

        # 1. Detect Language
        lang = override_language or self._detect_language(msg)

        # 2. Check for State-Modifying Action Requests (Safety Trigger)
        action_requested = self._detect_action_request(lower_msg)

        # 3. Action Intents (Run BEFORE Read-Only Intents)
        if action_requested:
            intent_name = "REPAYMENT_MODIFICATION" if "repayment" in action_requested or "emi" in action_requested or "tenure" in action_requested else ("LOAN_APPROVAL" if action_requested == "approve" else "MONEY_TRANSFER")
            return IntentClassificationResult(
                intent=intent_name,
                confidence=0.98,
                language=lang,
                requires_financial_data=False,
                requires_rag=False,
                requires_ml=False,
                action_requested=action_requested,
            )

        # 4. Parameter Extraction (Amounts, Tenure)
        amount = self._extract_amount(msg)
        tenure = self._extract_tenure(msg)


        # 4. Intent Classification Rules
        # LOAN_AFFORDABILITY
        if any(w in lower_msg for w in ["afford", "affordability", "loan le sakta", "loan le sakta hoon", "kya main loan", "loan lene ke kabil", "लोन", "ऋण", "ले सकता", "अफोर्ड"]):
            return IntentClassificationResult(
                intent="LOAN_AFFORDABILITY",
                confidence=0.95,
                language=lang,
                requires_financial_data=True,
                requires_rag=False,
                requires_ml=True,
                extracted_amount=amount or 500000.0,
                extracted_tenure_years=tenure or 3,
                action_requested=action_requested,
            )


        # REPAYMENT_QUERY
        if any(w in lower_msg for w in ["repay", "repayment", "next month", "due date", "kitna bharna", "kitna repay", "repay kitna"]):
            return IntentClassificationResult(
                intent="REPAYMENT_QUERY",
                confidence=0.95,
                language=lang,
                requires_financial_data=True,
                requires_rag=False,
                requires_ml=False,
                action_requested=action_requested,
            )

        # FINANCIAL_HEALTH_EXPLANATION
        if any(w in lower_msg for w in ["financial health", "health score", "score decrease", "score dropped", "health kyun kam", "score kam kyun"]):
            return IntentClassificationResult(
                intent="FINANCIAL_HEALTH_EXPLANATION",
                confidence=0.92,
                language=lang,
                requires_financial_data=True,
                requires_rag=False,
                requires_ml=True,
                action_requested=action_requested,
            )

        # LOAN_SCENARIO
        if any(w in lower_msg for w in ["what happens if", "scenario", "for 3 years", "for 5 years", "take a loan of", "kitna emi hoga", "kitna total repayment"]):
            return IntentClassificationResult(
                intent="LOAN_SCENARIO",
                confidence=0.90,
                language=lang,
                requires_financial_data=True,
                requires_rag=False,
                requires_ml=False,
                extracted_amount=amount or 500000.0,
                extracted_tenure_years=tenure or 3,
                action_requested=action_requested,
            )

        # RISK_EXPLANATION
        if any(w in lower_msg for w in ["high risk", "risk explanation", "why is this applicant", "risk score", "risk reason"]):
            return IntentClassificationResult(
                intent="RISK_EXPLANATION",
                confidence=0.94,
                language=lang,
                requires_financial_data=True,
                requires_rag=True,
                requires_ml=True,
                action_requested=action_requested,
            )

        # GENERAL_FINANCIAL_QUESTION / POLICY
        if any(w in lower_msg for w in ["policy", "rule", "guideline", "maximum dti", "interest rate"]):
            return IntentClassificationResult(
                intent="GENERAL_FINANCIAL_QUESTION",
                confidence=0.85,
                language=lang,
                requires_financial_data=False,
                requires_rag=True,
                requires_ml=False,
                action_requested=action_requested,
            )

        return IntentClassificationResult(
            intent="UNKNOWN",
            confidence=0.50,
            language=lang,
            requires_financial_data=True,
            requires_rag=False,
            requires_ml=False,
            action_requested=action_requested,
        )

    def _detect_language(self, msg: str) -> str:
        """Detects if message is Hindi (Devanagari), Hinglish, or English."""
        # Devanagari Unicode Range Check
        if re.search(r"[\u0900-\u097F]", msg):
            return "hi"

        lower = msg.lower()
        hinglish_words = ["mera", "meri", "hoga", "sakta", "hoon", "kya", "kitna", "bhai", "hai", "dekh", "kam", "kyun", "liye"]
        if any(w in lower.split() for w in hinglish_words):
            return "hinglish"

        return "en"

    def _detect_action_request(self, lower_msg: str) -> Optional[str]:
        """Detects state-modifying action requests that must be blocked for safety."""
        if "approve" in lower_msg:
            return "approve"
        if "transfer" in lower_msg or "bhejo" in lower_msg:
            return "transfer"

        repayment_modification_phrases = [
            "change my repayment",
            "modify my emi",
            "reduce my monthly repayment",
            "reduce my repayment",
            "change my repayment date",
            "skip my next repayment",
            "skip repayment",
            "extend my loan tenure",
            "extend tenure",
            "cancel my repayment",
            "change repayment",
            "modify repayment",
            "alter repayment",
            "repayment schedule",
            "change emi",
            "modify emi",
        ]
        if any(phrase in lower_msg for phrase in repayment_modification_phrases):
            return "change_repayment"
        return None


    def _extract_amount(self, msg: str) -> Optional[float]:
        """Extracts numerical loan amount from text (handles ₹, lakh, etc.)."""
        lower = msg.lower()

        # Check Lakh pattern (e.g., 5 lakh, ₹5 lakh)
        lakh_match = re.search(r"(?:₹|\$|rs\.?\s*)?(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|lac|lacs)", lower)
        if lakh_match:
            return float(lakh_match.group(1)) * 100000.0

        # Check raw number pattern (e.g., 500000, 5,00,000)
        raw_match = re.search(r"(?:₹|\$|rs\.?\s*)?(\d{1,3}(?:,\d{2,3})+|\d{4,9})", lower)
        if raw_match:
            num_str = raw_match.group(1).replace(",", "")
            return float(num_str)

        return None

    def _extract_tenure(self, msg: str) -> Optional[int]:
        """Extracts loan tenure in years."""
        lower = msg.lower()
        tenure_match = re.search(r"(\d+)\s*(?:year|years|yr|yrs|saal)", lower)
        if tenure_match:
            return int(tenure_match.group(1))
        return None


intent_router = IntentRouter()
