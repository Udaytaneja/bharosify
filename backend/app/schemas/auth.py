from pydantic import BaseModel, EmailStr, Field

from backend.app.schemas.user import UserResponse


class LoginRequest(BaseModel):
    """Credentials submitted during login."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RegisterRequest(BaseModel):
    """Data required to create a new user account."""

    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    phone: str | None = Field(default=None, max_length=30)
    language: str = Field(default="en")


class TokenResponse(BaseModel):
    """Authentication tokens returned after successful authentication."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse