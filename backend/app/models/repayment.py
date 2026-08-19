from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class Repayment(Base):
    __tablename__ = "repayments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    loan_id: Mapped[int] = mapped_column(
        ForeignKey("loans.id", ondelete="CASCADE"), index=True, nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    paid_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="upcoming", nullable=False)
    # Statuses: upcoming, pending, paid, partially_paid, failed, overdue
    payment_reference: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    loan = relationship("Loan", backref="repayments")
