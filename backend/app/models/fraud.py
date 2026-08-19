from datetime import datetime
from typing import Any

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class FraudSignal(Base):
    __tablename__ = "fraud_signals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("transactions.id", ondelete="SET NULL"), nullable=True
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)  # info, warning, high, critical
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    evidence: Mapped[dict[str, Any] | list[Any]] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False)  # open, under_review, resolved, false_positive

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

    customer = relationship("User", backref="fraud_signals")
    transaction = relationship("Transaction", backref="fraud_signals")
