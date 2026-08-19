from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.financial import (
    FinancialHealthResponse,
    FinancialProfileResponse,
    FinancialProfileUpdate,
    TransactionCreate,
    TransactionResponse,
)
from backend.app.services.financial_service import (
    create_transaction,
    get_or_create_financial_health,
    get_or_create_financial_profile,
    list_user_transactions,
    update_financial_profile,
)

router = APIRouter(tags=["Financial"])


@router.get("/financial/profile", response_model=FinancialProfileResponse)
async def get_financial_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's financial profile."""
    return await get_or_create_financial_profile(db=db, user_id=current_user.id)


@router.put("/financial/profile", response_model=FinancialProfileResponse)
async def update_my_financial_profile(
    payload: FinancialProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user's financial profile."""
    return await update_financial_profile(db=db, user_id=current_user.id, update_data=payload)


@router.get("/financial/health", response_model=FinancialHealthResponse)
async def get_financial_health(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's financial health score and metrics."""
    return await get_or_create_financial_health(db=db, user_id=current_user.id)


@router.get("/transactions", response_model=list[TransactionResponse])
async def get_transactions(
    type: str | None = Query(default=None),
    category: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's transactions with filtering and pagination."""
    return await list_user_transactions(
        db=db,
        user_id=current_user.id,
        type_filter=type,
        category_filter=category,
        status_filter=status_filter,
        limit=limit,
        offset=offset,
    )


@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def add_transaction(
    payload: TransactionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Record a new transaction for the current user."""
    return await create_transaction(db=db, user_id=current_user.id, payload=payload)
