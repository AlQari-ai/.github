# OpenAPI Specification

This directory contains the ALQari API OpenAPI 3.1 specification in both YAML and JSON formats.

## Files

| File             | Description                          |
|------------------|--------------------------------------|
| `openapi.yaml`   | OpenAPI 3.1 spec (YAML — human-friendly) |
| `openapi.json`   | OpenAPI 3.1 spec (JSON — tooling-friendly) |

## Usage

### Import into Postman

1. Open Postman → **Import**
2. Select `openapi.yaml` or `openapi.json`
3. Postman generates a collection automatically

### Import into Insomnia

1. **Application** → **Import/Export** → **Import Data** → **From File**
2. Select `openapi.yaml`

### Generate a Client SDK

```bash
# Install OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# Generate a Python client
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python \
  -o ./sdk/python

# Generate a TypeScript/fetch client
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-fetch \
  -o ./sdk/typescript
```

### Validate the Spec

```bash
# Install Spectral
npm install -g @stoplight/spectral-cli

# Validate
spectral lint openapi.yaml
```

## Keeping the Spec Up to Date

The spec in this repository is updated alongside API releases. To fetch the latest spec directly from the live API:

```bash
python ../scripts/fetch-openapi.py
```
