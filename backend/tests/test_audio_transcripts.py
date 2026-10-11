from io import BytesIO

from civic_evidence.api.v1.audio import upload_audio
from civic_evidence.api.v1.transcripts import start_transcription
from civic_evidence.schemas.case import CaseCreate
from civic_evidence.services.audio_service import AudioService
from civic_evidence.services.case_service import CaseService


class DummyUpload:
    def __init__(self, filename: str, content_type: str, payload: bytes):
        self.filename = filename
        self.content_type = content_type
        self.file = BytesIO(payload)


def test_audio_upload_requires_consent_and_valid_type():
    case = CaseService().create_case(
        payload=CaseCreate(title="Audio case", description="Demo", consent_recorded=True),
        actor_id="user-1",
    )

    asset = AudioService().store_upload(
        case_id=case.id,
        filename="interview.wav",
        content_type="audio/wav",
        stream=BytesIO(b"RIFF....WAV"),
        actor_id="user-1",
    )

    assert asset["filename"] == "interview.wav"
    assert asset["case_id"] == case.id


def test_transcript_creation_uses_audio_asset():
    case = CaseService().create_case(
        payload=CaseCreate(title="Transcript case", description="Demo", consent_recorded=True),
        actor_id="user-1",
    )
    asset = AudioService().store_upload(
        case_id=case.id,
        filename="clip.mp3",
        content_type="audio/mpeg",
        stream=BytesIO(b"ID3\x00\x00\x00"),
        actor_id="user-1",
    )

    transcript = start_transcription(case.id, asset["id"])

    assert transcript["case_id"] == case.id
    assert transcript["audio_asset_id"] == asset["id"]
    assert transcript["status"] == "completed"
