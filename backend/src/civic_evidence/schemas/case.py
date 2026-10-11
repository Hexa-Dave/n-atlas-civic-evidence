from datetime import datetime

from pydantic import BaseModel, Field


class CaseBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    consent_recorded: bool = False


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    consent_recorded: bool | None = None
    status: str | None = None


class CaseRead(CaseBase):
    id: str
    status: str = "draft"
    created_at: datetime
