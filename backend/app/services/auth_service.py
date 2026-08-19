from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from backend.app.models.user import User


async def register_user(
    db: AsyncSession,
    email: str,
    password: str,
    name: str,
    phone: str | None = None,
    language: str = "en",
) -> User:
    """Register a new user."""

    result = await db.execute(
        select(User).where(User.email == email.lower())
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise ValueError("Email already registered")

    user = User(
        name=name,
        email=email.lower(),
        hashed_password=hash_password(password),
        phone=phone,
        role="user",
        language=language,
        is_active=True,
        is_verified=False,
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> User | None:
    """Authenticate a user using email and password."""

    result = await db.execute(
        select(User).where(User.email == email.lower())
    )

    user = result.scalar_one_or_none()

    if user is None:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    if not user.is_active:
        return None

    return user


def create_auth_tokens(user: User) -> dict[str, str]:
    """Create access and refresh tokens for an authenticated user."""

    access_token = create_access_token(
        subject=str(user.id),
    )

    refresh_token = create_refresh_token(
        subject=str(user.id),
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }