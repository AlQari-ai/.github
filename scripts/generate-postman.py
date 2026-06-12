#!/usr/bin/env python3
"""
generate-postman.py — Generate a Postman collection from the OpenAPI spec.

Requires: openapi/openapi.json to exist (run fetch-openapi.py first).

Output: postman/alqari.postman_collection.json

Usage:
    python scripts/generate-postman.py

This script produces a basic Postman collection. For more advanced features
(pre-request scripts, test scripts, auto-set variables) edit the output manually
or use Postman's own Import → OpenAPI flow.
"""

import json
import sys
from pathlib import Path

REPO_ROOT       = Path(__file__).parent.parent
SPEC_PATH       = REPO_ROOT / "openapi" / "openapi.json"
OUT_PATH        = REPO_ROOT / "postman" / "alqari.postman_collection.json"
BASE_URL_VAR    = "{{ALQARI_BASE_URL}}"


def load_spec(path: Path) -> dict:
    if not path.exists():
        print(f"Error: OpenAPI spec not found at {path}", file=sys.stderr)
        print("Run: python scripts/fetch-openapi.py  to download it first.", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def resolve_ref(spec: dict, ref: str) -> dict:
    parts = ref.lstrip("#/").split("/")
    node = spec
    for part in parts:
        node = node[part]
    return node


def build_item(path: str, method: str, op: dict, spec: dict) -> dict:
    """Build a single Postman request item from an OpenAPI operation."""
    # Replace path params with Postman-style {{PARAM}}
    postman_path = path.lstrip("/")
    path_parts = postman_path.split("/")
    for i, part in enumerate(path_parts):
        if part.startswith("{") and part.endswith("}"):
            var_name = part[1:-1].upper()
            path_parts[i] = f"{{{{{var_name}}}}}"
    postman_path = "/".join(path_parts)

    item: dict = {
        "name": op.get("summary", f"{method.upper()} {path}"),
        "request": {
            "method": method.upper(),
            "header": [],
            "url": {
                "raw": f"{BASE_URL_VAR}/{postman_path}",
                "host": [BASE_URL_VAR],
                "path": path_parts,
            },
            "description": op.get("description", ""),
        },
    }

    # Add Content-Type header for requests with a body
    if method in ("post", "put", "patch"):
        req_body = op.get("requestBody", {})
        content = req_body.get("content", {})
        if "application/json" in content:
            item["request"]["header"].append({"key": "Content-Type", "value": "application/json"})
            # Try to build an example body
            schema = content["application/json"].get("schema", {})
            if "$ref" in schema:
                schema = resolve_ref(spec, schema["$ref"])
            item["request"]["body"] = {
                "mode": "raw",
                "raw": json.dumps(_example_from_schema(schema, spec), ensure_ascii=False, indent=2),
            }

    return item


def _example_from_schema(schema: dict, spec: dict, depth: int = 0) -> object:
    """Recursively build a minimal example value from an OpenAPI schema."""
    if depth > 4:
        return None
    if "$ref" in schema:
        schema = resolve_ref(spec, schema["$ref"])
    t = schema.get("type", "object")
    if t == "object":
        props = schema.get("properties", {})
        return {k: _example_from_schema(v, spec, depth + 1) for k, v in props.items()}
    if t == "array":
        items = schema.get("items", {})
        return [_example_from_schema(items, spec, depth + 1)]
    if t == "string":
        return schema.get("default", schema.get("example", "string_value"))
    if t == "integer":
        return schema.get("default", schema.get("example", 0))
    if t == "number":
        return schema.get("default", schema.get("example", 0.0))
    if t == "boolean":
        return schema.get("default", False)
    return None


def main() -> None:
    spec = load_spec(SPEC_PATH)

    # Group by tag
    tag_items: dict[str, list] = {}
    for path, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method in ("get", "post", "put", "patch", "delete"):
                tags = operation.get("tags", ["General"])
                for tag in tags:
                    tag_items.setdefault(tag, []).append(
                        build_item(path, method, operation, spec)
                    )

    collection = {
        "info": {
            "_postman_id": "alqari-generated",
            "name": spec["info"]["title"],
            "description": spec["info"].get("description", ""),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "auth": {
            "type": "bearer",
            "bearer": [{"key": "token", "value": "{{ALQARI_API_KEY}}", "type": "string"}],
        },
        "item": [
            {"name": tag, "item": items}
            for tag, items in tag_items.items()
        ],
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(collection, f, ensure_ascii=False, indent=2)

    print(f"Generated Postman collection → {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
