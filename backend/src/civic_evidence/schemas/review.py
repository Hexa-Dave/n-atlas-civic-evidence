from datetime import datetime

from pydantic import BaseModel


class ReviewDecision(BaseModel):
    decision: str
    note: str | None = None


class ReviewEventRead(BaseModel):
    id: str
    claim_id: str
    reviewer_id: str
    decision: str
    note: str | None = None
    created_at: datetime
