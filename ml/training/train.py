# Fine-tuning entry point. Reads configs/finetuning.yaml.
from ml.src.model_registry import register


def main(config_path: str = "ml/configs/finetuning.yaml") -> None:
    raise NotImplementedError("Implement fine-tuning and record the run in the registry.")


if __name__ == "__main__":
    main()
