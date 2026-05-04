---
name: agent-memex
description: "Interact with the agent-memex personal knowledge base API. Use when an agent needs to: store/retrieve/search knowledge cards, link cards bidirectionally, log a reasoning session for traceability, queue raw input for later processing, manage assets, or check knowledge-base health (lint, stats). Requires a Bearer token stored in the MEMEX_API_TOKEN environment variable."
---

# agent-memex Skill

agent-memex is a personal knowledge base API. The user grows the knowledge base over time; agents read existing cards to answer questions, write new cards to capture insights, and log their reasoning so the user can audit how an answer was reached.

**Key entities**
- **Card** — a Markdown note with `tags`, `sources` (URLs), and `[[Title]]` bidirectional links
- **Session** — one reasoning run by an agent (query + trail of steps + final answer + cited cards)
- **Raw** — unstructured input queued for later distillation into cards
- **Asset** — uploaded binary files (images, PDFs)

## Setup

```bash
# Create a token once via the web UI at /tokens → 建立
export MEMEX_API_TOKEN=memex_xxxx
export MEMEX_BASE_URL=https://agent-memex.dev2.quanhox.com.tw   # prod
# or http://localhost:8360 for local
```

All requests:
```
Authorization: Bearer $MEMEX_API_TOKEN
Content-Type: application/json
```

---

## Capability Map — When to Use What

| Need | Endpoint | Why |
|------|----------|-----|
| Find existing knowledge before answering | `GET /api/search?q=` | Avoid duplicate cards; ground answers in existing notes |
| Read a specific card | `GET /api/cards/{id}` | Get full content + links |
| See what a card connects to | `GET /api/cards/{id}/backlinks` | Discover related context the user has captured |
| Capture new insight | `POST /api/cards` | Add to knowledge base |
| Update existing knowledge | `PATCH /api/cards/{id}` | Refine without losing history (auto-versioned) |
| See historical versions | `GET /api/cards/{id}/versions` | Review how the user thought about something over time |
| Restore a previous version | `POST /api/cards/{id}/restore` | Recover from a bad edit |
| Log how an answer was derived | Sessions API (see below) | Auditability + future debugging |
| Save raw input for later | `POST /api/raw` | Capture before processing (e.g., user pastes article) |
| Upload a file | `POST /api/assets` | Store images/PDFs referenced by cards |
| Check knowledge-base health | `GET /api/maintenance/lint` | Find cards needing attention (oversized, orphan, no tags) |
| Get statistics | `GET /api/maintenance/detailed-stats` | Tag distribution, growth, card health |

---

## Session — Why and How

**Purpose**: A Session is the agent's reasoning blackbox recorder for one query. It has three uses:
1. **Auditability** — the user can later inspect what cards the agent read and how it reasoned
2. **Citation tracking** — `cited_card_ids` ties an answer to specific cards; if those cards change, related sessions are flagged
3. **Activity history** — the Sessions UI shows past queries

**When to open a Session**: whenever an agent is answering a non-trivial query against the knowledge base. Skip for one-off CRUD (e.g., the user pastes a note → just create a card).

**Lifecycle**:
```bash
# 1. Open
POST /api/sessions  {"query": "What did I learn about transformers?"}
# → {id: "sess-uuid", ...}

# 2. Log each step (step_type: "thought" | "search" | "read" | "write")
POST /api/sessions/{id}/trail  {"step_type": "search", "content": "Searched 'transformer'; got 3 hits"}
POST /api/sessions/{id}/trail  {"step_type": "read",   "content": "Read card abc-123 'Attention Is All You Need'"}
POST /api/sessions/{id}/trail  {"step_type": "thought","content": "Self-attention is the core innovation..."}

# 3. Close
POST /api/sessions/{id}/complete
{"final_answer": "...", "cited_card_ids": ["abc-123", "def-456"]}
```

---

## Card Writing Guidelines

- **Markdown** with GFM extensions (tables, task lists, strikethrough OK)
- **`[[Other Card Title]]`** = link to another card (bidirectional, auto-resolved)
- **`tags`** lowercase, hyphenated (`machine-learning`, `quick-note`)
- **`sources`** = array of URLs the card is derived from
- **Search before creating** — duplicates pollute the knowledge base
- **Keep cards focused**: lint flags `word_count > 800` as oversized; prefer splitting

---

## Lint — Knowledge Base Health Check

`GET /api/maintenance/lint` returns issues for the agent or user to address:

```json
{
  "last_run": "2026-05-04T...",
  "summary": {"errors": 1, "warnings": 5, "info": 0, "total_checked": 6},
  "results": [
    {"type": "error",   "card_id": "...", "card_title": "...", "rule": "oversized", "word_count": 1200, "message": "卡片超過 800 字，建議拆分"},
    {"type": "warning", "card_id": "...", "card_title": "...", "rule": "orphan",    "message": "沒有任何連結或反向連結"},
    {"type": "warning", "card_id": "...", "card_title": "...", "rule": "no_tags",   "message": "沒有 tags"}
  ]
}
```

**Use cases**:
- After a writing session, check if newly created cards have orphan/no_tags warnings → fix them
- User asks "what should I clean up?" → lint gives a punch list
- Periodic maintenance: link orphan cards to related ones, split oversized cards

---

## Quick Reference — All Endpoints

### Search
```
GET /api/search?q=<keywords>
```

### Cards
```
GET    /api/cards?tag=&sort=&limit=&offset=
POST   /api/cards
GET    /api/cards/{id}
PATCH  /api/cards/{id}
DELETE /api/cards/{id}
GET    /api/cards/{id}/backlinks
GET    /api/cards/{id}/versions
GET    /api/cards/{id}/versions/{version_number}
POST   /api/cards/{id}/restore
```

### Sessions
```
GET  /api/sessions?page=
POST /api/sessions
GET  /api/sessions/{id}
POST /api/sessions/{id}/trail
POST /api/sessions/{id}/complete
```

### Raw
```
GET    /api/raw?status=&page=
POST   /api/raw
GET    /api/raw/{id}
DELETE /api/raw/{id}
POST   /api/raw/{id}/processed   # body: {card_id}
```

### Assets
```
GET    /api/assets?page=
POST   /api/assets               # multipart, field: file
GET    /api/assets/{id}
GET    /api/assets/{id}/download
DELETE /api/assets/{id}
```

### Maintenance
```
GET  /api/maintenance/stats              # dashboard summary
GET  /api/maintenance/detailed-stats     # full stats (growth, top tags, health)
GET  /api/maintenance/lint               # latest lint report
POST /api/maintenance/lint/run           # trigger fresh lint scan
GET  /api/maintenance/reindex            # reindex status (stub)
POST /api/maintenance/reindex/run        # trigger reindex (stub)
```

### Auth
```
POST   /api/auth/login         # {email, password, token_name}
POST   /api/auth/logout
GET    /api/auth/tokens
POST   /api/auth/tokens        # {name}
DELETE /api/auth/tokens/{token_id}
```

### Health
```
GET /api/health                # no auth required
```

---

For full request/response schemas and error codes, see [references/api_reference.md](references/api_reference.md).
