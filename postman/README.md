# Postman Collection

Ready-to-use Postman collection and environment for ALQari APIs.

## Import

1. Open **Postman** → **Import**
2. Select `alqari.postman_collection.json`
3. Select `alqari.postman_environment.json`
4. In the **Environments** panel, select **ALQari** and set `ALQARI_API_KEY` to your API key

## Variables

| Variable           | Description                          | Default                        |
|--------------------|--------------------------------------|--------------------------------|
| `ALQARI_API_KEY`   | Your API key (set this manually)     | `your_api_key_here`            |
| `ALQARI_BASE_URL`  | API base URL                         | `https://api.alqari.sa/v1`     |
| `DOCUMENT_ID`      | Auto-set by the Upload request       | —                              |
| `CONVERSATION_ID`  | Auto-set by the Chat request         | —                              |

## Workflow

Run requests in this order for a complete end-to-end flow:

1. **Documents / Upload Document** — set `DOCUMENT_ID` automatically
2. **OCR / Run OCR**
3. **Extraction / Run Extraction**
4. **Validation / Run Validation**
5. **Chat / Chat with Document**
6. **Search / Search Documents**

## Regenerating

To regenerate from the OpenAPI spec:

```bash
python ../scripts/generate-postman.py
```
