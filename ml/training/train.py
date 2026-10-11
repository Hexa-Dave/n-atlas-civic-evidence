# Fine-tuning entry point. Reads configs/finetuning.yaml.
from __future__ import annotations

import os
from pathlib import Path

import yaml

from ml.src.model_registry import register


def _resolve_config(path: str | Path) -> dict:
    config_path = Path(path)
    if not config_path.exists():
        return {}
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if isinstance(data, dict):
        if "base_model" in data and data["base_model"] == "${N_ATLAS_MODEL_ID}":
            data["base_model"] = os.environ.get("N_ATLAS_MODEL_ID", "demo-model")
    return data


def main(config_path: str = "ml/configs/finetuning.yaml") -> dict:
    config = _resolve_config(config_path)
    name = config.get("name") or "default-finetune"
    model_id = config.get("base_model") or os.environ.get("N_ATLAS_MODEL_ID", "demo-model")
    version = config.get("version") or "0.1.0"
    adapter_dir = config.get("output_dir") or "artifacts/model-adapters"
    Path(adapter_dir).mkdir(parents=True, exist_ok=True)
    return register(name=name, model_id=model_id, version=version, adapter_path=str(adapter_dir))


if __name__ == "__main__":
    main()
