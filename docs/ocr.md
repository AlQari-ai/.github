# OCR

Extract text from scanned, photographed, or printed Arabic and English documents — including Arabic handwriting.

---

## Endpoint

```
POST /documents/{document_id}/ocr
```

---

## Request Body

```json
{
  "language": "ar",
  "detect_orientation": true,
  "handwriting": false
}
```

| Field                | Type    | Default | Description                                                |
|----------------------|---------|---------|------------------------------------------------------------|
| `language`           | string  | `ar`    | `ar` · `en` · `ar+en` · `ar-hw` (Arabic handwriting)      |
| `detect_orientation` | boolean | `true`  | Auto-rotate pages to correct orientation                   |
| `handwriting`        | boolean | `false` | Enable Arabic handwriting recognition (`ar-hw`)            |
| `pages`              | int[]   | all     | Specific pages to process, e.g. `[1, 2]`                  |

---

## Example — Printed Arabic

```bash
curl -X POST https://api.alqari.sa/v1/documents/doc_abc123/ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "ar",
    "detect_orientation": true
  }'
```

## Example — Arabic Handwriting

```bash
curl -X POST https://api.alqari.sa/v1/documents/doc_abc123/ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "ar-hw",
    "handwriting": true
  }'
```

---

## Response

The response is returned synchronously when processing completes. A real example from a scanned Arabic handwritten document:

```json
{
  "document_id": "a5aa5d2b-c63d-4645-8ad3-8b142bcfb57c",
  "file_name": "sample-ar-handwriting.jpg",
  "status": "completed",
  "processing_time": 5.356,
  "total_words": 398,
  "created_at": "2026-06-06T14:03:33",
  "download_urls": {
    "original":   "https://api.alqari.sa/services/ocr-history/{document_id}/download/original",
    "ocr":        "https://api.alqari.sa/services/ocr-history/{document_id}/download/ocr",
    "markdown":   "https://api.alqari.sa/services/ocr-history/{document_id}/download/markdown",
    "html":       "https://api.alqari.sa/services/ocr-history/{document_id}/download/html",
    "blocks":     "https://api.alqari.sa/services/ocr-history/{document_id}/download/blocks"
  },
  "ocr_url":      "https://api.alqari.sa/services/ocr-output/{document_id}/ocr",
  "markdown_url": "https://api.alqari.sa/services/ocr-output/{document_id}/markdown",
  "html_url":     "https://api.alqari.sa/services/ocr-output/{document_id}/html",
  "blocks_url":   "https://api.alqari.sa/services/ocr-output/{document_id}/blocks",
  "metadata": {
    "pages": 1,
    "blocks": 9,
    "tables": 0,
    "figures": 0
  },
  "ocr_output": {
    "ocr": [
      {
        "bbox": [[614, 298], [1494, 298], [1494, 394], [614, 394]],
        "text": "الأمية معوقة للتنمية في كل المجالات",
        "confidence": 0.7835
      },
      {
        "bbox": [[1327, 444], [1879, 444], [1879, 554], [1327, 554]],
        "text": "١/ الأمية وأسبابها :.",
        "confidence": 0.7012
      },
      {
        "bbox": [[0, 892], [1906, 892], [1906, 2768], [0, 2768]],
        "text": "الأمية لغة هى نسبة إلى الأم وتعنى بقاء الشخص على ما ولدته أمه عليه...",
        "confidence": 0.7146
      }
    ],
    "layout": {
      "pages": 1,
      "blocks": [
        {
          "id": 1,
          "bbox": [614, 298, 1494, 394],
          "conf": 0.7835,
          "page": 1,
          "text": "الأمية معوقة للتنمية في كل المجالات",
          "raw_label": "title",
          "block_type": "heading_1"
        },
        {
          "id": 2,
          "bbox": [1327, 444, 1879, 554],
          "conf": 0.7012,
          "page": 1,
          "text": "١/ الأمية وأسبابها :.",
          "raw_label": "paragraph",
          "block_type": "paragraph"
        }
      ],
      "tables": [],
      "figures": [],
      "page_sizes": { "1": [1956, 3167] }
    }
  },
  "markdown": "## الأمية معوقة للتنمية في كل المجالات\n\n١/ الأمية وأسبابها :...\n"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `document_id` | string | Unique document identifier (UUID) |
| `file_name` | string | Original uploaded filename |
| `status` | string | `completed` · `processing` · `failed` |
| `processing_time` | number | Seconds taken to process |
| `total_words` | integer | Total word count across all pages |
| `created_at` | string | ISO 8601 timestamp |
| `download_urls` | object | Pre-signed download URLs for each output format |
| `ocr_url` | string | Direct URL to raw OCR JSON output |
| `markdown_url` | string | Direct URL to Markdown output |
| `html_url` | string | Direct URL to HTML output |
| `blocks_url` | string | Direct URL to block-level JSON |
| `metadata` | object | Page count, block count, table count, figure count |
| `ocr_output.ocr` | array | Per-block OCR results (see below) |
| `ocr_output.layout` | object | Layout analysis with typed block classification |
| `markdown` | string | Full document as Markdown |

### OCR Block Fields

Each entry in `ocr_output.ocr`:

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | Extracted text for this block |
| `confidence` | number | Confidence score 0.0–1.0 |
| `bbox` | array | Four corner coordinates `[[x1,y1],[x2,y1],[x2,y2],[x1,y2]]` |

### Layout Block Types

Each entry in `ocr_output.layout.blocks`:

| Field | Description |
|-------|-------------|
| `id` | Block index |
| `bbox` | `[x1, y1, x2, y2]` in pixels |
| `conf` | Confidence 0.0–1.0 |
| `page` | Page number (1-indexed) |
| `text` | Extracted text |
| `raw_label` | Raw model label: `title` · `paragraph` · `pageFooter` |
| `block_type` | Normalized type: `heading_1` · `paragraph` · `page_footer` |

### Download Formats

| Format | Description |
|--------|-------------|
| `original` | The original uploaded file |
| `ocr` | Raw OCR output as JSON |
| `markdown` | Document as Markdown (headings preserved) |
| `html` | Document as HTML with semantic structure |
| `blocks` | Interactive block viewer HTML |
| `extraction` | Structured field extraction (if run) |

---

## Get OCR Result

Retrieve a previously run OCR result:

```bash
curl https://api.alqari.sa/v1/documents/doc_abc123/ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

---

## Asynchronous Processing

For multi-page documents the OCR job runs asynchronously. Poll the `GET` endpoint until `status` is `completed` or `failed`, or use [webhooks](webhooks.md) to receive a push notification.

---

## Confidence Scores

The `confidence` field (0.0–1.0) indicates OCR accuracy per page and per word:

| Range     | Meaning                     |
|-----------|-----------------------------|
| 0.95–1.00 | Excellent — reliable        |
| 0.80–0.94 | Good — minor corrections may be needed |
| 0.60–0.79 | Fair — review recommended   |
| < 0.60    | Low — manual review required |

---

## Searchable PDF Output

After OCR, the document is automatically indexed for [search](search.md). You can also retrieve a searchable PDF:

```bash
curl https://api.alqari.sa/v1/documents/doc_abc123/ocr/pdf \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  --output searchable.pdf
```
