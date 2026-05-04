# Sessions

A Session is the agent's reasoning record for one user query. It captures: the original query, a trail of steps the agent took, and a final answer with citations.

## Why use Sessions

- **Auditability** — the user can later see what cards were read and how the agent reasoned
- **Citation tracking** — `cited_card_ids` ties an answer to specific cards
- **Activity history** — visible in the user's Sessions UI

## When to open one

- **Yes**: any non-trivial query that involves searching, reading, or reasoning across cards.
- **No**: pure CRUD instructions like "save this", "delete card X", "rename Y".

## Lifecycle

```bash
# 1. Open at the start of the query
POST /api/sessions
{"query": "What did I learn about transformers?"}
# → {"id": "sess-uuid", "query": "...", "status": "active", "created_at": "..."}

# 2. Log each meaningful step
POST /api/sessions/{id}/trail
{"step_type": "search", "content": "Searched 'transformer'; got 3 hits"}

POST /api/sessions/{id}/trail
{"step_type": "read", "content": "Read 'Attention Is All You Need' — confirmed self-attention is the core idea"}

POST /api/sessions/{id}/trail
{"step_type": "thought", "content": "User likely wants the intuition, not the math"}

# 3. Close with the final answer
POST /api/sessions/{id}/complete
{
  "final_answer": "The Transformer architecture uses self-attention...",
  "cited_card_ids": ["card-uuid-1", "card-uuid-2"]
}
```

## Step types

| `step_type` | Use it for |
|-------------|-----------|
| `thought` | Reasoning, planning, decisions |
| `search` | Calls to `/api/search` (record query + summary of hits) |
| `read` | Reading a specific card's content |
| `write` | Creating or updating a card during the session |

Use them honestly — they describe what the agent actually did, not what it intended.

## Listing past sessions

```
GET /api/sessions?page=1
```
```json
{
  "items": [
    {"id": "uuid", "query": "...", "status": "completed", "created_at": "..."}
  ],
  "total": 12,
  "page": 1
}
```

## Reading one session

```
GET /api/sessions/{id}
```
Returns the full session including all trail steps and the final answer.

## Tips

- Don't log every API call — log meaningful decisions and findings.
- It's fine to leave a session "active" if the agent stops mid-task; the user will see it as incomplete in the UI.
- `cited_card_ids` should be the cards that actually shaped the answer, not every card you happened to read.
