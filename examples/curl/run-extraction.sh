#!/usr/bin/env bash
# run-extraction.sh — Extract structured fields from a document
#
# Usage:
#   export ALQARI_API_KEY="your_api_key_here"
#   bash run-extraction.sh <document_id>
#
# By default this script uses the built-in "invoice" schema.
# Edit the --data block below to use a custom schema.

set -euo pipefail

BASE_URL="${ALQARI_BASE_URL:-https://api.alqari.sa/v1}"
DOCUMENT_ID="${1:?Usage: bash run-extraction.sh <document_id>}"

if [[ -z "${ALQARI_API_KEY:-}" ]]; then
  echo "Error: ALQARI_API_KEY environment variable is not set." >&2
  exit 1
fi

echo "Running extraction on document: $DOCUMENT_ID"

# ── Option A: Pre-built schema ─────────────────────────────────────────────
curl --fail-with-body \
  --request POST \
  --url "${BASE_URL}/documents/${DOCUMENT_ID}/extraction" \
  --header "Authorization: Bearer ${ALQARI_API_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "schema_id": "invoice"
  }' \
  | python3 -m json.tool

# ── Option B: Custom schema (uncomment and replace Option A above) ─────────
# curl --fail-with-body \
#   --request POST \
#   --url "${BASE_URL}/documents/${DOCUMENT_ID}/extraction" \
#   --header "Authorization: Bearer ${ALQARI_API_KEY}" \
#   --header "Content-Type: application/json" \
#   --data '{
#     "schema": [
#       { "name": "invoice_number", "type": "string" },
#       { "name": "invoice_date",   "type": "date" },
#       { "name": "total_amount",   "type": "number" },
#       { "name": "vendor_name",    "type": "string" }
#     ]
#   }' \
#   | python3 -m json.tool
