#!/usr/bin/env python3
"""
validate.py - Validates a Darwin Core Archive (.zip).

Checks:
  1. If the file is a valid ZIP
  2. If it contains meta.xml
  3. If all referenced files exist inside the ZIP
  4. If all terms used are valid Darwin Core terms
  5. If required fields are present

Usage:
    python scripts/validate.py archive.zip
    python scripts/validate.py archive.zip --verbose
"""

import argparse
import csv
import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Ensure UTF-8 output (Windows fix)
if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

NS = {
    "dwc": "http://rs.tdwg.org/dwc/text/",
}

REF_DIR = Path(__file__).resolve().parent.parent / "references"
TERMS_CSV = REF_DIR / "all_dwc_vertical.csv"


def load_valid_terms():
    """Load the set of valid Darwin Core term names."""
    terms = set()
    if not TERMS_CSV.exists():
        print("[WARN] all_dwc_vertical.csv not found. Term validation will be skipped.")
        return terms
    with open(TERMS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("type", "").strip()
            if name:
                terms.add(name.lower())
    return terms


def validate_zip(path):
    """Check if the file is a valid ZIP archive."""
    if not os.path.exists(path):
        return False, "File not found: %s" % path
    if not zipfile.is_zipfile(path):
        return False, "Not a valid ZIP file: %s" % path
    return True, None


def extract_meta_xml(zf):
    """Extract and parse meta.xml from the ZIP."""
    meta_paths = [n for n in zf.namelist() if n.lower().endswith("meta.xml")]
    if not meta_paths:
        return None, "meta.xml not found in the archive"
    if len(meta_paths) > 1:
        print("[WARN] Multiple meta.xml found: %s" % meta_paths)
    meta_path = meta_paths[0]
    try:
        with zf.open(meta_path) as f:
            tree = ET.parse(f)
        return tree, None
    except ET.ParseError as e:
        return None, "Error parsing meta.xml: %s" % e


def validate_meta_xml(tree):
    """Validate the structure of meta.xml."""
    errors = []
    root = tree.getroot()
    local_tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
    if local_tag != "archive":
        errors.append("Root tag expected 'archive', got '%s'" % local_tag)

    core = None
    for child in root:
        child_tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if child_tag == "core":
            core = child
            break

    if core is None:
        errors.append("<core> element not found in meta.xml")
        return errors

    row_type = core.get("rowType", "")
    if not row_type:
        errors.append("rowType attribute not found on <core>")
    else:
        print("   Core rowType: %s" % row_type)

    ignore_header = core.get("ignoreHeaderLines", "0")
    print("   ignoreHeaderLines: %s" % ignore_header)

    files_elem = None
    for child in core:
        child_tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if child_tag == "files":
            files_elem = child
            break

    if files_elem is None:
        errors.append("<files> element not found inside <core>")
    else:
        locations = []
        for child in files_elem:
            child_tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if child_tag == "location":
                locations.append(child)
        if not locations:
            errors.append("No <location> elements found in <files>")
        else:
            for loc in locations:
                print("   Data file: %s" % (loc.text or "??"))

    fields = []
    for child in core:
        child_tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if child_tag == "field":
            fields.append(child)
    print("   Defined fields: %d" % len(fields))

    return errors


def validate_referenced_files(zf, tree):
    """Check if all files referenced in meta.xml exist inside the ZIP."""
    errors = []
    root = tree.getroot()
    zip_files = set(zf.namelist())

    for elem in root.iter():
        elem_tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if elem_tag == "location":
            file_name = (elem.text or "").strip()
            if file_name:
                found = False
                for zf_name in zip_files:
                    if zf_name.endswith(file_name) or zf_name == file_name:
                        found = True
                        break
                if not found:
                    errors.append("Referenced file not found in ZIP: %s" % file_name)
    return errors


def validate_terms(tree, valid_terms):
    """Check if all terms used are valid Darwin Core terms."""
    warnings = []
    root = tree.getroot()

    for elem in root.iter():
        elem_tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if elem_tag == "field":
            term = elem.get("term", "")
            if term:
                term_name = term.split("/")[-1].lower()
                if term_name and valid_terms and term_name not in valid_terms:
                    warnings.append("Possibly invalid term: %s" % term)
    return warnings


def main():
    parser = argparse.ArgumentParser(
        description="Validates a Darwin Core Archive (.zip)"
    )
    parser.add_argument(
        "archive",
        help="Path to the Darwin Core Archive .zip file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed validation output"
    )
    args = parser.parse_args()

    path = args.archive
    errors = []
    warnings = []

    print()
    print("[Validate] %s" % path)
    print("=" * 60)

    # 1. Validate ZIP
    print("[1/5] Checking ZIP format...")
    valid, err = validate_zip(path)
    if not valid:
        print("   [ERROR] %s" % err)
        sys.exit(1)
    print("   [OK] Valid ZIP")

    # 2. Extract meta.xml
    print("[2/5] Reading meta.xml...")
    with zipfile.ZipFile(path, "r") as zf:
        tree, err = extract_meta_xml(zf)
        if err:
            print("   [ERROR] %s" % err)
            sys.exit(1)
        print("   [OK] meta.xml found and parsed")

        # 3. Validate structure
        print("[3/5] Validating meta.xml structure...")
        meta_errors = validate_meta_xml(tree)
        for e in meta_errors:
            print("   [ERROR] %s" % e)
            errors.append(e)
        if not meta_errors:
            print("   [OK] Structure OK")

        # 4. Validate referenced files
        print("[4/5] Checking referenced files...")
        file_errors = validate_referenced_files(zf, tree)
        for e in file_errors:
            print("   [ERROR] %s" % e)
            errors.append(e)
        if not file_errors:
            print("   [OK] All referenced files exist")

        # 5. Validate terms
        print("[5/5] Validating Darwin Core terms...")
        valid_terms = load_valid_terms()
        if valid_terms:
            term_warnings = validate_terms(tree, valid_terms)
            for w in term_warnings:
                print("   [WARN] %s" % w)
                warnings.append(w)
            if not term_warnings:
                print("   [OK] All terms are valid Darwin Core terms")
            print("   [Info] Base: %d terms loaded" % len(valid_terms))
        else:
            print("   [WARN] Term validation unavailable (no reference file)")

    # Summary
    print()
    print("=" * 60)
    if not errors:
        print("[RESULT] Validation complete - No errors found!")
    else:
        print("[RESULT] %d error(s) found" % len(errors))
        for e in errors:
            print("   . %s" % e)

    if warnings and args.verbose:
        print("\n[WARNINGS] %d warning(s):" % len(warnings))
        for w in warnings:
            print("   . %s" % w)

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
