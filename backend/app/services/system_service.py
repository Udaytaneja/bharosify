from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.audit import AuditEvent
from backend.app.models.notification import Notification
from backend.app.models.payment import Payment
from backend.app.models.user import User
from backend.app.schemas.system import AIRequest, AIResponse, PaymentCreate


# Audit Helper
async def log_audit_event(
    db: AsyncSession,
    actor_id: int | None,
    actor_type: str,
    action: str,
    resource: str,
    resource_id: str | None = None,
    result: str = "success",
) -> AuditEvent:
    event = AuditEvent(
        actor_id=actor_id,
        actor_type=actor_type,
        action=action,
        resource=resource,
        resource_id=str(resource_id) if resource_id is not None else None,
        result=result,
        timestamp=datetime.utcnow(),
    )
    db.add(event)
    await db.commit()
    return event


async def get_user_audit_events(db: AsyncSession, user_id: int) -> list[AuditEvent]:
    res = await db.execute(
        select(AuditEvent)
        .where(AuditEvent.actor_id == user_id)
        .order_by(AuditEvent.timestamp.desc())
    )
    return list(res.scalars().all())


# Notification Services
async def get_user_notifications(db: AsyncSession, recipient_id: int) -> list[Notification]:
    res = await db.execute(
        select(Notification)
        .where(Notification.recipient_id == recipient_id)
        .order_by(Notification.created_at.desc())
    )
    return list(res.scalars().all())


async def mark_notification_as_read(
    db: AsyncSession, notification_id: int, recipient_id: int
) -> Notification | None:
    res = await db.execute(
        select(Notification).where(
            Notification.id == notification_id, Notification.recipient_id == recipient_id
        )
    )
    notif = res.scalar_one_or_none()
    if notif is None:
        return None
    notif.read = True
    await db.commit()
    await db.refresh(notif)
    return notif


# Payment Services
async def process_payment(
    db: AsyncSession, user_id: int, payload: PaymentCreate
) -> Payment:
    # Check idempotency
    res_idem = await db.execute(
        select(Payment).where(Payment.idempotency_key == payload.idempotency_key)
    )
    existing = res_idem.scalar_one_or_none()
    if existing is not None:
        return existing

    payment = Payment(
        user_id=user_id,
        transaction_id=payload.transaction_id,
        repayment_id=payload.repayment_id,
        amount=payload.amount,
        payment_reference=payload.payment_reference,
        idempotency_key=payload.idempotency_key,
        status="pending",
        reconciled=False,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)

    await log_audit_event(
        db=db,
        actor_id=user_id,
        actor_type="user",
        action="payment_processed",
        resource="payments",
        resource_id=str(payment.id),
    )

    return payment


from ai.app.gateway import ai_gateway
from ai.app.schemas.requests import AIExecutionRequest


# AI Backend Integration Wrapper
async def handle_ai_request(
    db: AsyncSession, current_user: User, payload: AIRequest, task_type: str
) -> AIResponse:
    """Wrapper that validates auth/context, audits the call, and delegates to Member 3 AI interface."""
    await log_audit_event(
        db=db,
        actor_id=current_user.id,
        actor_type=current_user.role,
        action=f"ai_{task_type}",
        resource="ai_engine",
        resource_id=payload.request_id,
    )

    exec_req = AIExecutionRequest(
        request_id=payload.request_id,
        user_id=current_user.id,
        role=current_user.role,
        task=task_type,
        input=payload.input,
        language=payload.language,
        context=payload.context or {},
    )

    res = await ai_gateway.execute(exec_req)

    return AIResponse(
        request_id=res.request_id,
        response=res.response,
        confidence=res.confidence,
        reasoning_summary=res.reasoning_summary,
        evidence=res.evidence,
        recommendation=res.recommendation,
        requires_human_review=res.requires_human_review,
    )
