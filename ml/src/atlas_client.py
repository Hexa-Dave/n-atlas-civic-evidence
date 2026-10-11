# HTTP client wrapper for N-ATLAS model access.
import os

import httpx


class AtlasClient:
    def __init__(self, base_url=None, api_key=None, model_id=None, timeout=None):
        self.base_url = base_url or os.environ.get("N_ATLAS_BASE_URL", "")
        self.api_key = api_key or os.environ.get("N_ATLAS_API_KEY", "")
        self.model_id = model_id or os.environ.get("N_ATLAS_MODEL_ID", "")
        self.timeout = timeout or float(os.environ.get("N_ATLAS_TIMEOUT_SECONDS", "60"))

    def complete(self, prompt: str, **params) -> str:
        if not self.base_url or not self.model_id:
            raise RuntimeError("N-ATLAS endpoint is not configured; refusing to fabricate output.")
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        payload = {"model": self.model_id, "prompt": prompt, **params}
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        return data.get("output", "")
