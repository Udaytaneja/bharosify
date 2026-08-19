from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user, require_role
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.system import AIRequest, AIResponse
from backend.app.services.system_service import handle_ai_request

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/chat", response_model=AIResponse)
async def ai_chat(
    payload: AIRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Financial AI assistant chat endpoint."""
    return await handle_ai_request(db=db, current_user=current_user, payload=payload, task_type="chat")


@router.post("/scenario", response_model=AIResponse)
async def ai_scenario(
    payload: AIRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Financial scenario analysis endpoint."""
    return await handle_ai_request(db=db, current_user=current_user, payload=payload, task_type="scenario")


@router.post("/risk-analysis", response_model=AIResponse)
async def ai_risk_analysis(
    payload: AIRequest,
    current_user: User = Depends(require_role("banker")),
    db: AsyncSession = Depends(get_db),
):
    """AI-assisted risk analysis endpoint (Banker only)."""
    return await handle_ai_request(db=db, current_user=current_user, payload=payload, task_type="risk_analysis")


@router.post("/underwriting", response_model=AIResponse)
async def ai_underwriting(
    payload: AIRequest,
    current_user: User = Depends(require_role("banker")),
    db: AsyncSession = Depends(get_db),
):
    """AI-assisted underwriting endpoint (Banker only)."""
    return await handle_ai_request(db=db, current_user=current_user, payload=payload, task_type="underwriting")
