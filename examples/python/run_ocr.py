"""
run_ocr.py — Run OCR on an uploaded document.

Usage:
    python run_ocr.py <document_id> [language]

    language: ar (default) | en | ar+en | ar-hw (handwriting)

Environment variables:
    ALQARI_API_KEY   Required.
    ALQARI_BASE_URL  Optional. Defaults to https://api.alqari.sa/v1
"""

import os
import sys
import json
import requests

BASE_URL = os.environ.get("ALQARI_BASE_URL", "https://api.alqari.sa/v1").rstrip("/")


def get_api_key() -> str:
    key = os.environ.get("ALQARI_API_KEY")
    if not key:
        print("Error: ALQARI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return key


def run_ocr(document_id: str, language: str = "ar") -> dict:
    api_key = get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "language": language,
        "detect_orientation": True,
        "handwriting": language == "ar-hw",
    }
    resp = requests.post(
        f"{BASE_URL}/documents/{document_id}/ocr",
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python run_ocr.py <document_id> [language]", file=sys.stderr)
        sys.exit(1)

    document_id = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "ar"

    print(f"Running OCR on document: {document_id} (language: {language})")
    result = run_ocr(document_id, language)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
