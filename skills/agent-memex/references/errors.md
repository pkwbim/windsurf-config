# Errors

The API returns standard HTTP status codes. The body is always JSON:

```json
{"detail": "<message>"}
```

## Status codes

| Status | Meaning | What to do |
|--------|---------|------------|
| 200 | OK | Continue |
| 201 | Created (POST) | Continue |
| 204 | No content (DELETE) | Continue |
| 400 | Bad request — malformed JSON or invalid query string | Fix the request |
| 401 | Token missing or invalid | Stop. Ask the user to provide a token. |
| 403 | Token revoked or expired | Stop. Ask the user to issue a new one. |
| 404 | Resource not found | The card/session/asset may have been deleted. Re-check the ID or surface to the user. |
| 422 | Validation error — body doesn't match schema | Inspect `detail` for the field(s) that failed; fix and retry. |
| 5xx | Server error | Retry once. If it persists, surface to the user; don't loop. |

## Common 422 cases

- Missing required field (e.g. `title` on POST /api/cards)
- Wrong type (e.g. `tags` as a string instead of array)
- `step_type` not one of `thought | search | read | write` on session trail

## Health check

If you suspect the API itself is down:
```
GET /api/health
```
Returns `{"status": "ok"}` (no auth required).

## Tip

Don't retry a 4xx error as-is — fix the request first. Only retry 5xx errors, and only once.
