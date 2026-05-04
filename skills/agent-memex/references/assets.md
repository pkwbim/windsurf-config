# Assets

Binary files (images, PDFs, etc.) that can be uploaded and embedded in cards.

## Endpoints

```
GET    /api/assets?page=N
POST   /api/assets                        # multipart/form-data, fields: file, folder (optional)
GET    /api/assets/names                  # {wiki-key: id} map for ![[]] resolution
GET    /api/assets/{id}
GET    /api/assets/{id}/download
DELETE /api/assets/{id}
```

## Upload

Multipart form, field name `file`. Optionally include `folder` (a logical label, not a filesystem path):

```bash
# Root-level file
curl -X POST $MEMEX_BASE_URL/api/assets \
  -H "Authorization: Bearer $MEMEX_API_TOKEN" \
  -F "file=@/path/to/photo.png"

# File inside a folder
curl -X POST $MEMEX_BASE_URL/api/assets \
  -H "Authorization: Bearer $MEMEX_API_TOKEN" \
  -F "file=@/path/to/photo.png" \
  -F "folder=images"
```

Response:
```json
{
  "id": "uuid",
  "name": "photo.png",
  "folder": "images",
  "mime_type": "image/png",
  "size": 12345,
  "checksum": "sha256:...",
  "created_at": "..."
}
```

## Folders

`folder` is a logical label (e.g. `images`, `documents`, `diagrams`). It is separate from how files are stored on disk — the server stores files under `YYYY/MM/uuid.ext` automatically.

- Names within the same folder must be unique per user. The DB enforces `(user_id, folder, name)` uniqueness.
- Root-level files (no folder) use `folder: ""`.

## Naming rule (important)

**The agent is responsible for choosing a filename that won't collide.** Uploading a file with the same `(folder, name)` as an existing asset returns **`409 Conflict`** — the API does not auto-rename and does not silently overwrite.

```json
HTTP 409
{"detail": "檔名已存在：images/photo.png。請改名後重試，或先刪除舊的 asset。"}
```

When you hit a 409:
- **If you intend to update the existing file** (same logical asset, new bytes): `DELETE /api/assets/{id}` first, then re-upload. (No PATCH endpoint for asset content.)
- **If it's a different file that happens to have the same name**: pick a more specific name (e.g. `kgi-bank-form-2026-05.jpg` instead of `form.jpg`) or put it in a different `folder`.

Do not retry blindly with the same name. Names should be descriptive enough that collisions are rare in practice.

## Embed in cards with `![[]]`

Reference an asset using wiki syntax inside card content:

```markdown
![[photo.png]]              # root-level file (folder: "") — rendered as <img>
![[images/photo.png]]       # file in the "images" folder — rendered as <img>
![[documents/report.pdf]]   # non-image — rendered as a download link
```

**How to construct the wiki key after uploading:**

Use the `name` and `folder` fields from the upload response:

```
folder == ""        →  ![[{name}]]
folder == "images"  →  ![[images/{name}]]
```

Example: upload returns `{"name": "photo.png", "folder": "images"}` → write `![[images/photo.png]]` in the card.

**Do not guess or hard-code the filename.** Always derive the key from the upload response or from `GET /api/assets/names`.

- `mime_type` starting with `image/` → rendered as `<img>` (determined by DB value, not extension)
- All other `mime_type` → rendered as a download link
- Unresolved key → rendered as inline code `` `![[...]]` `` (won't break the page)

URLs are resolved server-side at render time using relative paths, so they work regardless of which domain the app is running on.

## Name resolution map

```
GET /api/assets/names
```
Returns a flat `{wiki-key: id}` map used internally by the renderer:
```json
{
  "photo.png": "uuid1",
  "images/banner.png": "uuid2",
  "documents/report.pdf": "uuid3"
}
```
Key format: `folder/name` for files with a folder, `name` for root files.

## Download

```
GET /api/assets/{id}/download
```
Returns the raw binary file with the correct `Content-Type`.

## Delete

```
DELETE /api/assets/{id}
```
Returns 204. Deletes both the DB record and the file on disk.

## Tips

- Choose `folder` names that group files by type or topic: `images`, `diagrams`, `docs`, `screenshots`.
- Upload before referencing — the asset must exist before a card can embed it.
- The `folder` in the wiki key must match exactly, including case.
