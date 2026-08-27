from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_current_active_user, require_role
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.system import AIRequest, AIResponse
from backend.app.services.system_service import handle_ai_request
from ai.app.perception import DocumentIntelligenceResult, document_intelligence_pipeline

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/document", response_model=DocumentIntelligenceResult)
async def analyze_document(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role("banker")),
):
    """Authenticated prototype bridge to the existing document-perception pipeline."""
    del current_user
    try:
        file_bytes = await file.read()
        return await document_intelligence_pipeline.process_document(
            file_bytes=file_bytes,
            file_name=file.filename or "document.bin",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "DOCUMENT_PROCESSING_ERROR", "message": str(exc)},
        ) from exc


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


@router.post("/financial-intelligence", response_model=AIResponse)
async def ai_financial_intelligence(
    payload: AIRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """AgentTrust Financial Intelligence service endpoint (supports all 7 features)."""
    return await handle_ai_request(db=db, current_user=current_user, payload=payload, task_type="financial_intelligence")


@router.post("/digital-twin", response_model=AIResponse)
async def ai_digital_twin(
    payload: AIRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Financial Digital Twin state analysis endpoint."""
    return await handle_ai_request(db=db, current_user=current_user, payload=payload, task_type="digital_twin")


@router.post("/what-if", response_model=AIResponse)
async def ai_what_if(
    payload: AIRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """What-if financial simulation endpoint."""
    return await handle_ai_request(db=db, current_user=current_user, payload=payload, task_type="what_if_simulation")
