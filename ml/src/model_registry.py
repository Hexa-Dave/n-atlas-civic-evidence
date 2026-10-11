# Tracks the exact model identifiers and adapters used for each run.

_REGISTRY: dict[str, dict] = {}


def register(name: str, model_id: str, version: str, adapter_path: str | None = None) -> dict:
    entry = {"name": name, "model_id": model_id, "version": version, "adapter_path": adapter_path}
    _REGISTRY[name] = entry
    return entry


def get(name: str) -> dict:
    if name not in _REGISTRY:
        raise KeyError(f"Unknown model entry: {name}")
    return _REGISTRY[name]
