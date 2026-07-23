---
name: grist-master
description: >
  Provides comprehensive technical knowledge about Grist (getgrist.com), the
  spreadsheet-database hybrid tool: REST API, SQL endpoint, MCP server, OAuth
  apps, webhooks, Python formulas and the full Excel-like function reference,
  column types, references/lookups, summary tables, access rules, self-hosted
  (Docker) installation and administration, and integrations (Zapier, n8n,
  Make, embedding, custom widgets). Use when the user mentions "Grist",
  "getgrist.com", "grist-core", "grist-widget", building or debugging Grist
  formulas, querying the Grist REST/SQL API, connecting an MCP client to
  Grist, self-hosting Grist with Docker, writing Grist access rules, or
  building a Grist custom widget or integration.
license: MIT
metadata:
  author: biodiversityDataSkills
  repository: https://github.com/<your-username>/biodiversityDataSkills
  source: https://support.getgrist.com/
---

# Grist Master

Reference knowledge base for [Grist](https://www.getgrist.com/), the open-source
spreadsheet-database hybrid. Built from the official
[Grist Help Center](https://support.getgrist.com/). Use this skill to answer
questions, write formulas, call the API, configure self-hosted instances, or
build integrations without re-deriving Grist behavior from scratch.

This is a pure reference skill — no scripts, no dependencies. Read the
relevant file(s) below before answering non-trivial Grist questions.

## What Grist is

Grist stores data as **tables of records** (not spreadsheet cells with row/column
addresses). Each table has typed columns; formulas are **Python**, apply to a
whole column at once (no per-row `A1`-style addressing), and are recalculated
automatically. A document = one SQLite file (`.grist`), containing all tables,
pages, widgets, and access rules.

## Quick reference — where to look

| Topic | File |
|---|---|
| REST API (orgs/workspaces/docs/records/tables/columns/attachments/webhooks), SQL endpoint, API keys, OAuth apps, client libraries | [references/API_REFERENCE.md](references/API_REFERENCE.md) |
| MCP server setup (hosted + self-hosted), OAuth/CIMD, tool catalogue | [references/MCP_SERVER.md](references/MCP_SERVER.md) |
| Formula basics, Python sandbox, trigger formulas, `Record`/`RecordSet`/`UserTable`, `lookupOne`/`lookupRecords`, full function reference (Date/Logical/Lookup/Math/Stats/Text), summary tables | [references/FORMULAS_AND_FUNCTIONS.md](references/FORMULAS_AND_FUNCTIONS.md) |
| Column types (Text, Numeric, Integer, Toggle, Date, DateTime, Choice, Choice List, Reference, Reference List, Attachment), two-way references, dropdown filtering | [references/COLUMN_TYPES.md](references/COLUMN_TYPES.md) |
| Access rules: enabling, default rules, row/column restrictions, `user`/`rec`/`newRec`, permissions (`R`/`U`/`C`/`D`/`S`), link keys, user attribute tables | [references/ACCESS_RULES.md](references/ACCESS_RULES.md) |
| Self-hosted Grist: Docker install, sandboxing (`gvisor`), teams, auth, full-edition activation, storage/backends, snapshots, telemetry, upgrades | [references/SELF_HOSTED.md](references/SELF_HOSTED.md) |
| Webhooks, Zapier/n8n/Make/Pabbly/Integrately, embedding (iframe), custom widget Plugin API | [references/INTEGRATIONS.md](references/INTEGRATIONS.md) |
| Frequently asked questions (accounts, plans, sharing, embedding, row limits) | [references/FAQ.md](references/FAQ.md) |
| Glossary of Grist UI/data-model terms | [references/GLOSSARY.md](references/GLOSSARY.md) |

## Core concepts an agent must get right

- **Formulas are Python 3.11**, evaluated in a network-isolated sandbox with no
  persistent filesystem. `$Field` in a formula == `rec.Field`. A formula
  applies to the *whole column*, not one cell.
- **References, not VLOOKUP.** Cross-table relationships use Reference /
  Reference List columns (foreign keys to a whole record) or
  `Table.lookupOne(...)` / `Table.lookupRecords(...)`. `VLOOKUP` exists only
  as a `lookupOne` alias for spreadsheet-familiarity.
- **Trigger formulas** run once on new records and/or on every update of
  specific columns; they see extra `value`/`user` variables and are how you
  implement timestamps, authorship, or data sanitization — not by using a
  regular formula.
- **Summary tables** are Grist's `GROUP BY` — never hand-roll aggregate rows
  in a data table; add a summary widget and use `$group`.
- **Access rules** are evaluated top-to-bottom per rule group in order
  (column rules → table rules → default rules); first matching rule wins for
  each permission letter. The `S` (structure) permission can bypass all other
  restrictions because formulas aren't sandboxed from data.
- **API auth**: a personal API key carries full account access (`Authorization: Bearer <key>`
  against `docs.getgrist.com` or `<team>.getgrist.com`). For third-party
  tools acting on a user's behalf, prefer **OAuth apps** (scoped, revocable)
  over handing out API keys.
- **SQL endpoint** (`/api/docs/{docId}/sql`) is **read-only** `SELECT`
  against the document's underlying SQLite — separate from the
  records/tables CRUD endpoints, and may not fully respect row-level access
  rules, so treat it as an owner-only tool.
- **Self-hosted**: `gristlabs/grist` Docker image toggles between Community
  (free, OSS, Apache-2.0) and the full edition (30-day trial, then an
  activation key). Always set `GRIST_SANDBOX_FLAVOR=gvisor` in production —
  it's what isolates Python formulas from the host and network.

## When answering Grist questions

1. Formula / function question → read `FORMULAS_AND_FUNCTIONS.md` first;
   don't guess Excel-function availability, check the table there (many
   Excel-lookalikes like `HLOOKUP`, `INDEX`, `MATCH` are **not implemented**
   in Grist — `lookupRecords`/references are the idiomatic replacement).
2. "Call the Grist API" → read `API_REFERENCE.md` for the exact path/verb and
   auth header; distinguish REST CRUD endpoints from the SQL endpoint.
3. "Connect an AI assistant to Grist" → `MCP_SERVER.md`, not the REST API.
4. "Self-host" / Docker / env vars → `SELF_HOSTED.md`.
5. "Who can see/edit this" → `ACCESS_RULES.md`.
