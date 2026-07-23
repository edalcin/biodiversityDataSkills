# Grist Integrations

Source: [support.getgrist.com/webhooks](https://support.getgrist.com/webhooks/),
[support.getgrist.com/integrators](https://support.getgrist.com/integrators/),
[support.getgrist.com/embedding](https://support.getgrist.com/embedding/),
[support.getgrist.com/code](https://support.getgrist.com/code/) (Plugin API).

## Webhooks

Full field reference and payload shape: [API_REFERENCE.md#webhooks](API_REFERENCE.md#webhooks).
Configure per-document: **Tools (bottom of left nav) → Settings → API →
Manage Webhooks**.

Key design point — **readiness column**: since rows are often filled in
incrementally, gate notifications with a Toggle column formula (e.g.
`bool($Name and $Email)`) set as the webhook's *Ready column*, so the "add"
event only fires once a row is actually complete; further edits while true
fire "update" events. Decide the enable order carefully:
- Want the integration to also cover **existing** rows → enable the webhook
  with an empty readiness column first, then flip existing readiness cells on.
- Want it to fire **only for new/future** rows → make sure all existing rows'
  readiness cells are already `true` *before* enabling, or you'll get a
  flood of notifications for the backlog.

Self-hosted security: restrict destinations with `ALLOWED_WEBHOOK_DOMAINS`,
or `ALLOWED_WEBHOOK_DOMAINS=*` routed through `GRIST_HTTPS_PROXY` (what
Grist's own SaaS does) — see [SELF_HOSTED.md](SELF_HOSTED.md).

## No-code integrator platforms

Native connectors exist for:
- [Zapier](https://zapier.com/apps/grist/integrations)
- [Integrately](https://integrately.com/integrations/grist)
- [Pabbly Connect](https://www.pabbly.com/connect/integrations/grist/)
- [n8n](https://n8n.io/integrations/n8n-nodes-base.grist)
- [Make](https://www.make.com/en/integrations/grist)

Grist can be either the **trigger** (new/updated row → external action) or
the **action** (external event → add/update/query a Grist table). Prefer a
connected [OAuth app](API_REFERENCE.md#oauth-apps-third-party-tools-ai-agents-partner-apps)
over a raw API key where the integrator supports it — scoped and revocable
per document.

**Zapier setup shape** (representative of most integrators): pick a
trigger app/event (e.g. Google Forms "New Response") → pick the Grist
action ("Create Record") → authenticate Grist with an API key → choose
team/document/table → map fields → test → enable.

**Instant vs. polled triggers**: Zapier's "New or Updated Record (Instant)"
uses Grist's webhook mechanism directly (fast, seconds); regular
non-instant triggers poll periodically (slower) and need a specific column
to monitor for changes (ideally an `Updated At` timestamp column).

n8n example workflows (each with an importable JSON + sample doc): updating
multiple tables from a single form submission, an AI node that rewrites
data on change, AI email summarization into a CRM, and scheduled/cron
automations.

## Embedding (iframe)

1. Turn on [public access / link sharing](https://support.getgrist.com/sharing/#public-access-and-link-sharing) for the document.
2. Embed:
   ```html
   <iframe src="https://<host>/<docId>/<Name>/p/<N>?embed=true"
           height="250px" width="100%" frameborder="0"></iframe>
   ```

**URL parameters** (chain with `&`, first one uses `?`):
- `embed=true` — read-only, strips toolbar/page-menu/creator-panel.
- `style=singlePage` — same stripped chrome but **editable**, subject to
  [access rules](ACCESS_RULES.md).
- `themeAppearance=light|dark` — force a theme.
- `themeSyncWithOs=false` — stop following the OS theme (combine with
  `themeAppearance`).

Any page type can be embedded: table grid, card/card-list, chart, or a page
with multiple sections; it updates live as the source document changes.

## Custom widgets (Plugin API)

A custom widget is external code (any web page) embedded as a page widget,
interacting with the host document via the `grist` Plugin API object
(`window.grist` inside the widget iframe). Used for chart libraries, custom
forms, or any bespoke visualization/edit UI Grist doesn't natively provide.

- Widget examples & starting points: https://github.com/gristlabs/grist-widget
- Full Plugin API reference (methods on the `grist` object): https://support.getgrist.com/code/modules/grist_plugin_api/
- Widget gallery in the Grist UI is powered by a `manifest.json` — see
  [SELF_HOSTED.md#customization](SELF_HOSTED.md#customization) for
  self-hosting your own gallery/fork.

## Related

- REST API / SQL endpoint for programmatic (non-webhook) integration:
  [API_REFERENCE.md](API_REFERENCE.md).
- MCP server for AI-assistant integration: [MCP_SERVER.md](MCP_SERVER.md).
- OAuth apps for building a multi-user third-party tool:
  [API_REFERENCE.md#authentication](API_REFERENCE.md#authentication).
