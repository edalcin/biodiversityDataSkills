# Grist REST API Reference

Source: [support.getgrist.com/rest-api](https://support.getgrist.com/rest-api/),
[support.getgrist.com/api](https://support.getgrist.com/api/),
[support.getgrist.com/oauth-apps](https://support.getgrist.com/oauth-apps/),
[support.getgrist.com/webhooks](https://support.getgrist.com/webhooks/).

Interactive console: https://docs.getgrist.com/apiconsole

## Authentication

### API keys (script/personal use)

1. Account settings → **Developer** page (`https://docs.getgrist.com/account/developer`) → **Create** an API key.
2. Send it as `Authorization: Bearer <API-KEY>` on every request.
3. An API key carries the **full account access** of the user who owns it.

```bash
curl -H "Authorization: Bearer <API-KEY>" https://docs.getgrist.com/api/orgs
```

- Personal site → `docs.getgrist.com`
- Team site → `<TEAM>.getgrist.com`

Changes via `POST`/`PATCH`/`PUT` need `Content-Type: application/json`:

```bash
curl -XPATCH \
  -H "Authorization: Bearer <API-KEY>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Lesson Plans"}' \
  https://<docs|TEAM>.getgrist.com/api/docs/<DOC-ID>
```

### OAuth apps (third-party tools, AI agents, partner apps)

Use instead of API keys when your tool acts on **someone else's** data. Each
user authorizes your app for specific documents/workspaces/orgs and can
revoke access individually — safer than a shared API key.

- **Discovery**: `GET https://login.getgrist.com/.well-known/oauth-authorization-server`
  (self-hosted: `GET https://<your-grist-server>/.well-known/oauth-authorization-server`)
- **Register**: Account settings → Developer → **OAuth apps** → *Register app*
  (name, redirect URI — `https://` required, `http://localhost` allowed,
  scopes). Client secret is shown once; regenerate from the app settings page
  if lost.
- **Flow**: standard OAuth 2.0 authorization code + PKCE (S256 recommended,
  **required**). Confidential clients only — no `token_endpoint_auth_method=none`.
- `offline_access` scope (refresh token) requires `prompt=consent` on the
  auth request, else `invalid_request: offline_access scope requires prompt=consent`.

### Scopes

| Scope | Grants |
|---|---|
| `doc:read` | Read records, schema, structure |
| `doc:write` | Create/update/delete records |
| `doc.schema:write` | Update structure and formulas (== the `S` access-rule permission — can read anything via formulas) |
| `doc:download` | Download the full `.grist` file (bypasses row access rules; owner-only) |
| `doc:webhooks` | Manage webhooks |
| `user.profile:read` | Name + email |
| `offline_access` | Issue a refresh token |

**Endpoints usable with OAuth tokens** (curated subset of the full REST API):

| Path | Read scope | Write scope |
|---|---|---|
| `/api/docs/{docId}/tables` | `doc:read` | `doc.schema:write` |
| `/api/docs/{docId}/tables/{tableId}/columns*` | `doc:read` | `doc.schema:write` |
| `/api/docs/{docId}/tables/{tableId}/records*` | `doc:read` | `doc:write` |
| `/api/docs/{docId}/attachments*` | `doc:read` | `doc:write` |
| `/api/docs/{docId}/download/*` (csv/xlsx/…) | `doc:read` | — |
| `/api/docs/{docId}/download` (full `.grist`) | `doc:download` | — |
| `/api/docs/{docId}/webhooks*` | `doc:webhooks` | `doc:webhooks` |
| `/api/orgs`, `/api/orgs/{orgId}/workspaces` | any `doc*` scope | — |
| `/api/workspaces/{wsId}/docs` | — | `doc:write` + `doc.schema:write` |
| `/api/profile/user` | `user.profile:read` | — |

**Tokens:** access token prefix `grist_at_` (TTL 1h); refresh token prefix
`grist_rt_` (TTL 60d, rotates on use past a fraction of its lifetime — a job
refreshing at least every 30 days runs indefinitely). Revoke per RFC 7009:
`POST /oidc/revocation`.

```bash
# 1. Authorize (browser)
$SERVER/oidc/auth?response_type=code&client_id=$CLIENT_ID&redirect_uri=$REDIRECT_URI\
  &scope=doc:read+offline_access&state=$STATE\
  &code_challenge=$PKCE_CHALLENGE&code_challenge_method=S256&prompt=consent

# 2. Exchange code
curl -u "$CLIENT_ID:$CLIENT_SECRET" "$SERVER/oidc/token" \
  -d grant_type=authorization_code -d code="$CODE" \
  -d redirect_uri="$REDIRECT_URI" -d code_verifier="$PKCE_VERIFIER"
# -> { access_token, refresh_token, expires_in, token_type: "Bearer", scope }

# 3. Call the API
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  "$SERVER/api/docs/$DOC_ID/tables/$TABLE_ID/records"

# 4. Refresh
curl -u "$CLIENT_ID:$CLIENT_SECRET" "$SERVER/oidc/token" \
  -d grant_type=refresh_token -d refresh_token="$REFRESH_TOKEN"
```

Errors follow OAuth 2.0 format: HTTP 4xx + JSON `{error, error_description}`.
Resource selection (which orgs/workspaces/docs the grant covers) is enforced
server-side; an out-of-grant request returns `403` even if the user could
otherwise access that document.

## REST endpoint groups

Full interactive reference: https://support.getgrist.com/api/. Grouped by
resource (verb prefix = HTTP method):

- **orgs** — `GET` list/describe, `PATCH` modify, `DELETE`, `GET`/`PATCH` access, `GET` usage summary
- **workspaces** — `GET` list workspaces+docs in an org, `POST` create, `GET`/`PATCH`/`DELETE` describe/modify/delete, `POST` trash/restore, `GET`/`PATCH` access
- **docs** — create (empty / import / general), `GET` describe, `PATCH` metadata, `DELETE`, trash/restore/move/pin/unpin/disable/enable/copy/fork, `GET`/`PATCH` access, `GET` "View As" users, download as SQLite/Excel/CSV/TSV/DSV, `GET` table schema, snapshots (list/remove), action history (states/compare/truncate), change proposals (list/create/apply), reload/flush/reassign/replace-content/recovery-mode, formula timing (get/start/stop), `POST` apply a list of user actions
- **records** — `GET` fetch, `POST` add, `PATCH` modify, `PUT` add-or-update (upsert), `POST` delete
- **tables** — `GET` list, `POST` add, `PATCH` modify
- **columns** — `GET` list, `POST` add, `PATCH` modify, `PUT` add-or-update, `DELETE`
- **data** — `GET`/`POST`/`PATCH`/`POST delete` — legacy row-oriented variant of records
- **attachments** — list metadata, upload, get metadata/download one/download all, upload missing, external store config, transfer status, delete unused, usage tracking, integrity verification
- **webhooks** — `GET` list, `POST` create, `PATCH` modify, `DELETE` remove, `DELETE` clear queue (all or one)
- **sql** — see below
- **users** — `DELETE`/`POST disable`/`POST enable` (admin)
- **service accounts** — CRUD + API key generation
- **scim** — SCIM 2.0 user/group provisioning (enterprise)

### SQL endpoint

`https://{host}/api/docs/{docId}/sql` — **read-only** `SELECT` (with `WITH`
allowed) directly against the document's SQLite database.

- `GET ?q=<SQL>` — simple queries, no parameters/options.
- `POST` (recommended) with JSON body:
  ```json
  { "sql": "SELECT * FROM Orders WHERE Status = ?", "args": ["Open"], "timeout": 1000 }
  ```
  `timeout` in ms, default 1000.
- Requires `Authorization: Bearer <API-KEY>` like any other endpoint.
- Only `SELECT` is permitted; any mutation attempt is rejected.
- Runs against the raw SQLite tables, so it may need owner-level access and
  is not guaranteed to fully respect granular row/column access rules —
  don't expose it to untrusted callers.

## API client libraries

Official (Grist Labs):
- JS/TS — https://www.npmjs.com/package/grist-api
- Python — https://pypi.org/project/grist-api/

Community:
- [Pygrister](https://github.com/ricpol/pygrister) (Python + CLI)
- [grist-js](https://github.com/ben-pr-p/grist-js) (TypeScript)
- [gorist](https://github.com/CoverWhale/gorist) (Go)
- [GristCTL](https://github.com/Ville-Eurometropole-Strasbourg/grist-ctl) (Go CLI)
- [vrist](https://github.com/SencilloDev/vrist) (V)
- [nimGristApi](https://github.com/enthus1ast/nimGristApi) (Nim)
- [grist-client-rs](https://github.com/QazCetelic/grist-client-rs) (Rust, in progress)
- [gristapi](https://spyrales.github.io/gristapi/) (R)

## Webhooks

Configure per-document: **Tools → Settings → API → Manage Webhooks**.

Fields: Name, Memo, Event types (add/modify), Table, optional
semicolon-separated column filter (only fires on modify if a listed column
changed), optional **Ready column** (Toggle column gating visibility — while
false, no events fire for that row; flipping true fires "add", further edits
fire "update"), URL, optional static `Authorization` header value, Enabled
toggle. Read-only: webhook id, Status (invocation history/errors).

Self-hosted: only domains in `ALLOWED_WEBHOOK_DOMAINS` are allowed; or set
`ALLOWED_WEBHOOK_DOMAINS=*` and route all webhook traffic through
`GRIST_HTTPS_PROXY` to avoid exposing internal endpoints (this is what
Grist's own SaaS does).

**Payload** — JSON array of the matching rows' fields (including `id`,
`manualSort`) — one array per delivery, multiple simultaneously-triggered
rows batch together. Failed deliveries retry periodically off a batched
queue; "Clear Queue" discards pending payloads.
