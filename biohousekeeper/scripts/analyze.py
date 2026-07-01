#!/usr/bin/env python3
"""
analyze.py - Analyzes a biodiversity spreadsheet and proposes a Darwin Core
column structure.

Reads a spreadsheet (CSV/XLSX/XLS), inspects column names AND sample values,
and produces:
  - a Markdown report (human-readable) proposing renames, splits, merges,
    and flagging redundant/missing columns
  - a JSON sidecar (machine-readable) with the same findings plus an
    `apply` flag per suggestion and a list of open questions for anything
    ambiguous enough to need the user's input before restructuring the file

Never modifies the input file. Run apply.py afterwards against the (possibly
edited) JSON sidecar to write a corrected copy.

Usage:
    python scripts/analyze.py data.xlsx
    python scripts/analyze.py data.xlsx --sheet "Occurrences"
    python scripts/analyze.py data.csv --out-dir ./report
"""

import argparse
import csv
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

# Ensure UTF-8 output (Windows fix)
if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import pandas as pd

REF_DIR = Path(__file__).resolve().parent.parent / "references"
TERMS_CSV = REF_DIR / "dwc_terms.csv"

SAMPLE_SIZE = 200  # rows sampled per column for value-based heuristics

# Occurrence-core fields commonly expected in a biodiversity record. Not all
# apply to every dataset (e.g. a checklist has no eventDate) - flagged as
# advisory notes, never a hard error.
RECOMMENDED_FIELDS = [
    "occurrenceID", "basisOfRecord", "scientificName", "eventDate",
    "decimalLatitude", "decimalLongitude", "recordedBy", "country",
]

# Synonym dictionary: common column names in English, Portuguese, Spanish ->
# Darwin Core term. Checked after normalization (lowercase, accents
# stripped, separators collapsed to '_').
SYNONYMS = {
    "id": "occurrenceID", "occurrence_id": "occurrenceID", "codigo": "occurrenceID",
    "catalog": "catalogNumber", "catalog_number": "catalogNumber", "catalogo": "catalogNumber",
    "numero_tombo": "catalogNumber", "tombo": "catalogNumber",
    "record_number": "recordNumber", "numero_registro": "recordNumber",
    "species": "scientificName", "especie": "scientificName", "especies": "scientificName",
    "nome_cientifico": "scientificName", "scientific_name": "scientificName",
    "nombre_cientifico": "scientificName",
    "genero": "genus", "genus": "genus", "genero_": "genus",
    "familia": "family", "family": "family",
    "ordem": "order", "orden": "order", "order": "order",
    "classe": "class", "clase": "class",
    "filo": "phylum", "phylum": "phylum",
    "reino": "kingdom", "kingdom": "kingdom",
    "autor": "scientificNameAuthorship", "author": "scientificNameAuthorship",
    "autor_taxon": "scientificNameAuthorship",
    "categoria_taxonomica": "taxonRank", "taxon_rank": "taxonRank", "rank": "taxonRank",
    "pais": "country", "country": "country", "país": "country",
    "estado": "stateProvince", "state": "stateProvince", "provincia": "stateProvince",
    "municipio": "municipality", "município": "municipality", "municipality": "municipality",
    "localidade": "locality", "locality": "locality", "localidad": "locality", "local": "locality",
    "latitude": "decimalLatitude", "lat": "decimalLatitude",
    "longitude": "decimalLongitude", "long": "decimalLongitude", "lng": "decimalLongitude", "lon": "decimalLongitude",
    "datum": "geodeticDatum", "geodetic_datum": "geodeticDatum",
    "altitude": "minimumElevationInMeters", "elevacao": "minimumElevationInMeters", "elevation": "minimumElevationInMeters",
    "data": "eventDate", "date": "eventDate", "data_coleta": "eventDate", "fecha": "eventDate",
    "ano": "year", "year": "year", "anio": "year",
    "mes": "month", "month": "month",
    "dia": "day", "day": "day",
    "coletor": "recordedBy", "collector": "recordedBy", "recorded_by": "recordedBy", "colector": "recordedBy",
    "protocolo_amostragem": "samplingProtocol", "sampling_protocol": "samplingProtocol",
    "habitat": "habitat",
    "instituicao": "institutionCode", "institution": "institutionCode", "institucion": "institutionCode",
    "colecao": "collectionCode", "collection": "collectionCode", "coleccion": "collectionCode",
    "tipo_registro": "basisOfRecord", "basis_of_record": "basisOfRecord",
    "quantidade": "individualCount", "individual_count": "individualCount", "cantidad": "individualCount",
    "sexo": "sex", "sex": "sex",
    "estagio_vida": "lifeStage", "life_stage": "lifeStage", "estadio": "lifeStage",
    "status_ocorrencia": "occurrenceStatus", "occurrence_status": "occurrenceStatus",
    "observacoes": "occurrenceRemarks", "remarks": "occurrenceRemarks", "notes": "occurrenceRemarks", "notas": "occurrenceRemarks",
    "identificado_por": "identifiedBy", "identified_by": "identifiedBy",
    "data_identificacao": "dateIdentified", "date_identified": "dateIdentified",
    "midia": "associatedMedia", "media": "associatedMedia", "foto": "associatedMedia", "photo": "associatedMedia", "imagem": "associatedMedia",
}

