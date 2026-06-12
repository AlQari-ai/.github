# Webhooks

Webhooks let ALQari push real-time event notifications to your server so you don't need to poll for job status.

---

## Endpoint

```
POST /webhooks
```

---

## Supported Events

| Event                          | Fired When                                         |
|--------------------------------|----------------------------------------------------|
| `document.uploaded`            | Document upload is complete                        |
| `document.ocr.completed`       | OCR job finished successfully                      |
| `document.ocr.failed`          | OCR job failed                                     |
| `document.extraction.completed`| Extraction job finished successfully               |
| `document.extraction.failed`   | Extraction job failed                              |
| `document.validation.completed`| Validation result is ready                         |
| `document.validation.reviewed` | Human review of validation is complete             |
| `document.deleted`             | Document was deleted                               |

---

## Register a Webhook

```bash
curl -X POST https://api.alqari.sa/v1/webhooks \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.example.com/alqari/webhook",
    "events": ["document.ocr.completed", "document.extraction.completed"],
    "secret": "your_webhook_signing_secret"
  }'
```

**Response:**

```json
{
  "webhook_id": "wh_xyz789",
  "url": "https://your-server.example.com/alqari/webhook",
  "events": ["document.ocr.completed", "document.extraction.completed"],
  "status": "active",
  "created_at": "2026-06-12T10:00:00Z"
}
```

---

## Webhook Payload

ALQari sends a `POST` request to your URL with a JSON body:

```json
{
  "event": "document.ocr.completed",
  "webhook_id": "wh_xyz789",
  "document_id": "doc_abc123",
  "timestamp": "2026-06-12T10:00:03Z",
  "data": {
    "status": "completed",
    "page_count": 3,
    "language": "ar"
  }
}
```

---

## Verifying Webhook Signatures

ALQari signs every webhook request with an HMAC-SHA256 signature. Verify it to ensure the payload came from ALQari:

```
X-ALQari-Signature: sha256=<hex_digest>
X-ALQari-Timestamp: 1749726003
```

### Python Verification Example

```python
import hashlib, hmac, os, time

def verify_webhook(payload_bytes: bytes, signature_header: str, timestamp_header: str, secret: str) -> bool:
    # Reject requests older than 5 minutes
    if abs(time.time() - int(timestamp_header)) > 300:
        return False
    message = timestamp_header.encode() + b"." + payload_bytes
    expected = "sha256=" + hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header)
```

### Node.js Verification Example

```js
import crypto from "crypto";

function verifyWebhook(payloadBuffer, signatureHeader, timestampHeader, secret) {
  if (Math.abs(Date.now() / 1000 - Number(timestampHeader)) > 300) return false;
  const message = `${timestampHeader}.${payloadBuffer.toString()}`;
  const expected = "sha256=" + crypto.createHmac("sha256", secret).update(message).digest("hex");
  return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(signatureHeader));
}
```

---

## Retries

If your endpoint returns a non-`2xx` response, ALQari retries the webhook with exponential backoff:

| Attempt | Delay   |
|---------|---------|
| 1       | 30 s    |
| 2       | 5 min   |
| 3       | 30 min  |
| 4       | 2 h     |
| 5       | 8 h     |

After 5 failed attempts the webhook is marked `failed` and no further retries are made.

---

## List and Delete Webhooks

```bash
# List
curl https://api.alqari.sa/v1/webhooks \
  -H "Authorization: Bearer $ALQARI_API_KEY"

# Delete
curl -X DELETE https://api.alqari.sa/v1/webhooks/wh_xyz789 \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```
