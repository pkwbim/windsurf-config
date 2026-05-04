---
name: agent-memex
description: "Interact with the agent-memex knowledge base API. Use when an agent needs to store, retrieve, search, or link knowledge cards; log a reasoning session; queue raw input for processing; or manage assets. Requires a Bearer token stored in the MEMEX_API_TOKEN environment variable."
---

# agent-memex Skill

agent-memex is a personal knowledge base API. Cards are Markdown documents with tags, source URLs, and `[[Title]]` bidirectional links. Agents read/write cards, log sessions (reasoning trails), and queue raw input.

## Setup

```bash
# Token is created once via the web UI at /tokens → Create
export MEMEX_API_TOKEN=memex_xxxx   # store in .env or agent config
export MEMEX_BASE_URL=http://localhost:8360  # or prod URL
```

All requests require:
```
Authorization: Bearer $MEMEX_API_TOKEN
Content-Type: application/json
```

## Core Workflow

```
1. Search first        → GET /api/search?q=<keywords>
2. Read card detail    → GET /api/cards/{id}
3. Create or update    → POST /api/cards  /  PATCH /api/cards/{id}
4. Log session         → POST /api/sessions → POST /sessions/{id}/trail → POST /sessions/{id}/complete
5. Queue raw input     → POST /api/raw
```

## Quick Reference

### Search
```bash
GET /api/search?q=machine+learning
# Returns: [{id, title, snippet, score}]
```

### Cards
```bash
# List
GET /api/cards?tag=ai&sort=updated&limit=20&offset=0

# Create
POST /api/cards
{"title": "Transformer Architecture", "content": "...", "tags": ["ai","nlp"], "sources": ["https://..."]}

# Read
GET /api/cards/{id}
# Returns: {id, title, content, tags, sources, word_count, oversized, links[], created_at, updated_at}

# Update (partial)
PATCH /api/cards/{id}
{"content": "...", "tags": ["ai"], "sources": [], "mode": "replace"}
# mode: "replace" (default) overwrites tags/sources; "append" merges them

# Backlinks (cards that link TO this card)
GET /api/cards/{id}/backlinks

# Version history & restore
GET /api/cards/{id}/versions
POST /api/cards/{id}/restore  {"version_number": 3}
```

### Sessions (reasoning log)
```bash
# Start
POST /api/sessions  {"query": "What do I know about transformers?"}
# → {id, ...}

# Log trail steps (step_type: "thought" | "search" | "read" | "write")
POST /api/sessions/{id}/trail
{"step_type": "search", "content": "Searched for 'attention mechanism', found 3 cards"}

# Complete
POST /api/sessions/{id}/complete
{"final_answer": "...", "cited_card_ids": ["uuid1", "uuid2"]}
```

### Raw input (queue for later processing)
```bash
POST /api/raw
{"text": "raw note or clipping", "source": "https://...", "meta": {"origin": "web"}}

# Mark processed after creating a card from it
POST /api/raw/{id}/processed  {"card_id": "uuid"}
```

## Card Writing Guidelines

- Use `[[Other Card Title]]` syntax to link to related cards — links are bidirectional
- Keep content in Markdown; `oversized` is set automatically when word_count > 800
- `tags` should be lowercase, hyphenated (e.g., `machine-learning`, `quick-note`)
- Always search before creating to avoid duplicates

## Full API Reference

For complete request/response schemas and error codes, see [references/api_reference.md](references/api_reference.md).
