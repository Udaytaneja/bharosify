from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.agents import router as agents_router
from backend.app.api.ai import router as ai_router
from backend.app.api.applications import router as applications_router
from backend.app.api.audit import router as audit_router
from backend.app.api.auth import router as auth_router
from backend.app.api.bankers import router as bankers_router
from backend.app.api.documents import router as documents_router
from backend.app.api.financial import router as financial_router
from backend.app.api.loans import router as loans_router
from backend.app.api.notifications import router as notifications_router
from backend.app.api.payments import router as payments_router
from backend.app.api.repayments import router as repayments_router
from backend.app.api.trust import router as trust_router
from backend.app.api.users import router as users_router
from backend.app.core.config import settings
from backend.app.core.database import engine
from backend.app.models import Base


@asynccontextmanager
async def lifespan(application: FastAPI):
    if settings.app_env == "development" and settings.database_url.startswith("sqlite"):
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="AgentTrust OS",
    description="Secure financial trust and intelligence platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list({settings.frontend_url, "http://localhost:5173", "http://127.0.0.1:5173"}),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Standard Error Format Handler matching contracts/schemas.md
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
        422: "UNPROCESSABLE_ENTITY",
        500: "INTERNAL_SERVER_ERROR",
    }
    error_code = code_map.get(exc.status_code, "ERROR")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": error_code,
                "message": exc.detail,
                "details": None,
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors(),
            }
        },
    )


api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(financial_router)
api_v1_router.include_router(trust_router)
api_v1_router.include_router(bankers_router)
api_v1_router.include_router(documents_router)
api_v1_router.include_router(applications_router)
api_v1_router.include_router(loans_router)
api_v1_router.include_router(repayments_router)
api_v1_router.include_router(payments_router)
api_v1_router.include_router(notifications_router)
api_v1_router.include_router(audit_router)
api_v1_router.include_router(ai_router)
api_v1_router.include_router(agents_router)

app.include_router(api_v1_router)


# Root-level fallback for backward compatibility
app.include_router(auth_router)


@app.get("/")
async def root():
    return {
        "message": "AgentTrust OS API is running",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
    }