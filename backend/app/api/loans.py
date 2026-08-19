from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.banking import LoanResponse
from backend.app.services.banking_service import get_loan_by_id, list_user_loans

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get("", response_model=list[LoanResponse])
async def get_loans(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get active loans for current user or all loans for a banker."""
    return await list_user_loans(db=db, current_user=current_user)


@router.get("/{loan_id}", response_model=LoanResponse)
async def get_loan(
    loan_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get loan details by ID."""
    loan = await get_loan_by_id(db=db, loan_id=loan_id, current_user=current_user)
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found or unauthorized",
        )
    return loan
