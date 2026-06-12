# Upload Documents

Upload a file to ALQari to make it available for OCR, extraction, chat, and search.

---

## Endpoint

```
POST /documents
```

**Content-Type:** `multipart/form-data`

---

## Supported File Types

| Format       | Extension(s)         | Notes                              |
|--------------|----------------------|------------------------------------|
| PDF          | `.pdf`               | Scanned and native/searchable      |
| Image        | `.jpg`, `.jpeg`, `.png`, `.tiff`, `.webp` | Single-page images |
| Word         | `.docx`              | Text and embedded images           |
| Text         | `.txt`               | Plain UTF-8 text                   |

Maximum file size: **50 MB**

---

## Request Parameters

| Parameter        | Type     | Required | Description                                             |
|------------------|----------|----------|---------------------------------------------------------|
| `file`           | file     | Yes      | The document file                                       |
| `language`       | string   | No       | Hint for OCR language: `ar`, `en`, `ar+en`, `ar-hw`. Default: `ar` |
| `tags`           | string[] | No       | Custom tags for organization (e.g., `["invoice","2026"]`) |
| `metadata`       | object   | No       | Arbitrary key-value metadata stored with the document   |
| `webhook_url`    | string   | No       | URL to notify when async processing completes           |

---

## Example

```bash
curl -X POST https://api.alqari.sa/v1/documents \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -F "file=@invoice.pdf" \
  -F "language=ar" \
  -F 'tags=["invoice","2026"]'
```

---

## Response

```json
{
  "document_id": "doc_abc123",
  "status": "uploaded",
  "filename": "invoice.pdf",
  "size_bytes": 204800,
  "mime_type": "application/pdf",
  "page_count": 3,
  "language_hint": "ar",
  "tags": ["invoice", "2026"],
  "metadata": {},
  "created_at": "2026-06-12T10:00:00Z"
}
```

---

## Document Statuses

| Status        | Description                                      |
|---------------|--------------------------------------------------|
| `uploaded`    | File received, not yet processed                 |
| `processing`  | OCR or extraction is running                     |
| `completed`   | All requested processing is done                 |
| `failed`      | Processing failed — see `error` field            |

---

## Get a Document

```bash
curl https://api.alqari.sa/v1/documents/doc_abc123 \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

---

## List Documents

```bash
curl "https://api.alqari.sa/v1/documents?limit=20" \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

---

## Delete a Document

```bash
curl -X DELETE https://api.alqari.sa/v1/documents/doc_abc123 \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

Deleted documents are permanently removed and cannot be recovered. OCR and extraction results are also deleted.
