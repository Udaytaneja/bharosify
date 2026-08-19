from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user, oauth2_scheme
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
)
from backend.app.schemas.user import UserResponse
from backend.app.services.auth_service import (
    authenticate_user,
    create_auth_tokens,
    logout_user,
    refresh_user_token,
    register_user,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user."""

    try:
        user = await register_user(
            db=db,
            email=request.email,
            password=request.password,
            name=request.name,
            phone=request.phone,
            language=request.language,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """Authenticate a user and return access/refresh tokens."""

    user = await authenticate_user(
        db=db,
        email=request.email,
        password=request.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    tokens = create_auth_tokens(user)

    return {
        **tokens,
        "user": user,
    }


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
async def refresh(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token using a valid refresh token."""
    try:
        result = await refresh_user_token(db=db, refresh_token=request.refresh_token)
        return result
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(
    token: str = Depends(oauth2_scheme),
):
    """Logout current user by revoking access token."""
    logout_user(token)
    return {"message": "Successfully logged out"}


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: User = Depends(get_current_active_user),
):
    """Get current authenticated user account."""
    return current_user