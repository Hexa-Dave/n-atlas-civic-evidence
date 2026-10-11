from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from civic_evidence.models.case import Base


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"), index=True)
    transcript_id: Mapped[str | None] = mapped_column(
        ForeignKey("transcripts.id"), nullable=True
    )
    source_segment_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    text: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="unverified")
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    model_run_id: Mapped[str | None] = mapped_column(ForeignKey("model_runs.id"), nullable=True)
