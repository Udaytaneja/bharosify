from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.models.fraud import FraudSignal
from backend.app.models.risk import RiskAssessment
from backend.app.models.trust import TrustFactor, TrustProfile


async def get_or_create_trust_profile(db: AsyncSession, user_id: int) -> TrustProfile:
    result = await db.execute(
        select(TrustProfile)
        .options(selectinload(TrustProfile.factors))
        .where(TrustProfile.user_id == user_id)
    )
    profile = result.scalar_one_or_none()

    if profile is None:
        profile = TrustProfile(user_id=user_id, score=720, level="good", change=5)
        db.add(profile)
        await db.commit()

        # Add initial trust factors
        f1 = TrustFactor(
            trust_profile_id=profile.id,
            name="On-Time Payments",
            impact="positive",
            value="+15 pts",
            description="Consistent record of fulfilling financial commitments.",
        )
        f2 = TrustFactor(
            trust_profile_id=profile.id,
            name="Verified Identity",
            impact="positive",
            value="Verified",
            description="Account verification and KYC compliance completed.",
        )
        db.add_all([f1, f2])
        await db.commit()

        result = await db.execute(
            select(TrustProfile)
            .options(selectinload(TrustProfile.factors))
            .where(TrustProfile.id == profile.id)
        )
        profile = result.scalar_one()

    return profile


async def get_user_risk_assessments(
    db: AsyncSession, customer_id: int
) -> list[RiskAssessment]:
    result = await db.execute(
        select(RiskAssessment)
        .where(RiskAssessment.customer_id == customer_id)
        .order_by(RiskAssessment.created_at.desc())
    )
    return list(result.scalars().all())


async def get_user_fraud_signals(
    db: AsyncSession, customer_id: int
) -> list[FraudSignal]:
    result = await db.execute(
        select(FraudSignal)
        .where(FraudSignal.customer_id == customer_id)
        .order_by(FraudSignal.created_at.desc())
    )
    return list(result.scalars().all())
