#!/usr/bin/env python3
"""
map_columns.py - Maps CSV columns to Darwin Core terms.

Analyzes a CSV, suggests mappings to DwC terms, and can generate
a new CSV with Darwin Core headers.

Usage:
    python scripts/map_columns.py data.csv
    python scripts/map_columns.py data.csv --output mapped.csv
    python scripts/map_columns.py data.csv --interactive
"""

import argparse
import csv
import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output (Windows fix)
if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REF_DIR = Path(__file__).resolve().parent.parent / "references"
TERMS_CSV = REF_DIR / "all_dwc_vertical.csv"


# Smart mapping dictionary: common patterns in English, Portuguese, Spanish, etc.
SUGGESTED_MAPPING = {
    # Identifiers
    "id": "occurrenceID",
    "code": "occurrenceID",
    "catalog": "catalogNumber",
    "catalognumber": "catalogNumber",
    "catalog_number": "catalogNumber",
    # Taxonomy
    "species": "scientificName",
    "scientificname": "scientificName",
    "scientific_name": "scientificName",
    "scientificnameauthorship": "scientificNameAuthorship",
    "genus": "genus",
    "genero": "genus",
    "family": "family",
    "familia": "family",
    "order": "order",
    "ordem": "order",
    "class": "class",
    "classe": "class",
    "phylum": "phylum",
    "filo": "phylum",
    "kingdom": "kingdom",
    "reino": "kingdom",
    "author": "scientificNameAuthorship",
    "autor": "scientificNameAuthorship",
    "taxon_rank": "taxonRank",
    "taxonrank": "taxonRank",
    "rank": "taxonRank",
    # Location
    "country": "country",
    "pais": "country",
    "state": "stateProvince",
    "stateprovince": "stateProvince",
    "estado": "stateProvince",
    "province": "stateProvince",
    "municipality": "municipality",
    "municipio": "municipality",
    "locality": "locality",
    "localidade": "locality",
    "location": "locality",
    "local": "locality",
    "latitude": "decimalLatitude",
    "lat": "decimalLatitude",
    "decimallatitude": "decimalLatitude",
    "decimal_latitude": "decimalLatitude",
    "longitude": "decimalLongitude",
    "lon": "decimalLongitude",
    "lng": "decimalLongitude",
    "decimallongitude": "decimalLongitude",
    "decimal_longitude": "decimalLongitude",
    "datum": "geodeticDatum",
    "geodeticdatum": "geodeticDatum",
    "altitude": "minimumElevationInMeters",
    "elevation": "minimumElevationInMeters",
    "verbatimcoordinates": "verbatimCoordinates",
    # Date
    "date": "eventDate",
    "eventdate": "eventDate",
    "event_date": "eventDate",
    "year": "year",
    "month": "month",
    "day": "day",
    # Collection
    "recordedby": "recordedBy",
    "recorded_by": "recordedBy",
    "collector": "recordedBy",
    "coletor": "recordedBy",
    "recordnumber": "recordNumber",
    "record_number": "recordNumber",
    "samplingprotocol": "samplingProtocol",
    "sampling_protocol": "samplingProtocol",
    "habitat": "habitat",
    # Institution
    "institution": "institutionCode",
    "institutioncode": "institutionCode",
    "institution_code": "institutionCode",
    "collection": "collectionCode",
    "collectioncode": "collectionCode",
    "collection_code": "collectionCode",
    # Record
    "basisofrecord": "basisOfRecord",
    "basis_of_record": "basisOfRecord",
    "individualcount": "individualCount",
    "individual_count": "individualCount",
    "quantity": "individualCount",
    "sex": "sex",
    "sexo": "sex",
    "lifestage": "lifeStage",
    "life_stage": "lifeStage",
    "estagio": "lifeStage",
    "occurrencestatus": "occurrenceStatus",
    "occurrence_status": "occurrenceStatus",
    "occurrenceremarks": "occurrenceRemarks",
    "notes": "occurrenceRemarks",
    "remarks": "occurrenceRemarks",
    # Identification
    "identifiedby": "identifiedBy",
    "identified_by": "identifiedBy",
    "dateidentified": "dateIdentified",
    "date_identified": "dateIdentified",
    # Media
    "media": "associatedMedia",
    "associatedmedia": "associatedMedia",
    "image": "associatedMedia",
    "photo": "associatedMedia",
}


