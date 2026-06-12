/**
 * upload-document.js — Upload a document to ALQari.
 *
 * Usage:
 *   node upload-document.js /path/to/document.pdf
 *
 * Environment variables:
 *   ALQARI_API_KEY   Required.
 *   ALQARI_BASE_URL  Optional. Defaults to https://api.alqari.sa/v1
 *   ALQARI_LANGUAGE  Optional. Defaults to "ar"
 */

import fs from "fs";
import path from "path";
import FormData from "form-data";

const BASE_URL  = (process.env.ALQARI_BASE_URL  ?? "https://api.alqari.sa/v1").replace(/\/$/, "");
const LANGUAGE  = process.env.ALQARI_LANGUAGE   ?? "ar";
const API_KEY   = process.env.ALQARI_API_KEY;

if (!API_KEY) {
  console.error("Error: ALQARI_API_KEY environment variable is not set.");
  process.exit(1);
}

const filePath = process.argv[2];
if (!filePath) {
  console.error("Usage: node upload-document.js <file_path>");
  process.exit(1);
}

if (!fs.existsSync(filePath)) {
  console.error(`Error: File not found: ${filePath}`);
  process.exit(1);
}

const form = new FormData();
form.append("file", fs.createReadStream(filePath), path.basename(filePath));
form.append("language", LANGUAGE);

console.log(`Uploading: ${filePath}`);

const resp = await fetch(`${BASE_URL}/documents`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    ...form.getHeaders(),
  },
  body: form,
});

if (!resp.ok) {
  const err = await resp.json().catch(() => ({}));
  console.error(`Error ${resp.status}:`, JSON.stringify(err, null, 2));
  process.exit(1);
}

const data = await resp.json();
console.log(JSON.stringify(data, null, 2));
console.log(`\nDocument ID: ${data.document_id}`);
