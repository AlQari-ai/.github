#!/usr/bin/env bash
# validate-document.sh — Run a validation workflow on a document
#
# Usage:
#   export ALQARI_API_KEY="your_api_key_here"
#   bash validate-document.sh <document_id>

set -euo pipefail

BASE_URL="${ALQARI_BASE_URL:-https://api.alqari.sa/v1}"
DOCUMENT_ID="${1:?Usage: bash validate-document.sh <document_id>}"

if [[ -z "${ALQARI_API_KEY:-}" ]]; then
  echo "Error: ALQARI_API_KEY environment variable is not set." >&2
  exit 1
fi

echo "Running validation on document: $DOCUMENT_ID"

curl --fail-with-body \
  --request POST \
  --url "${BASE_URL}/documents/${DOCUMENT_ID}/validation" \
  --header "Authorization: Bearer ${ALQARI_API_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "rules": [
      { "field": "invoice_number", "rule": "not_null" },
      { "field": "total_amount",   "rule": "greater_than", "value": 0 },
      { "field": "invoice_date",   "rule": "not_null" },
      { "field": "tax_number",     "rule": "regex", "pattern": "^3[0-9]{14}$" }
    ],
    "human_review_on_failure": false
  }' \
  | python3 -m json.tool
