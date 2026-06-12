# Search

Search across all your processed documents using full-text or semantic (vector) search.

---

## Endpoint

```
POST /search
```

---

## Request Body

```json
{
  "query": "فاتورة ضريبية 2026",
  "mode": "semantic",
  "limit": 10,
  "filters": {
    "tags": ["invoice"],
    "date_range": {
      "from": "2026-01-01",
      "to":   "2026-12-31"
    }
  }
}
```

| Field              | Type     | Default    | Description                                               |
|--------------------|----------|------------|-----------------------------------------------------------|
| `query`            | string   | —          | Search query in Arabic or English                         |
| `mode`             | string   | `semantic` | `fulltext` · `semantic` · `hybrid`                        |
| `limit`            | integer  | `10`       | Max results (1–100)                                       |
| `cursor`           | string   | —          | Pagination cursor from previous response                  |
| `filters.tags`     | string[] | —          | Filter to documents with these tags                       |
| `filters.date_range` | object | —          | `from` and `to` in ISO 8601 date format                   |
| `filters.document_ids` | string[] | —       | Restrict search to specific document IDs                  |

---

## Search Modes

| Mode        | Description                                                     |
|-------------|-----------------------------------------------------------------|
| `fulltext`  | Keyword-based search — fast, exact matches                      |
| `semantic`  | Embedding-based search — finds conceptually similar content     |
| `hybrid`    | Combines fulltext and semantic for best recall and precision    |

---

## Example

```bash
curl -X POST https://api.alqari.sa/v1/search \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "فاتورة ضريبية",
    "mode": "hybrid",
    "limit": 5
  }'
```

---

## Response

```json
{
  "query": "فاتورة ضريبية",
  "mode": "hybrid",
  "results": [
    {
      "document_id": "doc_abc123",
      "filename": "invoice.pdf",
      "score": 0.94,
      "snippet": "...فاتورة ضريبية\nالرقم: INV-00123\nالتاريخ: 2026-01-15...",
      "page": 1,
      "tags": ["invoice", "2026"]
    },
    {
      "document_id": "doc_def456",
      "filename": "receipt_jan.pdf",
      "score": 0.81,
      "snippet": "...إيصال دفع فاتورة رقم 00124...",
      "page": 1,
      "tags": ["receipt"]
    }
  ],
  "total": 2,
  "has_more": false,
  "next_cursor": null
}
```

---

## Notes

- Documents must have completed OCR before they are searchable.
- Semantic search uses multilingual embeddings optimized for Arabic and English.
- Hybrid mode is recommended for most production use cases.
