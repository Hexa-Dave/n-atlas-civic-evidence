# Audit trail. Records material actions without copying sensitive content.


class AuditService:
    def __init__(self, db):
        self.db = db

    def record(self, actor_id: str, action: str, resource_type: str, resource_id: str, detail=None):
        # Store identifiers and action metadata only; redact any free text.
        raise NotImplementedError("Persist an audit event.")
