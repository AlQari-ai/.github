"""
run_extraction.py — Extract structured fields from a document.

Usage:
    python run_extraction.py <document_id> [schema_id]

    schema_id: invoice (default) | national_id_sa | iqama | passport | bank_statement

    To use a custom schema, edit the CUSTOM_SCHEMA list below and pass "custom" as schema_id.

Environment variables:
    ALQARI_API_KEY   Required.
    ALQARI_BASE_URL  Optional. Defaults to https://api.alqari.sa/v1
"""

import os
import sys
import json
import requests

BASE_URL = os.environ.get("ALQARI_BASE_URL", "https://api.alqari.sa/v1").rstrip("/")

# Edit this list to define a custom extraction schema
CUSTOM_SCHEMA = [
    {"name": "invoice_number", "type": "string", "description": "Invoice or reference number"},
    {"name": "invoice_date",   "type": "date",   "description": "Date on the invoice"},
    {"name": "total_amount",   "type": "number", "description": "Total amount due"},
    {"name": "vendor_name",    "type": "string", "description": "Name of the issuing vendor"},
    {"name": "tax_number",     "type": "string", "description": "VAT/tax registration number"},
]


def get_api_key() -> str:
    key = os.environ.get("ALQARI_API_KEY")
    if not key:
        print("Error: ALQARI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return key


def run_extraction(document_id: str, schema_id: str = "invoice") -> dict:
    api_key = get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    if schema_id == "custom":
        payload = {"schema": CUSTOM_SCHEMA}
    else:
        payload = {"schema_id": schema_id}

    resp = requests.post(
        f"{BASE_URL}/documents/{document_id}/extraction",
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python run_extraction.py <document_id> [schema_id]", file=sys.stderr)
        sys.exit(1)

    document_id = sys.argv[1]
    schema_id = sys.argv[2] if len(sys.argv) > 2 else "invoice"

    print(f"Running extraction on document: {document_id} (schema: {schema_id})")
    result = run_extraction(document_id, schema_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
