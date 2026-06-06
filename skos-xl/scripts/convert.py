#!/usr/bin/env python3
"""
convert.py - Converts SKOS vocabulary between formats or label styles.

Operations:
  --to-format     Convert RDF serialization format
  --to-xl         Upgrade plain skos:prefLabel/altLabel/hiddenLabel to SKOS-XL
  --from-xl       Downgrade SKOS-XL labels to plain skos:prefLabel/altLabel

Operations can be combined (e.g. upgrade to XL and save as JSON-LD).

Usage:
    python scripts/convert.py vocab.rdf --to-format turtle
    python scripts/convert.py vocab.ttl --to-format jsonld --output vocab.jsonld
    python scripts/convert.py vocab.ttl --to-xl
    python scripts/convert.py vocab.ttl --from-xl
    python scripts/convert.py vocab.ttl --to-xl --to-format jsonld
"""

import argparse
import sys
import uuid
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

try:
    from rdflib import Graph, Namespace, RDF, URIRef
    from rdflib.namespace import SKOS
except ImportError:
    print("[ERROR] rdflib not installed. Run: pip install rdflib")
    sys.exit(1)

SKOSXL = Namespace("http://www.w3.org/2008/05/skos-xl#")

FORMAT_EXT = {
    "turtle": ".ttl",
    "xml": ".rdf",
    "json-ld": ".jsonld",
    "nt": ".nt",
    "n3": ".n3",
}

FORMAT_ALIASES = {
    "ttl": "turtle", "turtle": "turtle",
    "rdfxml": "xml", "rdf": "xml", "xml": "xml",
    "jsonld": "json-ld", "json-ld": "json-ld", "json": "json-ld",
    "nt": "nt", "n3": "n3",
}


def detect_format(path):
    return {
        ".ttl": "turtle", ".n3": "n3", ".nt": "nt",
        ".rdf": "xml", ".owl": "xml", ".xml": "xml",
        ".jsonld": "json-ld", ".json": "json-ld",
    }.get(Path(path).suffix.lower(), "turtle")


def upgrade_to_xl(g, base_uri):
    """Upgrade plain SKOS labels to SKOS-XL Label resources."""
    g.bind("skosxl", SKOSXL)
    to_remove = []
    to_add = []
    count = 0

    for skos_prop, xl_prop in [
        (SKOS.prefLabel, SKOSXL.prefLabel),
        (SKOS.altLabel, SKOSXL.altLabel),
        (SKOS.hiddenLabel, SKOSXL.hiddenLabel),
    ]:
        for subj, obj in list(g.subject_objects(skos_prop)):
            lbl_uri = URIRef("%s#label_%s" % (base_uri.rstrip("#/"), uuid.uuid4().hex[:8]))
            to_add.extend([
                (lbl_uri, RDF.type, SKOSXL.Label),
                (lbl_uri, SKOSXL.literalForm, obj),
                (subj, xl_prop, lbl_uri),
            ])
            to_remove.append((subj, skos_prop, obj))
            count += 1

    for t in to_remove:
        g.remove(t)
    for t in to_add:
        g.add(t)
    return count


def downgrade_from_xl(g):
    """Downgrade SKOS-XL labels to plain SKOS literal labels."""
    to_remove = []
    to_add = []
    labels_to_clean = set()
    count = 0

    for xl_prop, skos_prop in [
        (SKOSXL.prefLabel, SKOS.prefLabel),
        (SKOSXL.altLabel, SKOS.altLabel),
        (SKOSXL.hiddenLabel, SKOS.hiddenLabel),
    ]:
        for subj, lbl_node in list(g.subject_objects(xl_prop)):
            lit = g.value(lbl_node, SKOSXL.literalForm)
            if lit is not None:
                to_add.append((subj, skos_prop, lit))
            to_remove.append((subj, xl_prop, lbl_node))
            labels_to_clean.add(lbl_node)
            count += 1

    for t in to_remove:
        g.remove(t)
    for t in to_add:
        g.add(t)
    for lbl in labels_to_clean:
        for t in list(g.triples((lbl, None, None))):
            g.remove(t)
    return count


def main():
    parser = argparse.ArgumentParser(
        description="Converts SKOS vocabulary format or label style"
    )
    parser.add_argument("file", help="Input SKOS vocabulary file")
    parser.add_argument("--to-format", "-f",
                        help="Target format: turtle, rdfxml, jsonld, nt, n3")
    parser.add_argument("--to-xl", action="store_true",
                        help="Upgrade plain SKOS labels to SKOS-XL")
    parser.add_argument("--from-xl", action="store_true",
                        help="Downgrade SKOS-XL labels to plain SKOS")
    parser.add_argument("--output", "-o",
                        help="Output file path (default: derived from input)")
    parser.add_argument("--base", "-b",
                        help="Base URI for new label IRIs (used with --to-xl)")
    args = parser.parse_args()

    if not args.to_format and not args.to_xl and not args.from_xl:
        parser.error("Specify at least one operation: --to-format, --to-xl, or --from-xl")

    if args.to_xl and args.from_xl:
        parser.error("Cannot combine --to-xl and --from-xl")

    in_path = Path(args.file)
    if not in_path.exists():
        print("[ERROR] File not found: %s" % args.file)
        sys.exit(1)

    in_fmt = detect_format(str(in_path))
    print()
    print("[Convert] %s" % args.file)
    print("   Input format: %s" % in_fmt)

    g = Graph()
    try:
        g.parse(str(in_path), format=in_fmt)
        print("   [OK] Parsed (%d triples)" % len(g))
    except Exception as e:
        print("   [ERROR] Parse failed: %s" % e)
        sys.exit(1)

    base_uri = args.base or ("http://example.org/%s" % in_path.stem)

    if args.to_xl:
        count = upgrade_to_xl(g, base_uri)
        print("   [OK] Upgraded %d label(s) to SKOS-XL" % count)

    if args.from_xl:
        count = downgrade_from_xl(g)
        print("   [OK] Downgraded %d SKOS-XL label(s) to plain SKOS" % count)

    out_fmt_raw = args.to_format or ""
    out_fmt = FORMAT_ALIASES.get(out_fmt_raw.lower(), in_fmt)
    out_ext = FORMAT_EXT.get(out_fmt, ".ttl")

    if args.output:
        out_path = Path(args.output)
    else:
        suffix = ""
        if args.to_xl:
            suffix += "_xl"
        if args.from_xl:
            suffix += "_plain"
        out_path = in_path.with_name(in_path.stem + suffix + out_ext)

    try:
        g.serialize(destination=str(out_path), format=out_fmt)
        print("   [OK] Written: %s (%d triples)" % (out_path, len(g)))
        print()
        print("[Next] Validate with: python scripts/validate.py %s" % out_path)
    except Exception as e:
        print("   [ERROR] Serialization failed: %s" % e)
        sys.exit(1)


if __name__ == "__main__":
    main()
