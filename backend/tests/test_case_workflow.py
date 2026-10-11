from civic_evidence.schemas.case import CaseCreate
from civic_evidence.services.case_service import CaseService
from civic_evidence.services.claim_service import ClaimService
from civic_evidence.services.report_service import ReportService
from civic_evidence.services.review_service import ReviewService


class DummyModelClient:
    def complete(self, prompt: str) -> str:
        return '[{"claim_text": "A transcript states a line was missed.", "source_segment_id": "segment-1", "status": "unverified", "confidence": 0.87}]'


def test_case_lifecycle_round_trip():
    case = CaseService().create_case(
        payload=CaseCreate(title="Test case", description="Demo case", consent_recorded=True),
        actor_id="user-1",
    )

    assert case.title == "Test case"
    assert case.status == "draft"
    assert len(CaseService().list_cases("user-1")) >= 1
    assert CaseService().get_case(case.id, "user-1").id == case.id


def test_claim_review_and_report_generation():
    created_case = CaseService().create_case(
        payload=CaseCreate(title="Review case", description="Review flow", consent_recorded=True),
        actor_id="user-1",
    )
    claims = ClaimService(model_client=DummyModelClient()).extract_claims(
        case_id=created_case.id,
        transcript_id="transcript-1",
        actor_id="user-1",
    )
    assert len(claims) == 1

    review = ReviewService().record_decision(
        claim_id=claims[0]["id"],
        decision="accepted",
        note="Reviewer approved the extracted claim.",
        reviewer_id="reviewer-1",
    )
    assert review["decision"] == "accepted"

    report = ReportService().generate(case_id=created_case.id, actor_id="user-1")
    assert report.status == "finalized"
    assert report.sections[0].is_testimony is True
