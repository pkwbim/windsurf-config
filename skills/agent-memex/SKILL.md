---
name: agent-memex
description: "Read, write, search, and link knowledge cards in the user's agent-memex personal knowledge base. Use when the agent needs to: answer a question grounded in the user's notes, capture a new insight as a card, queue raw input for later processing, log a reasoning trail, or check knowledge-base health. Requires a Bearer token in MEMEX_API_TOKEN."
---

# agent-memex Skill

The user keeps personal knowledge as **cards** — Markdown notes with tags, sources, and `[[Title]]` links between them. As an agent, you read existing cards to answer questions and write new cards to capture lasting knowledge.

## Setup

```bash
export MEMEX_BASE_URL=https://agent-memex.dev2.quanhox.com.tw
export MEMEX_API_TOKEN=memex_xxxx   # create once at /tokens → 建立
```

Every request:
```
Authorization: Bearer $MEMEX_API_TOKEN
Content-Type: application/json
```

## Defaults (read these first)

These rules cover almost every situation. Follow them unless you have a specific reason not to.

1. **Search first, always.** Before writing or answering, `GET /api/search?q=<keywords>`. Default mode is `hybrid` — it handles keywords, semantics, AND literal strings (ID numbers, passwords, serials). **Don't pass `mode=` unless you specifically need only one engine.**
2. **One Session per user query.** Open a session at the start of any non-trivial query, log key steps, and close it with the final answer + cited card IDs. Skip it only for pure CRUD (e.g., "save this note").
3. **Title matters.** Title is weighted higher than content in search ranking. Pick titles a future you would search for.
4. **Use `[[Title]]` links liberally.** Links are bidirectional and auto-resolved. They turn a flat note pile into a graph.
5. **Tags lowercase + hyphenated.** `machine-learning`, `family`, `quick-note`. No spaces, no caps.
6. **Cards under 800 words.** Lint flags `oversized` over that. If a topic gets long, split into linked cards.

---

## Common Workflows

### A. Answer a question from the knowledge base
```
1. POST /api/sessions               {"query": "<user's question>"}              → save sess_id
2. GET  /api/search?q=<keywords>                                                  → top 3-5 hits
3. GET  /api/cards/{id}             (for each promising hit)                      → full content
4. POST /api/sessions/{sess_id}/trail   {"step_type": "thought", "content": "…"} → log reasoning
5. POST /api/sessions/{sess_id}/complete {"final_answer": "…", "cited_card_ids": [...]}
```

### B. Capture a new insight as a card
```
1. GET  /api/search?q=<topic>      → make sure no duplicate exists
2. POST /api/cards
   {
     "title": "Clear, searchable title",
     "content": "## Markdown content\n\nSee also: [[Related Card]]",
     "tags": ["topic-a", "topic-b"],
     "sources": ["https://..."]    // optional
   }
```
The card is **automatically embedded** for vector search — no extra step needed.

### C. Update an existing card (creates a new version automatically)
```
PATCH /api/cards/{id}
{
  "content": "Full new content",
  "tags": ["..."],
  "mode": "replace"        // or "append" to add new content + merge tags
}
```
The previous content is saved as a version; you can view via `GET /api/cards/{id}/versions` and restore via `POST /api/cards/{id}/restore {"version_number": N}`.

### D. Save raw input to process later
```
POST /api/raw
{"text": "...", "source": "https://...", "meta": {"origin": "..."}}
```
Use this when the user pastes something you can't immediately distill into a structured card. Later, when you turn it into a card:
```
POST /api/raw/{raw_id}/processed   {"card_id": "<new card id>"}
```

### E. Maintain the knowledge base
```
GET /api/maintenance/lint           → punch list of cards needing fixes
GET /api/maintenance/detailed-stats → tag distribution, top-connected cards, growth
```
Common follow-ups:
- `orphan` warnings → add a `[[Link]]` from a related card to this one
- `no_tags` warnings → add 1–3 tags
- `oversized` errors → split into linked cards

---

## Card Structure

```markdown
---
type: person
status: active
related: [[Other Card]]
---

## Section heading

Body content with **markdown**, [links](https://...), `code`,
GFM tables, task lists, `[[wiki links]]` to other cards.
```

