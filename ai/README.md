# AgentTrust OS — AI Subsystem

**Lead AI/ML Architect**: Member 3  
**Status**: Foundational AI Infrastructure Implemented  

---

## Overview

The `ai/` subsystem provides an isolated, enterprise-grade AI Gateway and model orchestration layer for **AgentTrust OS**.

### Core Architecture

```text
ai/
├── app/
│   ├── api/                # REST endpoints
│   ├── core/               # Settings (Pydantic) & Exception hierarchy
│   ├── gateway/            # Central AIGateway orchestrator
│   ├── routing/            # ModelRouter (Dynamic model selection)
│   ├── providers/          # Provider abstractions (Gemini, OpenAI, Mock)
│   ├── models/             # ModelRegistry (Catalog, token pricing)
│   ├── prompts/            # Versioned & localized prompt templates (en/hi)
│   ├── schemas/            # Request/Response/Telemetry Pydantic contracts
│   ├── rag/                # RAG & vector retrieval (placeholder)
│   ├── vision/             # OCR & document intelligence (placeholder)
│   ├── ml/                 # Tabular risk & fraud classifiers (placeholder)
│   ├── agents/             # Autonomous agent sandbox (placeholder)
│   ├── safety/             # PII sanitizer, Prompt shield, Decision guard
│   ├── observability/      # Token meter, Cost USD tracker, Audit logger
│   ├── evaluation/         # Model evaluation & benchmarks (placeholder)
│   └── main.py             # Standalone FastAPI service application
│
├── tests/                  # Pytest test suite for AI layer
├── configs/                # Model registry and prompt version configs
└── README.md
```

---

## Implemented Infrastructure Features

1. **AI Gateway (`ai/app/gateway/gateway.py`)**: Request ID generation, timeout handling, retries with backoff, fallback handling, structured output validation, cost/token/latency tracking, and audit logging.
2. **Provider Abstraction (`ai/app/providers/`)**: Standardized `BaseProvider` interface with Google Gemini adapter, OpenAI adapter, and deterministic `MockProvider` fallback.
3. **Model Registry (`ai/app/models/registry.py`)**: Central registry tracking pricing ($/1k tokens), max context length, capabilities, and recommended tasks.
4. **Model Router (`ai/app/routing/router.py`)**: Dynamic task-based router choosing optimal primary model and fallback model based on API key availability and task complexity.
5. **Prompt Versioning & Localization (`ai/app/prompts/`)**: Versioned templates supporting English (`en`) and Hindi (`hi`).
6. **AI Safety Middleware (`ai/app/safety/`)**:
   - **PII Sanitizer**: Automatically masks PAN card numbers, Aadhaar numbers, and Bank account numbers before LLM API calls.
   - **Prompt Shield**: Blocks prompt injections and malicious instruction overrides.
   - **Decision Guard**: Strictly enforces non-authoritative financial boundaries (ensuring model recommendations require human banker review).
7. **Observability Suite (`ai/app/observability/`)**: Calculates input/output token counts, cost in USD, execution latency in milliseconds, and emits structured JSON audit events.

---

## Safety Principles

> **CORE PRINCIPLE**: AI models generate predictions, signals, recommendations, classifications, and explanations **ONLY**.  
> AI services **NEVER** execute money transfers, approve/reject loans directly, or modify authoritative financial records. Member 1's backend policy engines remain authoritative.

---

## Environment Variables

Configure secrets in `.env`:

```ini
# AI Provider Credentials
AI_API_KEY=your-gemini-or-openai-key
AI_PROVIDER=gemini
AI_MODEL=gemini-1.5-flash
AI_FALLBACK_PROVIDER=mock
AI_FALLBACK_MODEL=mock-deterministic-v1

# Timeouts & Retries
AI_TIMEOUT_SECONDS=15.0
AI_MAX_RETRIES=2

# Safety & Guardrails
PII_REDACTION_ENABLED=true
PROMPT_SHIELD_ENABLED=true
DECISION_GUARD_ENABLED=true
```

---

## Testing

Run the AI subsystem test suite:

```bash
pytest ai/tests
```
