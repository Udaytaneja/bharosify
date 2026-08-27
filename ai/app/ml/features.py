from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RiskFeatureVector(BaseModel):
    """Strongly typed feature schema for credit risk model inference."""

    income: float = Field(ge=0.0)
    expenses: float = Field(ge=0.0)
    debt: float = Field(ge=0.0)
    savings: float = Field(ge=0.0)
    requested_amount: float = Field(ge=0.0)
    dti_ratio: float = Field(ge=0.0)
    savings_to_debt_ratio: float = Field(ge=0.0)
    loan_to_income_ratio: float = Field(ge=0.0)
    account_age_months: float = Field(ge=0.0)
    past_delinquencies: float = Field(ge=0.0)
    feature_schema_version: str = "risk_v1.0.0"

    def to_numpy(self) -> List[float]:

        return [
            self.income,
            self.expenses,
            self.debt,
            self.savings,
            self.requested_amount,
            self.dti_ratio,
            self.savings_to_debt_ratio,
            self.loan_to_income_ratio,
            self.account_age_months,
            self.past_delinquencies,
        ]


class FraudFeatureVector(BaseModel):
    """Strongly typed feature schema for fraud pattern model inference."""

    amount: float = Field(ge=0.0)
    failed_login_count: float = Field(ge=0.0)
    tx_velocity_10m: float = Field(ge=0.0)
    device_switch_flag: float = Field(ge=0.0, le=1.0)
    unusual_ip_flag: float = Field(ge=0.0, le=1.0)
    feature_schema_version: str = "fraud_v1.0.0"

    def to_numpy(self) -> List[float]:
        return [
            self.amount,
            self.failed_login_count,
            self.tx_velocity_10m,
            self.device_switch_flag,
            self.unusual_ip_flag,
        ]


class TransactionAnomalyFeatureVector(BaseModel):
    """Strongly typed feature schema for transaction anomaly model inference."""

    amount: float = Field(ge=0.0)
    avg_amount: float = Field(ge=0.0)
    amount_z_score: float
    tx_count_last_10m: float = Field(ge=0.0)
    velocity_ratio: float = Field(ge=0.0)
    feature_schema_version: str = "tx_anomaly_v1.0.0"

    def to_numpy(self) -> List[float]:
        return [
            self.amount,
            self.avg_amount,
            self.amount_z_score,
            self.tx_count_last_10m,
            self.velocity_ratio,
        ]


class BehaviourAnomalyFeatureVector(BaseModel):
    """Strongly typed feature schema for behavioral anomaly model inference."""

    session_duration_sec: float = Field(ge=0.0)
    navigation_depth: float = Field(ge=0.0)
    device_switch_flag: float = Field(ge=0.0, le=1.0)
    unusual_access_flag: float = Field(ge=0.0, le=1.0)
    feature_schema_version: str = "beh_anomaly_v1.0.0"

    def to_numpy(self) -> List[float]:
        return [
            self.session_duration_sec,
            self.navigation_depth,
            self.device_switch_flag,
            self.unusual_access_flag,
        ]


class FeaturePreprocessor:
    """Feature Extractor, Schema Validator, and Vector Normalizer for Financial ML Models."""

    def extract_risk_features(self, data: Dict[str, Any]) -> RiskFeatureVector:
        """Extracts and validates typed feature vector for credit risk modeling."""
        income = float(data.get("income", 50000.0))
        expenses = float(data.get("expenses", 20000.0))
        debt = float(data.get("debt", 10000.0))
        savings = float(data.get("savings", 15000.0))
        requested_amount = float(data.get("requested_amount", 20000.0))
        account_age_months = float(data.get("account_age_months", 12.0))
        past_delinquencies = float(data.get("past_delinquencies", 0.0))

        dti_ratio = (debt + expenses) / max(income, 1.0)
        savings_to_debt_ratio = savings / max(debt, 1.0)
        loan_to_income_ratio = requested_amount / max(income, 1.0)

        return RiskFeatureVector(
            income=income,
            expenses=expenses,
            debt=debt,
            savings=savings,
            requested_amount=requested_amount,
            dti_ratio=round(dti_ratio, 4),
            savings_to_debt_ratio=round(savings_to_debt_ratio, 4),
            loan_to_income_ratio=round(loan_to_income_ratio, 4),
            account_age_months=account_age_months,
            past_delinquencies=past_delinquencies,
            feature_schema_version="risk_v1.0.0",
        )

    def extract_fraud_features(self, data: Dict[str, Any]) -> FraudFeatureVector:
        """Extracts and validates typed feature vector for fraud classification."""
        failed_logins = float(data.get("failed_login_count", data.get("failed_login_attempts", 0.0)))
        tx_velocity = float(data.get("tx_velocity_10m", data.get("tx_velocity_spike_ratio", 1.0)))
        dev_switch = 1.0 if (data.get("device_switch_flag") or data.get("device_id_changed")) else 0.0
        ip_unusual = 1.0 if (data.get("unusual_ip_flag") or data.get("unusual_ip_detected")) else 0.0

        return FraudFeatureVector(
            amount=float(data.get("amount", 0.0)),
            failed_login_count=failed_logins,
            tx_velocity_10m=tx_velocity,
            device_switch_flag=dev_switch,
            unusual_ip_flag=ip_unusual,
            feature_schema_version="fraud_v1.0.0",
        )


    def extract_transaction_features(self, tx: Dict[str, Any], baseline: Dict[str, Any]) -> TransactionAnomalyFeatureVector:
        """Extracts and validates typed transaction anomaly features."""
        amount = float(tx.get("amount", 0.0))
        avg_amount = float(baseline.get("average_transaction_amount", 50.0))
        std_amount = float(baseline.get("std_transaction_amount", 20.0))
        tx_count_last_10m = float(tx.get("tx_count_last_10m", 1.0))

        z_score = (amount - avg_amount) / max(std_amount, 1.0)
        velocity_ratio = tx_count_last_10m / 2.0  # normalized baseline

        return TransactionAnomalyFeatureVector(
            amount=amount,
            avg_amount=avg_amount,
            amount_z_score=round(z_score, 2),
            tx_count_last_10m=tx_count_last_10m,
            velocity_ratio=round(velocity_ratio, 2),
            feature_schema_version="tx_anomaly_v1.0.0",
        )

    def extract_behaviour_features(
        self, session_features: Dict[str, Any], user_baseline: Dict[str, Any]
    ) -> BehaviourAnomalyFeatureVector:
        """Extracts and validates typed behavioral anomaly features."""
        return BehaviourAnomalyFeatureVector(
            session_duration_sec=float(session_features.get("session_duration_sec", 120.0)),
            navigation_depth=float(session_features.get("navigation_depth", 5.0)),
            device_switch_flag=1.0 if session_features.get("device_switch_flag") else 0.0,
            unusual_access_flag=1.0 if session_features.get("unusual_access_flag") else 0.0,
            feature_schema_version="beh_anomaly_v1.0.0",
        )


feature_preprocessor = FeaturePreprocessor()
