# Chat with Documents

Ask natural language questions over any document that has been processed with OCR. ALQari returns answers with source citations.

---

## Endpoint

```
POST /documents/{document_id}/chat
```

---

## Request Body

```json
{
  "message": "ما هو رقم الفاتورة والمبلغ الإجمالي؟",
  "language": "ar",
  "conversation_id": "conv_xyz789"
}
```

| Field             | Type   | Required | Description                                                       |
|-------------------|--------|----------|-------------------------------------------------------------------|
| `message`         | string | Yes      | The question or instruction in Arabic or English                  |
| `language`        | string | No       | Response language: `ar` or `en`. Default: matches question language |
| `conversation_id` | string | No       | Reuse a previous conversation for multi-turn context              |

---

## Example — First Turn

```bash
curl -X POST https://api.alqari.sa/v1/documents/doc_abc123/chat \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "ما هو رقم الفاتورة والمبلغ الإجمالي؟"
  }'
```

**Response:**

```json
{
  "document_id": "doc_abc123",
  "conversation_id": "conv_xyz789",
  "answer": "رقم الفاتورة هو INV-00123 والمبلغ الإجمالي هو 1500 ريال سعودي.",
  "citations": [
    {
      "page": 1,
      "text": "الرقم: INV-00123\nالمجموع: ١٥٠٠ ريال",
      "confidence": 0.97
    }
  ],
  "created_at": "2026-06-12T10:01:00Z"
}
```

---

## Example — Follow-up Turn (Multi-turn)

```bash
curl -X POST https://api.alqari.sa/v1/documents/doc_abc123/chat \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "من هو المورد؟",
    "conversation_id": "conv_xyz789"
  }'
```

**Response:**

```json
{
  "document_id": "doc_abc123",
  "conversation_id": "conv_xyz789",
  "answer": "المورد هو شركة النور التجارية.",
  "citations": [
    {
      "page": 1,
      "text": "شركة النور التجارية",
      "confidence": 0.94
    }
  ],
  "created_at": "2026-06-12T10:01:05Z"
}
```

---

## List Conversations

```bash
curl https://api.alqari.sa/v1/documents/doc_abc123/chat \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

---

## Notes

- Chat requires OCR to be completed on the document first.
- `conversation_id` is optional but recommended for multi-turn sessions; it maintains context across messages.
- The `citations` array points back to the exact text in the document that supports the answer.
- Questions can be asked in Arabic or English regardless of the document language.
