# AgentTrust-OS API Contract

## Base URL

All application APIs use:

`/api/v1`

---

## 1. Authentication

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/register` | Register a new account |
| POST | `/auth/login` | Login as User or Banker |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/logout` | Logout |
| GET | `/auth/me` | Get current authenticated account |

---

## 2. User

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/users/me` | Get current user profile |
| PUT | `/users/me` | Update current user profile |

---

## 3. Financial Profile

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/financial/profile` | Get financial profile |
| GET | `/financial/health` | Get financial health |
| GET | `/transactions` | Get transactions |

---

## 4. Trust

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/trust/me` | Get current trust profile |
| GET | `/trust/me/factors` | Get factors affecting trust |

---

## 5. Banker

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/bankers/customers` | Get customers available to banker |
| GET | `/bankers/customers/{customer_id}` | Get customer details |
| GET | `/bankers/applications` | Get customer applications |

---

## 6. Applications

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/applications` | Create application |
| GET | `/applications` | Get applications |
| GET | `/applications/{application_id}` | Get application details |
| PUT | `/applications/{application_id}` | Update application |

---

## 7. Loans

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/loans` | Get loans |
| GET | `/loans/{loan_id}` | Get loan details |

---

## 8. Repayments

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/repayments` | Get repayment information |
| GET | `/repayments/{loan_id}` | Get repayment schedule |

---

## 9. AI

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/ai/chat` | Financial AI assistant |
| POST | `/ai/scenario` | Financial scenario analysis |
| POST | `/ai/risk-analysis` | AI-assisted risk analysis |
| POST | `/ai/underwriting` | AI-assisted underwriting analysis |

---

## 10. Notifications

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/notifications` | Get notifications |
| PUT | `/notifications/{notification_id}/read` | Mark notification as read |

---

## 11. Audit

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/audit/me` | Get account activity history |

---

## API Rules

1. All APIs use `/api/v1`.
2. Backend owns the API implementation.
3. Frontend consumes the API.
4. AI uses approved backend interfaces.
5. API names must not be changed casually.
6. Response structures are defined in `schemas.md`.
7. Shared values are defined in `enums.md`.
8. Authentication and authorization are required where applicable.
9. Sensitive financial information must never be exposed without authorization.
10. Any new API must be discussed and added to this contract before implementation.