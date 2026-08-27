from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional


def round_curr(val: Decimal) -> Decimal:
    """Round currency decimal to 2 decimal places using HALF_UP."""
    return val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class FinancialEngine:
    """
    Authoritative, deterministic backend financial calculation engine.
    Uses pure python arithmetic and Decimal precision to ensure zero LLM calculation errors.
    """

    @staticmethod
    def calculate_emi(principal: Decimal, annual_rate_pct: Decimal, tenure_months: int) -> Dict[str, Any]:
        """
        Calculates exact Equated Monthly Installment (EMI) and repayment summary.
        Formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1)
        """
        if principal <= Decimal("0"):
            raise ValueError("Principal must be greater than zero")
        if tenure_months <= 0:
            raise ValueError("Tenure months must be greater than zero")

        if annual_rate_pct <= Decimal("0"):
            monthly_emi = round_curr(principal / Decimal(str(tenure_months)))
            total_payment = principal
            total_interest = Decimal("0.00")
        else:
            monthly_rate = (annual_rate_pct / Decimal("100")) / Decimal("12")
            # Calculate (1 + r)^n using float precision, then convert back to Decimal
            r_flt = float(monthly_rate)
            factor = Decimal(str((1 + r_flt) ** tenure_months))
            
            numerator = principal * monthly_rate * factor
            denominator = factor - Decimal("1")
            
            monthly_emi = round_curr(numerator / denominator)
            total_payment = round_curr(monthly_emi * Decimal(str(tenure_months)))
            total_interest = round_curr(total_payment - principal)

        interest_ratio = (
            round_curr((total_interest / principal) * Decimal("100"))
            if principal > Decimal("0")
            else Decimal("0.00")
        )

        return {
            "principal": round_curr(principal),
            "annual_rate_pct": annual_rate_pct,
            "tenure_months": tenure_months,
            "monthly_emi": monthly_emi,
            "total_interest": total_interest,
            "total_payment": total_payment,
            "interest_ratio_pct": interest_ratio,
        }

    @staticmethod
    def calculate_repayment_schedule(
        principal: Decimal, annual_rate_pct: Decimal, tenure_months: int
    ) -> Dict[str, Any]:
        """
        Generates full amortization repayment schedule month-by-month.
        """
        summary = FinancialEngine.calculate_emi(principal, annual_rate_pct, tenure_months)
        monthly_emi = summary["monthly_emi"]
        monthly_rate = (annual_rate_pct / Decimal("100")) / Decimal("12")

        remaining_balance = principal
        schedule: List[Dict[str, Any]] = []

        for month in range(1, tenure_months + 1):
            interest_payment = round_curr(remaining_balance * monthly_rate)
            if month == tenure_months:
                principal_payment = remaining_balance
                emi_actual = principal_payment + interest_payment
            else:
                principal_payment = monthly_emi - interest_payment
                emi_actual = monthly_emi

            remaining_balance = max(Decimal("0.00"), round_curr(remaining_balance - principal_payment))

            schedule.append({
                "month": month,
                "emi": emi_actual,
                "principal_payment": principal_payment,
                "interest_payment": interest_payment,
                "remaining_balance": remaining_balance,
            })

        return {
            "summary": summary,
            "schedule": schedule,
        }

    @staticmethod
    def calculate_debt_burden(
        monthly_income: Decimal,
        monthly_expenses: Decimal,
        existing_emis: Decimal = Decimal("0.00"),
    ) -> Dict[str, Any]:
        """
        Calculates Debt-to-Income (DTI), FOIR (Fixed Obligation to Income Ratio), and risk assessment.
        """
        if monthly_income <= Decimal("0"):
            return {
                "monthly_income": Decimal("0.00"),
                "monthly_expenses": round_curr(monthly_expenses),
                "existing_emis": round_curr(existing_emis),
                "dti_ratio_pct": Decimal("100.00"),
                "foir_pct": Decimal("100.00"),
                "risk_category": "Critical",
                "disposable_income": Decimal("0.00"),
            }

        dti = round_curr((existing_emis / monthly_income) * Decimal("100.00"))
        total_obligations = monthly_expenses + existing_emis
        foir = round_curr((total_obligations / monthly_income) * Decimal("100.00"))
        disposable_income = round_curr(monthly_income - total_obligations)

        if foir <= Decimal("35.00"):
            risk = "Low"
        elif foir <= Decimal("50.00"):
            risk = "Moderate"
        elif foir <= Decimal("65.00"):
            risk = "High"
        else:
            risk = "Critical"

        return {
            "monthly_income": round_curr(monthly_income),
            "monthly_expenses": round_curr(monthly_expenses),
            "existing_emis": round_curr(existing_emis),
            "total_obligations": round_curr(total_obligations),
            "dti_ratio_pct": dti,
            "foir_pct": foir,
            "risk_category": risk,
            "disposable_income": disposable_income,
        }

    @staticmethod
    def calculate_cash_flow(
        monthly_income: Decimal, monthly_expenses: Decimal, recurring_debt: Decimal = Decimal("0.00")
    ) -> Dict[str, Any]:
        """
        Calculates net monthly cash flow and savings rate.
        """
        total_outflow = round_curr(monthly_expenses + recurring_debt)
        net_surplus = round_curr(monthly_income - total_outflow)
        
        savings_rate = (
            round_curr((net_surplus / monthly_income) * Decimal("100.00"))
            if monthly_income > Decimal("0")
            else Decimal("0.00")
        )

        return {
            "monthly_income": round_curr(monthly_income),
            "monthly_expenses": round_curr(monthly_expenses),
            "recurring_debt": round_curr(recurring_debt),
            "total_outflow": total_outflow,
            "net_surplus": net_surplus,
            "savings_rate_pct": savings_rate,
            "is_cash_flow_positive": net_surplus > Decimal("0.00"),
        }

    @staticmethod
    def calculate_affordability(
        monthly_income: Decimal,
        monthly_expenses: Decimal,
        existing_emis: Decimal,
        proposed_annual_rate_pct: Decimal,
        tenure_months: int,
        target_max_foir_pct: Decimal = Decimal("50.00"),
    ) -> Dict[str, Any]:
        """
        Determines maximum affordable EMI and maximum supportable loan amount.
        """
        current_obligations = monthly_expenses + existing_emis
        max_allowed_obligations = round_curr(monthly_income * (target_max_foir_pct / Decimal("100.00")))
        max_affordable_emi = round_curr(max(Decimal("0.00"), max_allowed_obligations - current_obligations))

        if max_affordable_emi <= Decimal("0.00") or tenure_months <= 0:
            max_loan_amount = Decimal("0.00")
        else:
            if proposed_annual_rate_pct <= Decimal("0"):
                max_loan_amount = round_curr(max_affordable_emi * Decimal(str(tenure_months)))
            else:
                monthly_rate = (proposed_annual_rate_pct / Decimal("100")) / Decimal("12")
                r_flt = float(monthly_rate)
                factor = Decimal(str((1 + r_flt) ** tenure_months))
                # Formula: P = EMI * ((1+r)^n - 1) / (r * (1+r)^n)
                numerator = factor - Decimal("1")
                denominator = monthly_rate * factor
                max_loan_amount = round_curr(max_affordable_emi * (numerator / denominator))

        debt_burden_status = FinancialEngine.calculate_debt_burden(monthly_income, monthly_expenses, existing_emis)

        return {
            "monthly_income": round_curr(monthly_income),
            "monthly_expenses": round_curr(monthly_expenses),
            "existing_emis": round_curr(existing_emis),
            "target_max_foir_pct": target_max_foir_pct,
            "max_affordable_emi": max_affordable_emi,
            "max_loan_amount": max_loan_amount,
            "proposed_annual_rate_pct": proposed_annual_rate_pct,
            "tenure_months": tenure_months,
            "current_foir_pct": debt_burden_status["foir_pct"],
            "is_affordable": max_affordable_emi > Decimal("0.00"),
        }

    @staticmethod
    def analyze_loan_scenarios(
        scenarios: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compares multiple loan scenarios (principals, rates, tenures, down payments).
        """
        results = []
        for idx, sc in enumerate(scenarios, start=1):
            principal = Decimal(str(sc["principal"]))
            rate = Decimal(str(sc["annual_rate_pct"]))
            tenure = int(sc["tenure_months"])
            down_payment = Decimal(str(sc.get("down_payment", 0)))
            label = sc.get("label", f"Option {idx}")

            calc = FinancialEngine.calculate_emi(principal, rate, tenure)
            total_outlay = round_curr(calc["total_payment"] + down_payment)

            results.append({
                "label": label,
                "principal": round_curr(principal),
                "down_payment": round_curr(down_payment),
                "annual_rate_pct": rate,
                "tenure_months": tenure,
                "monthly_emi": calc["monthly_emi"],
                "total_interest": calc["total_interest"],
                "total_payment": calc["total_payment"],
                "total_outlay": total_outlay,
            })

        # Rank by lowest total interest
        sorted_by_interest = sorted(results, key=lambda x: x["total_interest"])
        # Rank by lowest monthly EMI
        sorted_by_emi = sorted(results, key=lambda x: x["monthly_emi"])

        return {
            "scenarios": results,
            "lowest_interest_option": sorted_by_interest[0]["label"] if sorted_by_interest else None,
            "lowest_emi_option": sorted_by_emi[0]["label"] if sorted_by_emi else None,
        }

    @staticmethod
    def detect_financial_anomalies(
        transactions: List[Dict[str, Any]],
        baseline_avg_monthly_expense: Optional[Decimal] = None
    ) -> Dict[str, Any]:
        """
        Detects financial anomalies deterministically (unusual spikes, large transactions, duplicate charges).
        """
        anomalies = []
        category_totals: Dict[str, Decimal] = {}
        seen_txs: Dict[str, Dict[str, Any]] = {}

        if not transactions:
            return {"anomalies_detected": False, "anomaly_count": 0, "anomalies": []}

        amounts = [Decimal(str(t.get("amount", 0))) for t in transactions if t.get("type") != "income"]
        if baseline_avg_monthly_expense and baseline_avg_monthly_expense > Decimal("0"):
            avg_amount = baseline_avg_monthly_expense
        elif amounts:
            # Use median or sorted low-end average to avoid outlier distortion
            sorted_amounts = sorted(amounts)
            mid = len(sorted_amounts) // 2
            avg_amount = sorted_amounts[mid]
        else:
            avg_amount = Decimal("0.00")

        threshold_large = avg_amount * Decimal("3.0") if avg_amount > Decimal("0") else Decimal("10000.00")

        for tx in transactions:
            tx_id = str(tx.get("id", ""))
            amount = round_curr(Decimal(str(tx.get("amount", 0))))
            category = tx.get("category", "General")
            merchant = tx.get("merchant", "Unknown")
            tx_type = tx.get("type", "expense")

            category_totals[category] = category_totals.get(category, Decimal("0.00")) + amount

            # Check duplicate (same merchant + same amount + expense)
            dup_key = f"{merchant}:{amount}"
            if dup_key in seen_txs:
                anomalies.append({
                    "tx_id": tx_id,
                    "type": "duplicate_charge",
                    "severity": "high",
                    "merchant": merchant,
                    "amount": amount,
                    "category": category,
                    "reason": f"Potential duplicate transaction matching transaction {seen_txs[dup_key]['tx_id']}.",
                })
            else:
                seen_txs[dup_key] = {"tx_id": tx_id, "amount": amount}

            # Check large single transaction spike
            if tx_type != "income" and amount >= threshold_large and amount > Decimal("5000.00"):
                anomalies.append({
                    "tx_id": tx_id,
                    "type": "unusual_spending_spike",
                    "severity": "medium",
                    "merchant": merchant,
                    "amount": amount,
                    "category": category,
                    "reason": f"Transaction amount ₹{amount:,.2f} is significantly higher than average expense ₹{avg_amount:,.2f}.",
                })

        return {
            "anomalies_detected": len(anomalies) > 0,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "category_totals": {k: round_curr(v) for k, v in category_totals.items()},
        }

    @staticmethod
    def get_digital_twin_state(
        savings: Decimal,
        monthly_income: Decimal,
        monthly_expenses: Decimal,
        existing_loans: Decimal,
        assets: Decimal = Decimal("0.00"),
        health_score: int = 750,
    ) -> Dict[str, Any]:
        """
        Constructs the state for the user's Financial Digital Twin.
        """
        cash_flow = FinancialEngine.calculate_cash_flow(monthly_income, monthly_expenses, existing_loans)
        debt_burden = FinancialEngine.calculate_debt_burden(monthly_income, monthly_expenses, existing_loans)

        net_worth = round_curr(savings + assets - existing_loans)

        # Baseline 12-month projection
        runway_months = (
            round_curr(savings / monthly_expenses)
            if monthly_expenses > Decimal("0")
            else Decimal("999.00")
        )

        projected_savings_12m = round_curr(savings + (cash_flow["net_surplus"] * Decimal("12")))

        return {
            "digital_twin_id": "DT-USER-CURRENT",
            "health_score": health_score,
            "savings": round_curr(savings),
            "assets": round_curr(assets),
            "existing_debt": round_curr(existing_loans),
            "net_worth": net_worth,
            "monthly_income": round_curr(monthly_income),
            "monthly_expenses": round_curr(monthly_expenses),
            "monthly_surplus": cash_flow["net_surplus"],
            "savings_rate_pct": cash_flow["savings_rate_pct"],
            "foir_pct": debt_burden["foir_pct"],
            "emergency_runway_months": runway_months,
            "projected_savings_12m": projected_savings_12m,
        }

    @staticmethod
    def run_what_if_simulation(
        twin_state: Dict[str, Any],
        income_change_pct: Decimal = Decimal("0.00"),
        expense_change_amount: Decimal = Decimal("0.00"),
        new_loan_principal: Decimal = Decimal("0.00"),
        new_loan_rate_pct: Decimal = Decimal("0.00"),
        new_loan_tenure_months: int = 0,
    ) -> Dict[str, Any]:
        """
        Simulates what-if financial changes on top of a Digital Twin state deterministically.
        """
        base_income = Decimal(str(twin_state["monthly_income"]))
        base_expenses = Decimal(str(twin_state["monthly_expenses"]))
        base_debt = Decimal(str(twin_state["existing_debt"]))
        base_savings = Decimal(str(twin_state["savings"]))
        base_score = int(twin_state.get("health_score", 750))

        # Adjust income
        sim_income = round_curr(base_income * (Decimal("1.00") + (income_change_pct / Decimal("100"))))
        # Adjust expenses
        sim_expenses = round_curr(max(Decimal("0.00"), base_expenses + expense_change_amount))

        # Calculate new loan EMI if requested
        new_emi = Decimal("0.00")
        if new_loan_principal > Decimal("0") and new_loan_tenure_months > 0:
            emi_calc = FinancialEngine.calculate_emi(new_loan_principal, new_loan_rate_pct, new_loan_tenure_months)
            new_emi = emi_calc["monthly_emi"]

        sim_total_debt = round_curr(base_debt + new_loan_principal)
        sim_recurring_debt = new_emi  # Additional recurring loan debt

        # New Cash Flow & Debt Burden
        sim_cash_flow = FinancialEngine.calculate_cash_flow(sim_income, sim_expenses, sim_recurring_debt)
        sim_debt_burden = FinancialEngine.calculate_debt_burden(sim_income, sim_expenses, sim_recurring_debt)

        # 12 Month Projected Savings
        sim_projected_savings_12m = round_curr(base_savings + (sim_cash_flow["net_surplus"] * Decimal("12")))

        # Impact on Health Score (Deterministic formula)
        # Baseline score adjusted by FOIR change and surplus change
        foir_diff = float(sim_debt_burden["foir_pct"] - Decimal(str(twin_state["foir_pct"])))
        score_delta = int(-foir_diff * 1.5)
        if sim_cash_flow["net_surplus"] < Decimal("0"):
            score_delta -= 30
        elif sim_cash_flow["net_surplus"] > Decimal(str(twin_state["monthly_surplus"])):
            score_delta += 15

        sim_health_score = max(300, min(900, base_score + score_delta))

        return {
            "simulation_parameters": {
                "income_change_pct": income_change_pct,
                "expense_change_amount": expense_change_amount,
                "new_loan_principal": new_loan_principal,
                "new_loan_rate_pct": new_loan_rate_pct,
                "new_loan_tenure_months": new_loan_tenure_months,
            },
            "baseline": {
                "monthly_income": base_income,
                "monthly_expenses": base_expenses,
                "monthly_surplus": twin_state["monthly_surplus"],
                "foir_pct": twin_state["foir_pct"],
                "health_score": base_score,
                "projected_savings_12m": twin_state["projected_savings_12m"],
            },
            "simulated": {
                "monthly_income": sim_income,
                "monthly_expenses": sim_expenses,
                "new_loan_emi": new_emi,
                "total_debt": sim_total_debt,
                "monthly_surplus": sim_cash_flow["net_surplus"],
                "savings_rate_pct": sim_cash_flow["savings_rate_pct"],
                "foir_pct": sim_debt_burden["foir_pct"],
                "risk_category": sim_debt_burden["risk_category"],
                "health_score": sim_health_score,
                "projected_savings_12m": sim_projected_savings_12m,
                "surplus_delta": round_curr(sim_cash_flow["net_surplus"] - Decimal(str(twin_state["monthly_surplus"]))),
            },
        }
