"""
validate_document.py — Run a validation workflow on a document.

Usage:
    python validate_document.py <document_id>

Environment variables:
    ALQARI_API_KEY   Required.
    ALQARI_BASE_URL  Optional. Defaults to https://api.alqari.sa/v1
"""

import os
import sys
import json
import requests

BASE_URL = os.environ.get("ALQARI_BASE_URL", "https://api.alqari.sa/v1").rstrip("/")

# Edit these rules to match your validation requirements
VALIDATION_RULES = [
    {"field": "invoice_number", "rule": "not_null"},
    {"field": "total_amount",   "rule": "greater_than", "value": 0},
    {"field": "invoice_date",   "rule": "not_null"},
    {"field": "tax_number",     "rule": "regex", "pattern": "^3[0-9]{14}$"},
]


def get_api_key() -> str:
    key = os.environ.get("ALQARI_API_KEY")
    if not key:
        print("Error: ALQARI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return key


def validate_document(document_id: str, human_review_on_failure: bool = False) -> dict:
    api_key = get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "rules": VALIDATION_RULES,
        "human_review_on_failure": human_review_on_failure,
    }
    resp = requests.post(
        f"{BASE_URL}/documents/{document_id}/validation",
        headers=headers,
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python validate_document.py <document_id>", file=sys.stderr)
        sys.exit(1)

    document_id = sys.argv[1]
    print(f"Running validation on document: {document_id}")
    result = validate_document(document_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    status = result.get("status")
    if status == "passed":
        print("\n✓ Validation passed.")
    elif status == "pending_review":
        print(f"\n⚠ Sent for human review: {result.get('review_url')}")
    else:
        print(f"\n✗ Validation status: {status}")


if __name__ == "__main__":
    main()
