#!/usr/bin/env bash
# run-ocr.sh — Run OCR on an uploaded document
#
# Usage:
#   export ALQARI_API_KEY="your_api_key_here"
#   bash run-ocr.sh <document_id> [language]
#
# Examples:
#   bash run-ocr.sh doc_abc123
#   bash run-ocr.sh doc_abc123 ar-hw    # Arabic handwriting
#   bash run-ocr.sh doc_abc123 ar+en    # Mixed Arabic/English

set -euo pipefail

BASE_URL="${ALQARI_BASE_URL:-https://api.alqari.sa/v1}"
DOCUMENT_ID="${1:?Usage: bash run-ocr.sh <document_id> [language]}"
LANGUAGE="${2:-ar}"

if [[ -z "${ALQARI_API_KEY:-}" ]]; then
  echo "Error: ALQARI_API_KEY environment variable is not set." >&2
  exit 1
fi

HANDWRITING="false"
if [[ "$LANGUAGE" == "ar-hw" ]]; then
  HANDWRITING="true"
fi

echo "Running OCR on document: $DOCUMENT_ID (language: $LANGUAGE)"

curl --fail-with-body \
  --request POST \
  --url "${BASE_URL}/documents/${DOCUMENT_ID}/ocr" \
  --header "Authorization: Bearer ${ALQARI_API_KEY}" \
  --header "Content-Type: application/json" \
  --data "{
    \"language\": \"${LANGUAGE}\",
    \"detect_orientation\": true,
    \"handwriting\": ${HANDWRITING}
  }" \
  | python3 -m json.tool
