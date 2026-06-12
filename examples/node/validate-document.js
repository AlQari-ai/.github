/**
 * validate-document.js — Run a validation workflow on a document.
 *
 * Usage:
 *   node validate-document.js <document_id>
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
  console.error("Usage: node validate-document.js <document_id>");
  process.exit(1);
}

// Edit these rules to match your validation requirements
const RULES = [
  { field: "invoice_number", rule: "not_null" },
  { field: "total_amount",   rule: "greater_than", value: 0 },
  { field: "invoice_date",   rule: "not_null" },
  { field: "tax_number",     rule: "regex", pattern: "^3[0-9]{14}$" },
];

console.log(`Running validation on document: ${documentId}`);

const resp = await fetch(`${BASE_URL}/documents/${documentId}/validation`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    rules: RULES,
    human_review_on_failure: false,
  }),
});

if (!resp.ok) {
  const err = await resp.json().catch(() => ({}));
  console.error(`Error ${resp.status}:`, JSON.stringify(err, null, 2));
  process.exit(1);
}

const data = await resp.json();
console.log(JSON.stringify(data, null, 2));

if (data.status === "passed") {
  console.log("\n✓ Validation passed.");
} else if (data.status === "pending_review") {
  console.log(`\n⚠ Sent for human review: ${data.review_url}`);
} else {
  console.log(`\n✗ Validation status: ${data.status}`);
}
