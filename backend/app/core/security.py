from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash

from backend.app.core.config import settings

password_hash = PasswordHash.recommended()

REVOKED_TOKENS: set[str] = set()


def hash_password(password: str) -> str:
    """Hash a plain-text password."""
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its stored hash."""
    return password_hash.verify(password, hashed_password)


def create_access_token(subject: str | int) -> str:
    """Create a short-lived access token."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )

    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def create_refresh_token(subject: str | int) -> str:
    """Create a longer-lived refresh token."""
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.jwt_refresh_token_expire_days
    )

    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": "refresh",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token."""
    if is_token_blacklisted(token):
        raise jwt.PyJWTError("Token has been revoked")

    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )


def blacklist_token(token: str) -> None:
    """Blacklist a token so it cannot be used again."""
    REVOKED_TOKENS.add(token)


def is_token_blacklisted(token: str) -> bool:
    """Check if a token is in the blacklist."""
    return token in REVOKED_TOKENS