# Search

```
GET /api/search?q=<query>[&mode=hybrid|fts|vector]
```
**Default mode is `hybrid`. For agents, almost always omit `mode` and use the default.**

## Modes

| Mode | What it does | When to pick it |
|------|--------------|-----------------|
| `hybrid` (default) | RRF fusion of FTS + ILIKE substring + vector embedding | Always, unless you have a specific reason. Handles conceptual + keyword + literal-string queries (IDs, passwords, serials) in one shot. |
| `fts` | pg_jieba full-text + ILIKE substring (title weighted A, content weighted B) | You only want text-based matching, no semantics. |
| `vector` | nomic-embed-text 768-dim cosine similarity only | Pure semantic search, no literal-string matching needed. |

## Response shape

```json
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
      "source": "both"
    }
  ]
}
```

## Field meanings

- `score` — higher is better. Magnitude depends on mode:
  - `hybrid`: RRF score (sum of 1/(60+rank) across engines)
  - `fts`: ts_rank value
  - `vector`: cosine similarity (0~1)
- `source` — which engine surfaced the result:
  - `both` — matched by both FTS and vector (strongest signal in hybrid)
  - `vector` — only the embedding matched
  - `fts` — only text/substring matched

## Tips

- Use 1–4 keywords. Long natural-language questions still work in hybrid (vector handles them).
- If hybrid returns nothing, the card likely doesn't exist — don't keep retrying with synonyms.
- For an exact ID/password/serial, hybrid still works (ILIKE fallback inside hybrid).
- Default page size is 20; the response gives you the top results sorted by score.
