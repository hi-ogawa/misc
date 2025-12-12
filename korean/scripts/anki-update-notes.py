#!/usr/bin/env python3
"""
Update existing Anki notes from TSV.

Usage:
    # Update text fields
    python scripts/anki-update-notes.py --input file.tsv --fields example_ko,example_en

    # Update audio fields
    python scripts/anki-update-notes.py --input file.tsv --fields korean_audio,example_ko_audio

    # Update + remove tag
    python scripts/anki-update-notes.py --input file.tsv --fields example_ko,example_en --remove-tag fix
"""

import argparse
import csv
import json
import sys
import urllib.request
from pathlib import Path
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
    parser = argparse.ArgumentParser(description="Update Anki notes from TSV")
    parser.add_argument("--input", required=True, help="Input TSV file (must have noteId column)")
    parser.add_argument("--fields", required=True, help="Comma-separated fields to update from TSV")
    parser.add_argument("--remove-tag", default="", help="Tag to remove after update")
    parser.add_argument("--dry-run", action="store_true", help="Print without executing")
    parser.add_argument("--url", default="http://localhost:8765", help="AnkiConnect URL")

    args = parser.parse_args()

    # Validate input
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        return 1

    # Read TSV
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)

    if not rows:
        print("No rows found in input file")
        return 0

    if "noteId" not in rows[0]:
        print("Error: TSV must contain 'noteId' column", file=sys.stderr)
        return 1

    fields = [f.strip() for f in args.fields.split(",")]

    # Validate fields exist in TSV
    missing = [f for f in fields if f not in rows[0]]
    if missing:
        print(f"Error: Fields not in TSV: {', '.join(missing)}", file=sys.stderr)
        return 1

    # Print config
    print(f"=== Updating {len(rows)} notes ===")
    print(f"Fields: {', '.join(fields)}")
    if args.remove_tag:
        print(f"Remove tag: {args.remove_tag}")
    print()

    success = 0
    failed = 0
    updated_note_ids = []

    for row in rows:
        note_id = int(row["noteId"])
        update_fields = {field: row[field] or "" for field in fields}

        if args.dry_run:
            print(f"[DRY-RUN] {note_id}")
            for k, v in update_fields.items():
                display_v = v[:60] + "..." if len(v) > 60 else v
                print(f"  {k}: {display_v}")
            success += 1
            continue

        try:
            anki_request("updateNoteFields", {"note": {"id": note_id, "fields": update_fields}}, args.url)
            print(f"[OK] {note_id}")
            updated_note_ids.append(note_id)
            success += 1
        except Exception as e:
            print(f"[FAIL] {note_id}: {e}", file=sys.stderr)
            failed += 1

    print()
    print(f"Updated: {success} success, {failed} failed")

    # Remove tag
    if args.remove_tag and updated_note_ids and not args.dry_run:
        if failed > 0:
            print(f"\nSkipping tag removal - some updates failed")
        else:
            print(f"\nRemoving tag '{args.remove_tag}'...")
            try:
                anki_request("removeTags", {"notes": updated_note_ids, "tags": args.remove_tag}, args.url)
                print(f"[OK] Removed tag from {len(updated_note_ids)} notes")
            except Exception as e:
                print(f"[FAIL] Remove tag: {e}", file=sys.stderr)
                return 1

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
