# agent-memex API Reference

Base URL: `$MEMEX_BASE_URL` (e.g., `http://localhost:8360`)
Auth header: `Authorization: Bearer $MEMEX_API_TOKEN`

---

## Auth

### POST /api/auth/login
No auth required.
```json
// Request
{"email": "...", "password": "...", "token_name": "my-agent"}

// Response 200
{"api_token": "memex_...", "user": {...}, "expires_at": "2026-06-01T..."}
```

### POST /api/auth/tokens
Create a named token (for agents; shown in /tokens UI).
```json
// Request
{"name": "claude-agent"}

// Response 201
{"id": "uuid", "name": "claude-agent", "api_token": "memex_...", "expires_at": "..."}
// NOTE: api_token is shown only once
```

### GET /api/auth/tokens
List all agent tokens (excludes `web-ui` tokens).

### DELETE /api/auth/tokens/{token_id}
Revoke a token immediately.

---

## Cards

### GET /api/cards
Query params: `tag`, `sort` (`created`|`updated`|`title`), `limit` (default 20), `offset`
```json
// Response 200
[{"id": "uuid", "title": "...", "tags": [], "word_count": 120, "updated_at": "..."}]
```

### POST /api/cards
```json
// Request
{
  "title": "Attention Is All You Need",
  "content": "## Summary\n\nThe Transformer model...\n\nSee also: [[Neural Networks]]",
  "tags": ["ai", "nlp", "paper"],
  "sources": ["https://arxiv.org/abs/1706.03762"]
}

// Response 201
{"id": "uuid", "title": "...", "content": "...", "tags": [...], "sources": [...],
 "word_count": 45, "oversized": false, "links": [], "created_at": "...", "updated_at": "..."}
```

### GET /api/cards/{id}
```json
// Response 200
{
  "id": "uuid", "title": "...", "content": "...", "tags": [...], "sources": [...],
  "word_count": 45, "oversized": false,
  "links": [{"id": "uuid2", "title": "Neural Networks"}],
  "created_at": "...", "updated_at": "..."
}
```

### PATCH /api/cards/{id}
All fields optional.
```json
// Request
{
  "content": "Updated content...",
  "tags": ["ai", "nlp"],
  "sources": ["https://..."],
  "mode": "replace"   // "replace" (default) | "append"
}
// "append" mode merges tags/sources with existing values
```

### DELETE /api/cards/{id}
Response 204 No Content.

### GET /api/cards/{id}/backlinks
Cards that contain `[[This Card Title]]`.
```json
[{"id": "uuid", "title": "...", "updated_at": "..."}]
```

### GET /api/cards/{id}/versions
```json
[{"version_number": 2, "content": "...", "created_at": "..."},
 {"version_number": 1, "content": "...", "created_at": "..."}]
```

### POST /api/cards/{id}/restore
```json
// Request
{"version_number": 1}
// Creates a new update (does not overwrite history)
```

---

## Sessions

### POST /api/sessions
```json
// Request
{"query": "What do I know about the Transformer architecture?"}

// Response 201
{"id": "uuid", "query": "...", "status": "active", "created_at": "..."}
```

### POST /api/sessions/{id}/trail
`step_type`: `"thought"` | `"search"` | `"read"` | `"write"`
```json
// Request
{"step_type": "search", "content": "Searched 'transformer attention', found 2 cards"}
```

### POST /api/sessions/{id}/complete
```json
// Request
{
  "final_answer": "The Transformer uses self-attention...",
  "cited_card_ids": ["uuid1", "uuid2"]
}
```

### GET /api/sessions
Query params: `page` (default 1)
```json
[{"id": "uuid", "query": "...", "status": "completed", "created_at": "..."}]
```

---

## Raw

### POST /api/raw
```json
// Request
{
  "text": "Interesting snippet or note...",
  "source": "https://example.com/article",    // optional
  "meta": {"origin": "web", "author": "..."}  // optional, arbitrary JSON
}

// Response 201
{"id": "uuid", "text": "...", "status": "pending", "created_at": "..."}
```

### GET /api/raw
Query params: `status` (`pending`|`processed`|`skipped`), `page`

### POST /api/raw/{id}/processed
```json
{"card_id": "uuid"}   // the card created from this raw item
```

### DELETE /api/raw/{id}
Response 204.

---

## Assets

### POST /api/assets
Multipart form: field name `file`.
```bash
curl -X POST $MEMEX_BASE_URL/api/assets \
  -H "Authorization: Bearer $MEMEX_API_TOKEN" \
  -F "file=@/path/to/image.png"
```
```json
// Response 201
{"id": "uuid", "filename": "image.png", "mime_type": "image/png",
 "size_bytes": 12345, "checksum": "sha256:...", "created_at": "..."}
```

### GET /api/assets/{id}/download
Returns the binary file (proxied).

---

## Search

### GET /api/search?q=...
Full-text search across card titles and content.
```json
// Response 200
[
  {"id": "uuid", "title": "Transformer Architecture", "snippet": "...highlighted...", "score": 0.95},
  {"id": "uuid2", "title": "Attention Mechanism", "snippet": "...", "score": 0.82}
]
```

---

## Health

### GET /api/health
No auth required. Returns `{"status": "ok"}`.

---

## Error Responses

| Status | Meaning |
|--------|---------|
| 401 | Invalid or missing token |
| 403 | Token revoked or expired |
| 404 | Resource not found |
| 422 | Validation error — check request body |
| 500 | Server error |

```json
{"detail": "error message"}
```
