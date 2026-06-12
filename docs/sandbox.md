# Sandbox

The ALQari sandbox lets you test integrations without consuming production quota or affecting live data.

---

## Sandbox Base URL

```
https://sandbox.api.alqari.sa/v1
```

---

## Getting Sandbox Credentials

1. Sign in to [alqari.sa/dashboard](https://alqari.sa/dashboard)
2. Switch to the **Sandbox** environment in the top navigation
3. Navigate to **API Keys** and create a sandbox key

Sandbox keys are prefixed with `sk_sandbox_`.

---

## Differences from Production

| Feature            | Production            | Sandbox                                       |
|--------------------|-----------------------|-----------------------------------------------|
| File retention     | Per plan (30–365 days)| 24 hours                                      |
| Rate limits        | Per plan              | 10 requests / minute                          |
| OCR accuracy       | Full model            | Full model                                    |
| Webhooks           | Real delivery         | Delivered to your URL (use a tunnel for local)|
| Billing            | Yes                   | No                                            |
| Data isolation     | Production data       | Completely separate                           |

---

## Testing with Sample Documents

ALQari provides pre-built test documents in the sandbox. Upload them using the document ID shortcuts:

| Shortcut                  | Description                      |
|---------------------------|----------------------------------|
| `sample:invoice_ar`       | Arabic tax invoice (PDF)         |
| `sample:national_id_sa`   | Saudi national ID scan           |
| `sample:handwriting_ar`   | Arabic handwritten form          |
| `sample:mixed_doc`        | Mixed Arabic/English document    |

```bash
curl -X POST https://sandbox.api.alqari.sa/v1/documents \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "sample": "sample:invoice_ar" }'
```

---

## Local Webhook Testing

Use a tunneling tool to expose your local server to the sandbox:

```bash
# Using ngrok
ngrok http 3000
# Use the generated https URL as your webhook URL
```

---

## Switching Environments in Examples

All code examples in this repository read the base URL from an environment variable:

```bash
# Production
export ALQARI_BASE_URL=https://api.alqari.sa/v1

# Sandbox
export ALQARI_BASE_URL=https://sandbox.api.alqari.sa/v1
```
