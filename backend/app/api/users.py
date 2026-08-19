from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.profile import UserProfileResponse, UserProfileUpdate
from backend.app.services.profile_service import get_or_create_user_profile, update_user_profile

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's profile information."""
    return await get_or_create_user_profile(db=db, user=current_user)


@router.put("/me", response_model=UserProfileResponse)
async def update_my_profile(
    payload: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user's profile information."""
    return await update_user_profile(db=db, user=current_user, update_data=payload)
