from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.user import User
from backend.app.models.user_profile import UserProfile
from backend.app.schemas.profile import UserProfileResponse, UserProfileUpdate


async def get_or_create_user_profile(db: AsyncSession, user: User) -> UserProfileResponse:
    """Fetch or initialize the UserProfile for a given user."""
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user.id))
    profile = result.scalar_one_or_none()

    if profile is None:
        profile = UserProfile(user_id=user.id, profile_status="complete")
        db.add(profile)
        await db.commit()
        await db.refresh(profile)

    return UserProfileResponse(
        user_id=user.id,
        name=user.name,
        email=user.email,
        phone=user.phone,
        language=user.language,
        profile_status=profile.profile_status,
    )


async def update_user_profile(
    db: AsyncSession, user: User, update_data: UserProfileUpdate
) -> UserProfileResponse:
    """Update allowed fields of current user profile (name, phone, language)."""
    if update_data.name is not None:
        user.name = update_data.name
    if update_data.phone is not None:
        user.phone = update_data.phone
    if update_data.language is not None:
        user.language = update_data.language

    user.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(user)

    return await get_or_create_user_profile(db, user)
