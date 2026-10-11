from ml.src.validation import load_schema, validate


def test_claim_schema_requires_source_segment():
    missing = validate({"claim_text": "x", "status": "unverified"}, "claim.schema.json")
    assert "source_segment_id" in missing


def test_incident_schema_loads():
    schema = load_schema("incident.schema.json")
    assert schema["title"] == "IncidentClassification"
