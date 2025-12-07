#!/usr/bin/env python3
"""
Update existing Anki notes from TSV and optionally remove tags.

Usage:
    python scripts/anki-update-notes.py --input anki/output/fix-cards-fixed.tsv --dry-run
    python scripts/anki-update-notes.py --input anki/output/fix-cards-fixed.tsv
    python scripts/anki-update-notes.py --input anki/output/fix-cards-fixed.tsv --remove-tag fix
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
    parser.add_argument("--input", required=True, help="Input TSV file")
    parser.add_argument("--fields", default="example_ko,example_en",
                        help="Comma-separated fields to update (default: example_ko,example_en)")
    parser.add_argument("--audio-prefix", default="",
                        help="Audio filename prefix (e.g., 'koreantopik1_example_ko_fix_')")
    parser.add_argument("--remove-tag", default="", help="Tag to remove after update (e.g., 'fix')")
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
        return 1

    if "number" not in rows[0]:
        print("Error: TSV must contain 'number' column", file=sys.stderr)
        return 1

    fields = [f.strip() for f in args.fields.split(",")]

    # Update notes
    print(f"=== Updating {len(rows)} notes ===")
    print(f"Fields: {', '.join(fields)}")
    if args.audio_prefix:
        print(f"Audio prefix: {args.audio_prefix}")
    print()

    success = 0
    failed = 0
    updated_note_ids = []

    for row in rows:
        number = row["number"]

        if args.dry_run:
            print(f"[DRY-RUN] Would update: number={number}")
            for field in fields:
                if field in row:
                    val = row[field]
                    print(f"  {field}: {val[:50]}..." if len(val) > 50 else f"  {field}: {val}")
            if args.audio_prefix:
                print(f"  example_ko_audio: [sound:{args.audio_prefix}{int(number):04d}.mp3]")
            success += 1
            continue

        # Find note ID
        note_ids = anki_request("findNotes", {"query": f"number:{number}"}, args.url)
        if not note_ids:
            print(f"[FAIL] Note not found: number={number}", file=sys.stderr)
            failed += 1
            continue

        note_id = note_ids[0]

        # Build fields to update
        update_fields = {field: row[field] for field in fields if field in row}
        if args.audio_prefix:
            update_fields["example_ko_audio"] = f"[sound:{args.audio_prefix}{int(number):04d}.mp3]"

        try:
            anki_request("updateNoteFields", {"note": {"id": note_id, "fields": update_fields}}, args.url)
            print(f"[OK] Updated: number={number}")
            updated_note_ids.append(note_id)
            success += 1
        except Exception as e:
            print(f"[FAIL] number={number}: {e}", file=sys.stderr)
            failed += 1

    print()
    print(f"Update: {success} success, {failed} failed")

    # Remove tag
    if args.remove_tag and (success > 0 or args.dry_run):
        print()
        print(f"=== Removing tag '{args.remove_tag}' ===")

        if args.dry_run:
            print(f"[DRY-RUN] Would remove tag '{args.remove_tag}' from {len(rows)} notes")
        elif failed > 0:
            print("Skipping tag removal - some updates failed")
        else:
            try:
                anki_request("removeTags", {"notes": updated_note_ids, "tags": args.remove_tag}, args.url)
                print(f"[OK] Removed tag '{args.remove_tag}' from {len(updated_note_ids)} notes")
            except Exception as e:
                print(f"[FAIL] Remove tag: {e}", file=sys.stderr)
                return 1

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
