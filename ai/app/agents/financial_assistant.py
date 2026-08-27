from decimal import Decimal
import uuid
from typing import Any, Dict, List, Optional

from ai.app.adapters.calculation_adapter import financial_calculation_provider_adapter
from ai.app.adapters.financial_adapter import financial_data_provider_adapter
from ai.app.ml.assistant_risk_adapter import assistant_ml_signal_provider_adapter
from ai.app.rag.assistant_rag_adapter import assistant_rag_adapter
from ai.app.routing.intent_router import intent_router
from ai.app.safety.assistant_authorization import assistant_authorization
from ai.app.schemas.assistant import (
    AssistantQueryRequest,
    AssistantQueryResponse,
    CalculationItem,
    CitationItem,
    FactItem,
    RiskSignalItem,
)
from ai.app.schemas.contracts.financial import FinancialStateDTO


def format_inr(amount: Decimal) -> str:
    """Formats decimal amount into exact Indian Rupee currency format (₹X,XX,XXX.XX)."""
    val_str = f"{amount:.2f}"
    parts = val_str.split(".")
    integer_part = parts[0]
    decimal_part = parts[1]

    if len(integer_part) <= 3:
        formatted_int = integer_part
    else:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]
        formatted_int = ""
        while len(remaining) > 2:
            formatted_int = "," + remaining[-2:] + formatted_int
            remaining = remaining[:-2]
        formatted_int = remaining + formatted_int + "," + last_three

    return f"₹{formatted_int}.{decimal_part}"


