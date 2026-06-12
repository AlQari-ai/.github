# Python Examples

Self-contained Python scripts for every ALQari API operation.

## Requirements

Python 3.8+ and the `requests` library:

```bash
pip install -r requirements.txt
```

## Configuration

```bash
export ALQARI_API_KEY="your_api_key_here"
export ALQARI_BASE_URL="https://api.alqari.sa/v1"   # optional, defaults to production
```

## Scripts

| Script | Description |
|--------|-------------|
| `upload_document.py`   | Upload a document file |
| `run_ocr.py`           | Run OCR on a document |
| `run_extraction.py`    | Extract structured fields |
| `validate_document.py` | Run a validation workflow |
| `chat_with_document.py`| Chat with a document |

## Usage

```bash
python upload_document.py /path/to/document.pdf
python run_ocr.py doc_abc123
python run_extraction.py doc_abc123
python validate_document.py doc_abc123
python chat_with_document.py doc_abc123 "ما هو رقم الفاتورة؟"
```
