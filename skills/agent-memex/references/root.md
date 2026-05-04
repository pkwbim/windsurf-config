# Root Card (Homepage)

The user can pin **one** card as their root — like a homepage or dashboard for the knowledge base. The UI exposes it as 「首頁」in the sidebar. The root card has no special schema; it's just a regular card that the user (or an agent) chose as the entry point.

## Endpoints

```
GET    /api/root           # full content of the current root card (404 if none set)
PUT    /api/root           # body: {card_id} — set a card as root
DELETE /api/root           # unset (no body, returns 204)
```

## Read the root card

```
GET /api/root
```

If a root is set, returns the full card object (same shape as `GET /api/cards/{id}`):
```json
{
  "id": "uuid", "title": "我的知識庫首頁",
  "content": "...", "tags": [...], "sources": [...],
  "links": [...], "backlinks": [...],
  ...
}
```

If no root is set: `404` with `{"detail": "尚未設定根卡片"}`.

## Set the root card

```json
PUT /api/root
{"card_id": "uuid-of-existing-card"}
```
Response:
```json
{"card_id": "uuid", "title": "..."}
```
The card must already exist (otherwise 404). There is exactly **one** root per user — setting a new one replaces the previous.

## Unset the root card

```
DELETE /api/root
```
Returns 204. Subsequent `GET /api/root` will return 404.

## When agents should touch this

- **Read** `GET /api/root` at the start of a session to see the user's curated entry point — useful for orienting before searching.
- **Write the content** of the root card (`PATCH /api/cards/{root_id}`) to keep the homepage fresh: list of important cards, current focus, todo, recent activity, etc.
- **Set** a card as root (`PUT /api/root`) only when the user explicitly asks ("make this my homepage").

## Notes

- If the root card is deleted, the database FK clears the reference automatically (`ON DELETE SET NULL`). `GET /api/root` will then return 404.
- The root card still shows up in regular `/api/cards` listings and search — it isn't hidden.
