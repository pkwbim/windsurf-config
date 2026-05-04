# Cards

A card is a Markdown note with `tags`, `sources` (URLs), and `[[Title]]` links to other cards.

## Endpoints

```
GET    /api/cards?tags=<tag>&page=N      # list (paginated)
POST   /api/cards                        # create — auto-embeds in background
GET    /api/cards/{id}                   # full content + links + backlinks
PATCH  /api/cards/{id}                   # partial update — auto-versions + re-embeds
DELETE /api/cards/{id}
GET    /api/cards/{id}/backlinks
GET    /api/cards/{id}/versions
GET    /api/cards/{id}/versions/{n}
POST   /api/cards/{id}/restore           # body: {version_number}
```

## Create

```json
POST /api/cards
{
  "title": "Attention Is All You Need",
  "content": "## Summary\n\nThe Transformer model uses self-attention.\n\nSee [[Neural Networks]].",
  "tags": ["ai", "nlp", "paper"],
  "sources": ["https://arxiv.org/abs/1706.03762"]
}
```
Response: full card object (see "Read" below) plus `created_at`. Embedding is generated in the background — search will pick it up shortly after.

### YAML front matter (optional)

`content` may begin with YAML between `---` lines for structured metadata. It's parsed and shown in the UI sidebar; it is NOT rendered into the body HTML.

```markdown
---
type: paper
status: read
year: 2017
---

## Summary

Body content here…
```

### Markdown features

- GFM extensions: tables, task lists (`- [ ] todo`), strikethrough (`~~text~~`), fenced code blocks
- `[[Other Card Title]]` auto-resolves to a card link (or a search link if no card with that title exists)
- Links between cards are bidirectional — backlinks are computed automatically
- `![[filename.png]]` embeds an uploaded asset (image → `<img>`, other files → download link). Use `![[folder/filename.png]]` for assets stored in a folder. See [assets.md](assets.md) for upload and folder details.

## List

```
GET /api/cards?tags=ai&page=1
```
Query params: `tags` (repeatable, e.g. `?tags=ai&tags=nlp`), `page` (default 1).

```json
{
  "items": [
    {
      "id": "uuid", "title": "...", "tags": ["..."],
      "word_count": 120, "oversized": false, "connections": 3,
      "created_at": "...", "updated_at": "..."
    }
  ],
  "total": 42,
  "page": 1
}
```

## Read

```
GET /api/cards/{id}
```
```json
{
  "id": "uuid",
  "title": "...",
  "content": "...",
  "tags": ["..."],
  "sources": ["..."],
  "word_count": 45,
  "oversized": false,
  "connections": 2,
  "links":     [{"id": "uuid2", "title": "Linked Card"}],     // outgoing [[links]]
  "backlinks": [{"id": "uuid3", "title": "Card Linking Here"}],
  "created_at": "...",
  "updated_at": "..."
}
```

## Update

All fields optional.

```json
PATCH /api/cards/{id}
{
  "content": "Full new content...",     // body
  "tags": ["ai", "nlp"],                // tag list
  "sources": ["https://..."],
  "mode": "replace"                     // "replace" (default) or "append"
}
```
- `mode: "replace"` — overwrite content. Old content saved as a version automatically.
- `mode: "append"` — append `content` to existing body, merge `tags` and `sources` with existing values.

Embedding is regenerated in the background after every update.

## Versions and restore

```
GET  /api/cards/{id}/versions          → list of versions, newest first
GET  /api/cards/{id}/versions/{n}      → specific version content
POST /api/cards/{id}/restore           → body: {"version_number": N}
```
Restore creates a new update with the old content; it does NOT erase newer versions.

## Backlinks

```
GET /api/cards/{id}/backlinks
```
Returns cards that contain `[[<this card's title>]]`.
```json
[{"id": "uuid", "title": "...", "updated_at": "..."}]
```

## Delete

```
DELETE /api/cards/{id}
```
Returns 204. Deletes the card, its versions, and any links pointing to it.

## Tips

- **Title is heavily weighted in search ranking.** Choose titles a future user would search for.
- **Search before creating** to avoid duplicates: see [search.md](search.md).
- **Lint flags** `oversized` (>800 words), `orphan` (no in/out links), `no_tags` — see [maintenance.md](maintenance.md).
