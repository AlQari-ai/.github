# Authentication

All ALQari API requests require authentication using a **Bearer token** (your API key).

---

## Getting an API Key

1. Sign in to [alqari.sa/dashboard](https://alqari.sa/dashboard)
2. Navigate to **API Keys**
3. Click **Create new key**
4. Copy the key immediately — it is only shown once

---

## Using Your API Key

Include your API key in the `Authorization` header of every request:

```
Authorization: Bearer YOUR_API_KEY
```

### cURL

```bash
curl https://api.alqari.sa/v1/documents \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

### Python

```python
import os, requests

headers = {"Authorization": f"Bearer {os.environ['ALQARI_API_KEY']}"}
resp = requests.get("https://api.alqari.sa/v1/documents", headers=headers)
```

### Node.js

```js
const headers = {
  Authorization: `Bearer ${process.env.ALQARI_API_KEY}`
};
const resp = await fetch("https://api.alqari.sa/v1/documents", { headers });
```

---

## Key Scopes

When creating a key you can restrict its permissions:

| Scope              | Access                                  |
|--------------------|-----------------------------------------|
| `documents:read`   | List and retrieve documents             |
| `documents:write`  | Upload and delete documents             |
| `ocr:run`          | Run OCR jobs                            |
| `extraction:run`   | Run extraction jobs                     |
| `validation:run`   | Run validation workflows                |
| `chat:run`         | Use chat API                            |
| `search:run`       | Use search API                          |
| `webhooks:manage`  | Create, update, delete webhooks         |
| `*`                | Full access (default for new keys)      |

---

## Key Rotation

Rotate your keys regularly:

1. Create a new key in the dashboard
2. Update your application to use the new key
3. Delete the old key

To revoke a compromised key immediately, go to **Dashboard → API Keys → Revoke**.

---

## Security Best Practices

- **Never** hardcode API keys in source code.
- Use environment variables or a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.).
- Use the `.env.example` pattern for local development (see the [repository root](https://github.com/alqari/alqari-developer-hub/blob/main/.env.example)).
- Apply least-privilege scopes to production keys.

---

## Authentication Errors

| HTTP Status | Code                  | Meaning                              |
|-------------|-----------------------|--------------------------------------|
| `401`       | `unauthorized`        | Missing or invalid API key           |
| `403`       | `forbidden`           | Key lacks the required scope         |

See [Errors](errors.md) for full error response format.
