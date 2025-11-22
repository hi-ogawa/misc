#!/usr/bin/env python3
"""
Filter Anki import TSV by number range or specific numbers.
Optionally outputs a list of audio files to copy.

Usage:
  # Filter by range
  python scripts/filter-anki-import.py \
    --input output/koreantopik1/koreantopik1_anki_import_v3.tsv \
    --output output/koreantopik1/koreantopik1_anki_import_v3_partial.tsv \
    --start 500

  # Filter by range with end
  python scripts/filter-anki-import.py \
    --input output/koreantopik1/koreantopik1_anki_import_v3.tsv \
    --output output/koreantopik1/koreantopik1_anki_import_v3_partial.tsv \
    --start 500 --end 1000

  # Filter by specific numbers (supports ranges with -)
  python scripts/filter-anki-import.py \
    --input output/koreantopik1/koreantopik1_anki_import_v3.tsv \
    --output output/koreantopik1/koreantopik1_anki_import_v3_partial.tsv \
    --numbers "1,5,10,100-200,500"

  # Also output audio file list for copying
  python scripts/filter-anki-import.py \
    --input output/koreantopik1/koreantopik1_anki_import_v3.tsv \
    --output output/koreantopik1/koreantopik1_anki_import_v3_partial.tsv \
    --start 500 \
    --audio output/koreantopik1/koreantopik1_anki_import_v3_partial_audio.txt
"""

import argparse
import re
import sys


def parse_numbers(numbers_str: str) -> set[int]:
    """Parse number specification like '1,5,10,100-200,500' into a set of integers."""
    result = set()
    for part in numbers_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            result.update(range(int(start), int(end) + 1))
        else:
            result.add(int(part))
    return result


def get_number_from_row(row: str) -> int | None:
    """Extract the number (first column) from a TSV row."""
    if row.startswith("#"):
        return None
    parts = row.split("\t")
    if not parts:
        return None
    try:
        # Handle both plain numbers (1, 2, 3) and prefixed (koreantopik2_1)
        num_str = parts[0]
        if "_" in num_str:
            num_str = num_str.split("_")[-1]
        return int(num_str)
    except ValueError:
        return None


def main():
    parser = argparse.ArgumentParser(description="Filter Anki import TSV by number")
    parser.add_argument("--input", required=True, help="Input TSV file")
    parser.add_argument("--output", required=True, help="Output TSV file")
    parser.add_argument("--start", type=int, help="Start number (inclusive)")
    parser.add_argument("--end", type=int, help="End number (inclusive)")
    parser.add_argument(
        "--numbers", help="Specific numbers to include (e.g., '1,5,10,100-200')"
    )
    parser.add_argument(
        "--audio", help="Output file for audio file list (one per line)"
    )
    args = parser.parse_args()

    # Validate arguments
    if args.numbers and (args.start or args.end):
        print("Error: Cannot use --numbers with --start/--end", file=sys.stderr)
        sys.exit(1)
    if not args.numbers and not args.start and not args.end:
        print(
            "Error: Must specify --start/--end or --numbers",
            file=sys.stderr,
        )
        sys.exit(1)

    # Build filter set
    if args.numbers:
        include_numbers = parse_numbers(args.numbers)
    else:
        include_numbers = None  # Use range instead

    # Process file
    with open(args.input, "r", encoding="utf-8") as f:
        lines = f.readlines()

    output_lines = []
    included_count = 0

    for line in lines:
        line = line.rstrip("\n")

        # Keep comment/header lines
        if line.startswith("#"):
            output_lines.append(line)
            continue

        num = get_number_from_row(line)
        if num is None:
            continue

        # Check if should include
        include = False
        if include_numbers is not None:
            include = num in include_numbers
        else:
            if args.start and args.end:
                include = args.start <= num <= args.end
            elif args.start:
                include = num >= args.start
            elif args.end:
                include = num <= args.end

        if include:
            output_lines.append(line)
            included_count += 1

    # Write output
    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")

    print(f"Filtered {included_count} rows -> {args.output}")

    # Extract and write audio files if requested
    if args.audio:
        audio_files = []
        sound_pattern = re.compile(r"\[sound:([^\]]+)\]")
        for line in output_lines:
            if line.startswith("#"):
                continue
            matches = sound_pattern.findall(line)
            audio_files.extend(matches)

        with open(args.audio, "w", encoding="utf-8") as f:
            f.write("\n".join(audio_files) + "\n")

        print(f"Audio files: {len(audio_files)} -> {args.audio}")


if __name__ == "__main__":
    main()
