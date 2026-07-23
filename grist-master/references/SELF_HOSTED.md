# Self-Hosted Grist

Source: [support.getgrist.com/self-managed](https://support.getgrist.com/self-managed/),
[support.getgrist.com/technical-docs](https://support.getgrist.com/technical-docs/).

## Editions

- **Full edition** — licensed, all features (admin controls, automations,
  email notifications, AI assistant, audit logging, cloud storage). 30-day
  free trial on any install; then requires an activation key
  (`GRIST_ACTIVATION` or `GRIST_ACTIVATION_FILE`), or revert to Community.
- **Grist Community edition** — free, open-source (Apache-2.0,
  [github.com/gristlabs/grist-core](https://github.com/gristlabs/grist-core/)):
  editing, access control, forms, SSO. Toggle full ↔ Community from the
  **Admin Panel**.
- **Grist Desktop** — Electron app built on Community edition, no
  internet/account needed: https://github.com/gristlabs/grist-desktop/releases

## Install (Docker)

```bash
docker run -p 8484:8484 \
  -v ~/grist:/persist \
  -e GRIST_SESSION_SECRET=invent-a-secret-here \
  -e GRIST_DEFAULT_EMAIL=your-email@example.com \
  -it gristlabs/grist
```

- Visit `http://localhost:8484` → boot login → Quick setup wizard.
- Image `gristlabs/grist` toggles full/Community; `gristlabs/grist-oss` is
  Community-only (no toggle), less opinionated telemetry defaults.
- `/persist` volume is required — everything durable lives there.
- Port `8484` (override via `PORT`).
- `GRIST_SESSION_SECRET` must be set to a real secret.
- AWS/Azure hosting: see the "Grist Builder Edition" doc.

Typical next steps: sandboxing → serving from a public host → auth → snapshots.

## Administrator account

The user matching `GRIST_DEFAULT_EMAIL` (default `you@example.com` if unset)
becomes admin on first run — access to Admin Panel → Installation. Changing
`GRIST_DEFAULT_EMAIL` later **revokes** admin from the old user (unless
they've separately been added as a team owner beforehand via
[team sharing](./#how-do-i-set-up-a-team)).

**Multiple admins** (full edition): unset `GRIST_SINGLE_ORG`, create a team
site (e.g. `admins`), add the desired users as `OWNER` role on it, set
`GRIST_INSTALL_ADMIN_ORG=admins`, restart.

## Sandboxing (important for production)

```bash
docker run ... -e GRIST_SANDBOX_FLAVOR=gvisor ...
```

Isolates each document's Python formulas from other documents and the
network, using [gvisor](https://gvisor.dev/). Verify: a formula
`import glob; glob.glob('/etc/*')` should return empty.

- **`XSAVE` missing** — CPU needs Sandy Bridge+ (`x86_64`); check
  `grep -q '\bxsave\b' /proc/cpuinfo`.
- **`PTRACE` unavailable** — grant `--cap-add=SYS_PTRACE` (Docker) or the
  equivalent capability (e.g. AWS ECS `linuxParameters.capabilities`).

## Serving publicly

Set `APP_HOME_URL="https://grist.example.com"`. Requires a reverse proxy for
TLS termination that forwards **HTTP 1.1 websockets** (`Upgrade`,
`Connection`, `Host` headers) — a broken proxy config breaks live
collaboration. Minimal nginx example:

```nginx
server {
    server_name grist.example.com;
    location / {
        proxy_pass http://localhost:8484;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```
[Grist Omnibus](https://github.com/gristlabs/grist-omnibus) bundles Grist +
reverse proxy + Let's Encrypt automatically.

## Single-team mode

```bash
docker run ... -e GRIST_SINGLE_ORG=cool-beans ...
```
Drops the `/o/<team-name>` URL prefix for installs that will only ever have
one team (lowercase a-z, 0-9, `-` only). Combine with `GRIST_HIDE_UI_ELEMENTS`
(see [Customization](#customization)).

## Authentication

`GRIST_FORCE_LOGIN=true` redirects anonymous users to login.
`COOKIE_MAX_AGE` — session cookie lifetime in ms, or `none` for a
browser-session-only cookie. Multiple SSO methods (OIDC, SAML, etc.) — see
the dedicated `install/authentication-overview` doc for exact env vars.

## Customization

- **`GRIST_HIDE_UI_ELEMENTS`** — comma-separated:
  `helpCenter,billing,templates,multiSite,multiAccounts`.
- **`GRIST_PAGE_TITLE_SUFFIX`** — replaces the default `- Grist` suffix; set
  to `_blank` to remove entirely.
- **Custom CSS**: `APP_STATIC_INCLUDE_CUSTOM_CSS=true` loads `custom.css`
  (mount over `/grist/static/custom.css`; every rule needs `!important`).
  Template: [grist-core's custom.css](https://github.com/gristlabs/grist-core/blob/main/static/custom.css).
  `APP_STATIC_URL` serves static assets from a CDN (custom CSS must then be
  reachable from that base URL too).
- **Custom widget gallery**: `GRIST_WIDGET_LIST_URL=https://github.com/gristlabs/grist-widget/releases/download/latest/manifest.json`
  (or your own fork/`manifest.json`). Optional without it — widgets still
  work by full URL, just no gallery picker. `manifest.json` fields: `name`,
  `description`, `authors`, `lastUpdatedAt`.
- **Email notifications**: needs a [state store](#state-store-redis) +
  [Nodemailer](https://nodemailer.com/) config:
  ```bash
  -e GRIST_NODEMAILER_CONFIG='{"host":"smtp.example.com","port":587,"auth":{"user":"u","pass":"p"}}' \
  -e GRIST_NODEMAILER_SENDER='{"name":"Grist Admin","email":"admin@example.com"}' \
  -e REDIS_URL="redis://hostname/N"
  ```
- **Extra Python packages** for formulas: not configurable without building
  a custom image:
  ```dockerfile
  FROM gristlabs/grist
  RUN apt update && apt install -y openssl && python3 -m pip install phonenumbers
  ```
  Documents made with custom packages don't carry them when copied to
  another installation — formulas will error there.
- **Webhooks**: only `ALLOWED_WEBHOOK_DOMAINS`-listed hosts are reachable —
  see [INTEGRATIONS.md](INTEGRATIONS.md#webhooks).

## Operations

### Hardware

Reasonable baseline: **8 GB RAM, 2 CPUs, 20 GB disk**. Architectures:
x86_64 (Sandy Bridge+ if sandboxed) and ARM64. Each document is its own
SQLite DB — footprint scales with concurrently-active documents, not total
document count. Sandboxing needs `gvisor`-compatible capabilities: works in
plain Docker containers, AWS EC2, AWS Fargate (with `SYS_PTRACE`
capability); fails on pre-Sandy-Bridge Intel CPUs (no `XSAVE`).

### What Grist stores (in `/persist`)

- `docs/*.grist` — one SQLite file per document (inspectable with `sqlite3`,
  portable between installs). Snapshot support adds sidecar files per doc.
- `grist-sessions.db` — SQLite session store (superseded by Redis if configured).
- `home.sqlite3` — the **home database**: org/workspace/doc metadata only
  (names, timestamps — not document contents). Swap for PostgreSQL via
  `TYPEORM_TYPE=postgres` + `TYPEORM_DATABASE`/`_USERNAME`/`_PASSWORD`/`_HOST`/`_PORT`.
  Supported PostgreSQL 10–16; **disable JIT** (`-c jit=off`) on PG ≥12 for
  Grist versions <1.5.0 — it causes multi-second-per-cell slowdowns. Grist
  ≥1.5.0 disables PG JIT automatically.
- Grist Omnibus adds `auth/` (login state DB + certs) and `param/` (secrets).

### State store (Redis)

`REDIS_URL=redis://hostname/N` — optional for most features, **required**
for webhooks and notifications, recommended for snapshots.

### Snapshots / cloud storage

S3-compatible (any edition) or Azure (full edition) sync of documents +
version history. Local MinIO test setup:

```bash
docker network create grist
docker run --rm --network grist --name redis redis
docker run --rm --network grist --name minio -v /tmp/minio:/data \
  -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=grist -e MINIO_ROOT_PASSWORD=admingrist \
  -it minio/minio server /data -console-address ":9001"
# create+version-enable a "grist-docs" bucket at http://localhost:9000

docker run --rm --network grist \
  -e GRIST_DOCS_MINIO_ACCESS_KEY=grist -e GRIST_DOCS_MINIO_SECRET_KEY=admingrist \
  -e GRIST_DOCS_MINIO_USE_SSL=0 -e GRIST_DOCS_MINIO_BUCKET=grist-docs \
  -e GRIST_DOCS_MINIO_ENDPOINT=minio -e GRIST_DOCS_MINIO_PORT=9000 \
  -e REDIS_URL=redis://redis \
  -v /tmp/grist:/persist -p 8484:8484 -it gristlabs/grist
```
For real AWS S3: point `GRIST_DOCS_MINIO_ENDPOINT=s3.amazonaws.com` with
your AWS keys (default region `us-east-1`, override with
`GRIST_DOCS_MINIO_BUCKET_REGION`).

**External attachments**: enable snapshots, set
`GRIST_EXTERNAL_ATTACHMENTS_MODE=snapshots`, then enable per-document in
Document Settings.

### Telemetry

Off by default. Opt in via the "Support Grist" banner (owner only) or
`GRIST_TELEMETRY_LEVEL=limited` (env var takes priority over the UI
setting; `off` is the alternative explicit value). Sends usage-shape data
(not document contents) to help Grist Labs prioritize self-hosting work.

### Automatic version checks

Weekly check by default on `gristlabs/grist`; toggle in Admin Panel or
`GRIST_ALLOW_AUTOMATIC_VERSION_CHECKING=false`. `gristlabs/grist-oss` has it
off by default; opt in with `=true`. Sends: version number, edition
(full/Community), anonymized install ID.

### Upgrades

New images roughly weekly; Grist self-migrates documents/DB on start.
[Watchtower](https://containrrr.dev/watchtower/) can automate pulls.

### Installation ID

Found in Admin Panel → Version → Enterprise (full edition only). Tied to
the **home database**, not the host/container — survives container
moves/upgrades as long as the home DB (SQLite volume or PostgreSQL data) is
preserved.

### Removing a user

Full edition: Admin Panel → **Admin Controls** (installation admin only).

### High availability

Contact Grist Labs (Enterprise) for scaling/HA guidance — no generic
self-service config documented.

## Webhooks & custom widgets (self-hosted specifics)

See [INTEGRATIONS.md](INTEGRATIONS.md) for the feature docs;
`ALLOWED_WEBHOOK_DOMAINS` / `GRIST_HTTPS_PROXY` and
`GRIST_WIDGET_LIST_URL` are the self-hosting-relevant env vars.
