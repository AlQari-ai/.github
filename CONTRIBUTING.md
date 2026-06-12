# Contributing to ALQari Developer Hub

Thank you for helping improve the ALQari developer experience!

## What We Welcome

- **Bug fixes** in code examples
- **New examples** for languages or frameworks not yet covered
- **Documentation corrections** (typos, outdated info, broken links)
- **Translations** of guides to additional languages
- **New guides** for specific use cases (KYC, invoices, etc.)

## What We Don't Accept

- Changes to the OpenAPI spec that don't reflect the actual live API
- Breaking changes to existing examples without discussion
- Commits containing real API keys or secrets

---

## Getting Started

1. **Fork** this repository
2. **Clone** your fork

   ```bash
   git clone https://github.com/YOUR_USERNAME/alqari-developer-hub.git
   cd alqari-developer-hub
   ```

3. **Create a branch**

   ```bash
   git checkout -b fix/typo-in-quickstart
   ```

4. **Make your changes**

5. **Test your examples** (see below)

6. **Open a pull request** against `main`

---

## Testing Examples

### Python

```bash
cd examples/python
pip install -r requirements.txt
export ALQARI_API_KEY=your_sandbox_key
python upload_document.py
```

### Node.js

```bash
cd examples/node
npm install
export ALQARI_API_KEY=your_sandbox_key
node upload-document.js
```

### cURL

```bash
cd examples/curl
export ALQARI_API_KEY=your_sandbox_key
bash upload-document.sh
```

Use the **sandbox** base URL (`https://sandbox.api.alqari.sa/v1`) during development.

---

## Code Style

- **Python**: follow PEP 8; keep examples simple and self-contained.
- **Node.js**: use ES modules (`import`/`export`); target Node 18+.
- **cURL**: use long flags (`--header` over `-H`) for readability where practical.
- **Markdown**: wrap lines at 120 characters; use ATX-style headings (`#`).

---

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(examples): add PHP upload example
fix(docs): correct webhook signature header name
docs(quickstart): clarify sandbox vs production URL
```

---

## Pull Request Checklist

- [ ] Examples run without errors against the sandbox
- [ ] No real API keys in code or git history
- [ ] Markdown passes the lint check (`markdownlint`)
- [ ] OpenAPI changes pass `spectral lint` (if applicable)

---

## Questions?

Open a [GitHub Discussion](https://github.com/alqari/alqari-developer-hub/discussions) or email **developers@alqari.sa**.
