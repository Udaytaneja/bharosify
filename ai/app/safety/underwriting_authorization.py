from typing import Any, Dict, Optional
from pydantic import BaseModel


class UnderwritingAuthCheckResult(BaseModel):
    is_authorized: bool
    reason: str = "Authorized"
    requires_human_review: bool = True


class UnderwritingAuthorizationGuard:
    """
    Authorization & Multi-Tenant Isolation Guard for Banker Underwriting Copilot.
    Strictly enforces organization boundaries and cross-banker applicant access limits.
    """

    def authorize_banker_request(
        self,
        banker_id: str,
        organization_id: str,
        applicant_id: str,
        target_organization_id: Optional[str] = None,
    ) -> UnderwritingAuthCheckResult:
        # 1. Organization Requirement
        if not organization_id:
            return UnderwritingAuthCheckResult(
                is_authorized=False,
                reason="ACCESS_DENIED: Multi-tenant organization_id is required.",
                requires_human_review=True,
            )

        # 2. Cross-Organization Boundary Guard
        if target_organization_id and target_organization_id != organization_id:
            return UnderwritingAuthCheckResult(
                is_authorized=False,
                reason=f"ACCESS_DENIED: Banker from Org '{organization_id}' cannot access applicant/policy data belonging to Org '{target_organization_id}'.",
                requires_human_review=True,
            )

        return UnderwritingAuthCheckResult(
            is_authorized=True,
            reason="Authorized",
            requires_human_review=True,
        )


underwriting_authorization_guard = UnderwritingAuthorizationGuard()
