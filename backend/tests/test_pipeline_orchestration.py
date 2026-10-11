import asyncio
from unittest.mock import patch

from civic_evidence.config import Settings
from civic_evidence.dependencies import initialize_database


def _prepared_db(tmp_path):
    db_path = tmp_path / "pipeline.db"
    fake_settings = Settings(database_url=f"sqlite:///{db_path}")
    import civic_evidence.dependencies as deps

    deps._engine = None
    deps._SessionLocal = None
    with patch("civic_evidence.dependencies.get_settings", return_value=fake_settings):
        initialize_database()
        assert deps._SessionLocal is not None
        return deps


def test_interview_pipeline_generates_reviewed_report(tmp_path):
    db_path = tmp_path / "pipeline.db"
    fake_settings = Settings(database_url=f"sqlite:///{db_path}")
    with patch("civic_evidence.dependencies.get_settings", return_value=fake_settings):
        import civic_evidence.dependencies as deps

        deps._engine = None
        deps._SessionLocal = None
        initialize_database()

        case_id = "case-pipeline-a"
        audio_asset_id = "asset-pipeline-a"
        with deps._SessionLocal() as db:
            from civic_evidence.models.audio_asset import AudioAsset
            from civic_evidence.models.case import Case

            db.add(Case(id=case_id, title="Interview case", description="desc", consent_recorded=True, status="draft"))
            db.add(
                AudioAsset(
                    id=audio_asset_id,
                    case_id=case_id,
                    filename="clip.wav",
                    content_type="audio/wav",
                    storage_key="demo/clip.wav",
                )
            )
            db.commit()

        from civic_evidence.pipelines.interview_pipeline import run_interview_pipeline

        result = asyncio.run(run_interview_pipeline(case_id, audio_asset_id, "reviewer-1"))
        assert result["transcript"]["status"] == "completed"
        assert result["claims"]
        assert result["report"]["status"] == "finalized"


def test_incident_pipeline_classifies_and_reports(tmp_path):
    db_path = tmp_path / "pipeline.db"
    fake_settings = Settings(database_url=f"sqlite:///{db_path}")
    with patch("civic_evidence.dependencies.get_settings", return_value=fake_settings):
        import civic_evidence.dependencies as deps

        deps._engine = None
        deps._SessionLocal = None
        initialize_database()

        case_id = "case-pipeline-b"
        with deps._SessionLocal() as db:
            from civic_evidence.models.case import Case

            db.add(Case(id=case_id, title="Incident case", description="desc", consent_recorded=True, status="draft"))
            db.commit()

        from civic_evidence.pipelines.incident_pipeline import run_incident_pipeline

        result = asyncio.run(run_incident_pipeline(case_id, "A student was denied access and reported an injury.", "reviewer-1"))
        assert result["classification"] == "safety_incident"
        assert result["report"]["status"] == "finalized"
