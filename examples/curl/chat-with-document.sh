#!/usr/bin/env bash
# chat-with-document.sh — Ask a question about a document
#
# Usage:
#   export ALQARI_API_KEY="your_api_key_here"
#   bash chat-with-document.sh <document_id> "<question>"
#
# Examples:
#   bash chat-with-document.sh doc_abc123 "ما هو رقم الفاتورة؟"
#   bash chat-with-document.sh doc_abc123 "What is the total amount?"

set -euo pipefail

BASE_URL="${ALQARI_BASE_URL:-https://api.alqari.sa/v1}"
DOCUMENT_ID="${1:?Usage: bash chat-with-document.sh <document_id> \"<question>\"}"
MESSAGE="${2:?Please provide a question as the second argument}"

if [[ -z "${ALQARI_API_KEY:-}" ]]; then
  echo "Error: ALQARI_API_KEY environment variable is not set." >&2
  exit 1
fi

echo "Chatting with document: $DOCUMENT_ID"
echo "Question: $MESSAGE"

# Use Python to safely JSON-encode the user message
PAYLOAD=$(python3 -c "
import json, sys
msg = sys.argv[1]
print(json.dumps({'message': msg}))
" "$MESSAGE")

curl --fail-with-body \
  --request POST \
  --url "${BASE_URL}/documents/${DOCUMENT_ID}/chat" \
  --header "Authorization: Bearer ${ALQARI_API_KEY}" \
  --header "Content-Type: application/json" \
  --data "$PAYLOAD" \
  | python3 -m json.tool
