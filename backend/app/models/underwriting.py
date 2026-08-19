from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import JSON, Boolean, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class Underwriting(Base):
    __tablename__ = "underwritings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("loan_applications.id", ondelete="CASCADE"), unique=True, index=True, nullable=False
    )
    risk_score: Mapped[int] = mapped_column(Integer, default=700, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    factors: Mapped[dict[str, Any] | list[Any]] = mapped_column(JSON, default=list, nullable=False)
    evidence: Mapped[dict[str, Any] | list[Any]] = mapped_column(JSON, default=dict, nullable=False)
    recommendation: Mapped[str] = mapped_column(String(50), default="review", nullable=False)
    confidence: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal("0.85"), nullable=False)
    human_review_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    decision: Mapped[str] = mapped_column(String(20), default="review", nullable=False)  # approve, review, reject

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    application = relationship("LoanApplication", backref="underwriting")
