# Maintenance — Lint, Stats, Reindex

For monitoring and improving the health of the knowledge base.

## Lint

```
GET  /api/maintenance/lint            # latest report
POST /api/maintenance/lint/run        # run a fresh scan
```

Lint checks every card against three rules:

| Rule | Severity | Trigger | Suggested fix |
|------|----------|---------|---------------|
| `oversized` | error | `word_count > 800` | Split into linked cards |
| `orphan` | warning | No outgoing or incoming `[[links]]` | Link from a related card |
| `no_tags` | warning | Empty `tags` array | Add 1–3 lowercase-hyphenated tags |

Response:
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

### Lint use cases for agents

- After creating new cards, run lint and fix any orphan/no_tags warnings on the new cards.
- User asks "what should I clean up?" → fetch lint, summarize the punch list.
- Periodically, propose to split oversized cards.

## Stats

```
GET /api/maintenance/stats            # lightweight dashboard summary
GET /api/maintenance/detailed-stats   # full statistics
```

`/stats` (small):
```json
{
  "total_cards": 42,
  "total_assets": 5,
  "active_sessions": 2,
  "raw_pending": 0,
  "embedding_healthy": true
}
```

`/detailed-stats` (large):
```json
{
  "overview": {"total_cards": 42, "total_assets": 5, "total_sessions": 2, ...},
  "cards_growth": [{"date": "5/1", "count": 38}, ...],
  "top_tags": [{"tag": "ai", "count": 12}, ...],
  "top_connected": [{"id": "uuid", "title": "...", "connections": 8}, ...],
  "card_health": {"oversized": 1, "orphan": 3, "no_tags": 2, "healthy": 36},
  "file_types": [],
  "disk_usage": {"assets_mb": 0, "db_mb": 0, "logs_mb": 0}
}
```

## Reindex

```
POST /api/maintenance/reindex/run
```
Re-generates vector embeddings for all of the user's cards. Use after:
- the embedding model has changed
- you suspect some cards have missing or stale embeddings (e.g., search returns no vector results for an obvious match)

Response:
```json
{"status": "completed", "cards_processed": 16, "cards_updated": 16}
```

```
GET /api/maintenance/reindex
```
Returns the current reindex status (currently a stub returning `idle`):
```json
{"current_status": "idle", "last_run": null, "history": []}
```
