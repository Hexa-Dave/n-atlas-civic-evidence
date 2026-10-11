# End-to-end interview pipeline: audio -> transcript -> claims -> review -> report.


async def run_interview_pipeline(case_id: str, audio_asset_id: str, actor_id: str) -> dict:
    steps = ["transcribe", "extract_claims", "await_review", "assemble_report"]
    raise NotImplementedError(
        "Wire these steps through the corresponding services. Steps: " + ", ".join(steps)
    )
