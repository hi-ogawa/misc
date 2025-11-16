#!/usr/bin/env python3
"""
Generate Anki update TSV with updated examples and audio references.
"""

import argparse
import csv
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Generate Anki update TSV for importing updated examples"
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input TSV file with updated examples (e.g., output/examples-v2-all.tsv)"
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output TSV file for Anki import (e.g., output/anki-update-v2.tsv)"
    )
    parser.add_argument(
        "--audio-prefix",
        type=str,
        default="koreantopik1_v2",
        help="Audio file prefix (default: koreantopik1_v2)"
    )

    args = parser.parse_args()

    # Read input TSV
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        return 1

    output_file = Path(args.output)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"Reading from: {input_file}")
    print(f"Writing to:   {output_file}")
    print(f"Audio prefix: {args.audio_prefix}")
    print()

    # Read input and generate output
    rows_written = 0
    with open(input_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", encoding="utf-8", newline="") as outfile:

        reader = csv.DictReader(infile, delimiter="\t")

        # Check required columns
        required_columns = ["number", "example_ko", "example_en"]
        if not all(col in reader.fieldnames for col in required_columns):
            print(f"Error: Input TSV must contain columns: {required_columns}", file=sys.stderr)
            print(f"Found columns: {list(reader.fieldnames)}", file=sys.stderr)
            return 1

        # Write output with 4 columns
        writer = csv.writer(outfile, delimiter="\t")
        writer.writerow(["number", "example_ko", "example_en", "example_ko_audio"])

        for row in reader:
            number = int(row["number"])
            example_ko = row["example_ko"]
            example_en = row["example_en"]
            audio_ref = f"[sound:{args.audio_prefix}_{number:04d}.mp3]"

            writer.writerow([number, example_ko, example_en, audio_ref])
            rows_written += 1

    print(f"Successfully wrote {rows_written} rows to {output_file}")
    print()
    print("Next steps:")
    print(f"1. Copy audio files: cp output/audio-v2/{args.audio_prefix}_*.mp3 ~/.local/share/Anki2/\"User 1\"/collection.media/")
    print(f"2. Import {output_file} in Anki with 'number' as the matching field")

    return 0


if __name__ == '__main__':
    sys.exit(main())
