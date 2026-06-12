"""
upload_document.py — Upload a document to ALQari.

Usage:
    python upload_document.py /path/to/document.pdf

Environment variables:
    ALQARI_API_KEY   Required. Your ALQari API key.
    ALQARI_BASE_URL  Optional. Defaults to https://api.alqari.sa/v1
    ALQARI_LANGUAGE  Optional. OCR language hint (ar, en, ar+en, ar-hw). Defaults to ar.
"""

import os
import sys
import json
import requests

BASE_URL = os.environ.get("ALQARI_BASE_URL", "https://api.alqari.sa/v1").rstrip("/")
LANGUAGE = os.environ.get("ALQARI_LANGUAGE", "ar")


def get_api_key() -> str:
    key = os.environ.get("ALQARI_API_KEY")
    if not key:
        print("Error: ALQARI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return key


def upload_document(file_path: str) -> dict:
    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}"}

    with open(file_path, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/documents",
            headers=headers,
            files={"file": (os.path.basename(file_path), f)},
            data={"language": LANGUAGE},
            timeout=60,
        )

    resp.raise_for_status()
    return resp.json()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python upload_document.py <file_path>", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Uploading: {file_path}")
    result = upload_document(file_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nDocument ID: {result.get('document_id')}")


if __name__ == "__main__":
    main()
