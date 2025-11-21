#!/usr/bin/env python3
"""
Merge new example sentences into an existing Anki import TSV file.

Replaces example_ko and example_en columns while preserving all other fields.
"""

import argparse
import csv
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Merge new examples into existing Anki import file"
    )
    parser.add_argument("--base", required=True, help="Base Anki import TSV file")
    parser.add_argument("--examples", required=True, help="New examples TSV file")
    parser.add_argument("--output", required=True, help="Output TSV file")
    args = parser.parse_args()

    base_file = Path(args.base)
    examples_file = Path(args.examples)
    output_file = Path(args.output)

    if not base_file.exists():
        print(f"Error: Base file not found: {base_file}", file=sys.stderr)
        return 1

    if not examples_file.exists():
        print(f"Error: Examples file not found: {examples_file}", file=sys.stderr)
        return 1

    # Read base file
    print(f"Reading base file: {base_file}")
    base_data = {}
    with open(base_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            base_data[row['number']] = dict(row)

    # Read new examples
    print(f"Reading examples file: {examples_file}")
    new_examples = {}
    with open(examples_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            new_examples[row['number']] = {
                'example_ko': row['example_ko'],
                'example_en': row['example_en']
            }

    # Merge
    merged_count = 0
    for num in base_data:
        if num in new_examples:
            base_data[num]['example_ko'] = new_examples[num]['example_ko']
            base_data[num]['example_en'] = new_examples[num]['example_en']
            merged_count += 1

    # Write output (column order matches TOPIK 2 structure)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ['number', 'korean', 'english', 'example_ko', 'example_en',
                  'etymology', 'notes', 'korean_audio', 'example_ko_audio']

    print(f"Writing output: {output_file}")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for num in sorted(base_data.keys(), key=int):
            writer.writerow(base_data[num])

    print(f"Done! Merged {merged_count} examples into {len(base_data)} entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
