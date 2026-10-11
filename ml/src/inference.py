# Runs a task through the N-ATLAS model using a versioned prompt.
from pathlib import Path

from ml.src.atlas_client import AtlasClient

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def load_prompt(task: str) -> str:
    return (PROMPTS_DIR / f"{task}.txt").read_text(encoding="utf-8")


def run_task(task: str, context: dict, client: AtlasClient | None = None) -> str:
    template = load_prompt(task)
    for key, value in context.items():
        template = template.replace("{{" + key + "}}", str(value))
    return (client or AtlasClient()).complete(template)
