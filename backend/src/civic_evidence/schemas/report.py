from datetime import datetime

from pydantic import BaseModel


class ReportCitation(BaseModel):
    title: str
    url: str | None = None
    source_id: str | None = None


class ReportSection(BaseModel):
    heading: str
    body: str
    citations: list[ReportCitation] = []
    is_testimony: bool = False


class ReportRead(BaseModel):
    id: str
    case_id: str
    status: str = "draft"
    sections: list[ReportSection] = []
    generated_at: datetime
