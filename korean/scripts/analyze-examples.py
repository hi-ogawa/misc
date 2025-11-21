#!/usr/bin/env python3
"""
Analyze Korean example sentence word count statistics.
"""

import argparse
import csv
import statistics
import sys
from pathlib import Path
from collections import defaultdict


def main():
    """Analyze Korean example sentence word counts."""
    parser = argparse.ArgumentParser(
        description="Analyze Korean example sentence word count statistics"
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input TSV file"
    )
    parser.add_argument(
        "--name",
        type=str,
        default=None,
        help="Dataset name (default: derived from filename)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Batch size for per-batch analysis (default: 100)"
    )

    args = parser.parse_args()

    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        return 1

    # Derive dataset name
    dataset_name = args.name
    if not dataset_name:
        filename = input_file.stem
        if 'topik1' in filename.lower():
            dataset_name = "TOPIK 1"
        elif 'topik2' in filename.lower():
            dataset_name = "TOPIK 2"
        else:
            dataset_name = filename.replace('_', ' ').title()

    print(f"Analyzing {input_file}")
    print(f"Batch size: {args.batch_size}")

    # Load data
    entries = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        if 'example_ko' not in reader.fieldnames:
            print(f"Error: Missing 'example_ko' column", file=sys.stderr)
            return 1

        for row in reader:
            example_ko = row['example_ko']
            word_count = len(example_ko.strip().split()) if example_ko.strip() else 0
            entries.append({
                'number': int(row.get('number', len(entries) + 1)),
                'word_count': word_count
            })

    print(f"Loaded {len(entries)} entries")

    if len(entries) == 0:
        print("Error: No entries found", file=sys.stderr)
        return 1

    # Calculate overall stats
    word_counts = [e['word_count'] for e in entries]
    total_entries = len(entries)
    mean_words = statistics.mean(word_counts)
    median_words = statistics.median(word_counts)
    stdev_words = statistics.stdev(word_counts) if len(word_counts) > 1 else 0
    min_words = min(word_counts)
    max_words = max(word_counts)

    # Calculate per-batch stats
    batches = defaultdict(list)
    for entry in entries:
        batch_num = (entry['number'] - 1) // args.batch_size + 1
        batches[batch_num].append(entry['word_count'])

    batch_stats = []
    for batch_num in sorted(batches.keys()):
        batch_counts = batches[batch_num]
        batch_stats.append({
            'batch': batch_num,
            'entries': len(batch_counts),
            'mean': statistics.mean(batch_counts),
            'median': statistics.median(batch_counts),
            'stdev': statistics.stdev(batch_counts) if len(batch_counts) > 1 else 0,
            'min': min(batch_counts),
            'max': max(batch_counts)
        })

    mean_variance = statistics.mean([b['stdev'] for b in batch_stats])
    outliers = [b for b in batch_stats if b['stdev'] > mean_variance * 1.5]

    # Generate report content (used for both stdout and markdown)
    output = f"""\
# Example Sentence Statistics: {dataset_name}

Total entries: {total_entries}
Total batches: {len(batch_stats)}

## Overall Statistics

Mean: {mean_words:.2f}
Median: {median_words:.1f}
Std deviation: {stdev_words:.2f}
Range: {min_words}-{max_words} words

Per-batch mean σ: {mean_variance:.2f}

"""

    if outliers:
        output += f"High variance batches (>{mean_variance * 1.5:.2f}σ):\n\n"
        for batch in outliers:
            output += f"- Batch {batch['batch']}: σ={batch['stdev']:.2f} (range: {batch['min']}-{batch['max']} words)\n"
        output += "\n"

    output += """\
## Per-Batch Analysis

| Batch | Entries |  Mean |    σ | Range   |
|-------|---------|-------|------|---------|
"""
    for batch in batch_stats:
        output += f"| {batch['batch']:5d} | {batch['entries']:7d} | {batch['mean']:5.2f} | {batch['stdev']:4.2f} | {batch['min']}-{batch['max']:<5} |\n"

    # Print to stdout
    print()
    print("=" * 60)
    print(output, end='')
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
