# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| v1.x    | ✅ Yes     |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Please report security issues by emailing **security@alqari.sa** with:

1. A clear description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Any suggested fixes (optional)

We will acknowledge your report within **48 hours** and provide a resolution timeline.

## Responsible Disclosure

We follow a 90-day responsible disclosure policy. We ask that you:

- Allow us reasonable time to investigate and fix the issue before any public disclosure.
- Avoid accessing or modifying other users' data.
- Act in good faith.

## API Key Security

- **Never commit API keys** to version control. Use `.env` files (excluded by `.gitignore`).
- Rotate keys immediately at [alqari.sa/dashboard/api-keys](https://alqari.sa/dashboard/api-keys) if you suspect exposure.
- Use separate API keys for production and development environments.
- Apply the principle of least privilege — use scoped keys when available.

## Transport Security

All ALQari API traffic is encrypted using TLS 1.2 or higher. Plain HTTP requests are rejected.
