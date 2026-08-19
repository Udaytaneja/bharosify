from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.system import NotificationResponse
from backend.app.services.system_service import get_user_notifications, mark_notification_as_read

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=list[NotificationResponse])
async def get_notifications(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get notifications for current user."""
    return await get_user_notifications(db=db, recipient_id=current_user.id)


@router.put("/{notification_id}/read", response_model=NotificationResponse)
async def read_notification(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark a notification as read."""
    notif = await mark_notification_as_read(db=db, notification_id=notification_id, recipient_id=current_user.id)
    if notif is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found or unauthorized",
        )
    return notif
