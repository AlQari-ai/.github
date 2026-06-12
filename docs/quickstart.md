# Quickstart

Get your first OCR result in under 5 minutes.

## Prerequisites

- An ALQari account — [sign up free](https://alqari.sa/signup)
- An API key — [generate one](https://alqari.sa/dashboard/api-keys)
- `curl`, Python 3.8+, or Node.js 18+

---

## Step 1 — Set your API key

```bash
export ALQARI_API_KEY="your_api_key_here"
```

> **Tip:** Add this to your shell profile (`~/.bashrc`, `~/.zshrc`) or use a `.env` file (see [`.env.example`](../.env.example)).

---

## Step 2 — Upload a document

```bash
curl -X POST https://api.alqari.sa/v1/documents \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -F "file=@/path/to/document.pdf"
```

**Response:**

```json
{
  "document_id": "doc_abc123",
  "status": "uploaded",
  "filename": "document.pdf",
  "size_bytes": 204800,
  "created_at": "2026-06-12T10:00:00Z"
}
```

Save the `document_id` — you'll use it in every subsequent request for this document.

---

## Step 3 — Run OCR

```bash
curl -X POST https://api.alqari.sa/v1/documents/doc_abc123/ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"language": "ar"}'
```

**Response:**

```json
{
  "document_id": "doc_abc123",
  "status": "completed",
  "pages": [
    {
      "page": 1,
      "text": "فاتورة ضريبية\nالرقم: 00123\nالتاريخ: 2026-01-15",
      "confidence": 0.98,
      "bounding_boxes": []
    }
  ],
  "completed_at": "2026-06-12T10:00:03Z"
}
```

---

## What's Next?

- Extract structured fields → [Extraction](extraction.md)
- Validate document data → [Validation](validation.md)
- Chat with the document → [Chat](chat.md)
- Search across documents → [Search](search.md)
- Set up webhooks for async processing → [Webhooks](webhooks.md)

---

## Language Support

| Value    | Description                  |
|----------|------------------------------|
| `ar`     | Arabic (printed)             |
| `en`     | English                      |
| `ar+en`  | Arabic and English (mixed)   |
| `ar-hw`  | Arabic handwriting           |
