# cURL Examples

Copy-paste ready cURL commands for every ALQari API endpoint.

## Prerequisites

```bash
export ALQARI_API_KEY="your_api_key_here"
export ALQARI_BASE_URL="https://api.alqari.sa/v1"   # or sandbox URL
```

## Scripts

| Script | Description |
|--------|-------------|
| `upload-document.sh`   | Upload a PDF or image file |
| `run-ocr.sh`           | Run OCR on an uploaded document |
| `run-extraction.sh`    | Extract structured fields |
| `validate-document.sh` | Run a validation workflow |
| `chat-with-document.sh`| Ask a question about a document |

## Usage

```bash
bash upload-document.sh /path/to/document.pdf
bash run-ocr.sh doc_abc123
bash run-extraction.sh doc_abc123
bash validate-document.sh doc_abc123
bash chat-with-document.sh doc_abc123 "ما هو رقم الفاتورة؟"
```
