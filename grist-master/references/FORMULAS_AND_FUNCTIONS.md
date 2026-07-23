# Grist Formulas & Functions

Source: [support.getgrist.com/formulas](https://support.getgrist.com/formulas/),
[support.getgrist.com/functions](https://support.getgrist.com/functions/),
[support.getgrist.com/python](https://support.getgrist.com/python/),
[support.getgrist.com/references-lookups](https://support.getgrist.com/references-lookups/),
[support.getgrist.com/summary-tables](https://support.getgrist.com/summary-tables/).

## Formula basics

- Formulas are **Python** (currently **3.11**; formerly Python 2 — see
  [Python 2→3 gotchas](#python-2-to-3-migration-notes) below), evaluated in a
  **sandbox** with no internet access and no persistent filesystem.
- A formula applies to a **whole column at once** — no per-row addressing
  like `B1*C1`. Entering `=` in a cell shows the column's Python identifier
  prefixed with `$` (e.g. `$Quantity * $Unit_Price`), with autocomplete.
- Multi-line formulas: `Shift+Enter` to add lines; the value of the last line
  is returned automatically (or use explicit `return`).
- The entire Python **standard library** is importable. Plus a suite of
  Excel-like functions, all UPPERCASE (`IF`, `SUM`, ...) — Python keywords
  stay lowercase (`if`), so `if` ≠ `IF`.
- Equality is `==`/`!=` (not Excel's `=`/`<>`).
- **Special variables** available in formulas:
  - `rec` — the current row (`Record`); `$Field` is shorthand for `rec.Field`.
  - `table` — the current table (`UserTable`).
  - Every table in the document is available by name as a `UserTable`.

### Column behavior (3 states)

- **Data column** — plain stored value, optionally set by a trigger formula.
- **Formula column** — always reflects its formula; not directly editable.
- **Empty column** — new/unset; typing a value → Data column, typing `=formula` → Formula column.

Convert via the **COLUMN BEHAVIOR** menu in the creator panel: *Set
formula*, *Set/Convert to trigger formula*, *Make into data column*,
*Convert column to data* (freeze — keeps the calculated values but stops
recalculating; the original formula is retained inactive and can be restored
or reused as a trigger formula), *Clear and make into formula*, *Clear and
reset*.

### Varying formula behavior by row

Use a conditional inside the formula — there's no separate per-row formula
mechanism:

```python
if $Product.endswith("(Sample)"):
    return 0
else:
    return $Quantity * $Unit_Price
```

### Aggregating without hand-written "totals rows"

Do **not** add special summary rows to a data table (a spreadsheet habit).
Instead add another table widget with formulas outside the base table, or —
better — a **[summary table](#summary-tables)**:

```python
len(Materials.all)                                    # row count
AVERAGE(Materials.all.Price)                           # average of a column
[m.Product for m in Materials.all if m.Quantity > 80]  # list comprehension
max(Materials.all, key=lambda m: m.Quantity).Product   # row with max value
```

For exact-match lookups on large tables, always prefer `lookupRecords`/`lookupOne`
over iterating `.all` — they're indexed and much faster.

### Code viewer

A read-only, pure-Python summary of every formula in the document — useful
to get an overview after being invited to an unfamiliar document.

## Trigger formulas

Trigger formulas store independent data but *optionally* recompute it from a
formula under conditions you choose: timestamps, authorship stamps, data
cleanup on entry, default values.

Create via **Set trigger formula** (or **Convert to trigger formula** on an
existing formula column) in the creator panel. Two independent toggles:

- **Apply to new records** — evaluated once when a row is created (default value).
- **Apply on record changes** — evaluated when specific *other* columns
  change (choose which trigger it), or on the column's **own** value being
  entered (**Current field** option) — this lets you transform/sanitize the
  incoming value before it's saved.

Inside a trigger formula, two extra variables are available (not present in
regular formulas):
- `value` — the value the user is trying to enter.
- `user` — the user object making the change (same shape as in
  [access rules](ACCESS_RULES.md#the-user-variable)).

```python
value.upper()                                    # force uppercase
value if value.startswith("SK") else "SK" + value  # sanitize/prefix
value or $Client.Phone                           # default from a reference
```

## Recursion / self-referencing lookups

```python
yesterday = Events.lookupOne(date=$date - datetime.timedelta(days=1))
$events + (yesterday.cumulative or 0)
```
`lookupOne` on no match returns a special empty record whose fields are
`None` rather than raising — always guard with `or 0` / similar.

## Grist object model (from the function reference)

### `class Record` (`rec`)

The record the formula is evaluated for. `$Field` ≡ `rec.Field`.

```python
def Full_Name(rec, table):
    return rec.First_Name + ' ' + rec.LastName
```

### `$group` (inside a summary table)

The `RecordSet` of underlying rows summarized by the current line, e.g.
`len($group)` counts them, `sum($group.Amount)` sums a field.

### `class RecordSet`

Returned by `lookupRecords()` or `$group`. Iterable; `record_set.Field` is
the list of that field across all records (shorthand for the generator
expression). `len(record_set)` counts records.

`RecordSet.find.*(value)` — binary search on a **sorted** RecordSet (i.e.
one created with `order_by=`), returning the nearest matching record:
`lt`/`le`/`gt`/`ge`/`eq` ("less"≈"before", "greater"≈"after" per the sort
order — flips if `order_by` is negative). Faster than filtering + `max()`
for "value applicable as of a date" patterns. If `find` is shadowed by a
user column, use `_find`.

```python
rates = Rates.lookupRecords(Person=$Person, Role=$Role, order_by="Rate_Start")
rate = rates.find.le($Date)
return rate.Hourly_Rate
```

### `class UserTable`

Every data table, available in formulas by its (capitalized) name.

- `UserTable.all` — list of all records: `len(Students.all)`, `sum(r.Population for r in Countries.all)`.
- `UserTable.lookupOne(Field=value, ...)` — first matching `Record` (or the
  special empty record if none match). Optional `order_by="Col"` /
  `order_by="-Col"` (prefix `-` reverses) decides which match is "first";
  default is lowest row ID. Equivalent to the Excel-style alias `VLOOKUP(Table, Field=value, ...)`.
- `UserTable.lookupRecords(Field=value, ...)` — matching `RecordSet`.
  `order_by` accepts a tuple for multi-column sort, e.g.
  `order_by=("Account", "-Date")`. Legacy `sort_by` = single-field only, no
  `manualSort` fallback. With no `order_by`, sorted by row id (`"id"`).
  `order_by=None` matches the manual/unsorted view order.

```python
Tasks.lookupOne(Project=$id, order_by="Priority")   # smallest Priority
Rates.lookupOne(Person=$id, order_by="-Date")        # latest Date
Transactions.lookupRecords(Account=$Account, order_by="Date")
```

`CONTAINS(value, match_empty=...)` — use as a lookup value to match against
Choice-List / Reference-List *container* columns:
```python
MoviesTable.lookupRecords(genre=CONTAINS("Drama"))   # "Drama" in $genre
```

### Cumulative functions

- `NEXT(rec, *, group_by=(), order_by)` / `PREVIOUS(rec, *, group_by=(), order_by)`
  — adjacent record in table order/grouping. `order_by=None` walks the
  manually-sorted row order.
- `RANK(rec, *, group_by=(), order_by, order='asc')` — 1-based rank within
  its group; ties share a rank.

## References, lookups, and dot notation

**REQUIRED READING before writing cross-table formulas.** Reference /
Reference List columns are Grist's foreign keys — prefer them over
`lookupOne`/`lookupRecords` whenever the relationship is structural, because
they're editable in the UI and give dot-notation for free.

- **Dot notation**: `$RefCol.OtherField` follows a Reference column into the
  referenced table's field. Chains: `$Class.Instructor.Phone`.
- A Reference column's *raw stored value* is the referenced record's numeric
  row id; the UI's "Show Column" setting only controls the *displayed*
  label.
- **`lookupOne`** — when two independently-sourced tables overlap by a
  matching field (e.g. matching emails between an attendee list and a
  sponsor list) rather than a designed relationship. Format:
  `Table.lookupOne(FieldInTable=$FieldInThisRow)`. Chainable with dot
  notation: `Sponsors.lookupOne(Contact_Email=$Email).Sponsor_Level`.
- **`lookupRecords`** — same idea, returns a `RecordSet` for one-to-many.
  `All_Registrations.lookupRecords(Registration_Email=$Email).Event` returns
  a list of matched Event values.
- **Reverse lookups**: exploit the reference stored on the *other* side —
  `All_Registrations.lookupRecords(Event=$id)` finds every registration
  whose `Event` reference points at the current row's id.
- **Record sets in formulas**:
  ```python
  SUM($Registrants.Balance)                                    # via a Reference List column
  SUM(Table.lookupRecords(Column_A=$Column_B).Column_C)
  SUM(person.Balance for person in $Registrants)                # explicit iteration
  len(All_Registrations.lookupRecords(Sponsor=$id))
  len(Enrollments.lookupRecords(Class=$id, Status="Confirmed"))  # multiple match args
  ```

See [COLUMN_TYPES.md](COLUMN_TYPES.md#reference-columns) for creating/configuring
Reference and Reference List columns, two-way references, and dropdown
filtering.

## Summary tables (`GROUP BY`)

Add via **Add New → Add Page/Widget to Page**, click the Σ icon next to a
table, choose **Group-by fields** (the buckets — e.g. Status, or
Status+Department). Grist auto-creates:

- `count` — `len($group)`
- one same-named column per numeric field in the source table — `SUM($group.Field)`

Edit or delete these formulas freely; add more. Recipes:

```python
AVERAGE($group.PayRate)                    # or SUM($group.PayRate) / $count
STDEV($group.PayRate)
MAX($group.PayRate) / MIN($group.PayRate)
SUM(r.AnnualPay for r in $group if r.EmploymentStatus == "Active")
AVERAGE_WEIGHTED(zip($group.Life_Expectancy, $group.Population))
```

- Non-formula columns cannot be added to a summary table.
- **Summarize by date period**: add a helper column via *Add Column → Date
  helpers...* extracting year/quarter/month/week, then group-by that column.
- Group-by columns themselves aren't editable — they mirror the source
  table; new source values auto-add new summary rows.
- Change grouping later via the widget's **Data selection** panel.
- Summary widgets can be **linked** as selectors for detail widgets (select
  a group → see its rows) — see linking-widgets docs.
- **Detach** (right panel → Data tab → Detach) turns a summary table into an
  independent, editable table (e.g. to add a description per group) — it
  stops auto-updating with new source values once detached.

## Function reference

Full Python stdlib + this Excel-like suite (case-sensitive, all UPPERCASE).
**Not every Excel function is implemented** — check before assuming
availability; Grist's philosophy is "use references/lookups", not cell-range
functions.

| Category | Functions |
|---|---|
| Grist | `Record`/`rec`, `$Field`/`rec.Field`, `$group`/`rec.group`, `RecordSet`, `find.*`, `UserTable`, `all`, `lookupOne`, `lookupRecords` |
| Cumulative | `NEXT`, `PREVIOUS`, `RANK` |
| Date | `DATE`, `DATEADD`, `DATEDIF`, `DATEVALUE`, `DATE_TO_XL`, `DAY`, `DAYS`, `DTIME`, `EDATE`, `EOMONTH`, `HOUR`, `ISOWEEKNUM`, `MINUTE`, `MONTH`, `MOONPHASE`, `NETWORKDAYS`, `NOW`, `SECOND`, `TODAY`, `WEEKDAY`, `WEEKNUM`, `XL_TO_DATE`, `YEAR`, `YEARFRAC` |
| Info | `CELL`\*, `ISBLANK`\*, `ISEMAIL`, `ISERR`, `ISERROR`, `ISLOGICAL`, `ISNA`, `ISNONTEXT`, `ISNUMBER`, `ISREF`, `ISREFLIST`, `ISTEXT`, `ISURL`, `N`, `NA`, `PEEK`, `RECORD`, `REQUEST`\*, `TYPE`\* |
| Logical | `AND`, `FALSE`, `IF`, `IFERROR`, `NOT`, `OR`, `TRUE` |
| Lookup | `lookupOne`, `lookupRecords`, `ADDRESS`\*, `CHOOSE`\*, `COLUMN`\*, `COLUMNS`\*, `CONTAINS`, `GETPIVOTDATA`\*, `HLOOKUP`\*, `HYPERLINK`\*, `INDEX`\*, `INDIRECT`\*, `LOOKUP`\*, `MATCH`\*, `OFFSET`\*, `ROW`\*, `ROWS`\*, `SELF_HYPERLINK`, `VLOOKUP` |
| Math | `ABS`, `ACOS`, `ACOSH`, `ARABIC`, `ASIN`, `ASINH`, `ATAN`, `ATAN2`, `ATANH`, `CEILING`, `COMBIN`, `COS`, `COSH`, `DEGREES`, `EVEN`, `EXP`, `FACT`, `FACTDOUBLE`, `FLOOR`, `GCD`, `INT`, `LCM`, `LN`, `LOG`, `LOG10`, `MOD`, `MROUND`, `MULTINOMIAL`, `NUM`, `ODD`, `PI`, `POWER`, `PRODUCT`, `QUOTIENT`, `RADIANS`, `RAND`, `RANDBETWEEN`, `ROMAN`, `ROUND`, `ROUNDDOWN`, `ROUNDUP`, `SERIESSUM`, `SIGN`, `SIN`, `SINH`, `SQRT`, `SQRTPI`, `SUBTOTAL`, `SUM`, `SUMIF`, `SUMIFS`, `SUMPRODUCT`, `SUMSQ`, `TAN`, `TANH`, `TRUNC`, `UUID` |
| Schedule | `SCHEDULE` |
| Stats | `AVEDEV`, `AVERAGE`, `AVERAGEA`, `AVERAGEIF`, `AVERAGEIFS`, `AVERAGE_WEIGHTED`, `BINOMDIST`, `CONFIDENCE`, `CORREL`, `COUNT`, `COUNTA`, `COVAR`, `CRITBINOM`, `DEVSQ`, `EXPONDIST`, `FDIST`, `FISHER`, `FISHERINV`, `FORECAST`, `F_DIST`, `F_DIST_RT`, `GEOMEAN`, `HARMEAN`, `HYPGEOMDIST`, `INTERCEPT`, `KURT`, `LARGE`, `LOGINV`, `LOGNORMDIST`, `MAX`, `MAXA`, `MEDIAN`, `MIN`, `MINA`, `MODE`, `NEGBINOMDIST`, `NORMDIST`, `NORMINV`, `NORMSDIST`, `NORMSINV`, `PEARSON`, `PERCENTILE`, `PERCENTRANK`, `PERCENTRANK_EXC`, `PERCENTRANK_INC`, `PERMUT`, `POISSON`, `PROB`, `QUARTILE`, `RANK_AVG`, `RANK_EQ`, `RSQ`, `SKEW`, `SLOPE`, `SMALL`, `STANDARDIZE`, `STDEV`, `STDEVA`, `STDEVP`, `STDEVPA`, `STEYX`, `TDIST`, `TINV`, `TRIMMEAN`, `TTEST`, `T_INV`, `T_INV_2T`, `VAR`, `VARA`, `VARP`, `VARPA`, `WEIBULL`, `ZTEST` |
| Text | `CHAR`, `CLEAN`, `CODE`, `CONCAT`, `CONCATENATE`, `DOLLAR`, `EXACT`, `FIND`, `FIXED`, `LEFT`, `LEN`, `LOWER`, `MID`, `PHONE_FORMAT`, `PROPER`, `REGEXEXTRACT`, `REGEXMATCH`, `REGEXREPLACE`, `REPLACE`, `REPT`, `RIGHT`, `SEARCH`, `SUBSTITUTE`, `T`, `TEXT`, `TRIM`, `UPPER`, `VALUE` |

`\*` = **not currently implemented in Grist** despite appearing in the
reference (calling it raises/no-ops) — for these, use the idiomatic Python
or Grist replacement noted below:

- `CELL`, `ISBLANK` → use `value == ""` / `value is None` directly.
- `TYPE` → use `isinstance(value, type)` / `type(value)`.
- `REQUEST` → not available (sandbox has no network access).
- `ADDRESS`, `CHOOSE`, `COLUMN`, `COLUMNS`, `GETPIVOTDATA`, `HLOOKUP`,
  `HYPERLINK` (use Markdown links instead — see COLUMN_TYPES.md), `INDEX`,
  `INDIRECT`, `LOOKUP`, `MATCH`, `OFFSET`, `ROW`, `ROWS` → these are
  spreadsheet cell-range concepts that don't map onto Grist's record model;
  use references, `lookupOne`/`lookupRecords`, or Python indexing instead.

### Notable signatures worth remembering

```python
DATE(year, month, day)                      # rolls over-range month/day like Excel
DATEADD(start_date, days=0, months=0, years=0, weeks=0)
DATEDIF(start_date, end_date, unit)         # unit: Y / M / D / MD / YM / YD
DATEVALUE(date_string, tz=None)
NETWORKDAYS(start_date, end_date, holidays=[])
WEEKDAY(date, return_type=1)                # many return_type conventions, see Excel docs
YEARFRAC(start_date, end_date, basis=0)     # basis -1 = Google Sheets variant

IF(logical_expression, value_if_true, value_if_false)   # lazy-evaluates both branches
IFERROR(value, value_if_error='')
ISERROR(value)   # true also for NaN / invalid-typed cell, unlike ISERR
PEEK(func)        # read a cell's stored value without creating a dependency
                  # (breaks circular-reference errors, esp. in trigger formulas)
RECORD(record_or_list, dates_as_iso=False, expand_refs=0)  # record(s) -> dict(s)

SELF_HYPERLINK(label=None, page=None, **kwargs)
# kwargs of the form LinkKey_NAME set user.LinkKey.NAME for access rules
# see ACCESS_RULES.md#link-keys

CONTAINS(value, match_empty=no_match_empty)  # lookupRecords(field=CONTAINS(x)) on list columns
VLOOKUP(table, **field_value_pairs)          # == table.lookupOne(**field_value_pairs)
```

## Python 2 to 3 migration notes

Relevant only when adapting old Grist documents / templates written before
the Python 3.11 upgrade:

- Integer division: `9 / 2` is `4.5` in Py3 (was `4` in Py2) — use `//` for
  the old truncating behavior.
- Stdlib import paths moved, e.g. `from urllib import quote_plus` →
  `from urllib.parse import quote_plus`.
- `round()` now uses banker's rounding (round-half-to-even); to force
  Excel/Py2-style rounding use the `ROUND()` Excel-like function instead of
  the builtin.
- Hashing/encoding: `hashlib.sha256($Email)` now needs `.encode()`:
  `hashlib.sha256($Email.encode()).hexdigest()`.
