#!/usr/bin/env python3
"""
Create Anki import TSV file by merging all enhancement files.

Usage:
    python scripts/create-anki-import.py <dataset_name>

Example:
    python scripts/create-anki-import.py koreantopik2
"""

import csv
import sys
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/create-anki-import.py <dataset_name>")
        print("Example: python scripts/create-anki-import.py koreantopik2")
        sys.exit(1)

    dataset = sys.argv[1]

    # Input files
    base_file = Path(f"input/{dataset}.tsv")
    etymology_file = Path(f"output/{dataset}/etymology-all.tsv")
    examples_file = Path(f"output/{dataset}/examples-all.tsv")
    notes_file = Path(f"output/{dataset}/notes-all.tsv")

    # Output file
    output_file = Path(f"output/{dataset}/{dataset}_anki_import.tsv")

    # Verify all input files exist
    for f in [base_file, etymology_file, examples_file, notes_file]:
        if not f.exists():
            print(f"ERROR: Input file not found: {f}", file=sys.stderr)
            sys.exit(1)

    # Read all files into dictionaries keyed by number
    base_data = {}
    etymology_data = {}
    examples_data = {}
    notes_data = {}

    print("Reading base file...")
    with open(base_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            num = row['number']
            base_data[num] = {
                'number': num,
                'korean': row['korean'],
                'english': row['english']
            }

    print("Reading etymology file...")
    with open(etymology_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            num = row['number']
            etymology_data[num] = row.get('etymology', '')

    print("Reading examples file...")
    with open(examples_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            num = row['number']
            examples_data[num] = {
                'example_ko': row.get('example_ko', ''),
                'example_en': row.get('example_en', '')
            }

    print("Reading notes file...")
    with open(notes_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            num = row['number']
            notes_data[num] = row.get('notes', '')

    # Merge all data
    print("Merging data...")
    merged_data = []

    for num in sorted(base_data.keys(), key=int):
        base = base_data[num]
        etymology = etymology_data.get(num, '')
        examples = examples_data.get(num, {})
        notes = notes_data.get(num, '')

        # Format audio references
        korean_audio = f"[sound:{dataset}_korean_{int(num):04d}.mp3]"
        example_ko_audio = f"[sound:{dataset}_example_ko_{int(num):04d}.mp3]"

        # Use prefixed number for unique identification across datasets
        prefixed_number = f"{dataset}_{num}"

        merged_row = {
            'number': prefixed_number,
            'korean': base['korean'],
            'english': base['english'],
            'example_ko': examples.get('example_ko', ''),
            'example_en': examples.get('example_en', ''),
            'etymology': etymology,
            'notes': notes,
            'korean_audio': korean_audio,
            'example_ko_audio': example_ko_audio
        }

        merged_data.append(merged_row)

    # Write output file
    print(f"Writing Anki import file to {output_file}...")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['number', 'korean', 'english', 'example_ko', 'example_en',
                      'etymology', 'notes', 'korean_audio', 'example_ko_audio']
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')

        writer.writeheader()
        writer.writerows(merged_data)

    print(f"✓ Anki import file created successfully!")
    print(f"  Total entries: {len(merged_data)}")
    print(f"  Output: {output_file}")

    # Verify
    with open(output_file, 'r', encoding='utf-8') as f:
        line_count = sum(1 for _ in f)

    expected_lines = len(merged_data) + 1  # +1 for header
    if line_count == expected_lines:
        print(f"✓ Verification passed: {line_count} lines (including header)")
    else:
        print(f"⚠ Warning: Expected {expected_lines} lines, got {line_count}")
        sys.exit(1)

    # Show sample
    print("\nSample row (entry #1):")
    with open(output_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        first_row = next(reader)
        for key, value in first_row.items():
            print(f"  {key}: {value}")

if __name__ == '__main__':
    main()
