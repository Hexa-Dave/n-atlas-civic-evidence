# Incident-report pipeline: text report -> claims/classification -> review -> report.


async def run_incident_pipeline(case_id: str, report_text: str, actor_id: str) -> dict:
    steps = ["classify_incident", "extract_claims", "await_review", "assemble_report"]
    raise NotImplementedError(
        "Wire these steps through the corresponding services. Steps: " + ", ".join(steps)
    )
