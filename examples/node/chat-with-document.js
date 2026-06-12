/**
 * chat-with-document.js — Ask a question about a document using natural language.
 *
 * Usage:
 *   node chat-with-document.js <document_id> "<question>"
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
  console.error("Usage: node chat-with-document.js <document_id> \"<question>\"");
  process.exit(1);
}

const message = process.argv[3];
if (!message) {
  console.error("Please provide a question as the second argument.");
  process.exit(1);
}

console.log(`Document: ${documentId}`);
console.log(`Question: ${message}\n`);

const resp = await fetch(`${BASE_URL}/documents/${documentId}/chat`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ message }),
});

if (!resp.ok) {
  const err = await resp.json().catch(() => ({}));
  console.error(`Error ${resp.status}:`, JSON.stringify(err, null, 2));
  process.exit(1);
}

const data = await resp.json();
console.log(JSON.stringify(data, null, 2));
console.log(`\nAnswer: ${data.answer}`);
