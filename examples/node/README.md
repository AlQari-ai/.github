# Node.js Examples

Copy-paste ready Node.js scripts for every ALQari API operation.

## Requirements

Node.js 18+ (uses native `fetch` and ES modules)

```bash
npm install
```

## Configuration

```bash
export ALQARI_API_KEY="your_api_key_here"
export ALQARI_BASE_URL="https://api.alqari.sa/v1"   # optional
```

## Scripts

| Script | Description |
|--------|-------------|
| `upload-document.js`   | Upload a document file |
| `run-ocr.js`           | Run OCR on a document |
| `run-extraction.js`    | Extract structured fields |
| `validate-document.js` | Run a validation workflow |
| `chat-with-document.js`| Chat with a document |

## Usage

```bash
node upload-document.js /path/to/document.pdf
node run-ocr.js doc_abc123
node run-extraction.js doc_abc123
node validate-document.js doc_abc123
node chat-with-document.js doc_abc123 "ما هو رقم الفاتورة؟"
```
