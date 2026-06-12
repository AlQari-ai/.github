This directory contains visual assets for the ALQari Developer Hub.

## Files

| File | Description |
|------|-------------|
| `alqari-demo.gif` | Animated demo of uploading a document and running OCR |
| `demo-thumbnail.png` | Static thumbnail / logo image for the README header |
| `sample-ar-handwriting.jpg` | Sample Arabic handwritten document used in all code examples |

## Sample Document — `sample-ar-handwriting.jpg`

This is a real scanned Arabic handwritten/printed document (a one-page academic text on the topic of illiteracy — *الأمية معوقة للتنمية في كل المجالات*). It was processed by the ALQari OCR API and returned 398 words with an average confidence of ~0.74.

The corresponding real API response is stored at [`examples/sample-output/ocr-response.json`](../examples/sample-output/ocr-response.json).

**To add the image:** place the file named `sample-ar-handwriting.jpg` in this directory. It is referenced as `SAMPLE_FILE` in [`.env.example`](../.env.example) and used by all code examples in [`examples/`](../examples/).

## Replacing with Real Assets

To add a real demo GIF:

1. Record a screen capture of your ALQari integration flow
2. Convert to GIF using a tool like [gifski](https://gif.ski/) or [Gifox](https://gifox.io/)
3. Keep the file size under 5 MB for fast GitHub rendering
4. Replace this file and commit

For the logo/thumbnail:
- Recommended dimensions: 400 × 400 px, transparent background
- Formats: PNG (preferred) or SVG
