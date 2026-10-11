from ml.src.postprocessing import parse_json_objects


def test_parse_json_list():
    assert parse_json_objects('[{"claim_text": "a", "source_segment_id": "s", "status": "unverified"}]')


def test_parse_invalid_returns_empty():
    assert parse_json_objects("not json") == []
