import json
import logging
import sys
from datetime import datetime
from ai.app.schemas.requests import AuditEventPayload, TelemetryMetadata

logger = logging.getLogger("AgentTrust.AI.Audit")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)


class AIAuditLogger:
    """Emits structured JSON audit events for compliance & monitoring."""

    def log_event(
        self,
        request_id: str,
        actor_id: int | None,
        actor_type: str,
        action: str,
        status: str,
        telemetry: TelemetryMetadata | None = None,
    ) -> AuditEventPayload:
        event = AuditEventPayload(
            event_id=f"evt_{request_id}_{int(datetime.utcnow().timestamp())}",
            request_id=request_id,
            actor_id=actor_id,
            actor_type=actor_type,
            action=action,
            resource="ai_engine",
            status=status,
            telemetry=telemetry,
            timestamp=datetime.utcnow(),
        )

        log_data = event.model_dump(mode="json")
        logger.info(json.dumps(log_data))
        return event


ai_audit_logger = AIAuditLogger()
