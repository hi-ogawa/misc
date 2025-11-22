#!/usr/bin/env python3
"""
Merge new example sentences into an existing Anki import/export TSV file.

Replaces example_ko and example_en columns while preserving all other fields.
Handles both raw TSV and Anki export format (with #metadata lines).

Usage:
  python scripts/merge-examples.py \
    --base output/koreantopik1/koreantopik1_v2_backup.txt \
    --examples output/koreantopik1/koreantopik1_anki_import_v3.tsv \
    --output output/koreantopik1/koreantopik1_anki_import_v3_merged.tsv
"""

import argparse
import sys
from pathlib import Path

# Column indices for Anki format:
# 0:number, 1:korean, 2:english, 3:example_ko, 4:example_en, 5:etymology, 6:notes, 7:korean_audio, 8:example_ko_audio
COL_NUMBER = 0
COL_EXAMPLE_KO = 3
COL_EXAMPLE_EN = 4


def main():
    parser = argparse.ArgumentParser(
        description="Merge new examples into existing Anki import file"
    )
    parser.add_argument("--base", required=True, help="Base Anki import/export TSV file")
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

    # Read new examples (keyed by number)
    print(f"Reading examples file: {examples_file}")
    new_examples = {}
    with open(examples_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 5:
                continue
            new_examples[parts[COL_NUMBER]] = {
                "example_ko": parts[COL_EXAMPLE_KO],
                "example_en": parts[COL_EXAMPLE_EN],
            }

    # Process base file, preserving metadata and structure
    print(f"Reading base file: {base_file}")
    output_lines = []
    merged_count = 0

    with open(base_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")

            # Preserve metadata/comment lines
            if line.startswith("#"):
                output_lines.append(line)
                continue

            parts = line.split("\t")
            if len(parts) < 5:
                output_lines.append(line)
                continue

            num = parts[COL_NUMBER]
            if num in new_examples:
                parts[COL_EXAMPLE_KO] = new_examples[num]["example_ko"]
                parts[COL_EXAMPLE_EN] = new_examples[num]["example_en"]
                merged_count += 1

            output_lines.append("\t".join(parts))

    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    print(f"Writing output: {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")

    print(f"Done! Merged {merged_count} examples.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
