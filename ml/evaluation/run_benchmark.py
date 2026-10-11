# Runs base and fine-tuned models on the held-out benchmark under identical settings.
from ml.evaluation.metrics import compute_metrics


def main() -> None:
    raise NotImplementedError("Iterate the benchmark manifest and call compute_metrics.")


if __name__ == "__main__":
    main()
