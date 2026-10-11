# Validates model output against the JSON schemas in ml/schemas.
import json
from pathlib import Path

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"


def load_schema(name: str) -> dict:
    return json.loads((SCHEMAS_DIR / name).read_text(encoding="utf-8"))


def validate(record: dict, schema_name: str) -> list[str]:
    # Lightweight structural check. Swap in jsonschema for full validation.
    schema = load_schema(schema_name)
    required = schema.get("required", [])
    return [field for field in required if field not in record]
