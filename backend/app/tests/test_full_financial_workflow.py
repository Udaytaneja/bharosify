import pytest
from decimal import Decimal
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from backend.app.core.database import AsyncSessionLocal
from backend.app.main import app


@pytest.mark.asyncio
async def test_full_financial_end_to_end_workflow():
    """End-to-end integration test verifying complete database state at every stage."""
    async with AsyncSessionLocal() as session:
        await session.execute(
            text("DELETE FROM users WHERE email IN ('e2e_cust@example.com', 'e2e_banker@example.com');")
        )
        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Step 1: User Registration
        reg_c = await client.post(
            "/api/v1/auth/register",
            json={
                "name": "E2E Customer",
                "email": "e2e_cust@example.com",
                "password": "Password123!",
                "phone": "9876543210",
                "language": "en",
            },
        )
        assert reg_c.status_code == 201
        c_id = reg_c.json()["id"]

        # Step 2: Banker Registration
        reg_b = await client.post(
            "/api/v1/auth/register",
            json={
                "name": "E2E Banker",
                "email": "e2e_banker@example.com",
                "password": "Password123!",
            },
        )
        assert reg_b.status_code == 201
        b_id = reg_b.json()["id"]

    # Promote banker in DB
    async with AsyncSessionLocal() as session:
        await session.execute(text(f"UPDATE users SET role = 'banker' WHERE id = {b_id};"))
        await session.commit()

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Step 3: Login User & Banker
        log_c = await client.post("/api/v1/auth/login", json={"email": "e2e_cust@example.com", "password": "Password123!"})
        hc = {"Authorization": f"Bearer {log_c.json()['access_token']}"}

        log_b = await client.post("/api/v1/auth/login", json={"email": "e2e_banker@example.com", "password": "Password123!"})
        hb = {"Authorization": f"Bearer {log_b.json()['access_token']}"}

        # Step 4: Financial Profile Update
        fp_resp = await client.put(
            "/api/v1/financial/profile",
            json={"income": 12000.00, "expenses": 4000.00, "savings": 15000.00},
            headers=hc,
        )
        assert fp_resp.status_code == 200

        # Direct DB verification
        async with AsyncSessionLocal() as session:
            res_fp = await session.execute(text(f"SELECT income, expenses FROM financial_profiles WHERE user_id = {c_id};"))
            row_fp = res_fp.fetchone()
            assert row_fp.income == Decimal("12000.00")
            assert row_fp.expenses == Decimal("4000.00")

        # Step 5: Transaction Creation
        tx_resp = await client.post(
            "/api/v1/transactions",
            json={"amount": 2500.00, "type": "income", "category": "Salary", "merchant": "Employer Inc"},
            headers=hc,
        )
        assert tx_resp.status_code == 201
        tx_id = tx_resp.json()["id"]

        # Direct DB verification of transaction
        async with AsyncSessionLocal() as session:
            res_tx = await session.execute(text(f"SELECT amount, type FROM transactions WHERE id = {tx_id};"))
            row_tx = res_tx.fetchone()
            assert row_tx.amount == Decimal("2500.00")
            assert row_tx.type == "income"

        # Step 6: Loan Application Submission
        app_resp = await client.post(
            "/api/v1/applications",
            json={"amount": 12000.00, "purpose": "Equipment Purchase"},
            headers=hc,
        )
        assert app_resp.status_code == 201
        app_id = app_resp.json()["id"]

        # Direct DB verification of application & underwriting record
        async with AsyncSessionLocal() as session:
            res_app = await session.execute(text(f"SELECT status, amount FROM loan_applications WHERE id = {app_id};"))
            row_app = res_app.fetchone()
            assert row_app.status == "submitted"
            assert row_app.amount == Decimal("12000.00")

            res_uw = await session.execute(text(f"SELECT application_id, decision FROM underwritings WHERE application_id = {app_id};"))
            row_uw = res_uw.fetchone()
            assert row_uw is not None
            assert row_uw.decision == "review"

        # Step 7: Application State Transitions by Banker (submitted -> under_review -> underwriting -> approved)
        await client.put(f"/api/v1/applications/{app_id}", json={"status": "under_review"}, headers=hb)
        await client.put(f"/api/v1/applications/{app_id}", json={"status": "underwriting"}, headers=hb)
        app_approved = await client.put(f"/api/v1/applications/{app_id}", json={"status": "approved"}, headers=hb)
        assert app_approved.status_code == 200

        # Step 8: DB Verification of Auto-Provisioned Loan and Repayments
        async with AsyncSessionLocal() as session:
            res_loan = await session.execute(text(f"SELECT id, principal, duration, status FROM loans WHERE application_id = {app_id};"))
            row_loan = res_loan.fetchone()
            assert row_loan is not None
            assert row_loan.principal == Decimal("12000.00")
            assert row_loan.status == "active"
            loan_id = row_loan.id

            res_reps = await session.execute(text(f"SELECT amount FROM repayments WHERE loan_id = {loan_id} ORDER BY id ASC;"))
            rows_reps = res_reps.fetchall()
            assert len(rows_reps) == 12

            # MATHEMATICAL ACCURACY VERIFICATION: sum of all installments MUST equal principal exactly!
            total_repayments_sum = sum(r.amount for r in rows_reps)
            assert total_repayments_sum == Decimal("12000.00")

        # Step 9: Payment Processing & Explicit Confirmation
        pay_init = await client.post(
            "/api/v1/payments",
            json={"amount": 1000.00, "payment_reference": "PAY-E2E-100", "idempotency_key": "IDEM-E2E-100"},
            headers=hc,
        )
        assert pay_init.status_code == 201
        pay_id = pay_init.json()["id"]

        pay_conf = await client.post(f"/api/v1/payments/{pay_id}/confirm", headers=hc)
        assert pay_conf.status_code == 200

        # Direct DB verification of payment status
        async with AsyncSessionLocal() as session:
            res_p = await session.execute(text(f"SELECT status, reconciled FROM payments WHERE id = {pay_id};"))
            row_p = res_p.fetchone()
            assert row_p.status == "completed"
            assert row_p.reconciled is True

        # Step 10: Audit Log DB Verification
        async with AsyncSessionLocal() as session:
            res_aud = await session.execute(text(f"SELECT action, resource FROM audit_events WHERE actor_id = {c_id};"))
            actions = [r.action for r in res_aud.fetchall()]
            assert "payment_processed" in actions
            assert "payment_confirmed" in actions

    async with AsyncSessionLocal() as session:
        await session.execute(
            text("DELETE FROM users WHERE email IN ('e2e_cust@example.com', 'e2e_banker@example.com');")
        )
        await session.commit()
