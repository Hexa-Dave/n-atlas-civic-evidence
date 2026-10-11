# Exports a trained adapter to artifacts/model-adapters.
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def main(output_dir: str = "artifacts/model-adapters") -> dict:
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)

    manifest = {
        "adapter_id": "demo-lora-adapter",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "format": "lora",
        "files": [
            "adapter_config.json",
            "adapter_weights.bin",
        ],
    }
    (target / "adapter_config.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    (target / "adapter_weights.bin").write_bytes(b"stub-adapter")
    return manifest


if __name__ == "__main__":
    main()
