# API Overview

ALQari APIs give developers a single, consistent REST interface to upload documents, run Arabic and English OCR, extract structured fields, validate data against business rules, search document collections with semantic and full-text queries, chat with documents in natural language, and receive real-time processing updates over webhooks.

---

## Contents

1. [Base URLs](#base-urls)
2. [Authentication](#authentication)
3. [Request & Response Conventions](#request--response-conventions)
4. [Versioning](#versioning)
5. [Pagination](#pagination)
6. [Endpoint Reference](#endpoint-reference)
   - [Documents](#documents)
   - [OCR](#ocr)
   - [Extraction](#extraction)
   - [Validation](#validation)
   - [Chat](#chat)
   - [Search](#search)
   - [Webhooks](#webhooks)
7. [Common API Flows](#common-api-flows)
   - [Upload → OCR → Structured Output](#flow-1-upload--ocr--structured-output)
   - [Upload → Extract → Validate](#flow-2-upload--extract--validate)
   - [Upload → Chat with Document](#flow-3-upload--chat-with-document)
   - [Bulk Document Processing](#flow-4-bulk-document-processing)
   - [Webhook Callback Flow](#flow-5-webhook-callback-flow)
8. [Developer Notes](#developer-notes)

---

## Base URLs

| Environment | Base URL                           |
|-------------|------------------------------------|
| Production  | `https://api.alqari.sa/v1`         |
| Sandbox     | `https://sandbox.api.alqari.sa/v1` |

Use the **sandbox** environment during development. It runs the same models as production but incurs no billing and retains files for only 24 hours.

---

## Authentication

All endpoints require a **Bearer token**. Pass your API key in the `Authorization` header on every request:

```
Authorization: Bearer <ALQARI_API_KEY>
```

### Example

```bash
curl https://api.alqari.sa/v1/documents \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

### Security rules

- Store keys in environment variables or a secrets manager — never in source code.
- Never expose API keys in browser-side JavaScript or mobile app bundles.
- Use the sandbox key (`sk_sandbox_…`) for all development and CI work.
- Rotate production keys immediately if compromised — see [Dashboard → API Keys](https://alqari.sa/dashboard/api-keys).

---

## Request & Response Conventions

| Convention | Detail |
|---|---|
| **Encoding** | UTF-8 for all request and response bodies |
| **JSON requests** | `Content-Type: application/json` |
| **File uploads** | `Content-Type: multipart/form-data` |
| **Dates** | ISO 8601 — `2026-06-12T10:00:00Z` |
| **IDs** | String identifiers prefixed by type — `doc_`, `wh_`, `conv_` |
| **Success codes** | `200 OK`, `201 Created`, `202 Accepted`, `204 No Content` |
| **Error body** | Always `{ "error": { "code", "message", "status", "request_id" } }` |

---

## Versioning

The API version is embedded in the URL path (`/v1`). Non-breaking additions (new optional fields, new endpoints) are deployed within the current version. Breaking changes increment the version to `/v2`. The current stable version is **v1**.

---

## Pagination

List endpoints return cursor-based pages:

```
GET /documents?limit=20&cursor=<next_cursor>
```

```json
{
  "data": [ ... ],
  "next_cursor": "eyJpZCI6ImRvY18y...",
  "has_more": true
}
```

When `has_more` is `false`, you have reached the last page. `next_cursor` is `null`.

---

## Endpoint Reference

### Documents

Upload and manage document files. All document processing operations reference the `document_id` returned at upload time.

| Method | Path | Summary | Auth | Request Type | Success Response |
|--------|------|---------|------|--------------|-----------------|
| `POST` | `/documents` | Upload a document | Bearer | `multipart/form-data` | `201` — Document object |
| `GET` | `/documents` | List documents | Bearer | — | `200` — DocumentList |
| `GET` | `/documents/{document_id}` | Get document details | Bearer | — | `200` — Document object |
| `DELETE` | `/documents/{document_id}` | Delete a document | Bearer | — | `204` — No content |

**Upload request fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | binary | Yes | PDF, JPG, PNG, TIFF, WEBP, DOCX, or TXT. Max 50 MB. |
| `language` | string | No | OCR language hint: `ar` · `en` · `ar+en` · `ar-hw`. Default: `ar` |
| `tags` | string[] | No | Custom labels for filtering (e.g. `["invoice","2026"]`) |
| `metadata` | object | No | Arbitrary key-value metadata stored with the document |
| `webhook_url` | string (URI) | No | Receive a push notification when processing completes |

**Document statuses:**

| Status | Meaning |
|--------|---------|
| `uploaded` | File received, no processing started |
| `processing` | OCR or extraction is running |
| `completed` | All requested processing is done |
| `failed` | Processing failed — check the `error` field |

---

### OCR

Extract raw text from scanned, photographed, or printed Arabic and English documents — including Arabic handwriting (`ar-hw`).

| Method | Path | Summary | Auth | Request Type | Success Response |
|--------|------|---------|------|--------------|-----------------|
| `POST` | `/documents/{document_id}/ocr` | Run OCR on a document | Bearer | `application/json` | `202` — OcrResult (async) |
| `GET` | `/documents/{document_id}/ocr` | Get OCR result | Bearer | — | `200` — OcrResult |

**Run OCR request fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `language` | string | `ar` | `ar` · `en` · `ar+en` · `ar-hw` |
| `detect_orientation` | boolean | `true` | Auto-rotate pages before recognition |
| `handwriting` | boolean | `false` | Enable Arabic handwriting model |
| `pages` | integer[] | all | Specific page numbers to process |

**OcrResult statuses:** `processing` · `completed` · `failed`

Each result page includes `text`, `confidence` (0–1), `word_count`, and an optional `bounding_boxes` array.

---

### Extraction

Pull typed, structured fields out of a document after OCR. Define a custom schema or use a pre-built one (e.g. `invoice`, `national_id_sa`, `iqama`, `passport`).

| Method | Path | Summary | Auth | Request Type | Success Response |
|--------|------|---------|------|--------------|-----------------|
| `POST` | `/documents/{document_id}/extraction` | Run structured field extraction | Bearer | `application/json` | `202` — ExtractionResult (async) |
| `GET` | `/documents/{document_id}/extraction` | Get extraction result | Bearer | — | `200` — ExtractionResult |

**Run extraction request fields:**

| Field | Type | Description |
|-------|------|-------------|
| `schema` | ExtractionField[] | Array of `{ name, type, description }` objects |
| `schema_id` | string | Pre-built schema ID — mutually exclusive with `schema` |

**Field types:** `string` · `number` · `date` · `boolean` · `array` · `address` · `id_number`

Each extracted field in the response includes `value`, `confidence`, and `page`.

---

### Validation

Apply business rules to extracted fields. Optionally route failing documents to a human review queue.

| Method | Path | Summary | Auth | Request Type | Success Response |
|--------|------|---------|------|--------------|-----------------|
| `POST` | `/documents/{document_id}/validation` | Run validation workflow | Bearer | `application/json` | `200` — ValidationResult |
| `GET` | `/documents/{document_id}/validation` | Get validation result | Bearer | — | `200` — ValidationResult |

**Run validation request fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `rules` | ValidationRule[] | — | Array of rule objects (see below) |
| `human_review_on_failure` | boolean | `false` | Route to human reviewer when any rule fails |

**Rule object:**

```json
{ "field": "total_amount", "rule": "greater_than", "value": 0 }
```

Available rules: `not_null` · `greater_than` · `less_than` · `equals` · `regex` · `date_after` · `date_before` · `in_list` · `confidence_min`

**ValidationResult statuses:** `passed` · `failed` · `pending_review` · `reviewed`

When `pending_review`, the response contains a `review_url` that opens the task in the ALQari Review Dashboard.

---

### Chat

Ask natural language questions over any OCR-processed document. Supports multi-turn conversations.

| Method | Path | Summary | Auth | Request Type | Success Response |
|--------|------|---------|------|--------------|-----------------|
| `POST` | `/documents/{document_id}/chat` | Ask a question about a document | Bearer | `application/json` | `200` — ChatResponse |

**Request fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | Question or instruction in Arabic or English |
| `language` | string | No | Response language: `ar` or `en`. Defaults to the question language. |
| `conversation_id` | string | No | Continue a prior conversation for multi-turn context |

**Response fields:** `answer` (string), `conversation_id` (string), `citations` (array of `{ page, text, confidence }`).

---

### Search

Full-text and semantic search across all OCR-processed documents in your account.

| Method | Path | Summary | Auth | Request Type | Success Response |
|--------|------|---------|------|--------------|-----------------|
| `POST` | `/search` | Search across documents | Bearer | `application/json` | `200` — SearchResults |

**Request fields:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | string | — | Search string in Arabic or English |
| `mode` | string | `semantic` | `fulltext` · `semantic` · `hybrid` |
| `limit` | integer | `10` | Max results (1–100) |
| `cursor` | string | — | Pagination cursor |
| `filters.tags` | string[] | — | Restrict to documents with these tags |
| `filters.document_ids` | string[] | — | Restrict to specific document IDs |
| `filters.date_range` | object | — | `{ "from": "YYYY-MM-DD", "to": "YYYY-MM-DD" }` |

Each result includes `document_id`, `filename`, `score` (relevance, 0–1), `snippet`, `page`, and `tags`.

---

### Webhooks

Register HTTP endpoints to receive push notifications when document processing events fire.

| Method | Path | Summary | Auth | Request Type | Success Response |
|--------|------|---------|------|--------------|-----------------|
| `GET` | `/webhooks` | List registered webhooks | Bearer | — | `200` — Webhook[] |
| `POST` | `/webhooks` | Create a webhook | Bearer | `application/json` | `201` — Webhook |
| `DELETE` | `/webhooks/{webhook_id}` | Delete a webhook | Bearer | — | `204` — No content |

**Create webhook request fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string (URI) | Yes | HTTPS endpoint to receive events |
| `events` | string[] | Yes | One or more event names (see below) |
| `secret` | string | No | HMAC-SHA256 signing secret for signature verification |

**Available events:**

| Event | Fired When |
|-------|-----------|
| `document.uploaded` | Upload completes |
| `document.ocr.completed` | OCR job succeeds |
| `document.ocr.failed` | OCR job fails |
| `document.extraction.completed` | Extraction job succeeds |
| `document.extraction.failed` | Extraction job fails |
| `document.validation.completed` | Validation result is ready |
| `document.validation.reviewed` | Human review is complete |
| `document.deleted` | Document is deleted |

All webhook payloads include `event`, `webhook_id`, `document_id`, `timestamp`, and a `data` object. Verify the `X-ALQari-Signature` header on every delivery — see [Webhooks guide](webhooks.md#verifying-webhook-signatures).

---

## Common API Flows

### Flow 1 — Upload → OCR → Structured Output

The most common flow. Use it to turn a scanned PDF into searchable, machine-readable text.

```
1. POST /documents                      → document_id
2. POST /documents/{document_id}/ocr    → job starts (202)
3. GET  /documents/{document_id}/ocr    → poll until status = "completed"
   (or subscribe to document.ocr.completed webhook instead of polling)
4. Read pages[].text from the response
```

```bash
# Step 1 — upload
DOC=$(curl -sX POST https://api.alqari.sa/v1/documents \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -F "file=@invoice.pdf" | jq -r .document_id)

# Step 2 — start OCR
curl -sX POST https://api.alqari.sa/v1/documents/$DOC/ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"language":"ar"}'

# Step 3 — poll for result
curl -s https://api.alqari.sa/v1/documents/$DOC/ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY" | jq .status
```

---

### Flow 2 — Upload → Extract → Validate

Use this for KYC, invoice processing, or any workflow that needs typed fields and business-rule checks.

```
1. POST /documents                              → document_id
2. POST /documents/{document_id}/extraction     → job starts (202)
3. GET  /documents/{document_id}/extraction     → poll until status = "completed"
4. POST /documents/{document_id}/validation     → validation result (200)
5. If status = "pending_review": open review_url for human check
   If status = "passed":         proceed to downstream system
```

```bash
# Start extraction with pre-built invoice schema
curl -sX POST https://api.alqari.sa/v1/documents/$DOC/extraction \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"schema_id":"invoice"}'

# Run validation
curl -sX POST https://api.alqari.sa/v1/documents/$DOC/validation \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "rules": [
      {"field":"invoice_number","rule":"not_null"},
      {"field":"total_amount",  "rule":"greater_than","value":0},
      {"field":"tax_number",    "rule":"regex","pattern":"^3[0-9]{14}$"}
    ],
    "human_review_on_failure": true
  }'
```

---

### Flow 3 — Upload → Chat with Document

Use this to let users query documents in natural language — customer support, legal review, or document QA.

```
1. POST /documents                              → document_id
2. POST /documents/{document_id}/ocr            → OCR must complete first
3. POST /documents/{document_id}/chat           → first question → conversation_id
4. POST /documents/{document_id}/chat           → follow-up questions (pass conversation_id)
```

```bash
# First question — saves conversation_id from response
curl -sX POST https://api.alqari.sa/v1/documents/$DOC/chat \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message":"ما هو رقم الفاتورة؟"}'

# Follow-up using conversation_id
curl -sX POST https://api.alqari.sa/v1/documents/$DOC/chat \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message":"من هو المورد؟","conversation_id":"conv_xyz789"}'
```

---

### Flow 4 — Bulk Document Processing

Process many documents concurrently by uploading in parallel and using webhooks to receive results instead of polling.

```
1. Register a webhook for document.ocr.completed + document.extraction.completed
2. Upload all documents (POST /documents × N) — record each document_id
3. Start OCR on each document (POST /documents/{id}/ocr)
4. Receive webhook events as each job completes
5. Trigger extraction / validation on receipt of ocr.completed events
```

```python
import os, requests, concurrent.futures

BASE = "https://api.alqari.sa/v1"
H    = {"Authorization": f"Bearer {os.environ['ALQARI_API_KEY']}"}

def process(path):
    with open(path, "rb") as f:
        doc_id = requests.post(f"{BASE}/documents", headers=H,
                               files={"file": f}).json()["document_id"]
    requests.post(f"{BASE}/documents/{doc_id}/ocr", headers=H,
                  json={"language": "ar"})
    return doc_id

files = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    ids = list(pool.map(process, files))

print("Processing:", ids)
# Your webhook endpoint will receive results as they complete
```

---

### Flow 5 — Webhook Callback Flow

Avoid polling entirely by registering a webhook before uploading.

```
1. POST /webhooks                → webhook_id
2. POST /documents               → document_id (include webhook_url in body)
3. POST /documents/{id}/ocr      → job starts
4. ALQari calls your URL with:   POST https://your-server/hook
                                  X-ALQari-Signature: sha256=<hmac>
                                  { "event": "document.ocr.completed", ... }
5. Verify signature → process result
```

**Minimal Express.js webhook handler:**

```js
import express from "express";
import crypto  from "crypto";

const app    = express();
const SECRET = process.env.WEBHOOK_SECRET;

app.post("/hook", express.raw({ type: "application/json" }), (req, res) => {
  const sig  = req.headers["x-alqari-signature"];
  const ts   = req.headers["x-alqari-timestamp"];

  // Reject stale payloads (> 5 min)
  if (Math.abs(Date.now() / 1000 - Number(ts)) > 300) {
    return res.status(400).send("Timestamp too old");
  }

  const expected = "sha256=" + crypto
    .createHmac("sha256", SECRET)
    .update(`${ts}.${req.body}`)
    .digest("hex");

  if (!crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(sig))) {
    return res.status(401).send("Invalid signature");
  }

  const event = JSON.parse(req.body);
  console.log("Event received:", event.event, event.document_id);

  res.sendStatus(200); // Always respond 200 quickly; process async
});

app.listen(3000);
```

---

## Developer Notes

### Environment

- Use **sandbox** API keys (`sk_sandbox_…`) during development and CI. The sandbox is isolated from production data.
- Switch to production by changing the base URL to `https://api.alqari.sa/v1` and the API key to a production key.
- The base URL can be injected via the `ALQARI_BASE_URL` environment variable — no code changes needed to switch environments.

### API Key Security

- **Never** embed API keys in frontend code (HTML, JS bundles, mobile apps). Keys in client-side code are exposed to all users.
- Use environment variables or a secrets manager (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault).
- Create separate keys per environment (dev / staging / production) and per service.
- Scope keys to the minimum permissions your service needs.

### Async Processing

Many operations (`OCR`, `Extraction`) return `202 Accepted` and process in the background.

- Use **webhooks** (recommended) to receive results without polling.
- If polling, implement **exponential backoff**: start at 1 s, double each attempt, cap at 30 s.
- Always check `status` in the GET response before reading result fields — a job still `processing` will have empty `pages` / `fields`.

```python
import time

def poll(url, headers, max_attempts=20):
    delay = 1
    for _ in range(max_attempts):
        r = requests.get(url, headers=headers).json()
        if r["status"] in ("completed", "failed"):
            return r
        time.sleep(delay)
        delay = min(delay * 2, 30)
    raise TimeoutError("Job did not complete in time")
```

### ID and Request Management

- Persist `document_id` values returned on upload — they are required for all subsequent operations on that document.
- Include `request_id` (from error responses) when contacting support — it uniquely identifies the failed request server-side.
- `conversation_id` must be passed between turns to maintain multi-turn chat context.

### Confidence Scores

Each OCR page and each extracted field includes a `confidence` score (0.0–1.0):

| Range | Recommendation |
|-------|---------------|
| ≥ 0.95 | Safe to use automatically |
| 0.80–0.94 | Review before critical use |
| 0.60–0.79 | Flag for human review |
| < 0.60 | Require human verification |

Do not pass low-confidence values directly to downstream systems (payment processors, identity checks) without validation.

### Rate Limits and Retries

- On `429 Too Many Requests`, read the `Retry-After` header and wait that many seconds before retrying.
- On `5xx` errors, retry with exponential backoff — the service may be recovering from a transient fault.
- **Do not** retry immediately on `4xx` errors (except `429`) — they indicate a client-side issue that will not resolve on retry.

```python
RETRYABLE = {429, 500, 502, 503, 504}

def safe_request(method, url, **kwargs):
    for attempt in range(5):
        resp = requests.request(method, url, **kwargs)
        if resp.status_code not in RETRYABLE:
            return resp
        wait = int(resp.headers.get("Retry-After", 2 ** attempt))
        time.sleep(wait)
    return resp
```

### Pagination

Always handle pagination for list endpoints — your document count will grow over time.

```python
def list_all_documents(headers):
    url, docs = f"{BASE}/documents?limit=100", []
    while url:
        page = requests.get(url, headers=headers).json()
        docs.extend(page["data"])
        cursor = page.get("next_cursor")
        url = f"{BASE}/documents?limit=100&cursor={cursor}" if cursor else None
    return docs
```

---

*For full request/response schemas, see the [OpenAPI specification](https://github.com/alqari/alqari-developer-hub/blob/main/openapi/openapi.yaml). For errors and status codes, see [Errors](errors.md).*

