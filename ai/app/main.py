import os

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from ai.app.core.config import ai_settings
from ai.app.core.exceptions import SafetyViolationError, AIServiceException
from ai.app.gateway import ai_gateway
from ai.app.models import model_registry
from ai.app.schemas.requests import AIExecutionRequest, AIExecutionResponse

app = FastAPI(
    title="AgentTrust OS - AI Subsystem",
    description="Standalone Enterprise AI Infrastructure microservice",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": ai_settings.app_name,
        "environment": ai_settings.environment,
        "default_provider": ai_settings.default_provider,
        "default_model": ai_settings.default_model,
    }


@app.get("/models")
async def list_models():
    """Returns registered AI models and capabilities."""
    return {"models": model_registry.list_models()}


@app.post("/execute", response_model=AIExecutionResponse)
async def execute_ai_task(request: AIExecutionRequest):
    """
    Executes an AI task through the central AI Gateway.
    Handles safety, routing, retries, fallback, metrics, and audit logging.
    """
    try:
        return await ai_gateway.execute(request)
    except SafetyViolationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": e.code, "message": e.message, "details": e.details}
        )
    except AIServiceException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": e.code, "message": e.message, "details": e.details}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "AI_EXECUTION_ERROR", "message": str(e)}
        )


from ai.app.agents.financial_assistant import financial_intelligence_assistant
from ai.app.schemas.assistant import AssistantQueryRequest, AssistantQueryResponse


@app.post("/ai/assistant/query", response_model=AssistantQueryResponse)
async def query_financial_assistant(request: AssistantQueryRequest):
    """
    Executes a query through the Financial Intelligence Assistant.
    Orchestrates Member 1 DTOs, deterministic calculations, ML signals, RAG policy citations,
    and multi-language explainability (EN/HI/Hinglish) with safety action shields.
    """
    try:
        return await financial_intelligence_assistant.process_query(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "ASSISTANT_QUERY_ERROR", "message": str(e)}
        )


from ai.app.agents.banker_copilot import banker_underwriting_copilot
from ai.app.schemas.underwriting import UnderwritingAssessment, UnderwritingAssessmentRequest
from ai.app.perception import DocumentIntelligenceResult, document_intelligence_pipeline


@app.post("/perception/document", response_model=DocumentIntelligenceResult)
async def analyze_document(file: UploadFile = File(...)):
    """Prototype document upload endpoint for experimental layout/OCR evidence."""
    try:
        file_bytes = await file.read()
        return await document_intelligence_pipeline.process_document(
            file_bytes=file_bytes,
            file_name=file.filename or "document.bin",
        )
    except SafetyViolationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"code": e.code, "message": e.message})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"code": "DOCUMENT_PROCESSING_ERROR", "message": str(e)})


@app.post("/ai/banker/underwriting", response_model=UnderwritingAssessment)
async def generate_underwriting_assessment(request: UnderwritingAssessmentRequest):
    """
    Generates an Underwriting Assessment through the Banker Intelligence / Underwriting Copilot.
    Orchestrates evidence fusion across Member 1 DTOs, deterministic EMI/DTI math, ML risk signals (EXPERIMENTAL),
    document perception (YOLO/OCR), and RAG bank policies. Requires human banker decision (requires_human_review = True).
    """
    try:
        return await banker_underwriting_copilot.generate_assessment(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "UNDERWRITING_ASSESSMENT_ERROR", "message": str(e)}
        )


