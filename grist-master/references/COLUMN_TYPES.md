# Grist Column Types & References

Source: [support.getgrist.com/col-types](https://support.getgrist.com/col-types/),
[support.getgrist.com/col-refs](https://support.getgrist.com/col-refs/).

## Managing columns

- New tables start with columns `A`, `B`, `C`.
- Rename: double-click header, or header dropdown → *Rename column*
  (editing here also lets you edit the column's Python **ID** separately
  from its display **label** — click the link icon to unlock the ID field;
  IDs must stay Python-identifier-safe, non-ASCII chars get replaced with
  `_`).
- Delete: header dropdown → *Delete column*, or `Alt+Minus`.
- Add: `+` in the header row → plain column / pick a type immediately / add
  formula column (opens formula editor immediately) / hidden columns / a
  **Lookup** (adds a data column from a related table via a Reference
  column) / **Shortcuts** for common trigger-formula recipes (Timestamp,
  Authorship, duplicate detection, date helpers, UUID).
- Reorder: select the column header, click-hold ~1s, drag; or via the
  widget's *Visible columns* panel.

## Type inference & inspection

New columns start as `Any`. First value entered decides the type: a number →
`Numeric`; anything else → `Text`. Inspect/change via header dropdown →
*Column Options* → **Column Type**. Any value can still be typed into any
column regardless of type — an incompatible value is highlighted as an
error (and formulas referencing it error too).

## Supported types

| Type | Description |
|---|---|
| Text | (default) any string; supports multi-line (`Shift+Enter`) |
| Numeric | floating point |
| Integer | whole numbers |
| Toggle | boolean, shown as text / checkbox / switch |
| Date | date only |
| DateTime | date + time, with timezone |
| Choice | one value from a predefined set |
| Choice List | multiple values from a predefined set |
| Reference | link to a whole record in another table |
| Reference List | links to multiple records in another table |
| Attachment | files/images, with thumbnail preview |

## Text columns

Alignment + word-wrap options. Two rich formats:

- **Markdown** (recommended) — `**bold**`, `[label](url)`, headings, lists,
  code spans/blocks, blockquotes. No images/custom HTML. Stored as plain
  text; only rendering is affected.
- **HyperLink** (deprecated, superseded by Markdown) — last word of the
  value is the URL, everything before it is the link text:
  `Grist Labs https://getgrist.com`. A formula-friendly Markdown-link
  replacement: `f"[{$Company}]({$Website})"`.

## Numeric / Integer columns

Format options: `$` (currency, opens an international currency picker,
defaults to 2 decimals), `,` (thousands separator), `%`, `Exp` (scientific
notation), `(-)` (parenthesized negatives, accounting style). Document
default currency/timezone/locale set in Document Settings. "Spinner" cell
format adds +/- arrows.

## Toggle columns

Boolean; display as text, checkbox, or switch.

## Date / DateTime columns

Configurable display format ([moment.js format tokens](https://momentjs.com/docs/#/displaying/format/)).
DateTime additionally lets you pick a display timezone; document has a
default timezone (Document Settings).

## Choice / Choice List columns

Predefined value set with per-choice color. Populating from an existing text
column auto-seeds choices from its unique values. Choice = single value per
cell; Choice List = multiple. Editor supports drag-reorder, rename-in-place
(renames the value everywhere), keyboard multi-select, copy/paste of choice
sets between columns. Typing a non-listed value into a cell offers
"add as new choice" inline.

**Filtering the dropdown** (Choice, Choice List, and Reference/Reference
List columns): select the column → creator panel → *Set dropdown condition*
→ write a formula using `choice` to refer to the candidate row/value:

```python
choice.Country == $Stadium_Country
```
Same expression language as [access rules](ACCESS_RULES.md).

## Reference columns

Grist's foreign key. Column Type = `Reference`; pick **Data from Table**
(the underlying/referenced table) and **Show Column** (which field of the
referenced record to display — the *stored* value is always the whole
record's row id, display is just a label). Cross-references by column type,
not by name — table and column can be named anything.

- Typing a not-yet-existing value and selecting `+` in the dropdown creates
  a new row in the referenced table and links to it.
- Converting an existing **Text** column to `Reference` auto-matches values
  to referenced-table records by text; non-matches are flagged invalid for
  manual resolution.
- **Two-way references** (creator panel → Column tab → *Add two-way
  reference*): auto-creates a mirrored column in the referenced table (a
  Reference List if the relationship can be one-to-many) that stays in sync
  bidirectionally. Reassigning a record already linked elsewhere prompts for
  confirmation. Delete via the trash icon next to "Two-Way Reference" (only
  removes the mirror column, not the data). Not supported on Formula
  columns.
- **Pulling extra fields**: `+` → *Lookups* → hover the referenced table →
  pick a field (adds a formula column `=$RefCol.Field`), or select the
  Reference column → creator panel → *Add Referenced Columns*. In formulas
  the reference **column's** name is used (`$Client.Contact`), not the
  underlying table's name.

See [FORMULAS_AND_FUNCTIONS.md#references-lookups-and-dot-notation](FORMULAS_AND_FUNCTIONS.md#references-lookups-and-dot-notation)
for using references in formulas (dot notation, chaining, reverse lookups).

## Reference List columns

Same as Reference but multi-select (a list of record ids). Creating: set
Column Type = `Reference List` — existing single references convert to
one-element lists automatically. Cell editor: type to search + add, drag to
reorder, `Backspace`/click-`X` to remove.

## Attachment columns

Cells hold one or more files/images (paperclip icon; drag/paste to add).
Images show a thumbnail (size configurable). Double-click opens a browser to
rename/download/remove individual attachments.

## Four relationship shapes (design guidance)

1. **One-to-one** — e.g. a person ↔ their birth certificate.
2. **One-to-many** — e.g. a department → its employees (Reference List on
   the "one" side, or Reference on the "many" side pointing back).
3. **Many-to-one** — the inverse view of the above (Reference on the "many"
   side).
4. **Many-to-many** — e.g. students ↔ courses; typically modeled with a
   Reference List on at least one side, or a join table.
