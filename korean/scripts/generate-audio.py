#!/usr/bin/env python3
"""
Generate Korean audio files from example sentences using Edge TTS.
"""

import argparse
import csv
import subprocess
import sys
from pathlib import Path


def generate_audio(number: int, text: str, voice: str, output_dir: Path, skip_existing: bool = True) -> bool:
    """Generate audio file for a single text entry using edge-tts CLI."""
    output_file = output_dir / f"{number:04d}.mp3"

    if skip_existing and output_file.exists():
        print(f"  Skipping {number:04d} (already exists)")
        return True

    try:
        result = subprocess.run(
            ["edge-tts", "--voice", voice, "--text", text, "--write-media", str(output_file)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"  Generated {number:04d}: {text}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ERROR {number:04d}: {e.stderr}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  ERROR {number:04d}: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate Korean audio files from TSV")
    parser.add_argument(
        "--input",
        type=str,
        default="output/examples-all.tsv",
        help="Input TSV file (default: output/examples-all.tsv)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/audio",
        help="Output directory (default: output/audio)"
    )
    parser.add_argument(
        "--voice",
        type=str,
        default="ko-KR-SunHiNeural",
        choices=["ko-KR-SunHiNeural", "ko-KR-InJoonNeural"],
        help="Voice to use (default: ko-KR-SunHiNeural)"
    )
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Start from this entry number (inclusive, default: 1)"
    )
    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="End at this entry number (inclusive, default: last entry)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate existing files"
    )

    args = parser.parse_args()

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read TSV file
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    # Read TSV and collect rows
    rows = []
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        required_columns = ["number", "example_ko"]

        # Check columns
        if not all(col in reader.fieldnames for col in required_columns):
            print(f"Error: TSV must contain columns: {required_columns}", file=sys.stderr)
            print(f"Found columns: {list(reader.fieldnames)}", file=sys.stderr)
            sys.exit(1)

        for row in reader:
            rows.append(row)

    # Determine end if not specified
    if args.end is None:
        args.end = max(int(row["number"]) for row in rows)

    # Filter by range
    filtered_rows = [
        row for row in rows
        if args.start <= int(row["number"]) <= args.end
    ]

    total = len(filtered_rows)
    print(f"Generating audio for entries {args.start}-{args.end} ({total} total)")
    print(f"Voice: {args.voice}")
    print(f"Output: {output_dir}/")
    print()

    # Generate audio files
    success_count = 0
    for row in filtered_rows:
        number = int(row["number"])
        text = str(row["example_ko"])

        success = generate_audio(
            number, text, args.voice, output_dir, skip_existing=not args.force
        )
        if success:
            success_count += 1

    print()
    print(f"Completed: {success_count}/{total} files generated successfully")

    if success_count < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
