# Speech-to-text orchestration.


class TranscriptionService:
    def __init__(self, db):
        self.db = db

    def transcribe(self, case_id: str, audio_asset_id: str, actor_id: str):
        # Never fabricate a transcript if the speech-to-text path is unavailable.
        raise NotImplementedError("No supported speech-to-text path configured.")