- **YAML front matter** between `---` lines is optional. Use it for structured metadata (status, type, dates, etc.). It is parsed and shown separately in the UI sidebar; it is NOT rendered into the body.
- **GFM extensions** work: tables, task lists (`- [ ] todo`), strikethrough (`~~text~~`), fenced code blocks.
- **`[[Title]]`** auto-resolves to a card link. If no card with that title exists, it becomes a search link.

---

## Sessions — When and Why

A Session is the agent's reasoning record for one user query.

- **Auditability** — the user can later see what cards you read and how you reasoned
- **Citation tracking** — `cited_card_ids` ties an answer to its sources
- **Activity history** — visible in the Sessions UI

**Step types** (`step_type` in trail): `thought`, `search`, `read`, `write`. Use them honestly — they describe what you actually did.

**Open a session if** the work involves searching/reading/reasoning across cards.
**Skip a session if** the user just said "save this" or "delete that".

---

## Search — One Mode for Everything

```
GET /api/search?q=<query>
```
The default mode is `hybrid` (Reciprocal Rank Fusion of keyword + semantic + substring). It handles:
- **Conceptual queries** — "transformer architecture", "焦慮"
- **Keyword queries** — "Python decorator"
- **Literal substrings** — ID numbers, phone numbers, passwords, serial codes (caught by ILIKE fallback)

Response:
```json
{
  "query": "...", "mode": "hybrid",
  "results": [
    {"id": "...", "title": "...", "tags": [...], "excerpt": "...",
     "score": 0.0328, "source": "both"}
  ]
}
```
`source` = `"both"` (matched by both engines — strongest signal), `"vector"`, or `"fts"`.

Switch to `mode=fts` or `mode=vector` only if you have a clear reason. **For agents, always start with the default.**

---

## API Quick Reference

### Search
```
GET  /api/search?q=<keywords>[&mode=hybrid|fts|vector]
```

### Cards
```
GET    /api/cards?tags=<tag>&page=N      # list (paginated, returns {items, total, page})
POST   /api/cards                        # create — auto-embeds
GET    /api/cards/{id}                   # full content + links + backlinks
PATCH  /api/cards/{id}                   # partial update — auto-versions + re-embeds
DELETE /api/cards/{id}
GET    /api/cards/{id}/backlinks
GET    /api/cards/{id}/versions
GET    /api/cards/{id}/versions/{n}
POST   /api/cards/{id}/restore           # body: {version_number}
```

### Sessions
```
GET  /api/sessions?page=N                # {items, total, page}
POST /api/sessions                       # body: {query}
GET  /api/sessions/{id}
POST /api/sessions/{id}/trail            # body: {step_type, content}
POST /api/sessions/{id}/complete         # body: {final_answer, cited_card_ids}
```

### Raw
```
GET    /api/raw?status=pending&page=N
POST   /api/raw                          # body: {text, source?, meta?}
GET    /api/raw/{id}
DELETE /api/raw/{id}
POST   /api/raw/{id}/processed           # body: {card_id}
```

### Assets
```
POST   /api/assets                       # multipart, field: file
GET    /api/assets/{id}
GET    /api/assets/{id}/download
DELETE /api/assets/{id}
```

### Maintenance
```
GET  /api/maintenance/stats              # dashboard summary
GET  /api/maintenance/detailed-stats     # full stats
GET  /api/maintenance/lint               # latest lint report
POST /api/maintenance/lint/run           # fresh lint scan
POST /api/maintenance/reindex/run        # backfill embeddings (e.g., after model change)
```

### Auth
```
POST   /api/auth/tokens                  # body: {name} — create a new agent token
GET    /api/auth/tokens                  # list (excludes web-ui tokens)
DELETE /api/auth/tokens/{id}
```

### Health
```
GET /api/health                          # no auth required
```

---

## Errors

| Status | Meaning | What to do |
|--------|---------|------------|
| 401 | Token missing or invalid | Stop; ask the user to provide a token |
| 403 | Token revoked or expired | Stop; ask the user to issue a new one |
| 404 | Resource not found | Card/session may have been deleted |
| 422 | Validation error | Check request body matches schema |
| 5xx | Server error | Retry once; if it persists, surface to the user |

Error body: `{"detail": "<message>"}`

---

For full request/response schemas, see [references/api_reference.md](references/api_reference.md).
