#!/usr/bin/env python3
"""
Export cards from Anki via AnkiConnect.

Usage:
    python scripts/anki-export.py --query "deck:Korean::TOPIK1 flag:2" --fields number,korean,example_ko,example_en
    python scripts/anki-export.py --query "deck:Korean::TOPIK1 flag:2" --fields number,korean,example_ko,example_en --output anki/output/flag-2.tsv
"""

import argparse
import csv
import json
import sys
import urllib.request
from typing import Any


def anki_request(action: str, params: dict | None = None, url: str = "http://localhost:8765") -> Any:
    """Send request to AnkiConnect."""
    payload: dict = {"action": action, "version": 6}
    if params:
        payload["params"] = params

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    if result.get("error"):
        raise Exception(result["error"])
    return result["result"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Export cards from Anki via AnkiConnect")
    parser.add_argument("--query", required=True, help="Anki search query (e.g., 'deck:Korean::TOPIK1 flag:2')")
    parser.add_argument("--fields", required=True, help="Comma-separated field names to export")
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--url", default="http://localhost:8765", help="AnkiConnect URL")

    args = parser.parse_args()
    fields = [f.strip() for f in args.fields.split(",")]

    # Find cards
    card_ids = anki_request("findCards", {"query": args.query}, args.url)
    if not card_ids:
        print(f"No cards found for query: {args.query}", file=sys.stderr)
        return 0

    print(f"Found {len(card_ids)} cards", file=sys.stderr)

    # Get card info
    cards_info = anki_request("cardsInfo", {"cards": card_ids}, args.url)

    # Extract fields
    rows = []
    for card in cards_info:
        row = {}
        for field in fields:
            row[field] = card["fields"].get(field, {}).get("value", "")
        rows.append(row)

    # Write TSV
    out = open(args.output, "w", encoding="utf-8") if args.output else sys.stdout
    try:
        writer = csv.DictWriter(out, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    finally:
        if args.output:
            out.close()
            print(f"Wrote {len(rows)} rows to {args.output}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
