#!/usr/bin/env python3
"""
apply.py - Applies a BioHousekeeper plan (produced by analyze.py) to a
spreadsheet, writing a corrected copy. The original file is never modified.

Reads the JSON sidecar produced by analyze.py (after you've resolved its
`questions` by editing `apply`/`targets` fields), executes column renames
and the approved split/merge/drop operations in a safe order, and writes
the result to a new file.

Usage:
    python scripts/apply.py data.xlsx --plan data_biohousekeeper_report.json --output data_corrected.xlsx
"""

import argparse
import csv
import json
import sys
from pathlib import Path

# Ensure UTF-8 output (Windows fix)
if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import pandas as pd


def read_spreadsheet(path, sheet=None):
    ext = path.suffix.lower()
    if ext == ".csv":
        with open(path, "r", encoding="utf-8-sig") as f:
            sample = f.read(4096)
        try:
            dialect = csv.Sniffer().sniff(sample)
            sep = dialect.delimiter
        except csv.Error:
            sep = ","
        return pd.read_csv(path, sep=sep, dtype=str, keep_default_na=False, na_values=[""])
    elif ext in (".xlsx", ".xlsm"):
        xls = pd.ExcelFile(path, engine="openpyxl")
        target_sheet = sheet or xls.sheet_names[0]
        return xls.parse(target_sheet, dtype=str, keep_default_na=False, na_values=[""])
    raise ValueError("Unsupported file type '%s'. Use .csv or .xlsx." % ext)


def write_spreadsheet(df, path):
    ext = path.suffix.lower()
    if ext == ".csv":
        df.to_csv(path, index=False, encoding="utf-8")
    elif ext in (".xlsx", ".xlsm"):
        df.to_excel(path, index=False, engine="openpyxl")
    else:
        raise ValueError("Unsupported output type '%s'. Use .csv or .xlsx." % ext)


def unique_name(name, existing):
    if name not in existing:
        return name
    i = 2
    while "%s_%d" % (name, i) in existing:
        i += 1
    return "%s_%d" % (name, i)


def apply_split_coordinates(df, op, renames, warnings):
    col = op["source"]
    if col not in df.columns:
        warnings.append("split_coordinates: source column '%s' not found, skipped." % col)
        return
    delim = op["delimiter"]
    lat_col, lon_col = (
        (op["targets"][0], op["targets"][1]) if op["order"] == "lat_lon"
        else (op["targets"][1], op["targets"][0])
    )
    lat_col = unique_name(lat_col, df.columns)
    lon_col = unique_name(lon_col, df.columns)

    def split_val(v, idx):
        if pd.isna(v) or delim not in str(v):
            return None
        parts = str(v).split(delim)
        if len(parts) != 2:
            return None
        return parts[idx].strip()

    first = df[col].apply(lambda v: split_val(v, 0))
    second = df[col].apply(lambda v: split_val(v, 1))
    if op["order"] == "lat_lon":
        df[lat_col] = first
        df[lon_col] = second
    else:
        df[lon_col] = first
        df[lat_col] = second
    renames[col] = unique_name("verbatimCoordinates", [c for c in df.columns if c != col])


def apply_derive_taxon_epithets(df, op, renames, warnings):
    import re
    col = op["source"]
    if col not in df.columns:
        warnings.append("derive_taxon_epithets: source column '%s' not found, skipped." % col)
        return
    genus_col = unique_name(op["targets"][0], df.columns)
    epithet_col = unique_name(op["targets"][1], df.columns)
    binomial_re = re.compile(r"^([A-Z][a-z]+)\s+([a-z][a-z\-]+)")

    def extract(v, group):
        if pd.isna(v):
            return None
        m = binomial_re.match(str(v).strip())
        return m.group(group) if m else None

    df[genus_col] = df[col].apply(lambda v: extract(v, 1))
    df[epithet_col] = df[col].apply(lambda v: extract(v, 2))


def apply_split_locality(df, op, renames, warnings):
    col = op["source"]
    targets = op.get("targets")
    if col not in df.columns:
        warnings.append("split_locality: source column '%s' not found, skipped." % col)
        return
    if not targets:
        warnings.append("split_locality: no 'targets' resolved for '%s', skipped." % col)
        return
    delim = op["delimiter"]
    new_cols = {}
    for idx, target in enumerate(targets):
        if not target or target.lower() == "skip":
            continue
        tcol = unique_name(target, df.columns)
        new_cols[idx] = tcol

    def split_val(v, idx):
        if pd.isna(v):
            return None
        parts = str(v).split(delim)
        return parts[idx].strip() if idx < len(parts) else None

    for idx, tcol in new_cols.items():
        df[tcol] = df[col].apply(lambda v, i=idx: split_val(v, i))
    renames[col] = unique_name("verbatimLocality", [c for c in df.columns if c != col])


