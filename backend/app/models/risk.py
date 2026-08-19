from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import JSON, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[str] = mapped_column(String(20), nullable=False)  # low, medium, high, critical
    factors: Mapped[dict[str, Any] | list[Any]] = mapped_column(JSON, default=list, nullable=False)
    evidence: Mapped[dict[str, Any] | list[Any]] = mapped_column(JSON, default=dict, nullable=False)
    recommendation: Mapped[str] = mapped_column(String(50), nullable=False)  # approve, review, reject, escalate
    confidence: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0.90"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

    customer = relationship("User", backref="risk_assessments")
