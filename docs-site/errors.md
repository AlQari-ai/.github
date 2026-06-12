# Errors

ALQari uses standard HTTP status codes and returns a consistent error object for every failed request.

---

## Error Response Format

```json
{
  "error": {
    "code": "document_not_found",
    "message": "No document found with id 'doc_abc123'.",
    "status": 404,
    "request_id": "req_20260612abc"
  }
}
```

| Field        | Description                                          |
|--------------|------------------------------------------------------|
| `code`       | Machine-readable error code (see table below)        |
| `message`    | Human-readable description                           |
| `status`     | HTTP status code                                     |
| `request_id` | Unique request ID — include this when contacting support |

---

## HTTP Status Codes

| Status | Meaning                                                 |
|--------|---------------------------------------------------------|
| `200`  | OK — request succeeded                                  |
| `201`  | Created — resource was created                          |
| `202`  | Accepted — async job started                            |
| `204`  | No Content — DELETE succeeded                           |
| `400`  | Bad Request — invalid parameters                        |
| `401`  | Unauthorized — missing or invalid API key               |
| `403`  | Forbidden — API key lacks required scope                |
| `404`  | Not Found — resource does not exist                     |
| `409`  | Conflict — resource already exists                      |
| `413`  | Payload Too Large — file exceeds 50 MB limit            |
| `422`  | Unprocessable Entity — valid JSON but failed validation |
| `429`  | Too Many Requests — rate limit exceeded                 |
| `500`  | Internal Server Error — unexpected server error         |
| `503`  | Service Unavailable — temporary outage                  |

---

## Error Codes

| Code                         | Status | Description                                           |
|------------------------------|--------|-------------------------------------------------------|
| `unauthorized`               | 401    | API key is missing or invalid                         |
| `forbidden`                  | 403    | API key lacks the required scope                      |
| `document_not_found`         | 404    | Document ID does not exist                            |
| `webhook_not_found`          | 404    | Webhook ID does not exist                             |
| `invalid_file_type`          | 400    | Uploaded file type is not supported                   |
| `file_too_large`             | 413    | File exceeds the 50 MB size limit                     |
| `ocr_not_completed`          | 409    | Extraction or chat requested before OCR is done       |
| `invalid_schema`             | 422    | Extraction schema is malformed                        |
| `invalid_rule`               | 422    | Validation rule is malformed                          |
| `rate_limit_exceeded`        | 429    | Too many requests — see `Retry-After` header          |
| `internal_error`             | 500    | Unexpected server error                               |

---

## Rate Limit Errors

When you hit a rate limit, the response includes a `Retry-After` header:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1749726060
```

See [Rate Limits](rate-limits.md) for details.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `401 unauthorized` | Missing `Authorization` header | Add `Authorization: Bearer $ALQARI_API_KEY` |
| `403 forbidden` | Wrong key scope | Create a key with the required scope |
| `404 document_not_found` | Wrong document ID | Verify the `document_id` from the upload response |
| `409 ocr_not_completed` | Extraction before OCR | Run OCR first and wait for `status: completed` |
| `413 file_too_large` | File > 50 MB | Compress or split the file |
| `429 rate_limit_exceeded` | Too many requests | Respect `Retry-After` and add backoff |

---

## Contact Support

Include the `request_id` from the error response when emailing **support@alqari.sa**.
