# Render Deployment Readiness Guide — AgentTrust OS

**Status**: **DEPLOYMENT READY**  
**Date**: August 29, 2026  
**YOLO Checkpoint SHA-256**: `f1bc0e4d6e4b78f40681d93ce8bb4cf5cd34924bf1efb2ceddbc209d1da40250` (Verified)

---

## 1. Required Render Services

| Service Name | Render Service Type | Runtime | Build Command | Start Command |
|---|---|---|---|---|
| **agenttrust-os-api** | Web Service | Python 3.11 | `pip install -r requirements.txt && python -m alembic -c backend/alembic.ini upgrade head` | `gunicorn -k uvicorn.workers.UvicornWorker backend.app.main:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |
| **agenttrust-os-frontend** | Static Site | Static HTML/JS | `cd frontend && npm install && npm run build` | *Static publishing path*: `./frontend/dist` |
| **agenttrust-db** | PostgreSQL Database | PostgreSQL 16 | *Managed PostgreSQL instance* | *Managed PostgreSQL instance* |

---

## 2. Environment Variables Configuration

### Backend Web Service (`agenttrust-os-api`)

| Environment Variable | Recommended Production Value | Description |
|---|---|---|
| `APP_ENV` | `production` | Enables production mode & error handling |
| `DEBUG` | `false` | Disables debug logs & stack trace leakage |
| `DATABASE_URL` | *Internal Connection String* | PostgreSQL connection string from Render DB |
| `JWT_SECRET` | *Generate 64-char random hex* | Secret key used to sign JWT Bearer tokens |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Access token expiration duration |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | `30` | Refresh token expiration duration |
| `FRONTEND_URL` | `https://agenttrust-os-frontend.onrender.com` | Deployed frontend origin for CORS validation |
| `CORS_ORIGINS` | `https://agenttrust-os-frontend.onrender.com` | Comma-separated allowed origins |
| `STORAGE_PROVIDER` | `s3` (or `local` for disk) | Storage provider (`s3` or `local`) |
| `S3_BUCKET_NAME` | `agenttrust-documents` | Bucket name for Cloudflare R2 or AWS S3 |
| `S3_ENDPOINT_URL` | `https://<accountid>.r2.cloudflarestorage.com` | S3 API endpoint URL |
| `S3_ACCESS_KEY_ID` | *Secret* | S3 API Access Key ID |
| `S3_SECRET_ACCESS_KEY` | *Secret* | S3 API Secret Access Key |
| `S3_REGION` | `us-east-1` (or `auto`) | S3 bucket region |
| `YOLO_MODEL_PATH` | `runs/detect/artifacts/training/doc_layout/real_yolo_002/train_run/weights/best.pt` | Path to trained YOLOv8 PyTorch checkpoint |
| `OCR_ENABLED` | `true` | Enables PaddleOCR text recognition |
| `OCR_PYTHON_EXECUTABLE` | `python` | Interpreter for PaddleOCR (in-process on Linux) |
| `OCR_TIMEOUT_SECONDS` | `30` | Execution timeout limit for OCR processing |

### Frontend Static Site (`agenttrust-os-frontend`)

| Environment Variable | Recommended Production Value | Description |
|---|---|---|
| `VITE_API_BASE_URL` | `https://agenttrust-os-api.onrender.com/api/v1` | Public backend API URL |

---

## 3. Recommended Deployment Sequence

1. **Step 1: Provision Managed PostgreSQL Database**
   - Create a PostgreSQL 16 database instance named `agenttrust-db` on Render.
   - Note the **Internal Database URL** (`postgres://...`).

2. **Step 2: Deploy Backend Web Service (`agenttrust-os-api`)**
   - Create Python Web Service using `render.yaml` or Render Dashboard pointing to repo `https://github.com/Udaytaneja/Agenttrust-os-`.
   - Set environment variables (`DATABASE_URL`, `JWT_SECRET`, `FRONTEND_URL`, `STORAGE_PROVIDER`, `S3_*`).
   - Render runs `alembic upgrade head` during build to provision PostgreSQL schemas automatically.

3. **Step 3: Deploy Frontend Static Site (`agenttrust-os-frontend`)**
   - Create Static Site service pointing to `./frontend/dist`.
   - Set `VITE_API_BASE_URL` to the `agenttrust-os-api` backend URL.

---

## 4. Post-Deployment Smoke Test Script

1. **Unauthenticated Health Checks**:
   - `GET https://agenttrust-os-api.onrender.com/health` -> Expect `{"status": "healthy", "environment": "production"}`
   - `GET https://agenttrust-os-api.onrender.com/api/v1/health` -> Expect `{"status": "healthy", "service": "AgentTrust OS API"}`
2. **Role Routing & Auth Test**:
   - Open `https://agenttrust-os-frontend.onrender.com`. Select Applicant -> Register/Login -> Receive JWT token pair.
3. **Document Upload & Storage Test**:
   - Upload PDF document in Document Center -> Verify `POST /api/v1/documents/upload` returns `201 Created` with persistent UUID.
4. **Persisted AI Perception Test**:
   - Log in as Banker -> Open Document Intelligence -> Inspect uploaded document -> Verify YOLO layout regions and OCR lines render directly from PostgreSQL/Object Storage.

---

## 5. Deployment Rules & Constraints Summary

- **NO Visual Redesign**: Frontend design, styling, and WebGL shaders are 100% preserved.
- **NO Model Modification**: YOLO checkpoint SHA-256 is empirically verified.
- **NO Mock Business Data**: Backend database and AI pipeline are fully connected.
- **NO Automatic Commits/Pushes**: Pushing to remote repository is deferred for explicit user approval.
