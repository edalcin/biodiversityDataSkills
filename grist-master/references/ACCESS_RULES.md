# Grist Access Rules

Source: [support.getgrist.com/access-rules](https://support.getgrist.com/access-rules/)

Fine-grained, per-table/column/row permissions beyond the base
Viewer/Editor/Owner roles. Only document **Owners** can edit access rules.
Access the panel via the left sidebar **Access Rules** tool, or *Manage
Users* → *Open Access Rules*.

## Enabling / disabling

Disabled (default): every Editor/Owner is equally powerful (can edit
structure, formulas, layout). **Enabling** access rules restricts structure
changes and formula editing to Owners only, and unlocks per-table/column/row
rules. Must be manually **saved** after enabling — the change doesn't apply
until you click Save.

Disabling: delete every custom rule first; the "Disable Access Rules" button
appears once none remain.

## Rule evaluation order

1. **Column-specific rules**
2. **Table-wide rules**
3. **Default rules** (fallback for all tables; not editable, express base
   role semantics — Owners/Editors: full access; Viewers: read-only;
   everyone else: no access)

Within a rule group, conditions are checked **top to bottom**; the first
condition that resolves a given permission (Allow/Deny) wins for that
permission — later rules in the same group don't override it. A blank
condition (shown as "Everyone Else") or the literal `True` always matches.

## Permissions

Single-letter columns in the UI:

| Letter | Meaning |
|---|---|
| `R` | Read cells |
| `U` | Update cells |
| `C` | Create rows |
| `D` | Delete rows |
| `S` | Change table structure (only in the special "Allow Editors to edit structure" rule) |

Column rules support `R`/`U` only (no `C`/`D` — handle those in table rules).

**`S` is dangerous**: it permits creating/editing formulas, and formula
calculations aren't sandboxed from other rules — a user with `S` can write a
formula that surfaces any data in the document, circumventing row/column
restrictions elsewhere.

## Basic conditions

Common `user.Access`-based patterns:

```python
user.Access == EDITOR
user.Access != OWNER
user.Access in [VIEWER, EDITOR]
user.Access not in [EDITOR, OWNER]
```

### The `user` variable

- `user.Access` — `OWNER` / `EDITOR` / `VIEWER` (how the doc was shared)
- `user.Email` — or `anon@getgrist.com` if anonymous
- `user.UserID` — numeric
- `user.Name` — or `Anonymous`
- `user.LinkKey` — object of any `..._` URL parameters (web client only, not API) — see [Link keys](#link-keys)
- `user.SessionID` — stable per anonymous session, or `"u" + user id` when logged in
- `user.IsLoggedIn` — bool

### `rec` and `newRec`

- `rec` — the record's current state; using it makes the rule row-specific.
- `newRec` — available only for create/update, the record's state **after**
  a proposed change — lets you gate *what* changes are allowed:
  ```python
  (user.Team.Role == 'Delivery' and
    rec.Stage == 'Delivery' and
    newRec.Stage == 'Done')
  ```

**Important**: `rec`/`newRec` give raw field values only — **dot-notation
through references is not supported** in rule conditions (`rec.Person.Email`
does NOT work). A reference field yields the referenced record's numeric id;
compare ids directly (`rec.Purchaser == user.Team.id`) or against another
reference field of the same target table (`rec.Department ==
user.Team.Department`). To use richer referenced data in a rule, first
expose it as a regular formula column in the base table (e.g.
`$Purchaser.Role`), then reference that column from the rule.

Supported operators: `and`, `or`, `+ - * / %`, `== != < <= > >=`, `is`,
`is not`, `in`, `not in`. Comments: `#` or `"""`. The **first comment** in a
rule that ends up denying an action is shown to the user as an explanation
("access rule memo").

## Recipes

### Private table
Add table rules for the sensitive table, condition `user.Access != OWNER`,
"Deny all" — non-Owners neither see it in the sidebar nor can open it
directly.

### Column restriction
Table rules → `...` menu → *Add Column Rule* → pick columns → condition
(e.g. `user.Email == 'kiwi@getgrist.com'`) → deny `R`/`U` for those columns
to that user only. Different rule groups can hide different column sets
from different users.

### Row-level access control
Add a table-wide rule (not tied to specific columns): deny all by default,
then a follow-up rule allowing `R` when e.g.
`user.Team.Role == rec.Stage` — filters visible rows per user based on both
row content and the requesting user's attributes.

### Seed rules
A checkbox above Default Rules auto-populates a starter rule (e.g. "Owners
always get full access") whenever new table rules are added, avoiding
copy-pasting the same boilerplate rule into every table group.

## Special (document-wide) rules

- **Allow Editors to edit structure** — restores the pre-access-rules
  default (Editors == Owners for structure); expand it to see it controls
  the `S` permission.
- **Allow everyone to view access rules** — by default only Owners can see
  the rules themselves; enabling this lets any collaborator view (not edit)
  them.
- **Restrict non-Owners from copying/downloading the full document** —
  appears once the above is on; full copies/downloads include the access
  rules, so viewing-rules is a prerequisite for full-doc copy rights; you
  can still additionally restrict copy/download.
- **Template exemption** — lets restricted users copy/download anyway, for
  sharing non-sensitive template documents; not itself copied into the new
  copy.

## View as another user

Owners: **View As** dropdown → pick a shared collaborator to preview exactly
what they'd see (tables/columns/rows hidden, banner shown) without actually
becoming them (their own edits still attribute to the Owner). Also check
**Raw Data** to confirm the exposed surface. **View as Yourself** exits.

## User attribute tables

Scales rules beyond hardcoding individual users. Add a table (e.g. `Team`
with `Email`, `Role` columns) classifying users, then **Add User
Attributes**: give it a name (e.g. `Team`), pick the source table, the
`user.*` property to match on (typically `user.Email`), and the column in
the source table to match against. Rules can then reference `user.Team.Role`
etc. New team members just need a row in the attribute table — no rule
edits.

## Link keys

URL query parameters ending in `_` become available to rules as
`user.LinkKey.<Name>` (underscore stripped): `...?Token_=xx&Flavor_=vanilla`
→ `user.LinkKey.Token == "xx"`, `user.LinkKey.Flavor == "vanilla"`.

Pattern for "share one row with an outsider without making them a
collaborator":
1. Add a `UUID` column, formula `=UUID()`, then convert to a **trigger
   formula** applied only to new records (freezes the value so it doesn't
   regenerate).
2. Build a shareable link with `SELF_HYPERLINK(label=$Ref, LinkKey_UUID=$UUID)`
   (any `LinkKey_NAME=value` kwarg sets that link key).
3. Rule: allow `R` when `user.LinkKey.UUID == rec.UUID` (else Owner-only).

Link keys can span multiple rows/tables and combine with user attribute
tables.

## Access rule memos

Attach a human-readable explanation to any condition (memo icon next to the
condition) — shown to the user as the reason an action was denied, when that
condition's first comment triggers a denial.

## Reference templates

- [Lead lists](https://support.getgrist.com/examples/2021-03-leads/) — simple assignment-based access
- [Account-based Sales Team](https://templates.getgrist.com/38Dz6nMtzvwC/Account-based-Sales-Team) — reps see only their own accounts
- [Public Giveaway](https://templates.getgrist.com/vP7WpQp89hLi/Public-Giveaway) — anonymous participation via rules, no login
- [Simple Poll](https://templates.getgrist.com/jd234iH1zDsL/Simple-Poll) — one response per visitor
- [Crowdsourced List](https://templates.getgrist.com/dKztiPYamcCp/Crowdsourced-List) — moderators vs. contributor-scoped edits
- [Time Sheets](https://templates.getgrist.com/oGxD8EnzeVs6/Time-Sheets) — contractor scoping by month
- [Project Management](https://templates.getgrist.com/hifkng53AxyQ/Project-Management/) — department + manager scoping
