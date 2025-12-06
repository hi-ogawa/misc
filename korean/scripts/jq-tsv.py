#!/usr/bin/env python3
"""
TSV manipulation using jq syntax.

Converts TSV to JSON, pipes through jq, converts back to TSV.

Usage:
    python scripts/jq-tsv.py 'select(.tier == "1")' input.tsv > output.tsv
    python scripts/jq-tsv.py '{number, korean}' input.tsv > output.tsv
    python scripts/jq-tsv.py '.' file1.tsv file2.tsv > combined.tsv
    python scripts/jq-tsv.py --json '.' input.tsv  # Output as JSON
    python scripts/jq-tsv.py -s 'group_by(.tier) | map({tier: .[0].tier, count: length})' input.tsv  # Slurp mode
"""

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="TSV manipulation using jq syntax",
        epilog="Example: python scripts/jq-tsv.py 'select(.tier == \"1\")' input.tsv"
    )
    parser.add_argument("filter", help="jq filter expression")
    parser.add_argument("files", nargs="+", help="Input TSV file(s)")
    parser.add_argument("--no-header", action="store_true", help="Input has no header row")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of TSV")
    parser.add_argument("-s", "--slurp", action="store_true", help="Read all rows into array (for aggregations)")

    args = parser.parse_args()

    # Validate files exist
    for f in args.files:
        if not Path(f).exists():
            print(f"Error: File not found: {f}", file=sys.stderr)
            return 1

    # Read all TSV files into list of dicts
    rows = []
    header = None

    for filepath in args.files:
        with open(filepath, "r", encoding="utf-8") as f:
            if args.no_header:
                # Generate column names: col0, col1, col2, ...
                reader = csv.reader(f, delimiter="\t")
                for row in reader:
                    if header is None:
                        header = [f"col{i}" for i in range(len(row))]
                    rows.append(dict(zip(header, row)))
            else:
                reader = csv.DictReader(f, delimiter="\t")
                for row in reader:
                    if header is None:
                        header = reader.fieldnames
                    rows.append(row)

    if not rows:
        return 0

    # Convert to JSON and pipe through jq
    json_input = json.dumps(rows, ensure_ascii=False)

    # Build jq filter: per-row vs slurp mode
    if args.slurp:
        jq_filter = args.filter
    else:
        jq_filter = f".[] | {args.filter}"

    try:
        result = subprocess.run(
            ["jq", "-c", jq_filter],
            input=json_input,
            capture_output=True,
            text=True,
            check=True
        )
    except FileNotFoundError:
        print("Error: jq not found. Install with: sudo pacman -S jq", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as e:
        print(f"Error: jq failed: {e.stderr}", file=sys.stderr)
        return 1

    # Slurp mode
    if args.slurp:
        output = json.loads(result.stdout.strip())
        if args.json:
            # Output as JSON
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            # Try to convert back to TSV if it's an array of objects
            if isinstance(output, list) and output and isinstance(output[0], dict):
                # Array of objects -> TSV
                writer = csv.DictWriter(
                    sys.stdout,
                    fieldnames=output[0].keys(),
                    delimiter="\t",
                    lineterminator="\n"
                )
                writer.writeheader()
                writer.writerows(output)
            else:
                # Aggregation result (not TSV-convertible)
                print("Error: Result is not TSV-convertible (not an array of objects). Use --json flag for JSON output.", file=sys.stderr)
                return 1
        return 0

    # Parse jq output (one JSON object per line)
    output_rows = []
    output_header = None

    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        try:
            obj = json.loads(line)
            if obj is None:
                continue
            if output_header is None:
                output_header = list(obj.keys())
            output_rows.append(obj)
        except json.JSONDecodeError:
            continue

    if not output_rows:
        return 0

    if args.json:
        # Write JSON to stdout
        print(json.dumps(output_rows, ensure_ascii=False, indent=2))
    else:
        # Write TSV to stdout
        writer = csv.DictWriter(
            sys.stdout,
            fieldnames=output_header,
            delimiter="\t",
            lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(output_rows)

    return 0


if __name__ == "__main__":
    sys.exit(main())
