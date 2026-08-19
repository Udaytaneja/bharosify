from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import require_role
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.banking import CustomerResponse, LoanApplicationResponse
from backend.app.services.banking_service import (
    get_banker_customer_by_id,
    list_banker_customers,
    list_loan_applications,
)

router = APIRouter(prefix="/bankers", tags=["Bankers"])


@router.get("/customers", response_model=list[CustomerResponse])
async def get_customers(
    current_user: User = Depends(require_role("banker")),
    db: AsyncSession = Depends(get_db),
):
    """Get all customers available to the banker."""
    return await list_banker_customers(db=db)


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    current_user: User = Depends(require_role("banker")),
    db: AsyncSession = Depends(get_db),
):
    """Get detailed customer profile for a given customer_id."""
    customer = await get_banker_customer_by_id(db=db, customer_id=customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_44_NOT_FOUND if hasattr(status, "HTTP_404_NOT_FOUND") else 404,
            detail="Customer not found",
        )
    return customer


@router.get("/applications", response_model=list[LoanApplicationResponse])
async def get_all_applications(
    current_user: User = Depends(require_role("banker")),
    db: AsyncSession = Depends(get_db),
):
    """Get all loan applications across customers for banker review."""
    return await list_loan_applications(db=db, current_user=current_user)
