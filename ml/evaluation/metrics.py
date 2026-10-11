# Task-appropriate metrics for claim extraction and incident classification.


def prf(tp: int, fp: int, fn: int) -> dict[str, float]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def compute_metrics(gold: list[dict], predicted: list[dict]) -> dict[str, float]:
    # TODO: implement matching by claim identity and measure source attribution.
    raise NotImplementedError
