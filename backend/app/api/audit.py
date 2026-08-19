from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.system import AuditEventResponse
from backend.app.services.system_service import get_user_audit_events

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/me", response_model=list[AuditEventResponse])
async def get_my_audit_events(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get audit activity history for the current account."""
    return await get_user_audit_events(db=db, user_id=current_user.id)
