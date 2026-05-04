# Assets

Binary files (images, PDFs) attached to or referenced by cards.

## Endpoints

```
GET    /api/assets?page=N
POST   /api/assets                        # multipart/form-data, field: file
GET    /api/assets/{id}
GET    /api/assets/{id}/download
DELETE /api/assets/{id}
```

## Upload

Multipart form, field name `file`:

```bash
curl -X POST $MEMEX_BASE_URL/api/assets \
  -H "Authorization: Bearer $MEMEX_API_TOKEN" \
  -F "file=@/path/to/image.png"
```

Response:
```json
{
  "id": "uuid",
  "filename": "image.png",
  "mime_type": "image/png",
  "size_bytes": 12345,
  "checksum": "sha256:...",
  "created_at": "..."
}
```

## Download

```
GET /api/assets/{id}/download
```
Returns the raw binary file. The server proxies the file through (the underlying storage path is internal).

## Delete

```
DELETE /api/assets/{id}
```
Returns 204. Deletes the asset record AND the underlying file on disk.

## Tips

- Reference an asset from a card by including a Markdown link:
  `![alt text]($MEMEX_BASE_URL/api/assets/<id>/download)`
- Upload before referencing — the asset must exist before a card links to it.
