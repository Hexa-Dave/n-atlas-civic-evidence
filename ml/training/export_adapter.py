# Exports a trained adapter to artifacts/model-adapters.
from pathlib import Path


def main(output_dir: str = "artifacts/model-adapters") -> None:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    raise NotImplementedError("Write adapter files and a metadata manifest here.")


if __name__ == "__main__":
    main()
