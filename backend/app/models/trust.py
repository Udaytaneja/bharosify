from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class TrustProfile(Base):
    __tablename__ = "trust_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False
    )
    score: Mapped[int] = mapped_column(Integer, default=700, nullable=False)
    level: Mapped[str] = mapped_column(String(20), default="good", nullable=False)  # critical, needs_attention, good, trusted
    change: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    user = relationship("User", backref="trust_profile")
    factors = relationship("TrustFactor", backref="trust_profile", cascade="all, delete-orphan")


class TrustFactor(Base):
    __tablename__ = "trust_factors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    trust_profile_id: Mapped[int] = mapped_column(
        ForeignKey("trust_profiles.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    impact: Mapped[str] = mapped_column(String(20), nullable=False)  # positive, negative, neutral
    value: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
