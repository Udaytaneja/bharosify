from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base


class AgentModel(Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    owner_id: Mapped[int] = mapped_column(
        Integer,
        index=True,
        nullable=False,
    )

    organization_id: Mapped[str] = mapped_column(
        String(100),
        default="org_default",
        nullable=False,
    )

    agent_type: Mapped[str] = mapped_column(
        String(50),
        default="financial_advisor",
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="active",  # active | pending | suspended | revoked
        nullable=False,
    )

    trust_score: Mapped[int] = mapped_column(
        Integer,
        default=850,
        nullable=False,
    )

    risk_score: Mapped[int] = mapped_column(
        Integer,
        default=15,
        nullable=False,
    )

    capabilities: Mapped[str] = mapped_column(
        Text,
        default="[]",  # JSON array string of capabilities
        nullable=False,
    )

    permissions: Mapped[str] = mapped_column(
        Text,
        default="[]",  # JSON array string of permission scopes
        nullable=False,
    )

    policies: Mapped[str] = mapped_column(
        Text,
        default="[]",  # JSON array string of active policy IDs
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class AgentActionLogModel(Base):
    __tablename__ = "agent_action_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    agent_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    tool_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    resource: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    risk_level: Mapped[str] = mapped_column(
        String(20),
        default="low",  # low | medium | high | critical
        nullable=False,
    )

    decision: Mapped[str] = mapped_column(
        String(30),
        default="ALLOW",  # ALLOW | HOLD | BLOCK | HUMAN_REVIEW
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    audit_explanation: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True,
        nullable=False,
    )


class AgentPolicyModel(Base):
    __tablename__ = "agent_policies"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    rule_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,  # max_amount | tool_restriction | time_boundary | rate_limit | data_access_limit | privilege_restriction
    )

    threshold_value: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    action_on_violation: Mapped[str] = mapped_column(
        String(30),
        default="BLOCK",  # HOLD | BLOCK | HUMAN_REVIEW
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
