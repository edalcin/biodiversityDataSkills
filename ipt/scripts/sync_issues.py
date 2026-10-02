#!/usr/bin/env python3
"""
Sync gbif/ipt GitHub issues to a TSV file.

Downloads all issues (open and closed, excludes PRs) from the gbif/ipt repository
via GitHub REST API with pagination, writes to a TSV file sorted by number descending.

Usage:
    python sync_issues.py
    python sync_issues.py --out custom/path.tsv
    GITHUB_TOKEN=$(gh auth token) python sync_issues.py

Environment:
    GITHUB_TOKEN: optional Bearer token to bypass rate limit (default 60 req/hr, 5000 with auth)

Output TSV columns:
    number, state, created, closed, labels, title
    - dates as YYYY-MM-DD (closed is empty if still open)
    - labels joined with semicolon
    - tabs and newlines in titles replaced by spaces
"""

import urllib.request
import urllib.error
import json
import csv
import argparse
import os
from pathlib import Path
from datetime import datetime


def fetch_issues(token=None):
    """Fetch all non-PR issues from gbif/ipt, yield as dicts."""
    page = 1
    url_base = "https://api.github.com/repos/gbif/ipt/issues?state=all&per_page=100"
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    while True:
        url = f"{url_base}&page={page}"
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 403:
                raise RuntimeError(
                    "HTTP 403: GitHub API rate limit exceeded. "
                    "Set GITHUB_TOKEN environment variable: GITHUB_TOKEN=$(gh auth token) python sync_issues.py"
                )
            raise
        
        if not data:
            break
        
        for issue in data:
            # Skip pull requests
            if "pull_request" in issue:
                continue
            yield issue
        
        page += 1


def parse_issue(issue):
    """Convert issue dict to row tuple."""
    number = issue["number"]
    state = issue["state"]
    created = issue["created_at"][:10] if issue.get("created_at") else ""
    closed = issue["closed_at"][:10] if issue.get("closed_at") else ""
    labels = ";".join(label["name"] for label in issue.get("labels", []))
    title = issue["title"].replace("\t", " ").replace("\n", " ")
    
    return (number, state, created, closed, labels, title)


def main():
    parser = argparse.ArgumentParser(
        description="Sync gbif/ipt GitHub issues to TSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).parent.parent / "references" / "issues-index.tsv",
        help="Output TSV path (default: ../references/issues-index.tsv)"
    )
    args = parser.parse_args()
    
    token = os.environ.get("GITHUB_TOKEN")
    
    # Fetch and sort
    issues = list(fetch_issues(token))
    rows = [parse_issue(issue) for issue in issues]
    rows.sort(key=lambda r: int(r[0]), reverse=True)
    
    # Write TSV
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["number", "state", "created", "closed", "labels", "title"])
        writer.writerows(rows)
    
    print(f"Wrote {len(rows)} issues to {args.out}")


if __name__ == "__main__":
    main()
