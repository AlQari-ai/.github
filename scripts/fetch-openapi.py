#!/usr/bin/env python3
"""
fetch-openapi.py — Download the ALQari OpenAPI specification from the live API
and save it locally as both JSON and YAML.

Usage:
    python scripts/fetch-openapi.py

Dependencies (install once):
    pip install requests pyyaml

Environment variables:
    ALQARI_API_KEY   Optional. Sent as a Bearer token when provided.
                     Never printed or logged.
    ALQARI_BASE_URL  Optional. Override the API root.
                     Defaults to https://api.alqari.sa

The script probes candidate URLs in order and uses the first one that returns a
valid OpenAPI document (JSON containing "openapi", "info", and "paths").

Output files:
    openapi/openapi.json
    openapi/openapi.yaml
"""

import sys
import os
import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency check — give a clear message before hitting an ImportError
# ---------------------------------------------------------------------------
try:
    import requests
except ImportError:
    print(
        "Missing dependency: requests\n"
        "Install with:  pip install requests pyyaml",
        file=sys.stderr,
    )
    sys.exit(1)

try:
    import yaml
except ImportError:
    print(
        "Missing dependency: pyyaml\n"
        "Install with:  pip install requests pyyaml",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REPO_ROOT   = Path(__file__).resolve().parent.parent
OPENAPI_DIR = REPO_ROOT / "openapi"
TIMEOUT     = 15  # seconds per request

_base = os.environ.get("ALQARI_BASE_URL", "https://api.alqari.sa").rstrip("/")
# Strip any /v1 suffix so we probe the API root, not a versioned path
if _base.endswith("/v1"):
    _base = _base[:-3]

CANDIDATE_URLS: list[str] = [
    f"{_base}/openapi.json",
    f"{_base}/api/openapi.json",
    f"{_base}/swagger.json",
    f"{_base}/docs/openapi.json",
]

REQUIRED_KEYS = {"openapi", "info", "paths"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _auth_headers() -> dict[str, str]:
    """Return Authorization header only when ALQARI_API_KEY is set.
    The key value is never echoed to stdout or stderr."""
    key = os.environ.get("ALQARI_API_KEY", "").strip()
    if key:
        return {"Authorization": f"Bearer {key}"}
    return {}


def _try_fetch(url: str) -> dict | None:
    """
    Attempt to GET *url* and parse the response as JSON.
    Returns the parsed dict if it looks like a valid OpenAPI document,
    otherwise returns None (never raises).
    """
    headers = {
        "Accept": "application/json",
        "User-Agent": "alqari-developer-hub/fetch-openapi",
        **_auth_headers(),
    }
    try:
        resp = requests.get(url, headers=headers, timeout=TIMEOUT)
    except requests.exceptions.ConnectionError:
        print(f"  [skip] Cannot connect to {url}")
        return None
    except requests.exceptions.Timeout:
        print(f"  [skip] Timed out after {TIMEOUT}s — {url}")
        return None
    except requests.exceptions.RequestException as exc:
        print(f"  [skip] Request error ({exc.__class__.__name__}): {url}")
        return None

    if resp.status_code != 200:
        print(f"  [skip] HTTP {resp.status_code} — {url}")
        return None

    content_type = resp.headers.get("Content-Type", "")
    if "json" not in content_type and "yaml" not in content_type and "text" not in content_type:
        print(f"  [skip] Unexpected Content-Type '{content_type}' — {url}")
        return None

    try:
        spec = resp.json()
    except ValueError:
        print(f"  [skip] Response is not valid JSON — {url}")
        return None

    missing = REQUIRED_KEYS - spec.keys()
    if missing:
        print(f"  [skip] Missing required keys {missing} — {url}")
        return None

    print(f"  [ok]   {url}")
    return spec


def _count_operations(paths: dict) -> int:
    http_methods = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
    count = 0
    for path_item in paths.values():
        if isinstance(path_item, dict):
            count += sum(1 for m in path_item if m.lower() in http_methods)
    return count


def _collect_tags(spec: dict) -> list[str]:
    """Collect tag names from the top-level tags array, falling back to
    operation-level tags when the top-level array is absent."""
    if top_tags := spec.get("tags"):
        return [t.get("name", "") for t in top_tags if isinstance(t, dict)]

    seen: list[str] = []
    for path_item in spec.get("paths", {}).values():
        if not isinstance(path_item, dict):
            continue
        for operation in path_item.values():
            if not isinstance(operation, dict):
                continue
            for tag in operation.get("tags", []):
                if tag not in seen:
                    seen.append(tag)
    return seen


def _print_summary(spec: dict) -> None:
    info    = spec.get("info", {})
    title   = info.get("title", "(no title)")
    version = info.get("version", "(no version)")
    paths   = spec.get("paths", {})
    n_paths = len(paths)
    n_ops   = _count_operations(paths)
    tags    = _collect_tags(spec)

    print()
    print("=" * 56)
    print("  OpenAPI Specification Summary")
    print("=" * 56)
    print(f"  Title      : {title}")
    print(f"  Version    : {version}")
    print(f"  Paths      : {n_paths}")
    print(f"  Operations : {n_ops}")
    if tags:
        print(f"  Tags       : {', '.join(tags)}")
    else:
        print("  Tags       : (none defined)")
    print("=" * 56)
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("Probing candidate OpenAPI URLs …\n")
    for url in CANDIDATE_URLS:
        spec = _try_fetch(url)
        if spec is not None:
            break
    else:
        print(
            "\nError: Could not find a valid OpenAPI specification at any of "
            "the following URLs:\n" + "\n".join(f"  - {u}" for u in CANDIDATE_URLS) +
            "\n\nCheck that the API server is reachable and that the docs are "
            "published at one of the paths above.",
            file=sys.stderr,
        )
        sys.exit(1)

    OPENAPI_DIR.mkdir(parents=True, exist_ok=True)

    # ── Save JSON ──────────────────────────────────────────────────────────
    json_path = OPENAPI_DIR / "openapi.json"
    json_path.write_text(
        json.dumps(spec, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Saved  → {json_path.relative_to(REPO_ROOT)}")

    # ── Save YAML ──────────────────────────────────────────────────────────
    yaml_path = OPENAPI_DIR / "openapi.yaml"
    yaml_path.write_text(
        yaml.dump(spec, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )
    print(f"Saved  → {yaml_path.relative_to(REPO_ROOT)}")

    # ── Summary ────────────────────────────────────────────────────────────
    _print_summary(spec)
    print("Done. Review the files in openapi/ and commit if they look correct.")


if __name__ == "__main__":
    main()
