# AgentTrust-OS Shared Schemas

This file defines the shared data structures used by the Backend, Frontend, and AI modules.

All three modules must use the same field names and data structures.

## User

- id
- name
- email
- phone
- role
- language
- created_at
- updated_at

## Authentication

### Login Request

- email
- password

### Login Response

- access_token
- refresh_token
- token_type
- user

## User Profile

- user_id
- name
- email
- phone
- language
- profile_status

## Financial Profile

- user_id
- income
- expenses
- savings
- assets
- liabilities
- existing_loans

## Financial Health

- user_id
- score
- income
- expenses
- savings
- debt
- repayment_burden
- status
- updated_at

## Transaction

- id
- user_id
- amount
- type
- category
- merchant
- description
- date
- status

## Trust Profile

- user_id
- score
- level
- change
- factors
- updated_at

## Trust Factor

- name
- impact
- value
- description

## Customer

- id
- name
- email
- phone
- trust_profile
- financial_health
- account_status

## Loan Application

- id
- customer_id
- amount
- purpose
- status
- documents
- created_at
- updated_at

## Underwriting

- application_id
- risk_score
- risk_level
- factors
- evidence
- recommendation
- confidence
- human_review_required
- decision

## Loan

- id
- application_id
- customer_id
- principal
- interest_rate
- duration
- outstanding_amount
- status
- start_date
- maturity_date

## Repayment

- id
- loan_id
- amount
- due_date
- paid_date
- status
- payment_reference

## Risk Assessment

- id
- customer_id
- score
- level
- factors
- evidence
- recommendation
- confidence
- created_at

## Fraud Signal

- id
- customer_id
- transaction_id
- type
- severity
- score
- evidence
- status
- created_at

## Agent

- id
- name
- owner_id
- organization_id
- status
- trust_score
- capabilities
- permissions

## Agent Action

- id
- agent_id
- action
- resource
- risk_level
- decision
- reason
- timestamp

## AI Request

- request_id
- user_id
- role
- task
- input
- language
- context

## AI Response

- request_id
- response
- confidence
- reasoning_summary
- evidence
- recommendation
- requires_human_review

## Notification

- id
- recipient_id
- type
- title
- message
- read
- created_at

## Audit Event

- id
- actor_id
- actor_type
- action
- resource
- resource_id
- result
- timestamp

## Standard API Response

- success
- data
- message

## Standard API Error

- error
  - code
  - message
  - details

## Shared Rules

- Backend is the source of truth for financial data.
- Frontend consumes the defined schemas.
- AI uses the defined schemas when communicating with the backend.
- Shared field names must not be changed independently.
- New shared schemas must be agreed upon before implementation.
- Sensitive financial data must only be returned to authorized roles.
- All dates and timestamps must use a consistent ISO 8601 format.
- Currency values must use a consistent representation across the system.
- English and Hindi are supported through the language field.