COORD_NAME_HINTS = re.compile(r"coord|lat.?long|latlong|geo|posicao|position", re.IGNORECASE)
LOCALITY_NAME_HINTS = re.compile(r"local|address|endereco|hierarquia|geografia", re.IGNORECASE)
BINOMIAL_RE = re.compile(r"^([A-Z][a-z]+)\s+([a-z][a-z\-]+)(\s+([A-Z][A-Za-z .,&]+\d{0,4}))?$")
DELIMS = [",", ";", "/", "|", "-"]


def strip_accents(text):
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def normalize_column_name(name):
    name = strip_accents(str(name)).lower().strip()
    name = re.sub(r"[_\s\-]+", "_", name)
    name = re.sub(r"[^a-z0-9_]", "", name)
    return name.strip("_")


def load_dwc_terms():
    terms = {}
    if not TERMS_CSV.exists():
        return terms
    with open(TERMS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("type", "").strip()
            if name:
                terms[normalize_column_name(name)] = name
    return terms


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
        df = pd.read_csv(path, sep=sep, dtype=str, keep_default_na=False, na_values=[""])
        sheet_names = None
    elif ext in (".xlsx", ".xlsm"):
        xls = pd.ExcelFile(path, engine="openpyxl")
        sheet_names = xls.sheet_names
        target_sheet = sheet or sheet_names[0]
        df = xls.parse(target_sheet, dtype=str, keep_default_na=False, na_values=[""])
    else:
        raise ValueError(
            "Unsupported file type '%s'. Use .csv or .xlsx (convert legacy .xls first)." % ext
        )
    return df, sheet_names


def sample_values(series, n=SAMPLE_SIZE):
    non_null = series.dropna()
    non_null = non_null[non_null.str.strip() != ""]
    return non_null.head(n).tolist()


def looks_numeric(values, min_ratio=0.9):
    if not values:
        return False
    ok = 0
    for v in values:
        try:
            float(str(v).replace(",", "."))
            ok += 1
        except ValueError:
            pass
    return (ok / len(values)) >= min_ratio


def looks_like_lat(values):
    return _in_range(values, -90, 90)


def looks_like_lon(values):
    return _in_range(values, -180, 180)


def _in_range(values, lo, hi, min_ratio=0.9):
    nums = []
    for v in values:
        try:
            nums.append(float(str(v).replace(",", ".")))
        except ValueError:
            continue
    if not nums:
        return False
    ok = sum(1 for n in nums if lo <= n <= hi)
    return (ok / len(nums)) >= min_ratio


def detect_coordinate_pair(values):
    """Detect 'lat,lon' (or similar delimiter) packed into one column."""
    for delim in [",", ";", "/", " "]:
        parts_list = [v.split(delim) for v in values if delim in v]
        if len(parts_list) < max(3, 0.5 * len(values)):
            continue
        if not all(len(p) == 2 for p in parts_list):
            continue
        firsts = [p[0].strip() for p in parts_list]
        seconds = [p[1].strip() for p in parts_list]
        if not (looks_numeric(firsts) and looks_numeric(seconds)):
            continue
        if looks_like_lat(firsts) and looks_like_lon(seconds):
            return delim, "lat_lon"
        if looks_like_lon(firsts) and looks_like_lat(seconds):
            return delim, "lon_lat"
    return None, None


def detect_binomial(values):
    if not values:
        return False
    matches = sum(1 for v in values if BINOMIAL_RE.match(str(v).strip()))
    return (matches / len(values)) >= 0.7


def detect_locality_delimiter(values):
    if len(values) < 3:
        return None, 0
    for delim in DELIMS:
        counts = [len(v.split(delim)) for v in values]
        if not counts:
            continue
        common = max(set(counts), key=counts.count)
        if common < 2 or common > 5:
            continue
        ratio = counts.count(common) / len(counts)
        if ratio >= 0.8:
            return delim, common
    return None, 0


def columns_similarity(a_values, b_values):
    """Fraction of overlapping non-null rows where normalized values match."""
    pairs = [
        (str(a).strip().lower(), str(b).strip().lower())
        for a, b in zip(a_values, b_values)
        if str(a).strip() and str(b).strip()
    ]
    if len(pairs) < 3:
        return 0.0
    matches = sum(1 for a, b in pairs if a == b)
    return matches / len(pairs)


def analyze_columns(df, dwc_terms):
    columns_report = []
    year_col = month_col = day_col = None

    for col in df.columns:
        norm = normalize_column_name(col)
        values = sample_values(df[col])
        entry = {
            "original": col,
            "normalized": norm,
            "non_null_count": int(df[col].dropna().apply(lambda x: str(x).strip() != "").sum()),
            "sample_values": values[:5],
            "suggested_term": None,
            "confidence": "none",
            "auto_apply": False,
            "note": None,
        }

        if norm in SYNONYMS:
            entry["suggested_term"] = SYNONYMS[norm]
            entry["confidence"] = "high"
            entry["auto_apply"] = True
        elif norm in dwc_terms:
            entry["suggested_term"] = dwc_terms[norm]
            entry["confidence"] = "high"
            entry["auto_apply"] = True
            entry["note"] = "Column name already matches a Darwin Core term."
        else:
            candidates = sorted(
                {term for key, term in dwc_terms.items() if norm in key or key in norm},
                key=len,
            )
            if candidates:
                entry["suggested_term"] = candidates[0]
                entry["confidence"] = "low"
                entry["auto_apply"] = False
                entry["note"] = "Partial name match; confirm before applying."
                if len(candidates) > 1:
                    entry["alternatives"] = candidates[1:4]
            else:
                entry["note"] = "No Darwin Core term match found; keep as a custom/extension field or clarify intent."

        if norm in ("year", "ano", "anio"):
            year_col = col
        elif norm in ("month", "mes"):
            month_col = col
        elif norm in ("day", "dia"):
            day_col = col

        columns_report.append(entry)

    return columns_report, (year_col, month_col, day_col)


def detect_operations(df, columns_report, date_parts):
    operations = []
    questions = []
    by_original = {c["original"]: c for c in columns_report}

    # --- coordinate pair split ---
    for col in df.columns:
        norm = normalize_column_name(col)
        if not COORD_NAME_HINTS.search(col) and not COORD_NAME_HINTS.search(norm):
            continue
        values = sample_values(df[col])
        delim, order = detect_coordinate_pair(values)
        if delim:
            op = {
                "type": "split_coordinates",
                "source": col,
                "delimiter": delim,
                "order": order,
                "targets": (
                    ["decimalLatitude", "decimalLongitude"] if order == "lat_lon"
                    else ["decimalLongitude", "decimalLatitude"]
                ),
                "confidence": "high",
                "auto_apply": True,
                "note": "Column '%s' packs coordinates as '%s'-delimited pairs (%s)." % (col, delim, order),
            }
            operations.append(op)

    # --- scientific name split into genus/specificEpithet ---
    for col in df.columns:
        norm = normalize_column_name(col)
        mapped = by_original[col]["suggested_term"]
        if mapped != "scientificName" and norm not in ("species", "especie", "especies", "nome_cientifico"):
            continue
        values = sample_values(df[col])
        if detect_binomial(values):
            op = {
                "type": "derive_taxon_epithets",
                "source": col,
                "targets": ["genus", "specificEpithet"],
                "confidence": "medium",
                "auto_apply": False,
                "note": (
                    "Column '%s' looks like binomial names (e.g. '%s'). "
                    "Propose deriving genus/specificEpithet as new columns, keeping "
                    "scientificName intact." % (col, values[0] if values else "")
                ),
            }
            operations.append(op)
            questions.append({
                "id": "confirm_split_%s" % norm,
                "column": col,
                "question": (
                    "Split '%s' into genus + specificEpithet (derived columns), "
                    "keeping the original scientificName? yes/no" % col
                ),
                "related_operation": op["type"] + ":" + col,
            })

    # --- locality composite split ---
    for col in df.columns:
        norm = normalize_column_name(col)
        if not LOCALITY_NAME_HINTS.search(col) and not LOCALITY_NAME_HINTS.search(norm):
            continue
        values = sample_values(df[col])
        delim, parts_count = detect_locality_delimiter(values)
        if delim:
            op = {
                "type": "split_locality",
                "source": col,
                "delimiter": delim,
                "parts_count": parts_count,
                "targets": None,  # user must supply, order is dataset-specific
                "confidence": "low",
                "auto_apply": False,
                "note": (
                    "Column '%s' has %d '%s'-delimited parts in most rows. "
                    "Order (e.g. country/stateProvince/municipality) must be confirmed." % (col, parts_count, delim)
                ),
            }
            operations.append(op)
            questions.append({
                "id": "locality_order_%s" % norm,
                "column": col,
                "question": (
                    "Column '%s' splits into %d parts by '%s' (e.g. '%s'). "
                    "What DwC term does each part represent, left to right? "
                    "(e.g. country,stateProvince,municipality)" % (
                        col, parts_count, delim, values[0] if values else ""
                    )
                ),
                "related_operation": op["type"] + ":" + col,
            })

    # --- date parts merge ---
    year_col, month_col, day_col = date_parts
    if year_col and month_col and day_col:
        y_vals = sample_values(df[year_col])
        m_vals = sample_values(df[month_col])
        d_vals = sample_values(df[day_col])
        if (_in_range(y_vals, 1500, 2100) and _in_range(m_vals, 1, 12) and _in_range(d_vals, 1, 31)):
            operations.append({
                "type": "merge_date_parts",
                "sources": [year_col, month_col, day_col],
                "target": "eventDate",
                "confidence": "high",
                "auto_apply": True,
                "note": "Columns '%s'/'%s'/'%s' look like year/month/day; merge into ISO 8601 eventDate." % (
                    year_col, month_col, day_col
                ),
            })

    # --- redundant columns (pairwise) ---
    cols = list(df.columns)
    seen_pairs = set()
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            a, b = cols[i], cols[j]
            if (a, b) in seen_pairs:
                continue
            seen_pairs.add((a, b))
            sim = columns_similarity(df[a].tolist(), df[b].tolist())
            if sim >= 0.95:
                a_mapped = by_original[a]["suggested_term"] is not None
                b_mapped = by_original[b]["suggested_term"] is not None
                keep = a if (a_mapped and not b_mapped) else (b if (b_mapped and not a_mapped) else a)
                drop = b if keep == a else a
                op = {
                    "type": "drop_redundant",
                    "keep": keep,
                    "drop": drop,
                    "similarity": round(sim, 3),
                    "confidence": "medium",
                    "auto_apply": False,
                    "note": "Columns '%s' and '%s' match in %.0f%% of overlapping rows; likely duplicates." % (
                        a, b, sim * 100
                    ),
                }
                operations.append(op)
                questions.append({
                    "id": "confirm_drop_%s" % normalize_column_name(drop),
                    "column": drop,
                    "question": "Drop '%s' as a duplicate of '%s'? yes/no" % (drop, keep),
                    "related_operation": op["type"] + ":" + drop,
                })

    return operations, questions


def missing_recommended(columns_report, operations):
    """Recommended fields not yet mapped by a column AND not about to be
    produced by a pending split/merge operation (e.g. merge_date_parts
    creates eventDate; split_coordinates creates decimalLatitude/Longitude)."""
    mapped_terms = {c["suggested_term"] for c in columns_report if c["suggested_term"]}
    for op in operations:
        target = op.get("target")
        if target:
            mapped_terms.add(target)
        for t in (op.get("targets") or []):
            if t and t.lower() != "skip":
                mapped_terms.add(t)
    return [term for term in RECOMMENDED_FIELDS if term not in mapped_terms]


def build_report_md(file_path, sheet, df, columns_report, operations, questions, missing):
    lines = []
    lines.append("# BioHousekeeper Analysis Report")
    lines.append("")
    lines.append("Source: `%s`%s" % (file_path, (" (sheet: `%s`)" % sheet) if sheet else ""))
    lines.append("Rows: %d | Columns: %d" % (len(df), len(df.columns)))
    lines.append("")
    lines.append("## Column mapping")
    lines.append("")
    lines.append("| Column | Suggested DwC term | Confidence | Note |")
    lines.append("|---|---|---|---|")
    for c in columns_report:
        term = c["suggested_term"] or "_(unmapped)_"
        note = c["note"] or ""
        lines.append("| `%s` | `%s` | %s | %s |" % (c["original"], term, c["confidence"], note))
    lines.append("")

    lines.append("## Proposed transformations")
    lines.append("")
    if operations:
        for op in operations:
            lines.append("- **%s** (%s, auto_apply=%s): %s" % (
                op["type"], op["confidence"], op["auto_apply"], op["note"]
            ))
    else:
        lines.append("_No split/merge/redundancy transformations detected._")
    lines.append("")

    lines.append("## Missing recommended fields")
    lines.append("")
    if missing:
        for term in missing:
            lines.append("- `%s`" % term)
    else:
        lines.append("_All commonly recommended Occurrence-core fields are present._")
    lines.append("")

    lines.append("## Open questions")
    lines.append("")
    if questions:
        for q in questions:
            lines.append("- %s" % q["question"])
    else:
        lines.append("_None - every suggestion above is high-confidence and safe to auto-apply._")
    lines.append("")

    lines.append("## Next step")
    lines.append("")
    lines.append(
        "Review `open questions` above, edit the JSON sidecar's `apply`/`targets` "
        "fields to reflect your answers, then run:"
    )
    lines.append("")
    lines.append("```bash")
    lines.append("python scripts/apply.py %s --plan <report>.json --output corrected.xlsx" % file_path)
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyzes a biodiversity spreadsheet and proposes a Darwin Core column structure."
    )
    parser.add_argument("file", help="Path to the spreadsheet (.csv or .xlsx)")
    parser.add_argument("--sheet", help="Sheet name (xlsx only; default: first sheet)")
    parser.add_argument("--out-dir", default=".", help="Directory to write the report + JSON sidecar")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print("[ERROR] File not found: %s" % args.file)
        sys.exit(1)

    print("[Info] Loading Darwin Core term base...")
    dwc_terms = load_dwc_terms()
    print("   [OK] %d terms loaded" % len(dwc_terms))

    print("[Info] Reading: %s" % args.file)
    df, sheet_names = read_spreadsheet(path, args.sheet)
    print("   [OK] %d rows, %d columns" % (len(df), len(df.columns)))
    if sheet_names and len(sheet_names) > 1:
        print("   [Note] Workbook has other sheets not analyzed: %s" % ", ".join(
            s for s in sheet_names if s != (args.sheet or sheet_names[0])
        ))

    columns_report, date_parts = analyze_columns(df, dwc_terms)
    operations, questions = detect_operations(df, columns_report, date_parts)
    missing = missing_recommended(columns_report, operations)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = path.stem
    report_md_path = out_dir / ("%s_biohousekeeper_report.md" % stem)
    report_json_path = out_dir / ("%s_biohousekeeper_report.json" % stem)

    report_md = build_report_md(args.file, args.sheet, df, columns_report, operations, questions, missing)
    report_md_path.write_text(report_md, encoding="utf-8")

    report_json = {
        "source_file": str(path),
        "sheet": args.sheet or (sheet_names[0] if sheet_names else None),
        "row_count": len(df),
        "columns": columns_report,
        "operations": operations,
        "questions": questions,
        "missing_recommended_fields": missing,
    }
    report_json_path.write_text(json.dumps(report_json, indent=2, ensure_ascii=False), encoding="utf-8")

    print()
    print("[OK] Report written: %s" % report_md_path)
    print("[OK] Plan written:   %s" % report_json_path)
    if questions:
        print("[Note] %d open question(s) need your input before applying." % len(questions))


if __name__ == "__main__":
    main()
