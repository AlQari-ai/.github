# Rate Limits

ALQari enforces rate limits to ensure fair usage and platform stability.

---

## Default Limits

| Plan         | Requests / minute | Uploads / day | Pages / month |
|--------------|--------------------|---------------|---------------|
| Free         | 20                 | 50            | 500           |
| Starter      | 100                | 500           | 10,000        |
| Growth       | 500                | 5,000         | 100,000       |
| Enterprise   | Custom             | Custom        | Custom        |

Limits apply per API key.

---

## Rate Limit Headers

Every API response includes rate limit information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1749726060
```

| Header                  | Description                                          |
|-------------------------|------------------------------------------------------|
| `X-RateLimit-Limit`     | Max requests allowed in the current window           |
| `X-RateLimit-Remaining` | Requests remaining in the current window             |
| `X-RateLimit-Reset`     | Unix timestamp when the window resets                |
| `Retry-After`           | Seconds to wait before retrying (only on 429)        |

---

## Handling Rate Limits

When you exceed a limit you receive:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Retry after 30 seconds.",
    "status": 429
  }
}
```

### Recommended Retry Strategy

Use **exponential backoff with jitter**:

```python
import time, random, requests

def request_with_backoff(url, headers, max_retries=5):
    for attempt in range(max_retries):
        resp = requests.get(url, headers=headers)
        if resp.status_code != 429:
            return resp
        retry_after = int(resp.headers.get("Retry-After", 2 ** attempt))
        jitter = random.uniform(0, 1)
        time.sleep(retry_after + jitter)
    return resp
```

---

## Increasing Limits

To increase your rate limits, upgrade your plan at [alqari.sa/pricing](https://alqari.sa/pricing) or contact **sales@alqari.sa** for Enterprise options.
