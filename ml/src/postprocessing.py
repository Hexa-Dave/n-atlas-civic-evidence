# Post-processes raw model output into schema-valid records.
import json


def parse_json_objects(raw: str) -> list[dict]:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return []
    if isinstance(parsed, list):
        return [item for item in parsed if isinstance(item, dict)]
    return [parsed] if isinstance(parsed, dict) else []
