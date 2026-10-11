from pydantic import BaseModel, Field

CLAIM_STATUSES = ("unverified", "accepted", "edited", "rejected", "flagged")


class ClaimRead(BaseModel):
    id: str
    case_id: str
    text: str
    status: str = "unverified"
    source_segment_id: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class ClaimUpdate(BaseModel):
    text: str | None = None
    status: str | None = None
