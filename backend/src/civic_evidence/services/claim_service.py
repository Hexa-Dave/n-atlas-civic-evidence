# Claim extraction and persistence via the N-ATLAS model.


class ClaimService:
    def __init__(self, db, model_client):
        self.db = db
        self.model_client = model_client

    def extract_claims(self, case_id: str, transcript_id: str, actor_id: str):
        # Validate model output against the claim schema and keep it unverified.
        raise NotImplementedError

    def update_claim(self, claim_id: str, patch, actor_id: str):
        raise NotImplementedError
