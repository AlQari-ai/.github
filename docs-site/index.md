---
hide:
  - navigation
---

# ALQari Developer Docs

**ALQari is an Arabic-first Document Intelligence API platform** — OCR, Arabic handwriting recognition, document extraction, validation, chat with documents, and structured JSON output, all over a single REST API.

---

## What you can build

<div class="grid cards" markdown>

-   :material-file-document-scan: **OCR**

    Extract text from printed Arabic & English documents and scanned PDFs.

    [:octicons-arrow-right-24: OCR guide](ocr.md)

-   :material-draw-pen: **Handwriting OCR**

    Recognize Arabic handwritten text from forms, notes, and manuscripts.

    [:octicons-arrow-right-24: OCR guide](ocr.md)

-   :material-table-of-contents: **Extraction**

    Pull structured fields — names, dates, amounts, IDs — as typed JSON.

    [:octicons-arrow-right-24: Extraction guide](extraction.md)

-   :material-check-circle-outline: **Validation**

    Apply business rules and route documents to human review workflows.

    [:octicons-arrow-right-24: Validation guide](validation.md)

-   :material-chat-processing: **Chat**

    Ask natural language questions over any document.

    [:octicons-arrow-right-24: Chat guide](chat.md)

-   :material-magnify: **Search**

    Full-text and semantic search across your document collections.

    [:octicons-arrow-right-24: Search guide](search.md)

-   :material-webhook: **Webhooks**

    Receive real-time push notifications when processing completes.

    [:octicons-arrow-right-24: Webhooks guide](webhooks.md)

</div>

---

## Quickstart (3 steps)

### 1 — Get your API key

Sign up at **[alqari.sa](https://alqari.sa)** → **Dashboard** → **API Keys** → create a new key.

```bash
export ALQARI_API_KEY="your_api_key_here"
```

### 2 — Upload a document

```bash
curl -X POST https://api.alqari.sa/v1/documents \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -F "file=@invoice.pdf"
```

```json
{
  "document_id": "doc_abc123",
  "status": "uploaded",
  "filename": "invoice.pdf"
}
```

### 3 — Run OCR and get structured output

```bash
curl -X POST https://api.alqari.sa/v1/documents/doc_abc123/ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"language": "ar"}'
```

```json
{
  "document_id": "doc_abc123",
  "status": "completed",
  "pages": [
    {
      "page": 1,
      "text": "فاتورة ضريبية\nالرقم: 00123\nالتاريخ: 2026-01-15",
      "confidence": 0.98
    }
  ]
}
```

---

## Base URL

| Environment | URL |
|-------------|-----|
| Production  | `https://api.alqari.sa/v1` |
| Sandbox     | `https://sandbox.api.alqari.sa/v1` |

---

## Resources

| Resource | Link |
|----------|------|
| OpenAPI spec (YAML) | [openapi/openapi.yaml](https://github.com/alqari/alqari-developer-hub/blob/main/openapi/openapi.yaml) |
| OpenAPI spec (JSON) | [openapi/openapi.json](https://github.com/alqari/alqari-developer-hub/blob/main/openapi/openapi.json) |
| Postman collection | [postman/](https://github.com/alqari/alqari-developer-hub/tree/main/postman) |
| cURL examples | [examples/curl/](https://github.com/alqari/alqari-developer-hub/tree/main/examples/curl) |
| Python examples | [examples/python/](https://github.com/alqari/alqari-developer-hub/tree/main/examples/python) |
| Node.js examples | [examples/node/](https://github.com/alqari/alqari-developer-hub/tree/main/examples/node) |
| GitHub repository | [alqari/alqari-developer-hub](https://github.com/alqari/alqari-developer-hub) |
