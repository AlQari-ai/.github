# Security

Security best practices for integrating with ALQari APIs.

---

## Transport Security

- All ALQari API traffic is encrypted with **TLS 1.2 or higher**.
- Plain HTTP requests are rejected with `301 Moved Permanently`.
- Certificate pinning is supported for mobile applications — contact support for the certificate chain.

---

## API Key Security

### Do

- Store API keys in environment variables or a secrets manager (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, etc.)
- Use the `.env.example` pattern for local development (excluded from git by `.gitignore`)
- Use scoped keys with only the permissions your application needs
- Use separate keys for each environment (development, staging, production)
- Rotate keys regularly and immediately after any suspected exposure

### Do Not

- Hardcode keys in source code
- Commit `.env` files or keys to version control
- Share keys across teams or services
- Expose keys in client-side (browser) code
- Log keys in application logs

### Check for Exposed Keys

```bash
# Scan your repo history for accidentally committed secrets
git log -p | grep "sk_live_"
```

Use tools like [truffleHog](https://github.com/trufflesecurity/trufflehog) or [git-secrets](https://github.com/awslabs/git-secrets) in your CI pipeline.

---

## Webhook Security

- Always verify the `X-ALQari-Signature` header on incoming webhooks — see [Webhooks](webhooks.md#verifying-webhook-signatures).
- Reject webhook payloads older than **5 minutes** (compare `X-ALQari-Timestamp` to current time).
- Use HTTPS for your webhook endpoint.
- Never trust the payload without signature verification.

---

## Data Privacy

- Documents uploaded to ALQari are stored encrypted at rest (AES-256).
- Documents are scoped to your organization and never shared with other customers.
- You can delete a document and all its derived data at any time via `DELETE /documents/{document_id}`.
- For data residency or GDPR requirements, contact **privacy@alqari.sa**.

---

## Responsible Disclosure

Found a security vulnerability? See [SECURITY.md](../SECURITY.md).
