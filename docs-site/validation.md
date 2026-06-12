# Validation

Validation workflows let you apply business rules to extracted data and route documents for human review when needed.

---

## Endpoint

```
POST /documents/{document_id}/validation
```

---

## Request Body

```json
{
  "rules": [
    { "field": "invoice_date", "rule": "not_null" },
    { "field": "total_amount", "rule": "greater_than", "value": 0 },
    { "field": "tax_number",   "rule": "regex",       "pattern": "^3[0-9]{14}$" }
  ],
  "human_review_on_failure": true
}
```

### Rule Types

| Rule             | Description                                         |
|------------------|-----------------------------------------------------|
| `not_null`       | Field must be present and non-empty                 |
| `greater_than`   | Numeric field must be > `value`                     |
| `less_than`      | Numeric field must be < `value`                     |
| `equals`         | Field value must equal `value`                      |
| `regex`          | String field must match `pattern`                   |
| `date_after`     | Date field must be after `value` (ISO 8601)         |
| `date_before`    | Date field must be before `value` (ISO 8601)        |
| `in_list`        | Value must be in `values` array                     |
| `confidence_min` | OCR/extraction confidence must be ≥ `value` (0–1)  |

---

## Example

```bash
curl -X POST https://api.alqari.sa/v1/documents/doc_abc123/validation \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "rules": [
      { "field": "invoice_number", "rule": "not_null" },
      { "field": "total_amount",   "rule": "greater_than", "value": 0 }
    ],
    "human_review_on_failure": false
  }'
```

---

## Response — All Rules Passed

```json
{
  "document_id": "doc_abc123",
  "status": "passed",
  "results": [
    { "field": "invoice_number", "rule": "not_null", "passed": true },
    { "field": "total_amount",   "rule": "greater_than", "passed": true }
  ],
  "human_review_required": false,
  "completed_at": "2026-06-12T10:00:06Z"
}
```

## Response — Validation Failed with Human Review

```json
{
  "document_id": "doc_abc123",
  "status": "pending_review",
  "results": [
    { "field": "invoice_number", "rule": "not_null",     "passed": true },
    { "field": "tax_number",     "rule": "regex",        "passed": false, "message": "Value '123' does not match pattern '^3[0-9]{14}$'" }
  ],
  "human_review_required": true,
  "review_url": "https://app.alqari.sa/review/doc_abc123",
  "completed_at": "2026-06-12T10:00:06Z"
}
```

---

## Human Review

When `human_review_required` is `true`:

1. A task is created in the ALQari Review Dashboard
2. A reviewer can inspect the document, correct extracted values, and approve or reject
3. A webhook fires when the review is complete — see [Webhooks](webhooks.md)

Reviewers access the task at the `review_url` in the response.

---

## Get Validation Result

```bash
curl https://api.alqari.sa/v1/documents/doc_abc123/validation \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

---

## Validation Statuses

| Status           | Description                                        |
|------------------|----------------------------------------------------|
| `passed`         | All rules passed                                   |
| `failed`         | One or more rules failed, no human review          |
| `pending_review` | Sent for human review                              |
| `reviewed`       | Human review completed                             |
