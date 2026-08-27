import re
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from ai.app.adapters.financial_adapter import financial_data_provider_adapter
from ai.app.schemas.contracts.financial import FinancialStateDTO
from ai.app.schemas.financial_intelligence import (
    FinancialIntelligenceRequest,
    FinancialIntelligenceResponse,
    QueryUnderstanding,
)



def format_inr(amount: Decimal) -> str:
    """Format decimal amount in Indian Rupee format (₹X,XX,XXX.XX)."""
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


class FinancialIntelligenceService:
    """
    AgentTrust Financial Intelligence AI Service.
    
    Orchestrates the 7-Step AI Workflow:
    1. Understand question (intent classification & parameter extraction)
    2. Identify required data
    3. Request authorized backend data
    4. Invoke deterministic backend calculations (FinancialEngine)
    5. Analyze results
    6. Explain results (exact number preservation, multi-language EN/HI/Hinglish)
    7. Provide evidence
    """

    def __init__(self, db_session: Optional[AsyncSession] = None):
        self.db = db_session

    async def process_request(self, request: FinancialIntelligenceRequest) -> FinancialIntelligenceResponse:
        # Step 1: Understand Question & Language Detection
        understanding = self._understand_question(request.query, request.task, request.language, request.context)

        # Step 2 & 3: Identify & Request Authorized Data
        context_data = await self._fetch_authorized_data(request.user_id, request.context)

        # Step 4: Invoke Deterministic Calculations based on Intent
        intent = understanding.intent
        params = understanding.extracted_params
        calc_results, digital_twin_state, what_if_result = self._invoke_deterministic_calculations(
            intent, params, context_data
        )

        # Step 5: Analyze Results & Recommendation
        analysis, recommendation, confidence = self._analyze_results(intent, calc_results, context_data)

        # Step 6: Explain Results (Language specific with exact number retention)
        explanation = self._explain_results(
            intent=intent,
            language=understanding.detected_language,
            calc_results=calc_results,
            digital_twin_state=digital_twin_state,
            what_if_result=what_if_result,
            context_data=context_data,
            params=params,
        )

        # Step 7: Provide Evidence
        evidence = self._provide_evidence(intent, calc_results, digital_twin_state, what_if_result)

        return FinancialIntelligenceResponse(
            request_id=request.request_id,
            task=intent,
            language=understanding.detected_language,
            query_understanding=understanding,
            deterministic_results=calc_results,
            explanation=explanation,
            evidence=evidence,
            recommendation=recommendation,
            confidence=confidence,
            digital_twin_state=digital_twin_state,
            what_if_result=what_if_result,
        )

    def _understand_question(
        self, query: str, task_override: Optional[str], language_override: str, context: Dict[str, Any]
    ) -> QueryUnderstanding:
        q_lower = query.lower()

        # 1. Detect Language
        if language_override in ["en", "hi", "hinglish"]:
            lang = language_override
        else:
            if re.search(r"[\u0900-\u097F]", query):
                lang = "hi"
            elif any(w in q_lower for w in ["kya", "mera", "hoga", "kitna", "kar sakta", "saal", "mahine", "batao", "hai", "mujhe", "rupaye", "samjhao", "kaunsa"]):
                lang = "hinglish"
            else:
                lang = "en"

        # 2. Intent Classification
        if task_override and task_override not in ["auto", "financial_intelligence"]:
            intent = task_override
        else:
            if any(w in q_lower for w in ["what if", "simulate", "if i take", "if salary", "agar salary", "agar expense", "salary badh"]):
                intent = "what_if_simulation"
            elif any(w in q_lower for w in ["digital twin", "twin", "virtual state", "financial state"]):
                intent = "digital_twin"
            elif any(w in q_lower for w in ["anomaly", "anomalies", "duplicate", "suspicious", "spike", "unusual", "fraud"]):
                intent = "anomaly_explanation"
            elif any(w in q_lower for w in ["compare", "scenario", "option a", "which loan", "kaunsa loan", "versus", "vs"]):
                intent = "loan_scenario"
            elif any(w in q_lower for w in ["afford", "eligibility", "how much loan", "kitna loan", "max loan"]):
                intent = "affordability"
            elif any(w in q_lower for w in ["repayment", "schedule", "amortization", "breakdown", "emi", "monthly payment"]):
                intent = "repayment"
            elif any(w in q_lower for w in ["health", "score", "status", "dti", "foir"]):
                intent = "financial_health"
            else:
                intent = "financial_health"

        # 3. Extract Parameters
        extracted_params = self._extract_parameters(query, context)

        req_sources = ["financial_profile"]
        if intent in ["repayment", "loan_scenario", "affordability"]:
            req_sources.append("loan_calculator_engine")
        if intent in ["anomaly_explanation"]:
            req_sources.append("transaction_history")
        if intent in ["digital_twin", "what_if_simulation"]:
            req_sources.append("digital_twin_engine")

        return QueryUnderstanding(
            intent=intent,
            detected_language=lang,
            extracted_params=extracted_params,
            required_data_sources=req_sources,
        )

    def _extract_parameters(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        params: Dict[str, Any] = {}

        # 1. Parse Principal Amount
        # e.g., ₹5,00,000, 500000, 5L, 5 lakh, 50k, 50000
        principal = context.get("principal") or context.get("amount")
        if not principal:
            # Check 5L or 5 lakh
            lakh_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|l)\b", query, re.IGNORECASE)
            k_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:k|thousand)\b", query, re.IGNORECASE)
            num_match = re.search(r"₹?\s*([\d,]+(?:\.\d+)?)", query)

            if lakh_match:
                principal = float(lakh_match.group(1)) * 100000
            elif k_match:
                principal = float(k_match.group(1)) * 1000
            elif num_match:
                raw_num = num_match.group(1).replace(",", "")
                try:
                    val = float(raw_num)
                    if val > 100:  # avoid picking interest rate or tenure
                        principal = val
                except ValueError:
                    pass

        params["principal"] = Decimal(str(principal)) if principal else Decimal("500000.00")

        # 2. Parse Rate
        rate = context.get("annual_rate_pct") or context.get("rate")
        if not rate:
            rate_match = re.search(r"(\d+(?:\.\d+)?)\s*%", query)
            if rate_match:
                rate = float(rate_match.group(1))

        params["annual_rate_pct"] = Decimal(str(rate)) if rate else Decimal("12.50")

        # 3. Parse Tenure
        tenure = context.get("tenure_months") or context.get("tenure")
        if not tenure:
            yr_match = re.search(r"(\d+)\s*(?:years|year|yr|yrs|saal)\b", query, re.IGNORECASE)
            mo_match = re.search(r"(\d+)\s*(?:months|month|mo|mos|mahine)\b", query, re.IGNORECASE)
            if yr_match:
                tenure = int(yr_match.group(1)) * 12
            elif mo_match:
                tenure = int(mo_match.group(1))

        params["tenure_months"] = int(tenure) if tenure else 36

        # Parse income/expenses if in context or query
        params["income"] = Decimal(str(context.get("income", 100000.00)))
        params["expenses"] = Decimal(str(context.get("expenses", 40000.00)))
        params["savings"] = Decimal(str(context.get("savings", 200000.00)))
        params["existing_loans"] = Decimal(str(context.get("existing_loans", 10000.00)))
        params["health_score"] = int(context.get("health_score", 94))

        return params

    async def _fetch_authorized_data(self, user_id: Optional[int], context: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch authorized financial data via contract adapter."""
        dto: FinancialStateDTO = await financial_data_provider_adapter.get_financial_state(
            user_id=str(user_id) if user_id else None, db_session=self.db, context=context
        )
        return {
            "income": dto.income,
            "expenses": dto.expenses,
            "savings": dto.savings,
            "existing_loans": dto.existing_loans,
            "assets": dto.assets,
            "health_score": dto.health_score,
            "transactions": dto.transactions,
        }

    def _invoke_deterministic_calculations(
        self, intent: str, params: Dict[str, Any], context_data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        calc_results: Dict[str, Any] = {}
        digital_twin_state: Optional[Dict[str, Any]] = None
        what_if_result: Optional[Dict[str, Any]] = None

        principal = params["principal"]
        rate = params["annual_rate_pct"]
        tenure = params["tenure_months"]
        income = context_data["income"]
        expenses = context_data["expenses"]
        existing_debt = context_data["existing_loans"]
        savings = context_data["savings"]
        assets = context_data["assets"]
        health_score = context_data["health_score"]

        # Always construct Digital Twin State via adapter port
        digital_twin_state = financial_data_provider_adapter.get_digital_twin_state(
            savings=savings,
            monthly_income=income,
            monthly_expenses=expenses,
            existing_loans=existing_debt,
            assets=assets,
            health_score=health_score,
        )

        if intent in ["financial_health"]:
            calc_results["debt_burden"] = financial_data_provider_adapter.calculate_debt_burden(income, expenses, existing_debt)
            calc_results["cash_flow"] = financial_data_provider_adapter.calculate_cash_flow(income, expenses, existing_debt)
            calc_results["health_score"] = health_score

        elif intent in ["repayment"]:
            calc_results["emi_summary"] = financial_data_provider_adapter.calculate_emi(principal, rate, tenure)
            calc_results["schedule_data"] = financial_data_provider_adapter.calculate_repayment_schedule(principal, rate, tenure)

        elif intent in ["affordability"]:
            calc_results["affordability"] = financial_data_provider_adapter.calculate_affordability(
                monthly_income=income,
                monthly_expenses=expenses,
                existing_emis=existing_debt,
                proposed_annual_rate_pct=rate,
                tenure_months=tenure,
            )

        elif intent in ["loan_scenario"]:
            # Scenario A vs Scenario B
            scenarios = [
                {
                    "label": "Option A (Requested)",
                    "principal": float(principal),
                    "annual_rate_pct": float(rate),
                    "tenure_months": tenure,
                },
                {
                    "label": "Option B (Shorter Tenure 24m)",
                    "principal": float(principal),
                    "annual_rate_pct": float(rate),
                    "tenure_months": 24,
                },
                {
                    "label": "Option C (Lower Rate 10.5%)",
                    "principal": float(principal),
                    "annual_rate_pct": 10.5,
                    "tenure_months": tenure,
                },
            ]
            calc_results["loan_scenarios"] = financial_data_provider_adapter.analyze_loan_scenarios(scenarios)

        elif intent in ["anomaly_explanation"]:
            sample_txs = context_data["transactions"] or [
                {"id": "TX-101", "amount": 2500, "type": "income", "category": "Salary", "merchant": "Employer Inc"},
                {"id": "TX-102", "amount": 150, "type": "expense", "category": "Dining", "merchant": "Cafe Coffee Day"},
                {"id": "TX-103", "amount": 15000, "type": "expense", "category": "Electronics", "merchant": "Croma Tech"},
                {"id": "TX-104", "amount": 15000, "type": "expense", "category": "Electronics", "merchant": "Croma Tech"},  # Duplicate
            ]
            calc_results["anomalies"] = financial_data_provider_adapter.detect_financial_anomalies(sample_txs, baseline_avg_monthly_expense=expenses)

        elif intent in ["digital_twin"]:
            calc_results["twin_summary"] = digital_twin_state

        elif intent in ["what_if_simulation"]:
            what_if_result = financial_data_provider_adapter.run_what_if_simulation(
                twin_state=digital_twin_state,
                income_change_pct=Decimal("15.00"),
                expense_change_amount=Decimal("0.00"),
                new_loan_principal=principal,
                new_loan_rate_pct=rate,
                new_loan_tenure_months=tenure,
            )
            calc_results["what_if_summary"] = what_if_result

        return calc_results, digital_twin_state, what_if_result


    def _analyze_results(
        self, intent: str, calc_results: Dict[str, Any], context_data: Dict[str, Any]
    ) -> Tuple[str, str, float]:
        if intent == "affordability":
            aff = calc_results.get("affordability", {})
            if aff.get("is_affordable"):
                return "The proposed loan terms are fully within healthy debt limits.", "approve", 0.96
            else:
                return "The proposed loan exceeds recommended FOIR debt limits.", "review", 0.94

        elif intent == "anomaly_explanation":
            anom = calc_results.get("anomalies", {})
            if anom.get("anomalies_detected"):
                return f"Detected {anom['anomaly_count']} suspicious financial events.", "escalate", 0.95
            return "No suspicious transaction anomalies detected.", "approve", 0.98

        elif intent == "what_if_simulation":
            sim = calc_results.get("what_if_summary", {}).get("simulated", {})
            if sim.get("surplus_delta", Decimal("0")) >= Decimal("0"):
                return "Simulated scenario maintains positive cash flow and healthy trajectory.", "approve", 0.95
            return "Simulated scenario results in negative monthly cash flow.", "review", 0.92

        return "Financial analysis complete with deterministic mathematical backing.", "advise", 0.95

    def _explain_results(
        self,
        intent: str,
        language: str,
        calc_results: Dict[str, Any],
        digital_twin_state: Optional[Dict[str, Any]],
        what_if_result: Optional[Dict[str, Any]],
        context_data: Dict[str, Any],
        params: Dict[str, Any],
    ) -> str:
        score = context_data.get("health_score", 94)
        score_str = f"{score}/100"

        if intent == "repayment":
            summary = calc_results.get("emi_summary", {})
            p_formatted = format_inr(summary["principal"])
            emi_formatted = format_inr(summary["monthly_emi"])
            int_formatted = format_inr(summary["total_interest"])
            tot_formatted = format_inr(summary["total_payment"])
            rate_str = f"{summary['annual_rate_pct']}%"
            tenure_str = f"{summary['tenure_months']} months"

            if language == "hi":
                return (
                    f"आपके {p_formatted} ऋण पर {rate_str} की वार्षिक ब्याज दर से {tenure_str} के लिए exact मासिक EMI {emi_formatted} है। "
                    f"कुल ब्याज भुगतान {int_formatted} होगा और कुल देय राशि {tot_formatted} होगी।"
                )
            elif language == "hinglish":
                return (
                    f"Aapka monthly EMI {emi_formatted} hoga {p_formatted} loan par {rate_str} interest rate ke saath {tenure_str} ke liye. "
                    f"Isme total interest {int_formatted} aur total payment {tot_formatted} banega."
                )
            else:
                return (
                    f"For a loan principal of {p_formatted} at an annual interest rate of {rate_str} for a tenure of {tenure_str}, "
                    f"your exact monthly EMI is {emi_formatted}. The total interest payable is {int_formatted}, bringing the total repayment to {tot_formatted}."
                )

        elif intent == "financial_health":
            db = calc_results.get("debt_burden", {})
            cf = calc_results.get("cash_flow", {})
            inc_fmt = format_inr(context_data["income"])
            exp_fmt = format_inr(context_data["expenses"])
            surp_fmt = format_inr(cf.get("net_surplus", Decimal("0")))
            foir_str = f"{db.get('foir_pct', Decimal('0'))}%"

            if language == "hi":
                return (
                    f"आपका वित्तीय स्वास्थ्य स्कोर {score_str} (उत्कृष्ट) है। आपकी मासिक आय {inc_fmt} और मासिक खर्च {exp_fmt} है, "
                    f"जिससे आपकी नेट बचत {surp_fmt} और FOIR debt ratio {foir_str} है।"
                )
            elif language == "hinglish":
                return (
                    f"Aapka Financial Health score {score_str} hai. Aapki monthly income {inc_fmt} hai, expenses {exp_fmt} hain, "
                    f"aur monthly net surplus {surp_fmt} hai jisse aapka debt ratio (FOIR) {foir_str} rehta hai."
                )
            else:
                return (
                    f"Your overall Financial Health Score is {score_str}. With a monthly income of {inc_fmt} and expenses of {exp_fmt}, "
                    f"your monthly net cash flow surplus is {surp_fmt} and your Fixed Obligation to Income Ratio (FOIR) is {foir_str}."
                )

        elif intent == "affordability":
            aff = calc_results.get("affordability", {})
            max_emi_fmt = format_inr(aff.get("max_affordable_emi", Decimal("0")))
            max_loan_fmt = format_inr(aff.get("max_loan_amount", Decimal("0")))
            rate_str = f"{aff.get('proposed_annual_rate_pct', Decimal('12.5'))}%"
            tenure_str = f"{aff.get('tenure_months', 36)} months"
            max_foir_str = f"{aff.get('target_max_foir_pct', Decimal('50.0'))}%"

            if language == "hi":
                return (
                    f"50% FOIR सीमा के आधार पर, आप अधिकतम {max_emi_fmt} प्रति माह EMI वहन कर सकते हैं। "
                    f"{rate_str} ब्याज दर पर {tenure_str} के लिए आपकी अधिकतम ऋण क्षमता {max_loan_fmt} है।"
                )
            elif language == "hinglish":
                return (
                    f"{max_foir_str} FOIR limit ke base par, aap max {max_emi_fmt} monthly EMI afford kar sakte hain. "
                    f"{rate_str} rate par {tenure_str} ke liye aapki max loan capacity {max_loan_fmt} hai."
                )
            else:
                return (
                    f"Based on a target maximum FOIR threshold of {max_foir_str}, your maximum affordable monthly EMI is {max_emi_fmt}. "
                    f"At an interest rate of {rate_str} for {tenure_str}, your maximum affordable loan capacity is {max_loan_fmt}."
                )

        elif intent == "loan_scenario":
            sc = calc_results.get("loan_scenarios", {})
            options = sc.get("scenarios", [])
            opt_strs = []
            for o in options:
                opt_strs.append(f"{o['label']}: EMI {format_inr(o['monthly_emi'])}, Total Interest {format_inr(o['total_interest'])}")
            
            summary_opts = " | ".join(opt_strs)
            best_int = sc.get("lowest_interest_option")
            best_emi = sc.get("lowest_emi_option")

            if language == "hi":
                return (
                    f"ऋण विकल्पों का तुलनात्मक विश्लेषण: {summary_opts}। सबसे कम ब्याज लागत वाला विकल्प '{best_int}' है, "
                    f"और सबसे कम मासिक किस्त वाला विकल्प '{best_emi}' है।"
                )
            elif language == "hinglish":
                return (
                    f"Loan scenario comparison results: {summary_opts}. Sabse kam interest cost wala option '{best_int}' hai "
                    f"aur sabse kam monthly EMI option '{best_emi}' hai."
                )
            else:
                return (
                    f"Comparative Loan Analysis: {summary_opts}. Option with lowest total interest cost is '{best_int}', "
                    f"and lowest monthly EMI option is '{best_emi}'."
                )

        elif intent == "anomaly_explanation":
            an = calc_results.get("anomalies", {})
            count = an.get("anomaly_count", 0)
            items = an.get("anomalies", [])
            details = "; ".join([f"{i['merchant']} ({format_inr(i['amount'])}) - {i['reason']}" for i in items]) if items else "None"

            if language == "hi":
                return (
                    f"वित्तीय विसंगति रिपोर्ट: {count} विसंगतियां पाई गईं। विवरण: {details}।"
                )
            elif language == "hinglish":
                return (
                    f"Financial anomaly detection result: Total {count} anomalies payi gayin. Details: {details}."
                )
            else:
                return (
                    f"Financial Anomaly Explanation: Found {count} unusual transaction anomalies. Details: {details}."
                )

        elif intent == "digital_twin":
            dt = calc_results.get("twin_summary", {})
            net_fmt = format_inr(dt["net_worth"])
            surp_fmt = format_inr(dt["monthly_surplus"])
            proj_fmt = format_inr(dt["projected_savings_12m"])

            if language == "hi":
                return (
                    f"आपकी फाइनेंशियल डिजिटल ट्विन स्थिति: कुल संपत्ति (Net Worth) {net_fmt}, मासिक बचत {surp_fmt}, "
                    f"और 12 महीने में अनुमानित कुल बचत {proj_fmt} होगी। स्वास्थ्य स्कोर {score_str} है।"
                )
            elif language == "hinglish":
                return (
                    f"Aapki Financial Digital Twin state: Net Worth {net_fmt}, monthly net surplus {surp_fmt}, "
                    f"aur projected 12-month savings {proj_fmt} hai. Health Score {score_str} hai."
                )
            else:
                return (
                    f"Financial Digital Twin State: Current Net Worth is {net_fmt}, monthly cash flow surplus is {surp_fmt}, "
                    f"and projected 12-month cumulative savings is {proj_fmt}. Health score stands at {score_str}."
                )

        elif intent == "what_if_simulation":
            sim = what_if_result.get("simulated", {})
            new_surplus_fmt = format_inr(sim["monthly_surplus"])
            new_emi_fmt = format_inr(sim["new_loan_emi"])
            new_proj_fmt = format_inr(sim["projected_savings_12m"])
            new_score = sim["health_score"]

            if language == "hi":
                return (
                    f"व्हाट-इफ सिमुलेशन परिणाम: 15% आय वृद्धि और {new_emi_fmt} के नए ऋण EMI के साथ, "
                    f"आपकी नई मासिक बचत {new_surplus_fmt} होगी और 12 महीने में अनुमानित बचत {new_proj_fmt} होगी। "
                    f"अनुमानित स्वास्थ्य स्कोर {new_score}/100 होगा।"
                )
            elif language == "hinglish":
                return (
                    f"What-if simulation result: 15% salary hike aur {new_emi_fmt} naye EMI ke saath, "
                    f"aapki nayi monthly net surplus {new_surplus_fmt} hogi aur projected 12-month savings {new_proj_fmt} hogi. "
                    f"Projected Health Score {new_score}/100 hoga."
                )
            else:
                return (
                    f"What-If Simulation Results: Assuming a 15% income increase and adding a new monthly EMI of {new_emi_fmt}, "
                    f"your new monthly surplus will be {new_surplus_fmt}, projected 12-month savings will reach {new_proj_fmt}, "
                    f"and your adjusted health score will be {new_score}/100."
                )

        return f"Financial intelligence analysis completed for {intent}."

    def _provide_evidence(
        self,
        intent: str,
        calc_results: Dict[str, Any],
        digital_twin_state: Optional[Dict[str, Any]],
        what_if_result: Optional[Dict[str, Any]],
    ) -> List[str]:
        evidence = []
        evidence.append("[Engine] Backend Deterministic Calculation Engine: FinancialEngine v1.0")

        if intent == "repayment":
            summary = calc_results.get("emi_summary", {})
            evidence.append("[Formula] EMI = P * r * (1+r)^n / ((1+r)^n - 1)")
            evidence.append(f"[Input] Principal: {format_inr(summary['principal'])}, Rate: {summary['annual_rate_pct']}%, Tenure: {summary['tenure_months']} months")
            evidence.append(f"[Exact Calculation Output] Monthly EMI: {format_inr(summary['monthly_emi'])}, Total Interest: {format_inr(summary['total_interest'])}, Total Payment: {format_inr(summary['total_payment'])}")

        elif intent == "financial_health":
            db = calc_results.get("debt_burden", {})
            cf = calc_results.get("cash_flow", {})
            evidence.append("[Formula] FOIR = ((Monthly Expenses + Existing EMIs) / Monthly Income) * 100")
            evidence.append(f"[Exact Output] Monthly Income: {format_inr(cf['monthly_income'])}, Expenses: {format_inr(cf['monthly_expenses'])}, Surplus: {format_inr(cf['net_surplus'])}")
            evidence.append(f"[Exact Output] FOIR: {db['foir_pct']}%, DTI: {db['dti_ratio_pct']}%, Risk Category: {db['risk_category']}")

        elif intent == "affordability":
            aff = calc_results.get("affordability", {})
            evidence.append("[Formula] Max EMI = (Monthly Income * Target FOIR %) - Current Obligations")
            evidence.append(f"[Exact Output] Target Max FOIR: {aff['target_max_foir_pct']}%, Max Affordable EMI: {format_inr(aff['max_affordable_emi'])}, Max Affordable Loan: {format_inr(aff['max_loan_amount'])}")

        elif intent == "loan_scenario":
            sc = calc_results.get("loan_scenarios", {})
            for s in sc.get("scenarios", []):
                evidence.append(f"[Scenario] {s['label']}: Principal {format_inr(s['principal'])}, Rate {s['annual_rate_pct']}%, EMI {format_inr(s['monthly_emi'])}, Total Interest {format_inr(s['total_interest'])}")

        elif intent == "anomaly_explanation":
            an = calc_results.get("anomalies", {})
            evidence.append(f"[Rule] Anomalies Detected: {an['anomaly_count']}")
            for item in an.get("anomalies", []):
                evidence.append(f"[Anomaly Flag] Tx {item['tx_id']} - {item['merchant']} ({format_inr(item['amount'])}): {item['reason']}")

        elif intent == "digital_twin":
            evidence.append(f"[Digital Twin Model] Net Worth: {format_inr(digital_twin_state['net_worth'])}, Monthly Surplus: {format_inr(digital_twin_state['monthly_surplus'])}, Projected 12m Savings: {format_inr(digital_twin_state['projected_savings_12m'])}")

        elif intent == "what_if_simulation":
            sim = what_if_result.get("simulated", {})
            evidence.append(f"[Simulation Output] New Monthly Surplus: {format_inr(sim['monthly_surplus'])}, New Loan EMI: {format_inr(sim['new_loan_emi'])}, Projected 12m Savings: {format_inr(sim['projected_savings_12m'])}, Projected Score: {sim['health_score']}")

        return evidence
