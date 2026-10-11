# Case lifecycle operations.
from civic_evidence.schemas.case import CaseCreate


class CaseService:
    def __init__(self, db):
        self.db = db

    def create_case(self, payload: CaseCreate, actor_id: str):
        raise NotImplementedError("Persist to the cases table and write an audit event.")

    def list_cases(self, actor_id: str):
        raise NotImplementedError

    def get_case(self, case_id: str, actor_id: str):
        raise NotImplementedError
