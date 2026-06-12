#!/usr/bin/env bash
# upload-document.sh — Upload a document to ALQari
#
# Usage:
#   export ALQARI_API_KEY="your_api_key_here"
#   bash upload-document.sh /path/to/document.pdf
#
# Optional env vars:
#   ALQARI_BASE_URL  (default: https://api.alqari.sa/v1)
#   ALQARI_LANGUAGE  (default: ar)

set -euo pipefail

BASE_URL="${ALQARI_BASE_URL:-https://api.alqari.sa/v1}"
LANGUAGE="${ALQARI_LANGUAGE:-ar}"
FILE_PATH="${1:?Usage: bash upload-document.sh <file_path>}"

if [[ -z "${ALQARI_API_KEY:-}" ]]; then
  echo "Error: ALQARI_API_KEY environment variable is not set." >&2
  exit 1
fi

if [[ ! -f "$FILE_PATH" ]]; then
  echo "Error: File not found: $FILE_PATH" >&2
  exit 1
fi

echo "Uploading: $FILE_PATH"

curl --fail-with-body \
  --request POST \
  --url "${BASE_URL}/documents" \
  --header "Authorization: Bearer ${ALQARI_API_KEY}" \
  --form "file=@${FILE_PATH}" \
  --form "language=${LANGUAGE}" \
  | python3 -m json.tool
