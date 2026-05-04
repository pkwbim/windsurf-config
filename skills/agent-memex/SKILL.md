---
name: agent-memex
description: "Read, write, search, and link knowledge cards in the user's agent-memex personal knowledge base. Use when the agent needs to: answer a question grounded in the user's notes, capture a new insight as a card, queue raw input, log a reasoning trail, or check knowledge-base health. Requires a Bearer token in MEMEX_API_TOKEN. Detailed guides for each capability are in references/ — read only the one you need."
---

# agent-memex Skill

The user keeps personal knowledge as **cards** — Markdown notes with tags, sources, and `[[Title]]` links between them. Read existing cards to answer questions; write new cards to capture lasting knowledge.

## Setup

```bash
export MEMEX_BASE_URL=https://agent-memex.dev2.quanhox.com.tw
export MEMEX_API_TOKEN=memex_xxxx       # create once at /tokens → 建立
```
Every request needs:
```
Authorization: Bearer $MEMEX_API_TOKEN
Content-Type: application/json
```

## Defaults — follow unless you have a specific reason not to

1. **Search first.** Before answering or writing, hit `/api/search` (default mode `hybrid` covers keywords + semantics + literal strings).
2. **One Session per user query.** Open a session at the start, log key steps, close with the answer + `cited_card_ids`. Skip only for pure CRUD.
3. **Title matters** — it's weighted higher than content in search. Pick searchable titles.
4. **Use `[[Title]]` links** liberally. They're bidirectional and auto-resolved.
5. **Tags lowercase + hyphenated**: `machine-learning`, `family`, `quick-note`.
6. **Cards under 800 words.** Split if longer.

## Read more — only when you need it

Each guide is self-contained. Read just the one(s) for your current task.

| Task | Read |
|------|------|
| Search the knowledge base | [references/search.md](references/search.md) |
| Create / update / read / delete cards, link cards, use front matter | [references/cards.md](references/cards.md) |
| Log a reasoning Session | [references/sessions.md](references/sessions.md) |
| Save raw user input for later | [references/raw.md](references/raw.md) |
| Upload / link binary files | [references/assets.md](references/assets.md) |
| Lint, stats, reindex | [references/maintenance.md](references/maintenance.md) |
| Manage API tokens | [references/auth.md](references/auth.md) |
| Look up an HTTP error code | [references/errors.md](references/errors.md) |

## Minimal example: answer a question

```bash
# 1. Open a session
SESS=$(curl -s -X POST $MEMEX_BASE_URL/api/sessions \
  -H "Authorization: Bearer $MEMEX_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"query":"What did I learn about transformers?"}' | jq -r .id)

# 2. Search (default hybrid)
curl -s "$MEMEX_BASE_URL/api/search?q=transformer" \
  -H "Authorization: Bearer $MEMEX_API_TOKEN"

# 3. Read a card
curl -s $MEMEX_BASE_URL/api/cards/<id> -H "Authorization: Bearer $MEMEX_API_TOKEN"

# 4. Close the session
curl -s -X POST $MEMEX_BASE_URL/api/sessions/$SESS/complete \
  -H "Authorization: Bearer $MEMEX_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"final_answer":"...","cited_card_ids":["<id>"]}'
```

If you need anything beyond this flow — refining writes, handling versions, dealing with raw input, or interpreting lint output — read the matching file in `references/` first.