def apply_merge_date_parts(df, op, renames, warnings):
    y_col, m_col, d_col = op["sources"]
    for c in (y_col, m_col, d_col):
        if c not in df.columns:
            warnings.append("merge_date_parts: source column '%s' not found, skipped." % c)
            return
    target = unique_name(op["target"], df.columns)

    def build_date(row):
        y, m, d = row[y_col], row[m_col], row[d_col]
        if pd.isna(y) or pd.isna(m) or pd.isna(d):
            return None
        try:
            return "%04d-%02d-%02d" % (int(float(y)), int(float(m)), int(float(d)))
        except (ValueError, TypeError):
            return None

    df[target] = df.apply(build_date, axis=1)


def apply_drop_redundant(df, op, renames, warnings):
    drop = op["drop"]
    if drop not in df.columns:
        warnings.append("drop_redundant: column '%s' not found, skipped." % drop)
        return
    df.drop(columns=[drop], inplace=True)


OPERATION_HANDLERS = {
    "merge_date_parts": apply_merge_date_parts,
    "split_coordinates": apply_split_coordinates,
    "derive_taxon_epithets": apply_derive_taxon_epithets,
    "split_locality": apply_split_locality,
    "drop_redundant": apply_drop_redundant,
}

# Order matters: merges/splits/derives must run before column drops and
# before the final header rename pass, since later steps may reference the
# original (pre-rename) column names.
OPERATION_ORDER = [
    "merge_date_parts", "split_coordinates", "derive_taxon_epithets",
    "split_locality", "drop_redundant",
]


def main():
    parser = argparse.ArgumentParser(
        description="Applies a BioHousekeeper analysis plan to a spreadsheet, writing a corrected copy."
    )
    parser.add_argument("file", help="Path to the original spreadsheet (.csv or .xlsx)")
    parser.add_argument("--plan", required=True, help="Path to the JSON sidecar produced by analyze.py")
    parser.add_argument("--output", "-o", required=True, help="Path to write the corrected spreadsheet")
    parser.add_argument("--sheet", help="Sheet name (xlsx only; default: first sheet, or plan's recorded sheet)")
    args = parser.parse_args()

    path = Path(args.file)
    out_path = Path(args.output)
    plan_path = Path(args.plan)

    if not path.exists():
        print("[ERROR] File not found: %s" % args.file)
        sys.exit(1)
    if not plan_path.exists():
        print("[ERROR] Plan not found: %s" % args.plan)
        sys.exit(1)
    if out_path.resolve() == path.resolve():
        print("[ERROR] --output must differ from the input file; the original is never overwritten.")
        sys.exit(1)

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    sheet = args.sheet or plan.get("sheet")

    print("[Info] Reading: %s" % args.file)
    df = read_spreadsheet(path, sheet)
    print("   [OK] %d rows, %d columns" % (len(df), len(df.columns)))

    warnings = []
    renames = {}

    operations = plan.get("operations", [])
    unresolved = [
        op for op in operations
        if not op.get("auto_apply") and op.get("targets") is None and op["type"] == "split_locality"
    ]
    for op in unresolved:
        warnings.append(
            "split_locality on '%s' has no resolved 'targets' - skipped. "
            "Edit the plan JSON's targets list to apply it." % op["source"]
        )

    ops_by_type = {}
    for op in operations:
        ops_by_type.setdefault(op["type"], []).append(op)

    applied = 0
    for op_type in OPERATION_ORDER:
        for op in ops_by_type.get(op_type, []):
            if op is None:
                continue
            should_apply = op.get("apply", op.get("auto_apply", False))
            if not should_apply:
                continue
            if op_type == "split_locality" and not op.get("targets"):
                continue
            OPERATION_HANDLERS[op_type](df, op, renames, warnings)
            applied += 1

    # Column renames (from analyze.py's suggested_term) run last, using
    # whichever name is current after split/merge/drop operations may have
    # already renamed the source (e.g. verbatimCoordinates).
    header_renames = {}
    for col_entry in plan.get("columns", []):
        original = col_entry["original"]
        if original not in df.columns:
            continue  # consumed by an earlier operation (e.g. dropped)
        should_apply = col_entry.get("apply", col_entry.get("auto_apply", False))
        term = col_entry.get("suggested_term")
        if should_apply and term:
            header_renames[original] = term

    header_renames.update(renames)
    final_names = {}
    used = set(df.columns) - set(header_renames.keys())
    for old, new in header_renames.items():
        unique = unique_name(new, used)
        final_names[old] = unique
        used.add(unique)
    df.rename(columns=final_names, inplace=True)
    applied += len(final_names)

    write_spreadsheet(df, out_path)

    print()
    print("[OK] %d operation(s)/rename(s) applied" % applied)
    print("[OK] Corrected spreadsheet written: %s" % out_path)
    print("[OK] Original file untouched: %s" % path)
    if warnings:
        print()
        print("[Warnings]")
        for w in warnings:
            print("   - %s" % w)


if __name__ == "__main__":
    main()
