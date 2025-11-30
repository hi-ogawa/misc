#!/usr/bin/env python3
"""
Create filtered Anki import TSV by joining tier examples with etymology/notes.

Usage:
    python scripts/create-tier1-anki-import.py --tier tier-1-examples.tsv --anki anki_import.tsv --prefix koreantopik2_tier1
"""

import argparse
import csv
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Create filtered Anki import by joining tier examples with etymology/notes"
    )
    parser.add_argument("--tier", required=True, help="Tier examples TSV (number, korean, english, tier, example_ko, example_en)")
    parser.add_argument("--anki", required=True, help="Original Anki import TSV (for etymology, notes)")
    parser.add_argument("--prefix", required=True, help="Prefix for output numbering (e.g., koreantopik2_tier1)")
    parser.add_argument("--output", help="Output file (default: derived from prefix)")

    args = parser.parse_args()

    tier_file = Path(args.tier)
    anki_file = Path(args.anki)
    prefix = args.prefix

    # Derive output path if not specified
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = tier_file.parent / f"{prefix}_anki_import.tsv"

    # Validate inputs
    for f in [tier_file, anki_file]:
        if not f.exists():
            print(f"Error: File not found: {f}", file=sys.stderr)
            return 1

    # Read etymology and notes from existing anki import
    # Key: original number (e.g., "2" extracted from "koreantopik2_2")
    etymology_notes = {}

    print(f"Reading etymology/notes from {anki_file}...")
    with open(anki_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            # Extract number after last underscore (handles any prefix)
            orig_num = row['number'].rsplit('_', 1)[-1]
            etymology_notes[orig_num] = {
                'etymology': row.get('etymology', ''),
                'notes': row.get('notes', '')
            }

    # Read tier examples and merge
    print(f"Reading tier examples from {tier_file}...")
    merged_data = []
    new_num = 0

    with open(tier_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            new_num += 1
            orig_num = row['number']

            # Get etymology/notes from original
            ety_notes = etymology_notes.get(orig_num, {'etymology': '', 'notes': ''})

            # Format audio references with new numbering
            korean_audio = f"[sound:{prefix}_korean_{new_num:04d}.mp3]"
            example_ko_audio = f"[sound:{prefix}_example_ko_{new_num:04d}.mp3]"

            merged_row = {
                'number': f"{prefix}_{new_num}",
                'korean': row['korean'],
                'english': row['english'],
                'example_ko': row['example_ko'],
                'example_en': row['example_en'],
                'etymology': ety_notes['etymology'],
                'notes': ety_notes['notes'],
                'korean_audio': korean_audio,
                'example_ko_audio': example_ko_audio
            }

            merged_data.append(merged_row)

    # Write output file
    print(f"Writing to {output_file}...")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['number', 'korean', 'english', 'example_ko', 'example_en',
                      'etymology', 'notes', 'korean_audio', 'example_ko_audio']
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(merged_data)

    print(f"✓ Created {len(merged_data)} entries")

    # Show sample
    print("\nSample:")
    for row in merged_data[:2]:
        print(f"  {row['number']}: {row['korean']} - {row['example_ko'][:40]}...")

    return 0


if __name__ == '__main__':
    sys.exit(main())
