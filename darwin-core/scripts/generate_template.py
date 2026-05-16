#!/usr/bin/env python3
"""
generate_template.py - Generates a Darwin Core Archive template.

Creates the directory structure, meta.xml, and example CSV.

Usage:
    python scripts/generate_template.py my_project --dir ./output
    python scripts/generate_template.py my_project --core event --dir ./output
"""

import argparse
import os
import sys
from pathlib import Path

# Ensure UTF-8 output (Windows fix)
if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Supported core types
CORES = {
    "occurrence": {
        "row_type": "http://rs.tdwg.org/dwc/terms/Occurrence",
        "file": "occurrences.csv",
        "description": "Occurrence",
        "terms": [
            "occurrenceID", "basisOfRecord", "scientificName", "kingdom",
            "phylum", "class", "order", "family", "genus", "specificEpithet",
            "taxonRank", "identificationQualifier", "identificationRemarks",
            "identifiedBy", "dateIdentified", "recordedBy", "recordNumber",
            "eventDate", "year", "month", "day", "country", "stateProvince",
            "county", "municipality", "locality", "decimalLatitude",
            "decimalLongitude", "geodeticDatum", "coordinateUncertaintyInMeters",
            "minimumElevationInMeters", "maximumElevationInMeters",
            "individualCount", "sex", "lifeStage", "occurrenceStatus",
            "catalogNumber", "institutionCode", "collectionCode",
            "ownerInstitutionCode", "associatedMedia", "occurrenceRemarks"
        ],
    },
    "event": {
        "row_type": "http://rs.tdwg.org/dwc/terms/Event",
        "file": "events.csv",
        "description": "Event",
        "terms": [
            "eventID", "parentEventID", "eventDate", "eventTime",
            "day", "month", "year", "verbatimEventDate",
            "continent", "country", "stateProvince", "county",
            "municipality", "locality", "decimalLatitude",
            "decimalLongitude", "geodeticDatum", "coordinateUncertaintyInMeters",
            "minimumElevationInMeters", "maximumElevationInMeters",
            "samplingProtocol", "sampleSizeValue", "sampleSizeUnit",
            "samplingEffort", "eventRemarks", "fieldNotes",
            "fieldNumber", "habitat", "recordedBy", "recordedByID"
        ],
    },
    "taxon": {
        "row_type": "http://rs.tdwg.org/dwc/terms/Taxon",
        "file": "taxa.csv",
        "description": "Taxon",
        "terms": [
            "taxonID", "scientificName", "scientificNameAuthorship",
            "taxonRank", "kingdom", "phylum", "class", "order",
            "family", "genus", "subgenus", "specificEpithet",
            "infraspecificEpithet", "parentNameUsageID",
            "acceptedNameUsageID", "originalNameUsageID",
            "nameAccordingTo", "namePublishedIn",
            "taxonomicStatus", "nomenclaturalStatus",
            "taxonRemarks", "vernacularName",
            "higherClassification", "datasetID"
        ],
    },
}


def generate_meta_xml(core, file_name):
    """Generate the content of meta.xml."""
    info = CORES[core]
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<archive xmlns="http://rs.tdwg.org/dwc/text/"')
    lines.append('    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
    lines.append('    xmlns:xs="http://www.w3.org/2001/XMLSchema"')
    lines.append('    xsi:schemaLocation="http://rs.tdwg.org/dwc/text/ http://rs.tdwg.org/dwc/text/tdwg_dwc_text.xsd">')
    lines.append('')
    lines.append('    <core rowType="%s" ignoreHeaderLines="1">' % info["row_type"])
    lines.append('        <files>')
    lines.append('            <location>%s</location>' % file_name)
    lines.append('        </files>')
    lines.append('')
    for idx, term in enumerate(info["terms"]):
        uri = "http://rs.tdwg.org/dwc/terms/%s" % term
        lines.append('        <field index="%d" term="%s" />' % (idx, uri))
    lines.append('    </core>')
    lines.append('</archive>')
    return "\n".join(lines) + "\n"


def generate_example_csv(core):
    """Generate example CSV content with DwC headers."""
    info = CORES[core]
    header = ",".join(info["terms"])
    empty_row = ",".join([""] * len(info["terms"]))
    return "%s\n# %s\n# (Replace this line with your data)\n" % (header, empty_row)


def main():
    parser = argparse.ArgumentParser(
        description="Generates a Darwin Core Archive template"
    )
    parser.add_argument(
        "name",
        help="Project name (will be the folder name)"
    )
    parser.add_argument(
        "--core",
        default="occurrence",
        choices=["occurrence", "event", "taxon"],
        help="Core type (default: occurrence)"
    )
    parser.add_argument(
        "--dir", "-d",
        default=".",
        help="Output directory (default: current directory)"
    )
    args = parser.parse_args()

    core = args.core
    info = CORES[core]
    project_dir = Path(args.dir) / args.name
    project_dir.mkdir(parents=True, exist_ok=True)
    csv_file = info["file"]

    print()
    print("[Template] Generating Darwin Core Archive: %s" % args.name)
    print("=" * 60)
    print("   Core: %s - %s" % (core, info["description"]))
    print("   Directory: %s" % project_dir)
    print()

    # meta.xml
    meta_path = project_dir / "meta.xml"
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(generate_meta_xml(core, csv_file))
    print("   [OK] meta.xml created (%d fields)" % len(info["terms"]))

    # CSV
    csv_path = project_dir / csv_file
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(generate_example_csv(core))
    print("   [OK] %s created (%d columns)" % (csv_file, len(info["terms"])))

    print()
    print("Generated structure:")
    print("   %s/" % project_dir)
    print("   +-- meta.xml")
    print("   +-- %s" % csv_file)
    print()
    print("Next: edit the CSV, zip it, and validate with validate.py")


if __name__ == "__main__":
    main()
