# agent-memex API Reference

Base URL: `$MEMEX_BASE_URL`
- Production: `https://agent-memex.dev2.quanhox.com.tw`
- Local: `http://localhost:8360`
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
Query params: `tags` (repeatable, e.g. `?tags=ai&tags=nlp`), `page` (default 1).
```json
// Response 200
{
  "items": [{"id": "uuid", "title": "...", "tags": [], "word_count": 120,
             "oversized": false, "connections": 3,
             "created_at": "...", "updated_at": "..."}],
  "total": 42,
  "page": 1
}
```

### POST /api/cards
`content` may begin with optional YAML front matter delimited by `---` lines; it will be parsed and shown separately as metadata in the UI sidebar (and stripped before rendering as HTML).
```json
// Request
{
  "title": "Attention Is All You Need",
  "content": "---\ntype: paper\nstatus: read\n---\n\n## Summary\n\nThe Transformer model...\n\nSee also: [[Neural Networks]]",
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
  "word_count": 45, "oversized": false, "connections": 2,
  "links":     [{"id": "uuid2", "title": "Neural Networks"}],   // outgoing [[links]]
  "backlinks": [{"id": "uuid3", "title": "Deep Learning"}],     // cards linking to this
  "created_at": "...", "updated_at": "..."
}
```

Note: card creation and updates automatically trigger embedding regeneration in the background.

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
Query params: `page` (default 1).
```json
{
  "items": [{"id": "uuid", "query": "...", "status": "completed", "created_at": "..."}],
  "total": 12,
  "page": 1
}
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
Query params: `status` (`pending`|`processed`|`skipped`), `page` (default 1).
```json
{
  "items": [{"id": "uuid", "text": "...", "status": "pending", "created_at": "..."}],
  "total": 5,
  "page": 1
}
```

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

### GET /api/search?q=...&mode=hybrid
Three modes:
- `hybrid` (default) — combines FTS + ILIKE substring + vector via Reciprocal Rank Fusion (RRF, k=60). **Recommended for almost all queries** — covers conceptual, keyword, and literal-string (ID, password, serial) cases in one shot.
- `fts` — pg_jieba full-text + ILIKE substring (title weighted A, content weighted B). Use when you want only text-based matching.
- `vector` — nomic-embed-text 768-dim cosine similarity only. Use for purely semantic queries (no literal strings).

```json
// Response 200
{
  "query": "transformer",
  "mode": "hybrid",
  "results": [
    {
      "id": "uuid",
      "title": "Attention Is All You Need",
      "tags": ["ai", "nlp"],
      "excerpt": "...highlighted snippet...",
      "score": 0.0328,
      "source": "both"   // "fts" | "vector" | "both"
    }
  ]
}
```

**Score interpretation by mode:**
- `hybrid`: RRF score (sum of 1/(60+rank) across engines); higher is better
- `fts`: ts_rank value
- `vector`: cosine similarity (0~1)

The `source` field indicates which engine surfaced the result. In hybrid mode, `"both"` means both engines ranked it; this is the strongest signal.

---

## Maintenance

Use these to monitor knowledge-base health and statistics.

### GET /api/maintenance/stats
Lightweight dashboard summary.
```json
{
  "total_cards": 42,
  "total_assets": 5,
  "active_sessions": 2,
  "raw_pending": 0,
  "embedding_healthy": true
}
```

### GET /api/maintenance/detailed-stats
Full statistics including growth trends, top tags, top connected cards, and card health distribution.
```json
{
  "overview": {
    "total_cards": 42, "total_raw": 0, "total_assets": 5,
    "total_sessions": 2, "db_size_mb": 0, "last_reindex": null
  },
  "cards_growth": [{"date": "5/1", "count": 38}, {"date": "5/2", "count": 40}, ...],
  "top_tags": [{"tag": "ai", "count": 12}, ...],
  "top_connected": [{"id": "uuid", "title": "...", "connections": 8}, ...],
  "card_health": {"oversized": 1, "orphan": 3, "no_tags": 2, "healthy": 36},
  "file_types": [],
  "disk_usage": {"assets_mb": 0, "db_mb": 0, "logs_mb": 0}
}
```

### GET /api/maintenance/lint
Returns the latest lint report. Each card is checked against three rules:
- `oversized` (error) — `word_count > 800`, suggest splitting
- `orphan` (warning) — no outgoing or incoming `[[links]]`
- `no_tags` (warning) — empty tags array

```json
{
  "last_run": "2026-05-04T07:30:00+00:00",
  "status": "completed",
  "summary": {"errors": 1, "warnings": 5, "info": 0, "total_checked": 6},
  "results": [
    {
      "type": "error",
      "card_id": "uuid",
      "card_title": "Long Article",
      "rule": "oversized",
      "message": "卡片超過 800 字，建議拆分",
      "word_count": 1200
    },
    {
      "type": "warning",
      "card_id": "uuid2",
      "card_title": "Stranded Note",
      "rule": "orphan",
      "message": "沒有任何連結或反向連結"
    }
  ]
}
```

### POST /api/maintenance/lint/run
Triggers a fresh scan. Same response shape as `GET /api/maintenance/lint`.

### POST /api/maintenance/reindex/run
Re-generates embeddings for all cards belonging to the authenticated user.
Use after the embedding model changes, or to fix cards with missing/stale embeddings.
```json
{"status": "completed", "cards_processed": 16, "cards_updated": 16}
```

### GET /api/maintenance/reindex
Returns reindex history (currently a stub returning idle state):
```json
{"current_status": "idle", "last_run": null, "history": []}
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
