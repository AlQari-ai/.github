#!/usr/bin/env python3
"""
generate-docs-from-openapi.py — Generate Markdown documentation stubs from the OpenAPI spec.

Reads openapi/openapi.json and writes a docs/generated/ directory with one Markdown file
per tag, listing all operations with their paths, descriptions, and parameter tables.

Usage:
    python scripts/generate-docs-from-openapi.py
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SPEC_PATH = REPO_ROOT / "openapi" / "openapi.json"
OUT_DIR   = REPO_ROOT / "docs" / "generated"


def load_spec(path: Path) -> dict:
    if not path.exists():
        print(f"Error: OpenAPI spec not found at {path}", file=sys.stderr)
        print("Run: python scripts/fetch-openapi.py  to download it first.", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def resolve_ref(spec: dict, ref: str) -> dict:
    """Resolve a $ref pointer (supports #/components/... only)."""
    parts = ref.lstrip("#/").split("/")
    node = spec
    for part in parts:
        node = node[part]
    return node


def get_params(operation: dict, spec: dict) -> list[dict]:
    params = operation.get("parameters", [])
    resolved = []
    for p in params:
        if "$ref" in p:
            p = resolve_ref(spec, p["$ref"])
        resolved.append(p)
    return resolved


def render_operation(path: str, method: str, op: dict, spec: dict) -> str:
    lines = []
    lines.append(f"### `{method.upper()} {path}`")
    lines.append("")
    if summary := op.get("summary"):
        lines.append(f"**{summary}**")
        lines.append("")
    if desc := op.get("description"):
        lines.append(desc)
        lines.append("")

    params = get_params(op, spec)
    if params:
        lines.append("**Path / Query Parameters**")
        lines.append("")
        lines.append("| Name | In | Required | Type | Description |")
        lines.append("|------|----|----------|------|-------------|")
        for p in params:
            schema = p.get("schema", {})
            ptype = schema.get("type", "string")
            required = "Yes" if p.get("required") else "No"
            desc = p.get("description", "")
            lines.append(f"| `{p['name']}` | {p['in']} | {required} | {ptype} | {desc} |")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    spec = load_spec(SPEC_PATH)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Group operations by tag
    tag_ops: dict[str, list] = {}
    for path, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method in ("get", "post", "put", "patch", "delete"):
                tags = operation.get("tags", ["General"])
                for tag in tags:
                    tag_ops.setdefault(tag, []).append((path, method, operation))

    for tag, operations in tag_ops.items():
        filename = tag.lower().replace(" ", "-") + ".md"
        out_path = OUT_DIR / filename
        lines = [f"# {tag}", "", f"> Auto-generated from `openapi/openapi.json`. Do not edit manually.", ""]

        for path, method, op in operations:
            lines.append(render_operation(path, method, op, spec))

        out_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  Generated → {out_path.relative_to(REPO_ROOT)}")

    print(f"\nDone. {len(tag_ops)} files written to docs/generated/")


if __name__ == "__main__":
    main()
