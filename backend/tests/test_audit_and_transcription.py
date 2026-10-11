from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from civic_evidence.audit.audit_service import AuditService
from civic_evidence.models.audit_event import AuditEvent
from civic_evidence.models.audio_asset import AudioAsset
from civic_evidence.models.case import Base, Case
from civic_evidence.services.transcription_service import TranscriptionService


def test_audit_service_records_redacted_event():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    with SessionLocal() as db:
        AuditService(db).record(
            "user-1",
            "case_created",
            "case",
            "case-123",
            {"note": "Call 555-123-4567 for the intake desk."},
        )
        row = db.query(AuditEvent).one()
        assert row.actor_id == "user-1"
        assert "555" not in row.detail
        assert "intake" in row.detail.lower()


def test_transcription_service_uses_safe_fallback_and_audit_record():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    with SessionLocal() as db:
        db.add(Case(id="case-123", title="Demo", description="desc", consent_recorded=True))
        db.add(
            AudioAsset(
                id="asset-123",
                case_id="case-123",
                filename="clip.wav",
                content_type="audio/wav",
                storage_key="demo/clip.wav",
            )
        )
        db.commit()

        transcript = TranscriptionService(db).transcribe("case-123", "asset-123", "reviewer-1")
        assert transcript["status"] == "completed"
        assert "fallback" in transcript["text"].lower()
        assert db.query(AuditEvent).count() == 1
