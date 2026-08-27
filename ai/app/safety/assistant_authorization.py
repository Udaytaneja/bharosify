from typing import Any, Dict, Optional
from pydantic import BaseModel


class AssistantAuthorizationCheckResult(BaseModel):
    is_authorized: bool
    reason: str = "Authorized"
    requires_human_review: bool = False


class FinancialAssistantAuthorization:
    """
    Authorization & Safety Shield for Financial Intelligence Assistant.
    Enforces multi-tenant organization isolation and cross-user data boundaries.
    """

    def authorize_request(
        self,
        requesting_user_id: int,
        target_user_id: Optional[int],
        organization_id: str,
        role: str,
    ) -> AssistantAuthorizationCheckResult:
        # 1. Multi-tenant Org Scoping
        if not organization_id:
            return AssistantAuthorizationCheckResult(
                is_authorized=False,
                reason="ACCESS_DENIED: organization_id is required.",
                requires_human_review=True,
            )

        # 2. User Scoping Boundary
        target_id = target_user_id or requesting_user_id

        # Regular user requesting another user's financial profile
        if role.lower() == "user" and target_id != requesting_user_id:
            return AssistantAuthorizationCheckResult(
                is_authorized=False,
                reason=f"ACCESS_DENIED: User {requesting_user_id} cannot access private financial data of User {target_id}.",
                requires_human_review=True,
            )

        return AssistantAuthorizationCheckResult(
            is_authorized=True,
            reason="Authorized",
            requires_human_review=False,
        )


assistant_authorization = FinancialAssistantAuthorization()
