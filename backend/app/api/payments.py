from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.system import PaymentCreate, PaymentResponse
from backend.app.services.system_service import log_audit_event, process_payment

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payload: PaymentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Initialize a payment with payment reference and idempotency key (status: pending)."""
    return await process_payment(db=db, user_id=current_user.id, payload=payload)


@router.post("/{payment_id}/confirm", response_model=PaymentResponse)
async def confirm_payment(
    payment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Explicitly confirm a pending payment after provider verification."""
    from sqlalchemy import select
    from backend.app.models.payment import Payment

    res = await db.execute(select(Payment).where(Payment.id == payment_id, Payment.user_id == current_user.id))
    payment = res.scalar_one_or_none()

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found or unauthorized",
        )

    if payment.status == "completed":
        return payment

    payment.status = "completed"
    payment.reconciled = True
    await db.commit()
    await db.refresh(payment)

    await log_audit_event(
        db=db,
        actor_id=current_user.id,
        actor_type="user",
        action="payment_confirmed",
        resource="payments",
        resource_id=str(payment.id),
    )

    return payment
