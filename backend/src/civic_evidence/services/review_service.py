# Human review workflow.


class ReviewService:
    def __init__(self, db):
        self.db = db

    def record_decision(self, claim_id: str, decision: str, note: str | None, reviewer_id: str):
        # Verify the reviewer has authorization before writing a review event.
        raise NotImplementedError

    def reviewed_claim_ids(self, case_id: str) -> set[str]:
        raise NotImplementedError
