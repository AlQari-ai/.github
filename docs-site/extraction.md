# Extraction

Extract structured fields from a document after OCR. Define a schema of fields you want — ALQari returns typed, validated JSON values.

---

## Endpoint

```
POST /documents/{document_id}/extraction
```

---

## Request Body

```json
{
  "schema": [
    { "name": "invoice_number", "type": "string", "description": "Invoice or reference number" },
    { "name": "invoice_date",   "type": "date",   "description": "Date on the invoice" },
    { "name": "total_amount",   "type": "number", "description": "Total amount due" },
    { "name": "vendor_name",    "type": "string", "description": "Name of the issuing vendor" },
    { "name": "tax_number",     "type": "string", "description": "VAT or tax registration number" }
  ]
}
```

### Field Types

| Type       | Description                                        |
|------------|----------------------------------------------------|
| `string`   | Free text                                          |
| `number`   | Numeric value (integer or decimal)                 |
| `date`     | Date — returned as ISO 8601 string (`YYYY-MM-DD`)  |
| `boolean`  | True / false                                       |
| `array`    | List of values                                     |
| `address`  | Structured address object                          |
| `id_number`| National ID or passport number                     |

---

## Example

```bash
curl -X POST https://api.alqari.sa/v1/documents/doc_abc123/extraction \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "schema": [
      { "name": "invoice_number", "type": "string" },
      { "name": "invoice_date",   "type": "date" },
      { "name": "total_amount",   "type": "number" },
      { "name": "vendor_name",    "type": "string" }
    ]
  }'
```

---

## Response

```json
{
  "document_id": "doc_abc123",
  "status": "completed",
  "fields": {
    "invoice_number": {
      "value": "INV-00123",
      "confidence": 0.97,
      "page": 1
    },
    "invoice_date": {
      "value": "2026-01-15",
      "confidence": 0.99,
      "page": 1
    },
    "total_amount": {
      "value": 1500.00,
      "confidence": 0.96,
      "page": 1
    },
    "vendor_name": {
      "value": "شركة النور التجارية",
      "confidence": 0.94,
      "page": 1
    }
  },
  "completed_at": "2026-06-12T10:00:05Z"
}
```

---

## Get Extraction Result

```bash
curl https://api.alqari.sa/v1/documents/doc_abc123/extraction \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

---

## Pre-built Schemas

ALQari provides pre-built schemas for common document types:

| Schema ID           | Document Type         |
|---------------------|-----------------------|
| `invoice`           | Tax invoice (ZATCA)   |
| `national_id_sa`    | Saudi National ID     |
| `iqama`             | Resident ID (Iqama)   |
| `passport`          | International passport|
| `commercial_register` | CR certificate      |
| `bank_statement`    | Bank statement        |

Use a pre-built schema:

```bash
curl -X POST https://api.alqari.sa/v1/documents/doc_abc123/extraction \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "schema_id": "invoice" }'
```

---

## Notes

- Extraction requires OCR to be completed first (or runs OCR automatically if not yet done).
- Fields not found in the document return `null` with `confidence: 0`.
- For low-confidence fields consider triggering a [validation workflow](validation.md).
