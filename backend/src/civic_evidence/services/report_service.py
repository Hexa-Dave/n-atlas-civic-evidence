# Report assembly. Testimony and civic guidance stay in separate sections.


class ReportService:
    def __init__(self, db):
        self.db = db

    def generate(self, case_id: str, actor_id: str):
        # Refuse to finalize a report with zero human-reviewed claims.
        raise NotImplementedError
