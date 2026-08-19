from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.banking import (
    LoanApplicationCreate,
    LoanApplicationResponse,
    LoanApplicationUpdate,
)
from backend.app.services.banking_service import (
    create_loan_application,
    get_loan_application_by_id,
    list_loan_applications,
    update_loan_application,
)

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("", response_model=LoanApplicationResponse, status_code=status.HTTP_201_CREATED)
async def submit_application(
    payload: LoanApplicationCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new loan application for current user."""
    return await create_loan_application(db=db, customer_id=current_user.id, payload=payload)


@router.get("", response_model=list[LoanApplicationResponse])
async def get_applications(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get loan applications for the authenticated user or all applications for a banker."""
    return await list_loan_applications(db=db, current_user=current_user)


@router.get("/{application_id}", response_model=LoanApplicationResponse)
async def get_application(
    application_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get application details by ID."""
    app = await get_loan_application_by_id(db=db, application_id=application_id, current_user=current_user)
    if app is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found or unauthorized",
        )
    return app


@router.put("/{application_id}", response_model=LoanApplicationResponse)
async def update_application(
    application_id: int,
    payload: LoanApplicationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update application details or transition status."""
    try:
        updated = await update_loan_application(
            db=db, application_id=application_id, payload=payload, current_user=current_user
        )
        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found or unauthorized",
            )
        return updated
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
