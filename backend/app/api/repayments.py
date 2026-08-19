from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.banking import RepaymentResponse
from backend.app.services.banking_service import get_repayments_for_loan, list_repayments

router = APIRouter(prefix="/repayments", tags=["Repayments"])


@router.get("", response_model=list[RepaymentResponse])
async def get_repayments(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get repayment information for current user or all repayments for a banker."""
    return await list_repayments(db=db, current_user=current_user)


@router.get("/{loan_id}", response_model=list[RepaymentResponse])
async def get_loan_repayments(
    loan_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get repayment schedule for a specific loan."""
    repayments = await get_repayments_for_loan(db=db, loan_id=loan_id, current_user=current_user)
    if not repayments:
        # Check if loan exists or user unauthorized
        from backend.app.services.banking_service import get_loan_by_id

        loan = await get_loan_by_id(db=db, loan_id=loan_id, current_user=current_user)
        if loan is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found or unauthorized",
            )
    return repayments
