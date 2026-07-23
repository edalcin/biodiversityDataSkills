# Grist Glossary

Source: [support.getgrist.com/glossary](https://support.getgrist.com/glossary/)

- **Column** — vertical series of cells in a table, one value per row.
  Called a **field** when shown in a Card widget, a **series** when shown in
  a Chart widget. Columns typically describe one aspect across many
  records; rows describe many aspects of one entity.
- **Column Options** — per-column config accessed via header dropdown.
- **Column Type** — controls a column's editing UI and appearance; see
  [COLUMN_TYPES.md](COLUMN_TYPES.md).
- **Creator Panel** — the right-side configuration panel for the selected
  widget/column.
- **Dashboard** — informal name for a page built to summarize data via
  linked widgets — not a distinct Grist object.
- **Data Table** — named columns + rows; every row has a numeric `id`
  (`$id` in formulas), unique within that table. All tables listed on the
  **Raw Data** page.
- **Document** — a Grist "database"/"spreadsheet" — a set of tables plus
  the pages/widgets used to view/edit them, and access rules. One `.grist`
  SQLite file.
- **Drag handle** — UI affordance (left of a widget's title) for
  reordering widgets/pages by drag.
- **Fiddle mode** — the mode templates/examples open in: any edit
  auto-forks an unsaved copy, leaving the original untouched, until you
  "Save Copy". Force it by appending `/m/fork` to a doc URL.
- **Field** — a column as shown in a Card widget (see Column).
- **Import** — bringing external data (CSV/Excel/JSON files, or API calls)
  into a Grist document.
- **Lookups** — `lookupOne` (single match, ~VLOOKUP) and `lookupRecords`
  (multi-match) formula functions for cross-table matching without a
  designed Reference relationship; combine with dot notation. See
  [FORMULAS_AND_FUNCTIONS.md](FORMULAS_AND_FUNCTIONS.md).
- **Page** — a visual container for one or more widgets viewing/editing
  tables; listed (and nestable/re-groupable) in the left sidebar.
- **Record** — the data in one table row; unique id available as `id` in
  formulas; shown as a single card in Card/Card-List widgets.
- **Row** — horizontal series of cells across a table's columns; equivalent
  to a record.
- **Series** — a column's data as plotted in a Chart widget (see Column).
- **Trigger Formula** — a formula that only recalculates a stored value
  under chosen conditions (new record / specific column changes); used for
  timestamps, authorship, defaults, data cleanup. See
  [FORMULAS_AND_FUNCTIONS.md#trigger-formulas](FORMULAS_AND_FUNCTIONS.md#trigger-formulas).
- **User Menu** — the profile-icon menu (top right): profile, additional
  accounts, team sites, billing, document settings depending on context.
- **Widget** / **Page Widget** — a page section (Table, Card, Card List,
  Chart, Calendar, Custom, ...) used to view/edit a table.
- **Widget Options** — per-widget config via its three-dot menu → "Widget options".
- **Wrap Text** — cell display setting; off truncates overflow with `…`, on
  wraps and grows the row height.
