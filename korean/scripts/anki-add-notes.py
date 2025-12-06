#!/usr/bin/env python3
"""
Add notes to Anki from TSV and optionally unflag source cards.

Usage:
    python scripts/anki-add-notes.py --input anki/output/flag-2-cards.tsv --dry-run
    python scripts/anki-add-notes.py --input anki/output/flag-2-cards.tsv
    python scripts/anki-add-notes.py --input anki/output/flag-2-cards.tsv --unflag
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


def build_note(row: dict, deck: str, model: str, tags: list[str]) -> dict:
    """Build note object from TSV row."""
    # Generate number: extract_(source_number)_(korean) - Anki requires non-empty first field
    source_num = row.get("source_number", "")
    korean = row["korean"]
    number = f"extract_{source_num}_{korean}" if source_num else f"extract_{korean}"

    return {
        "deckName": deck,
        "modelName": model,
        "fields": {
            "number": number,
            "korean": korean,
            "english": row["english"],
            "example_ko": row["example_ko"],
            "example_en": row["example_en"],
            "etymology": row.get("etymology") or "",
            "notes": row.get("notes") or "",
            "korean_audio": "",
            "example_ko_audio": ""
        },
        "tags": tags
    }


def add_notes(rows: list[dict], deck: str, model: str, tags: list[str], dry_run: bool, url: str) -> bool:
    """Add notes to Anki."""
    print(f"=== Adding {len(rows)} notes ===")
    print(f"Deck: {deck}")
    print(f"Model: {model}")
    print(f"Tag: {tags}")
    print()

    success = 0
    failed = 0

    for row in rows:
        note = build_note(row, deck, model, tags)
        korean = row["korean"]

        if dry_run:
            print(f"[DRY-RUN] Would add: {note['fields']['number']}")
            success += 1
        else:
            try:
                note_id = anki_request("addNote", {"note": note}, url)
                print(f"[OK] Added: {korean} (note_id: {note_id})")
                success += 1
            except Exception as e:
                print(f"[FAIL] {korean}: {e}", file=sys.stderr)
                failed += 1

    print(f"Add notes: {success} success, {failed} failed")
    return failed == 0


def unflag_cards(rows: list[dict], dry_run: bool, url: str) -> bool:
    """Unflag source cards using source_number column."""
    numbers = list(set(row["source_number"] for row in rows if row.get("source_number")))
    print()
    print(f"=== Unflagging {len(numbers)} source cards ===")

    success = 0
    failed = 0

    for number in numbers:
        query = f"number:{number}"

        if dry_run:
            print(f"[DRY-RUN] Would unflag: number={number}")
            success += 1
            continue

        try:
            card_ids = anki_request("findCards", {"query": query}, url)
            if not card_ids:
                print(f"[WARN] No card found: number={number}", file=sys.stderr)
                failed += 1
                continue

            for card_id in card_ids:
                anki_request("setSpecificValueOfCard", {
                    "card": card_id,
                    "keys": ["flags"],
                    "newValues": [0]
                }, url)

            print(f"[OK] Unflagged: number={number}")
            success += 1
        except Exception as e:
            print(f"[FAIL] number={number}: {e}", file=sys.stderr)
            failed += 1

    print(f"Unflag: {success} success, {failed} failed")
    return failed == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Add notes to Anki from TSV")
    parser.add_argument("--input", required=True, help="Input TSV file (flag-2-cards.tsv)")
    parser.add_argument("--unflag", action="store_true", help="Unflag source cards (uses source_number column)")
    parser.add_argument("--deck", default="Korean::Custom", help="Target deck")
    parser.add_argument("--model", default="Korean Vocabulary", help="Note model")
    parser.add_argument("--tag", default="extracted", help="Tag to add")
    parser.add_argument("--dry-run", action="store_true", help="Print without executing")
    parser.add_argument("--url", default="http://localhost:8765", help="AnkiConnect URL")

    args = parser.parse_args()

    # Read cards TSV
    with open(args.input, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)

    tags = [args.tag] if args.tag else []

    # Add notes
    add_ok = add_notes(rows, args.deck, args.model, tags, args.dry_run, args.url)

    # Unflag only if notes succeeded (uses source_number column from same file)
    unflag_ok = True
    if args.unflag:
        if not add_ok and not args.dry_run:
            print("\nSkipping unflag - notes failed")
        else:
            unflag_ok = unflag_cards(rows, args.dry_run, args.url)

    return 0 if (add_ok and unflag_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
