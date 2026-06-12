/**
 * run-extraction.js — Extract structured fields from a document.
 *
 * Usage:
 *   node run-extraction.js <document_id> [schema_id]
 *
 *   schema_id: invoice (default) | national_id_sa | iqama | passport | bank_statement
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
  console.error("Usage: node run-extraction.js <document_id> [schema_id]");
  process.exit(1);
}

const schemaId = process.argv[3] ?? "invoice";

// Custom schema — used when schemaId === "custom"
const CUSTOM_SCHEMA = [
  { name: "invoice_number", type: "string",  description: "Invoice or reference number" },
  { name: "invoice_date",   type: "date",    description: "Date on the invoice" },
  { name: "total_amount",   type: "number",  description: "Total amount due" },
  { name: "vendor_name",    type: "string",  description: "Name of the issuing vendor" },
];

const payload = schemaId === "custom"
  ? { schema: CUSTOM_SCHEMA }
  : { schema_id: schemaId };

console.log(`Running extraction on document: ${documentId} (schema: ${schemaId})`);

const resp = await fetch(`${BASE_URL}/documents/${documentId}/extraction`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify(payload),
});

if (!resp.ok) {
  const err = await resp.json().catch(() => ({}));
  console.error(`Error ${resp.status}:`, JSON.stringify(err, null, 2));
  process.exit(1);
}

const data = await resp.json();
console.log(JSON.stringify(data, null, 2));
