import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.security import (
    blacklist_token,
    create_access_token,
    create_refresh_token,
    decode_token,
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


async def refresh_user_token(
    db: AsyncSession,
    refresh_token: str,
) -> dict[str, str | User]:
    """Validate a refresh token and return fresh access/refresh tokens along with the User."""
    try:
        payload = decode_token(refresh_token)
        user_id_str: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")

        if user_id_str is None or token_type != "refresh":
            raise ValueError("Invalid refresh token")

        user_id = int(user_id_str)
    except (jwt.PyJWTError, ValueError) as exc:
        raise ValueError("Invalid or expired refresh token") from exc

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        raise ValueError("User inactive or not found")

    tokens = create_auth_tokens(user)
    return {
        **tokens,
        "user": user,
    }


def logout_user(token: str) -> None:
    """Revoke/blacklist the given token."""
    blacklist_token(token)