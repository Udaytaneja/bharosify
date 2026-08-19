from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.intelligence import TrustFactorResponse, TrustProfileResponse
from backend.app.services.intelligence_service import get_or_create_trust_profile

router = APIRouter(prefix="/trust", tags=["Trust"])


@router.get("/me", response_model=TrustProfileResponse)
async def get_my_trust_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's trust profile and score."""
    profile = await get_or_create_trust_profile(db=db, user_id=current_user.id)
    return profile


@router.get("/me/factors", response_model=list[TrustFactorResponse])
async def get_my_trust_factors(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get factors affecting current user's trust score."""
    profile = await get_or_create_trust_profile(db=db, user_id=current_user.id)
    return profile.factors
