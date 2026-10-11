# Splits normalized documents into citable passages with stable ids.


def extract_passages(document: dict) -> list[dict]:
    raise NotImplementedError("Emit passages carrying source id, section, and text.")
