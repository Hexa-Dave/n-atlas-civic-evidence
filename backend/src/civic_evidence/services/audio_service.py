# Audio ingestion: validation, hashing, and storage delegation.


class AudioService:
    def __init__(self, db, storage):
        self.db = db
        self.storage = storage

    def store_upload(self, case_id: str, filename: str, content_type: str, stream, actor_id: str):
        raise NotImplementedError("Validate size/content-type/consent, then store.")
