# Raw Input

A "Raw" item is unstructured text the user wants to keep but hasn't yet distilled into a structured card. Use this when the user pastes something quickly and you can't immediately turn it into a well-formed card.

## When to use Raw vs Card

- **Raw** — quick capture, no structure required, will process later. Examples: a clipped article, a brain-dump, a screenshot's transcript.
- **Card** — structured knowledge with a meaningful title and intentional content. Created when you (or the user) have time to organize.

## Endpoints

```
GET    /api/raw?status=pending&page=N
POST   /api/raw                         # body: {text, source?, meta?}
GET    /api/raw/{id}
DELETE /api/raw/{id}
POST   /api/raw/{id}/processed          # body: {card_id}
```

## Create

```json
POST /api/raw
{
  "text": "Interesting snippet or note from the user",
  "source": "https://example.com/article",   // optional
  "meta": {"origin": "web", "author": "..."}  // optional, arbitrary JSON
}
```
Response:
```json
{"id": "uuid", "text": "...", "status": "pending", "created_at": "..."}
```

## List

```
GET /api/raw?status=pending&page=1
```
- `status` — filter by `pending` | `processed` | `skipped`. Omit for all.
- `page` — default 1.

```json
{
  "items": [{"id": "uuid", "text": "...", "status": "pending", "created_at": "..."}],
  "total": 5,
  "page": 1
}
```

## Mark as processed (after creating a card from it)

```json
POST /api/raw/{raw_id}/processed
{"card_id": "uuid-of-newly-created-card"}
```
This sets `status: "processed"` and links the raw item to the resulting card. The raw item is kept for traceability — don't delete it.

## Delete

```
DELETE /api/raw/{id}
```
Use only if the raw item was a mistake (e.g., duplicate, accidental capture).

## Typical workflow

1. User pastes/dictates something → `POST /api/raw`.
2. Later, agent (or user) decides to distill it → `POST /api/cards` with structured content.
3. Mark the raw item processed → `POST /api/raw/{raw_id}/processed`.
