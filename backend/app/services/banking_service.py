from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.application import LoanApplication
from backend.app.models.loan import Loan
from backend.app.models.repayment import Repayment
from backend.app.models.underwriting import Underwriting
from backend.app.models.user import User
from backend.app.schemas.banking import (
    CustomerResponse,
    LoanApplicationCreate,
    LoanApplicationUpdate,
)
from backend.app.services.financial_service import get_or_create_financial_health
from backend.app.services.intelligence_service import get_or_create_trust_profile


# Banker Customer Services
async def list_banker_customers(db: AsyncSession) -> list[CustomerResponse]:
    result = await db.execute(select(User).where(User.role == "user"))
    users = result.scalars().all()

    customers = []
    for u in users:
        tp = await get_or_create_trust_profile(db, u.id)
        fh = await get_or_create_financial_health(db, u.id)
        status_str = "active" if u.is_active else "inactive"
        customers.append(
            CustomerResponse(
                id=u.id,
                name=u.name,
                email=u.email,
                phone=u.phone,
                account_status=status_str,
                trust_profile=tp,
                financial_health=fh,
            )
        )
    return customers


async def get_banker_customer_by_id(db: AsyncSession, customer_id: int) -> CustomerResponse | None:
    result = await db.execute(select(User).where(User.id == customer_id, User.role == "user"))
    u = result.scalar_one_or_none()
    if u is None:
        return None

    tp = await get_or_create_trust_profile(db, u.id)
    fh = await get_or_create_financial_health(db, u.id)
    status_str = "active" if u.is_active else "inactive"
    return CustomerResponse(
        id=u.id,
        name=u.name,
        email=u.email,
        phone=u.phone,
        account_status=status_str,
        trust_profile=tp,
        financial_health=fh,
    )


# Loan Application Services
async def create_loan_application(
    db: AsyncSession, customer_id: int, payload: LoanApplicationCreate
) -> LoanApplication:
    app = LoanApplication(
        customer_id=customer_id,
        amount=payload.amount,
        purpose=payload.purpose,
        status="submitted",
        documents=payload.documents,
    )
    db.add(app)
    await db.commit()
    await db.refresh(app)

    # Initialize underwriting record
    uw = Underwriting(
        application_id=app.id,
        risk_score=710,
        risk_level="medium",
        factors=["Debt-to-income optimal", "Stable income history"],
        evidence={"verified_income": str(payload.amount)},
        recommendation="review",
        confidence=Decimal("0.88"),
        human_review_required=True,
        decision="review",
    )
    db.add(uw)
    await db.commit()

    return app


async def list_loan_applications(
    db: AsyncSession, current_user: User
) -> list[LoanApplication]:
    if current_user.role == "banker":
        query = select(LoanApplication).order_by(LoanApplication.created_at.desc())
    else:
        query = (
            select(LoanApplication)
            .where(LoanApplication.customer_id == current_user.id)
            .order_by(LoanApplication.created_at.desc())
        )
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_loan_application_by_id(
    db: AsyncSession, application_id: int, current_user: User
) -> LoanApplication | None:
    result = await db.execute(select(LoanApplication).where(LoanApplication.id == application_id))
    app = result.scalar_one_or_none()

    if app is None:
        return None

    if current_user.role != "banker" and app.customer_id != current_user.id:
        return None

    return app


async def update_loan_application(
    db: AsyncSession, application_id: int, payload: LoanApplicationUpdate, current_user: User
) -> LoanApplication | None:
    app = await get_loan_application_by_id(db, application_id, current_user)
    if app is None:
        return None

    VALID_TRANSITIONS = {
        "draft": {"submitted", "withdrawn"},
        "submitted": {"under_review", "withdrawn"},
        "under_review": {"documents_required", "underwriting", "rejected", "withdrawn"},
        "documents_required": {"under_review", "withdrawn"},
        "underwriting": {"approved", "rejected"},
        "approved": {"completed"},
        "rejected": set(),
        "withdrawn": set(),
        "completed": set(),
    }

    BANKER_ONLY_STATUSES = {
        "under_review",
        "documents_required",
        "underwriting",
        "approved",
        "rejected",
        "completed",
    }

    if payload.status is not None:
        current_status = app.status

        # Check if status transition is valid
        allowed = VALID_TRANSITIONS.get(current_status, set())
        if payload.status not in allowed:
            raise ValueError(f"Invalid status transition from '{current_status}' to '{payload.status}'")

        # Check role authorization for banker-only statuses
        if payload.status in BANKER_ONLY_STATUSES and current_user.role != "banker":
            raise ValueError(f"Forbidden: Only bankers can transition application status to '{payload.status}'")

        app.status = payload.status

        # If approved by banker, provision Loan and Repayments transactionally
        if payload.status == "approved":
            existing_loan = await db.execute(select(Loan).where(Loan.application_id == app.id))
            if existing_loan.scalar_one_or_none() is None:
                new_loan = Loan(
                    application_id=app.id,
                    customer_id=app.customer_id,
                    principal=app.amount,
                    interest_rate=Decimal("8.50"),
                    duration=12,
                    outstanding_amount=app.amount,
                    status="active",
                    start_date=datetime.utcnow(),
                    maturity_date=datetime.utcnow() + timedelta(days=365),
                )
                db.add(new_loan)
                await db.commit()
                await db.refresh(new_loan)

                # Provision Repayment schedule dynamically with exact Decimal precision
                duration = new_loan.duration
                principal = new_loan.principal
                if duration > 0:
                    base_installment = (principal / Decimal(duration)).quantize(
                        Decimal("0.01"), rounding=ROUND_HALF_UP
                    )
                    allocated = base_installment * Decimal(duration - 1)
                    final_installment = principal - allocated

                    for month in range(1, duration + 1):
                        amt = final_installment if month == duration else base_installment
                        rep = Repayment(
                            loan_id=new_loan.id,
                            amount=amt,
                            due_date=datetime.utcnow() + timedelta(days=30 * month),
                            status="upcoming",
                        )
                        db.add(rep)
                    await db.commit()

    if payload.purpose is not None:
        app.purpose = payload.purpose
    if payload.documents is not None:
        app.documents = payload.documents

    app.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(app)
    return app


# Loans Services
async def list_user_loans(db: AsyncSession, current_user: User) -> list[Loan]:
    if current_user.role == "banker":
        query = select(Loan).order_by(Loan.created_at.desc())
    else:
        query = select(Loan).where(Loan.customer_id == current_user.id).order_by(Loan.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_loan_by_id(db: AsyncSession, loan_id: int, current_user: User) -> Loan | None:
    result = await db.execute(select(Loan).where(Loan.id == loan_id))
    loan = result.scalar_one_or_none()
    if loan is None:
        return None
    if current_user.role != "banker" and loan.customer_id != current_user.id:
        return None
    return loan


# Repayments Services
async def list_repayments(db: AsyncSession, current_user: User) -> list[Repayment]:
    if current_user.role == "banker":
        query = select(Repayment).order_by(Repayment.due_date.asc())
    else:
        user_loans = await list_user_loans(db, current_user)
        loan_ids = [l.id for l in user_loans]
        if not loan_ids:
            return []
        query = select(Repayment).where(Repayment.loan_id.in_(loan_ids)).order_by(Repayment.due_date.asc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_repayments_for_loan(
    db: AsyncSession, loan_id: int, current_user: User
) -> list[Repayment]:
    loan = await get_loan_by_id(db, loan_id, current_user)
    if loan is None:
        return []
    result = await db.execute(select(Repayment).where(Repayment.loan_id == loan_id).order_by(Repayment.due_date.asc()))
    return list(result.scalars().all())
