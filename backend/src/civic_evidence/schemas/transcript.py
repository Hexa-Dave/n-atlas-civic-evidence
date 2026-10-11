from pydantic import BaseModel


class TranscriptSegment(BaseModel):
    id: str
    speaker: str | None = None
    start_seconds: float | None = None
    end_seconds: float | None = None
    text: str


class TranscriptRead(BaseModel):
    id: str
    case_id: str
    language: str | None = None
    segments: list[TranscriptSegment] = []
