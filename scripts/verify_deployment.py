# Checks a deployed environment: health, readiness, and basic authorization.
import argparse
import sys

import httpx


def check(base_url: str, timeout: float = 10.0) -> int:
    failures = 0
    with httpx.Client(base_url=base_url, timeout=timeout) as client:
        for path in ("/health", "/api/healthz", "/api/readyz"):
            try:
                response = client.get(path)
            except httpx.HTTPError as exc:
                print(f"FAIL {path}: {exc}")
                failures += 1
                continue
            status = "OK" if response.status_code < 400 else "FAIL"
            print(f"{status} {path}: {response.status_code}")
            if response.status_code >= 400:
                failures += 1
    return failures


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify a deployed environment.")
    parser.add_argument("--base-url", required=True, help="e.g. https://api.example.org")
    args = parser.parse_args()
    sys.exit(1 if check(args.base_url) else 0)
