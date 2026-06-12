/**
 * run-ocr.js — Run OCR on an uploaded document.
 *
 * Usage:
 *   node run-ocr.js <document_id> [language]
 *
 *   language: ar (default) | en | ar+en | ar-hw (handwriting)
 *
 * Environment variables:
 *   ALQARI_API_KEY   Required.
 *   ALQARI_BASE_URL  Optional. Defaults to https://api.alqari.sa/v1
 */

const BASE_URL = (process.env.ALQARI_BASE_URL ?? "https://api.alqari.sa/v1").replace(/\/$/, "");
const API_KEY  = process.env.ALQARI_API_KEY;

if (!API_KEY) {
  console.error("Error: ALQARI_API_KEY environment variable is not set.");
  process.exit(1);
}

const documentId = process.argv[2];
if (!documentId) {
  console.error("Usage: node run-ocr.js <document_id> [language]");
  process.exit(1);
}

const language = process.argv[3] ?? "ar";

console.log(`Running OCR on document: ${documentId} (language: ${language})`);

const resp = await fetch(`${BASE_URL}/documents/${documentId}/ocr`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    language,
    detect_orientation: true,
    handwriting: language === "ar-hw",
  }),
});

if (!resp.ok) {
  const err = await resp.json().catch(() => ({}));
  console.error(`Error ${resp.status}:`, JSON.stringify(err, null, 2));
  process.exit(1);
}

const data = await resp.json();
console.log(JSON.stringify(data, null, 2));