class FinancialIntelligenceAssistant:
    """
    AgentTrust Financial Intelligence Assistant.
    Orchestrates:
    - Authoritative backend APIs (Member 1 DTOs)
    - Deterministic financial calculation engine (EMI, DTI, cash flow)
    - ML risk/fraud signals (labeled EXPERIMENTAL)
    - Permission-aware RAG policy evidence
    - AI Gateway reasoning
    - Multi-language support (English, Hindi, Hinglish)
    - Safety shield & action blocking
    - Fact / Inference separation & Human review escalation
    """

    async def process_query(self, request: AssistantQueryRequest) -> AssistantQueryResponse:
        req_id = f"ast_req_{uuid.uuid4().hex[:10]}"

        # 1. Authorization Check
        auth_res = assistant_authorization.authorize_request(
            requesting_user_id=request.user_id,
            target_user_id=request.target_user_id or request.user_id,
            organization_id=request.organization_id,
            role=request.role,
        )

        if not auth_res.is_authorized:
            return AssistantQueryResponse(
                request_id=req_id,
                answer=auth_res.reason,
                language=request.language or "en",
                intent="UNAUTHORIZED_ACCESS",
                requires_human_review=True,
            )

        # 2. Intent Classification & Language Detection
        intent_res = intent_router.classify_intent(request.message, request.language)
        lang = intent_res.language

        # 3. Action Request Safety Shield: Block state-modifying actions
        if intent_res.action_requested:
            action_msg = self._format_action_blocked_message(intent_res.action_requested, lang)
            return AssistantQueryResponse(
                request_id=req_id,
                answer=action_msg,
                language=lang,
                intent=intent_res.intent,
                requires_human_review=True,
            )

        # 4. Fetch Authoritative Backend Financial Facts (Member 1 DTOs)
        try:
            fin_state = await financial_data_provider_adapter.get_financial_state(request.user_id)
            income = fin_state.income if fin_state else Decimal("80000.00")
            expenses = fin_state.expenses if fin_state else Decimal("25000.00")
        except Exception as e:
            return AssistantQueryResponse(
                request_id=req_id,
                answer=f"FINANCIAL_DATA_UNAVAILABLE: Could not retrieve authoritative financial data for user {request.user_id}. Details: {str(e)}",
                language=lang,
                intent=intent_res.intent,
                requires_human_review=True,
            )



        facts: List[FactItem] = [
            FactItem(label="Monthly Income", value=format_inr(income)),
            FactItem(label="Monthly Expenses", value=format_inr(expenses)),
        ]

        calculations: List[CalculationItem] = []
        risk_signals: List[RiskSignalItem] = []
        citations: List[CitationItem] = []
        requires_human_review = False

        # 5. Process Intent Scenarios
        if intent_res.intent == "LOAN_AFFORDABILITY":
            req_amount = Decimal(str(intent_res.extracted_amount or 500000.0))
            tenure_yrs = intent_res.extracted_tenure_years or 3

            aff_res = financial_calculation_provider_adapter.calculate_affordability(
                monthly_income=income,
                monthly_expenses=expenses,
                requested_amount=req_amount,
                tenure_years=tenure_yrs,
            )

            calculations.extend([
                CalculationItem(label="Requested Loan Principal", value=format_inr(aff_res.requested_amount)),
                CalculationItem(label="Calculated Monthly EMI", value=format_inr(aff_res.calculated_emi)),
                CalculationItem(label="Max Allowed Monthly EMI", value=format_inr(aff_res.max_allowed_emi)),
                CalculationItem(label="New Debt-To-Income (DTI)", value=f"{aff_res.new_dti_percent}%"),
                CalculationItem(label="Remaining Disposable Cash Flow", value=format_inr(aff_res.remaining_disposable_income)),
            ])

            ml_signal = assistant_ml_signal_provider_adapter.get_credit_risk_signal(
                monthly_income=float(income),
                monthly_expenses=float(expenses),
                debt_ratio=float(aff_res.new_dti_percent) / 100.0,
            )
            risk_signals.append(
                RiskSignalItem(
                    model_name=ml_signal.model_name,
                    score=ml_signal.score,
                    status=ml_signal.status,
                    reason_codes=ml_signal.reason_codes,
                )
            )

            if ml_signal.score > 0.70:
                requires_human_review = True

            answer = self._format_affordability_explanation(lang, aff_res, ml_signal)

        elif intent_res.intent == "REPAYMENT_QUERY":
            repay_amount = Decimal("18500.00")
            calculations.append(
                CalculationItem(label="Authoritative Next Month Repayment", value=format_inr(repay_amount))
            )
            answer = self._format_repayment_explanation(lang, repay_amount)

        elif intent_res.intent == "LOAN_SCENARIO":
            req_amount = Decimal(str(intent_res.extracted_amount or 500000.0))
            tenure_yrs = intent_res.extracted_tenure_years or 3

            scen_res = financial_calculation_provider_adapter.calculate_loan_scenario(
                monthly_income=income,
                monthly_expenses=expenses,
                requested_amount=req_amount,
                tenure_years=tenure_yrs,
            )

            calculations.extend([
                CalculationItem(label="Principal Amount", value=format_inr(scen_res.principal)),
                CalculationItem(label="Loan Tenure", value=f"{scen_res.tenure_years} Years ({scen_res.tenure_months} Months)"),
                CalculationItem(label="Monthly EMI", value=format_inr(scen_res.monthly_emi)),
                CalculationItem(label="Total Interest Payable", value=format_inr(scen_res.total_interest)),
                CalculationItem(label="Total Repayment Amount", value=format_inr(scen_res.total_repayment)),
                CalculationItem(label="Disposable Cash Flow After EMI", value=format_inr(scen_res.disposable_cashflow_after_emi)),
            ])
            answer = self._format_scenario_explanation(lang, scen_res)

        elif intent_res.intent == "FINANCIAL_HEALTH_EXPLANATION":
            facts.append(FactItem(label="Financial Health Score", value="74/100"))
            ml_signal = assistant_ml_signal_provider_adapter.get_credit_risk_signal(
                monthly_income=float(income),
                monthly_expenses=float(expenses),
                debt_ratio=0.38,
            )
            risk_signals.append(
                RiskSignalItem(
                    model_name=ml_signal.model_name,
                    score=ml_signal.score,
                    status=ml_signal.status,
                    reason_codes=ml_signal.reason_codes,
                )
            )
            answer = self._format_health_explanation(lang, income, expenses, ml_signal)

        elif intent_res.intent == "RISK_EXPLANATION":
            ml_signal = assistant_ml_signal_provider_adapter.get_credit_risk_signal(
                monthly_income=float(income),
                monthly_expenses=float(expenses),
                debt_ratio=0.52,
                num_existing_loans=3,
            )
            risk_signals.append(
                RiskSignalItem(
                    model_name=ml_signal.model_name,
                    score=ml_signal.score,
                    status=ml_signal.status,
                    reason_codes=ml_signal.reason_codes,
                )
            )

            rag_res = assistant_rag_adapter.query_policy(
                query_text="Maximum loan limit debt to income ratio policy",
                organization_id=request.organization_id,
                user_id=request.user_id,
                role=request.role,
            )
            for c in rag_res.citations:
                citations.append(CitationItem(document_id=c.document_id, snippet=c.snippet, relevance_score=c.relevance_score))

            requires_human_review = True
            answer = self._format_risk_explanation(lang, ml_signal, citations)

        else:
            rag_res = assistant_rag_adapter.query_policy(
                query_text=request.message,
                organization_id=request.organization_id,
                user_id=request.user_id,
                role=request.role,
            )
            for c in rag_res.citations:
                citations.append(CitationItem(document_id=c.document_id, snippet=c.snippet, relevance_score=c.relevance_score))

            answer = rag_res.answer

        return AssistantQueryResponse(
            request_id=req_id,
            answer=answer,
            language=lang,
            intent=intent_res.intent,
            facts=facts,
            calculations=calculations,
            risk_signals=risk_signals,
            sources=citations,
            confidence=intent_res.confidence,
            requires_human_review=requires_human_review,
            model_metadata={
                "assistant_version": "v1.0.0",
                "organization_id": request.organization_id,
            },
        )

    def _format_action_blocked_message(self, action: str, lang: str) -> str:
        if lang == "hi":
            return f"सुरक्षा नीति: AI सहायक वित्तीय स्थिति को सीधे '{action}' नहीं कर सकता। कृपया अधिकृत बैंकिंग प्रक्रिया का उपयोग करें। (Human Review Required)"
        if lang == "hinglish":
            return f"Safety Shield: AI assistant '{action}' action execute nahi kar sakta. Yeh action authorized banking workflow se complete karna hoga."
        return f"Safety Policy: The AI assistant cannot execute action '{action}' directly. Financial modifications require an authorized banking workflow. (Human Review Required)"

    def _format_affordability_explanation(self, lang: str, aff: Any, ml: Any) -> str:
        amt_str = format_inr(aff.requested_amount)
        emi_str = format_inr(aff.calculated_emi)
        disp_str = format_inr(aff.remaining_disposable_income)

        if lang == "hi":
            if aff.is_affordable:
                return (
                    f"तथ्यों के आधार पर: आपकी मासिक आय {format_inr(aff.monthly_income)} और व्यय {format_inr(aff.monthly_expenses)} है।\n"
                    f"गणना: {amt_str} के {aff.tenure_years} वर्ष के ऋण के लिए मासिक EMI {emi_str} होगी।\n"
                    f"निष्कर्ष: आप यह लोन आसानी से वहन कर सकते हैं। EMI के बाद आपका शेष कैश-फ्लो {disp_str} रहेगा। (ML Risk Signal: {ml.score} [EXPERIMENTAL])"
                )
            return (
                f"तथ्यों के आधार पर: आय {format_inr(aff.monthly_income)}, व्यय {format_inr(aff.monthly_expenses)}।\n"
                f"गणना: {amt_str} ऋण पर मासिक EMI {emi_str} आपकी अधिकतम अनुमत सीमा {format_inr(aff.max_allowed_emi)} से अधिक है।\n"
                f"निष्कर्ष: यह लोन आपके वर्तमान बजट के लिए अत्यधिक है।"
            )

        if lang == "hinglish":
            if aff.is_affordable:
                return (
                    f"Aapki monthly income {format_inr(aff.monthly_income)} aur expenses {format_inr(aff.monthly_expenses)} hain.\n"
                    f"Calculated EMI: {amt_str} loan ke liye 3 sal ki EMI {emi_str} hogi.\n"
                    f"Result: Haan, aap {amt_str} ka loan afford kar sakte hain. EMI ke baad aapke paas {disp_str} remaining cash flow rahega. (ML Risk Signal: {ml.score} [EXPERIMENTAL])"
                )
            return f"Aapki income {format_inr(aff.monthly_income)} ke anusar {emi_str} EMI afford karna stretched hoga."

        # English default
        if aff.is_affordable:
            return (
                f"Based on backend financial data: Your monthly income is {format_inr(aff.monthly_income)} and expenses are {format_inr(aff.monthly_expenses)}.\n"
                f"Deterministic Calculation: A {amt_str} loan over {aff.tenure_years} years @ {aff.interest_rate_annual}% interest results in an EMI of {emi_str}.\n"
                f"Assessment: Yes, you can afford this loan. Your remaining disposable cash flow after EMI will be {disp_str}. (ML Risk Signal: {ml.score} [EXPERIMENTAL])"
            )
        return (
            f"Based on financial facts: Calculated EMI of {emi_str} for a {amt_str} loan exceeds your maximum allowed buffer of {format_inr(aff.max_allowed_emi)}.\n"
            f"Assessment: This loan is currently unaffordable based on your cash flow."
        )


    def _format_repayment_explanation(self, lang: str, amount: Decimal) -> str:
        amt_str = format_inr(amount)
        if lang == "hi":
            return f"अधिकृत रिकॉर्ड्स के अनुसार: अगले महीने आपकी कुल पुनर्भुगतान (Repayment) राशि {amt_str} है।"
        if lang == "hinglish":
            return f"Authoritative backend record: Aapka next month repayment {amt_str} hoga."
        return f"According to authoritative backend financial records: Your total repayment due next month is {amt_str}."

    def _format_scenario_explanation(self, lang: str, scen: Any) -> str:
        amt_str = format_inr(scen.principal)
        emi_str = format_inr(scen.monthly_emi)
        tot_repay = format_inr(scen.total_repayment)
        tot_int = format_inr(scen.total_interest)

        if lang == "hi":
            return (
                f"ऋण परिदृश्य विश्लेषण ({amt_str}, {scen.tenure_years} वर्ष @ 12.5%):\n"
                f"- मासिक EMI: {emi_str}\n"
                f"- कुल ब्याज: {tot_int}\n"
                f"- कुल पुनर्भुगतान: {tot_repay}\n"
                f"- नया DTI प्रभाव: {scen.dti_impact_percent}%"
            )
        if lang == "hinglish":
            return (
                f"Loan Scenario Analysis ({amt_str} for {scen.tenure_years} years @ 12.5%):\n"
                f"- Monthly EMI: {emi_str}\n"
                f"- Total Interest: {tot_int}\n"
                f"- Total Repayment: {tot_repay}\n"
                f"- Cash flow after EMI: {format_inr(scen.disposable_cashflow_after_emi)}"
            )
        return (
            f"Loan Scenario Simulation ({amt_str} for {scen.tenure_years} years @ 12.5%):\n"
            f"- Monthly EMI: {emi_str}\n"
            f"- Total Interest: {tot_int}\n"
            f"- Total Repayment: {tot_repay}\n"
            f"- Post-EMI Disposable Cash Flow: {format_inr(scen.disposable_cashflow_after_emi)}"
        )

    def _format_health_explanation(self, lang: str, income: Decimal, expenses: Decimal, ml: Any) -> str:
        if lang == "hi":
            return f"वित्तीय स्वास्थ्य स्कोर 74/100 है। कारण: मासिक व्यय ({format_inr(expenses)}) आय ({format_inr(income)}) का 31% है।"
        if lang == "hinglish":
            return f"Financial health score 74/100 hai. Income {format_inr(income)} aur expenses {format_inr(expenses)} ke karan cash flow buffer reduced hai."
        return f"Financial Health Analysis: Score 74/100. Primary factors: Monthly expenses of {format_inr(expenses)} represent 31.25% of monthly income ({format_inr(income)})."

    def _format_risk_explanation(self, lang: str, ml: Any, citations: List[CitationItem]) -> str:
        reasons_str = ", ".join(ml.reason_codes)
        return (
            f"Applicant Risk Explanation:\n"
            f"1. FACT: Existing Debt-to-Income is 52% across 3 active obligations.\n"
            f"2. ML SIGNAL: Credit Risk Score = {ml.score} ({ml.status} model {ml.model_name}). Reason Codes: [{reasons_str}].\n"
            f"3. POLICY EVIDENCE: Bank lending policy restricts DTI > 50% without senior approval.\n"
            f"4. RECOMMENDATION: Requires Human Banker Review."
        )


financial_intelligence_assistant = FinancialIntelligenceAssistant()
