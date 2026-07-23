# Grist MCP Server

Source: [support.getgrist.com/mcp](https://support.getgrist.com/mcp/)

Model Context Protocol server letting MCP-aware assistants (Claude, ChatGPT,
Claude Code, Gemini CLI, ...) list/search tables, read/query rows, add or
update rows, and create documents/tables on a user's Grist team sites.

## Setup

- **Hosted Grist (getgrist.com)**: already on, no setup, available on every
  plan.
- **Self-hosted, full edition**: off by default. Enable with
  `GRIST_MCP_ENABLED=true`.
  - API-key clients need nothing else (`Authorization` header with the key).
  - Interactive-sign-in clients (Claude.ai, Claude Desktop, ChatGPT) need:
    ```
    GRIST_ENABLE_OIDC_SERVER=true
    GRIST_OIDC_CIMD_ALLOWED_HOSTS=claude.ai,chatgpt.com
    ```
    (CIMD = Client ID Metadata Documents — lets the assistant self-register.
    Clients that don't support CIMD need a manually registered
    [OAuth app](API_REFERENCE.md#oauth-apps-third-party-tools-ai-agents-partner-apps) instead.)

## Server URL

- Hosted: `https://docs.getgrist.com/api/mcp` (covers every team site + personal site)
- Self-hosted: `https://<your-grist-host>/api/mcp`

Terminal clients, e.g. Claude Code:
```bash
claude mcp add --transport http grist https://docs.getgrist.com/api/mcp
```

## Auth & consent

On first connect the client redirects to Grist sign-in, then shows a consent
screen with:

- **Access scopes** (each maps to what's in [API_REFERENCE.md](API_REFERENCE.md#scopes)):
  `openid`/`email`/`profile` (identify you), `user.profile:read`,
  `offline_access` (stay signed in), `doc:read`, `doc:write`,
  `doc.schema:write`, `doc:download` (unused by MCP tools currently),
  `doc:webhooks`.
- **Resource selection**: *All documents (now and in the future)* (default)
  or *Selected resources* (pick specific orgs/workspaces/docs — selecting a
  parent grants everything inside it). Change later from the user's
  "Authorized apps" page; changes can take up to an hour to propagate, or
  disconnect/reconnect the client to apply immediately.

A client may request only a subset of scopes up front and ask for more
later.

## Available tools

Every tool name is prefixed `grist_` when called (e.g. `grist_list_docs`).

### Discovery
`list_orgs`, `list_workspaces`, `list_docs`, `get_doc_info`,
`get_user_profile`, `help`.

### Reading data
`query_document` (natural-language or SQL-style query across a document's
tables), `list_records`, `get_tables`, `get_table_columns`,
`list_snapshots`, `get_grist_access_rules_reference`.

### Writing data
`add_records`, `update_records` (by row id), `remove_records`.

### Managing documents and schema
`create_doc`, `create_table`, `add_table_column`, `update_table_column`
(type/formula/label), `rename_table`, `remove_table`, `remove_table_column`.

### Pages and widgets
`get_pages`, `add_page_widget` (Table, Card, Card List, Chart, Calendar,
Custom, ...), `update_page_widget`, `update_page`, `remove_page`,
`get_page_widgets`, `remove_page_widget`, `get_page_widget_select_by_options`,
`set_page_widget_select_by`, `get_available_custom_widgets`.

### Attachments
`list_attachments`, `get_attachment_url` (short-lived download link).

## Related

Grist's own built-in AI assistant (inside the document editor) is a separate
feature — see the "AI Assistant" doc, not this MCP server.
