#!/usr/bin/env python3
"""
Merge Anki export with updated examples, preserving all existing fields.
"""

import argparse
import csv
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Merge Anki export with updated examples, preserving existing data"
    )
    parser.add_argument(
        "--anki-export",
        type=str,
        required=True,
        help="Anki export file (.txt) with existing cards"
    )
    parser.add_argument(
        "--new-examples",
        type=str,
        required=True,
        help="TSV file with updated examples (e.g., output/examples-v2-all.tsv)"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output file for reimport into Anki"
    )
    parser.add_argument(
        "--audio-prefix",
        type=str,
        default="koreantopik1_v2",
        help="Audio file prefix (default: koreantopik1_v2)"
    )
    parser.add_argument(
        "--start",
        type=int,
        default=None,
        help="Start from this entry number (inclusive, e.g., 1)"
    )
    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="End at this entry number (inclusive, e.g., 100)"
    )

    args = parser.parse_args()

    # Read input files
    anki_export_file = Path(args.anki_export)
    new_examples_file = Path(args.new_examples)
    output_file = Path(args.output)

    if not anki_export_file.exists():
        print(f"Error: Anki export file not found: {anki_export_file}", file=sys.stderr)
        return 1

    if not new_examples_file.exists():
        print(f"Error: New examples file not found: {new_examples_file}", file=sys.stderr)
        return 1

    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Determine range
    start = args.start if args.start is not None else 1
    end = args.end if args.end is not None else 9999

    range_info = ""
    if args.start or args.end:
        range_info = f" (range: {start}-{end})"

    print(f"Reading Anki export:  {anki_export_file}")
    print(f"Reading new examples: {new_examples_file}")
    print(f"Writing output to:    {output_file}")
    print(f"Audio prefix:         {args.audio_prefix}")
    if range_info:
        print(f"Update range:         {start}-{end}")
    print()

    # Read new examples into a dictionary keyed by number
    new_examples = {}
    with open(new_examples_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        required_columns = ["number", "example_ko", "example_en"]
        if not all(col in reader.fieldnames for col in required_columns):
            print(f"Error: New examples TSV must contain: {required_columns}", file=sys.stderr)
            print(f"Found columns: {list(reader.fieldnames)}", file=sys.stderr)
            return 1

        for row in reader:
            number = int(row["number"])
            new_examples[number] = {
                "example_ko": row["example_ko"],
                "example_en": row["example_en"]
            }

    print(f"Loaded {len(new_examples)} updated examples")

    # Read Anki export and merge
    rows_updated = 0
    rows_unchanged = 0
    rows_total = 0

    with open(anki_export_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", encoding="utf-8", newline="") as outfile:

        # Skip header lines (first 3 lines with #)
        for _ in range(3):
            infile.readline()

        # Process data lines
        # Expected columns: number, korean, english, example_ko, example_en, etymology, notes, example_ko_audio, [tags]
        for line in infile:
            line = line.rstrip("\n")
            fields = line.split("\t")

            if len(fields) < 8:
                print(f"Warning: Skipping malformed line with {len(fields)} fields", file=sys.stderr)
                continue

            rows_total += 1

            # Parse number from first field
            try:
                number = int(fields[0])
            except ValueError:
                print(f"Warning: Could not parse number from: {fields[0]}", file=sys.stderr)
                outfile.write(line + "\n")
                rows_unchanged += 1
                continue

            # Update fields if we have new data for this number AND it's in range
            if number in new_examples and start <= number <= end:
                # Update column indices (0-based):
                # 0: number, 1: korean, 2: english, 3: example_ko, 4: example_en, 5: etymology, 6: notes, 7: example_ko_audio
                fields[3] = new_examples[number]["example_ko"]  # example_ko
                fields[4] = new_examples[number]["example_en"]  # example_en
                fields[7] = f"[sound:{args.audio_prefix}_{number:04d}.mp3]"  # example_ko_audio
                rows_updated += 1
            else:
                rows_unchanged += 1

            # Write updated line
            outfile.write("\t".join(fields) + "\n")

    print()
    print(f"Processing complete:")
    print(f"  Total rows:     {rows_total}")
    print(f"  Updated:        {rows_updated}{range_info}")
    print(f"  Unchanged:      {rows_unchanged}")
    print()
    print(f"Output written to: {output_file}")
    print()
    print("Next steps:")
    if rows_updated > 0:
        print(f"1. Copy audio files: cp output/audio-v2/{args.audio_prefix}_*.mp3 ~/.local/share/Anki2/\"User 1\"/collection.media/")
        print(f"2. Import {output_file} in Anki (File → Import)")
    else:
        print("No rows were updated. Check your range settings or input data.")

    return 0


if __name__ == '__main__':
    sys.exit(main())
