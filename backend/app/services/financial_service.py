from datetime import datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.financial_health import FinancialHealth
from backend.app.models.financial_profile import FinancialProfile
from backend.app.models.transaction import Transaction
from backend.app.schemas.financial import (
    FinancialProfileResponse,
    FinancialProfileUpdate,
    TransactionCreate,
)


async def get_or_create_financial_profile(
    db: AsyncSession, user_id: int
) -> FinancialProfile:
    result = await db.execute(
        select(FinancialProfile).where(FinancialProfile.user_id == user_id)
    )
    profile = result.scalar_one_or_none()
    if profile is None:
        profile = FinancialProfile(user_id=user_id)
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    return profile


async def update_financial_profile(
    db: AsyncSession, user_id: int, update_data: FinancialProfileUpdate
) -> FinancialProfile:
    profile = await get_or_create_financial_profile(db, user_id)

    if update_data.income is not None:
        profile.income = update_data.income
    if update_data.expenses is not None:
        profile.expenses = update_data.expenses
    if update_data.savings is not None:
        profile.savings = update_data.savings
    if update_data.assets is not None:
        profile.assets = update_data.assets
    if update_data.liabilities is not None:
        profile.liabilities = update_data.liabilities
    if update_data.existing_loans is not None:
        profile.existing_loans = update_data.existing_loans

    profile.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(profile)
    return profile


async def get_or_create_financial_health(
    db: AsyncSession, user_id: int
) -> FinancialHealth:
    result = await db.execute(
        select(FinancialHealth).where(FinancialHealth.user_id == user_id)
    )
    health = result.scalar_one_or_none()

    fin_profile = await get_or_create_financial_profile(db, user_id)

    if health is None:
        # Calculate burden
        burden = (
            (fin_profile.expenses / fin_profile.income * Decimal("100.00"))
            if fin_profile.income > Decimal("0.00")
            else Decimal("0.00")
        )
        health = FinancialHealth(
            user_id=user_id,
            score=750,
            income=fin_profile.income,
            expenses=fin_profile.expenses,
            savings=fin_profile.savings,
            debt=fin_profile.liabilities + fin_profile.existing_loans,
            repayment_burden=round(burden, 2),
            status="good",
        )
        db.add(health)
        await db.commit()
        await db.refresh(health)
    else:
        # Refresh values from financial profile
        burden = (
            (fin_profile.expenses / fin_profile.income * Decimal("100.00"))
            if fin_profile.income > Decimal("0.00")
            else Decimal("0.00")
        )
        health.income = fin_profile.income
        health.expenses = fin_profile.expenses
        health.savings = fin_profile.savings
        health.debt = fin_profile.liabilities + fin_profile.existing_loans
        health.repayment_burden = round(burden, 2)
        health.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(health)

    return health


async def list_user_transactions(
    db: AsyncSession,
    user_id: int,
    type_filter: str | None = None,
    category_filter: str | None = None,
    status_filter: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Transaction]:
    query = select(Transaction).where(Transaction.user_id == user_id)
    if type_filter:
        query = query.where(Transaction.type == type_filter)
    if category_filter:
        query = query.where(Transaction.category == category_filter)
    if status_filter:
        query = query.where(Transaction.status == status_filter)

    query = query.order_by(Transaction.date.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_transaction(
    db: AsyncSession, user_id: int, payload: TransactionCreate
) -> Transaction:
    tx = Transaction(
        user_id=user_id,
        amount=payload.amount,
        type=payload.type,
        category=payload.category,
        merchant=payload.merchant,
        description=payload.description,
        date=payload.date or datetime.utcnow(),
        status=payload.status,
    )
    db.add(tx)
    await db.commit()
    await db.refresh(tx)
    return tx