def load_dwc_terms():
    """Load Darwin Core term names from the reference CSV."""
    terms = set()
    if not TERMS_CSV.exists():
        return terms
    with open(TERMS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("type", "").strip()
            if name:
                terms.add(name.lower())
    return terms


def normalize_column_name(name):
    """Normalize column name for dictionary lookup."""
    name = name.lower().strip()
    name = re.sub(r"[_\s\-]+", "_", name)
    name = re.sub(r"[^a-z0-9_]", "", name)
    return name


def suggest_mapping(columns, dwc_terms):
    """Suggest DwC term mapping for each CSV column."""
    mapping = {}
    unmapped = []

    for column in columns:
        col_norm = normalize_column_name(column)

        # Exact match in suggestion dictionary
        if col_norm in SUGGESTED_MAPPING:
            mapping[column] = SUGGESTED_MAPPING[col_norm]
            continue

        # If column name is already a valid DwC term
        if col_norm in dwc_terms:
            mapping[column] = col_norm
            continue

        # Partial match
        found = False
        for term in dwc_terms:
            if col_norm in term or term in col_norm:
                mapping[column] = term
                found = True
                break

        if not found:
            unmapped.append(column)

    return mapping, unmapped


def convert_csv(input_file, output_file, mapping):
    """Generate a new CSV with Darwin Core headers."""
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        original_cols = reader.fieldnames or []
        data = list(reader)

    new_headers = []
    for col in original_cols:
        if col in mapping:
            new = mapping[col]
            if new not in new_headers:
                new_headers.append(new)
        elif col not in new_headers:
            new_headers.append(col)

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=new_headers)
        writer.writeheader()
        for row in data:
            new_row = {}
            for col_orig, value in row.items():
                if col_orig in mapping:
                    new_name = mapping[col_orig]
                    if new_name not in new_row:
                        new_row[new_name] = value
                elif col_orig not in new_row:
                    new_row[col_orig] = value
            writer.writerow(new_row)


def main():
    parser = argparse.ArgumentParser(
        description="Maps CSV columns to Darwin Core terms"
    )
    parser.add_argument(
        "file",
        help="Path to the CSV file"
    )
    parser.add_argument(
        "--output", "-o",
        help="Generate a new CSV with DwC headers"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Confirm each mapping interactively"
    )
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print("[ERROR] File not found: %s" % args.file)
        sys.exit(1)

    # Load DwC terms
    print("[Info] Loading Darwin Core term base...")
    dwc_terms = load_dwc_terms()
    print("   [OK] %d terms loaded" % len(dwc_terms))

    # Read CSV
    print("[Info] Reading: %s" % args.file)
    with open(args.file, "r", encoding="utf-8") as f:
        dialect = csv.Sniffer().sniff(f.read(2048))
        f.seek(0)
        reader = csv.DictReader(f, dialect=dialect)
        columns = reader.fieldnames or []

    print("   [OK] %d columns found (delimiter='%s')" % (len(columns), dialect.delimiter))
    print()

    # Suggest mapping
    mapping, unmapped = suggest_mapping(columns, dwc_terms)

    print("[Mapping] Suggestions:")
    print("=" * 60)

    final_mapping = {}
    for column in columns:
        if column in mapping:
            suggestion = mapping[column]
            if args.interactive:
                resp = input("   %-30s -> %s [Enter=accept, n=skip, m=manual]: " % (column, suggestion))
                if resp.lower() == "n":
                    continue
                elif resp.lower() == "m":
                    manual = input("      DwC term: ").strip()
                    if manual:
                        final_mapping[column] = manual
                    continue
                final_mapping[column] = suggestion
            else:
                final_mapping[column] = suggestion
                print("   [OK] %-30s -> %s" % (column, suggestion))
        else:
            print("   [--] %-30s -> (unmapped)" % column)

    if unmapped:
        print()
        print("[WARN] %d unmapped column(s):" % len(unmapped))
        for c in unmapped:
            print("   . %s" % c)

    # Generate output CSV
    if args.output and final_mapping:
        print()
        print("[Output] Generating: %s" % args.output)
        convert_csv(args.file, args.output, final_mapping)
        print("   [OK] CSV generated with %d mapped columns" % len(final_mapping))
        print("   [Tip] Validate with: python scripts/validate.py %s" % args.output)

    print()
    print("[OK] Mapping complete!")


if __name__ == "__main__":
    main()
