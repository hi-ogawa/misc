#!/usr/bin/env python3
"""
Split a TSV file into multiple batch files for parallel processing.

Usage:
    python scripts/split-batches.py \
        --input input/koreantopik1.tsv \
        --output-dir input \
        --prefix koreantopik1-batch- \
        --batch-size 100
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Split a TSV file into multiple batch files for parallel processing"
    )
    parser.add_argument("--input", required=True, help="Input TSV file path")
    parser.add_argument("--output-dir", required=True, help="Output directory for batch files")
    parser.add_argument("--prefix", required=True, help="Prefix for batch filenames (e.g., 'koreantopik1-batch-')")
    parser.add_argument("--batch-size", type=int, default=100, help="Number of entries per batch (default: 100)")

    args = parser.parse_args()

    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1

    # Create output directory if needed
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Read input file
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) < 2:
        print(f"Error: Input file has no data rows (only {len(lines)} lines)", file=sys.stderr)
        return 1

    # Extract header and data
    header = lines[0]
    data_lines = lines[1:]

    total_entries = len(data_lines)
    num_batches = (total_entries + args.batch_size - 1) // args.batch_size  # Ceiling division

    print(f"Input file: {args.input}")
    print(f"Total entries: {total_entries}")
    print(f"Batch size: {args.batch_size}")
    print(f"Number of batches: {num_batches}")
    print()

    # Split into batches
    for batch_num in range(1, num_batches + 1):
        start_idx = (batch_num - 1) * args.batch_size
        end_idx = min(start_idx + args.batch_size, total_entries)
        batch_lines = data_lines[start_idx:end_idx]

        # Create output file
        output_file = output_path / f"{args.prefix}{batch_num}.tsv"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(header)
            f.writelines(batch_lines)

        entries_in_batch = len(batch_lines)
        print(f"Created: {output_file} ({entries_in_batch} entries, rows {start_idx + 1}-{end_idx})")

    print()
    print(f"✓ Successfully created {num_batches} batch files")

    return 0


if __name__ == "__main__":
    sys.exit(main())
