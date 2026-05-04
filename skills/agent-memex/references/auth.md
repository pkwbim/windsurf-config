# Auth — API Tokens

Most agent operations only need an existing Bearer token (already in `MEMEX_API_TOKEN`). These endpoints are for managing tokens themselves.

## Endpoints

```
POST   /api/auth/login            # email/password → token (rare; usually done via UI)
POST   /api/auth/logout           # revoke the current token
GET    /api/auth/tokens           # list all agent tokens (excludes web-ui tokens)
POST   /api/auth/tokens           # create a new named agent token
DELETE /api/auth/tokens/{id}      # revoke a specific token
```

## Create a new agent token

```json
POST /api/auth/tokens
{"name": "claude-agent"}
```
Response (201):
```json
{
  "id": "token-uuid",
  "name": "claude-agent",
  "api_token": "memex_abc...",
  "expires_at": "..."
}
```
**The plaintext `api_token` is shown ONCE.** Save it immediately. After this response, only the hashed form is stored server-side.

## List

```
GET /api/auth/tokens
```
Returns metadata for the user's tokens (does NOT return plaintext):
```json
[
  {"id": "uuid", "name": "claude-agent", "created_at": "...",
   "last_used_at": "...", "expires_at": "...", "is_revoked": false}
]
```
Web UI tokens (`name == "web-ui"`) are filtered out.

## Revoke

```
DELETE /api/auth/tokens/{token_id}
```
Returns 204. The token stops working immediately.

## Login (unusual)

```json
POST /api/auth/login
{"email": "user@example.com", "password": "...", "token_name": "my-agent"}
```
This is normally done by the web UI. Agents almost always start with a token already provisioned via the `/tokens` page in the UI.

## Tips

- **Never log plaintext tokens.** Treat them like passwords.
- Tokens expire after 30 days by default. If a 401 starts happening, the token may have expired.
- Use distinct names for distinct agents/tools so the user can tell them apart and revoke selectively.
