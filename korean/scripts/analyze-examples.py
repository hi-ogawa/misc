#!/usr/bin/env python3
"""
Analyze Korean example sentence statistics (word count and character count).
"""

import argparse
import csv
import statistics
import sys
from pathlib import Path
from collections import defaultdict


def main():
    """Analyze Korean example sentence statistics."""
    parser = argparse.ArgumentParser(
        description="Analyze Korean example sentence statistics (word count and character count)"
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input TSV file"
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
            char_count = len(example_ko.strip().replace(' ', '')) if example_ko.strip() else 0
            entries.append({
                'number': int(row.get('number', len(entries) + 1)),
                'word_count': word_count,
                'char_count': char_count
            })

    print(f"Loaded {len(entries)} entries")

    if len(entries) == 0:
        print("Error: No entries found", file=sys.stderr)
        return 1

    # Calculate overall stats - words
    word_counts = [e['word_count'] for e in entries]
    total_entries = len(entries)
    mean_words = statistics.mean(word_counts)
    median_words = statistics.median(word_counts)
    stdev_words = statistics.stdev(word_counts) if len(word_counts) > 1 else 0
    min_words = min(word_counts)
    max_words = max(word_counts)

    # Calculate overall percentiles - words
    sorted_word_counts = sorted(word_counts)
    n = len(sorted_word_counts)
    overall_words_p10 = sorted_word_counts[int(n * 0.10)]
    overall_words_p25 = sorted_word_counts[int(n * 0.25)]
    overall_words_p75 = sorted_word_counts[int(n * 0.75)]
    overall_words_p90 = sorted_word_counts[int(n * 0.90)]

    # Calculate overall stats - characters
    char_counts = [e['char_count'] for e in entries]
    mean_chars = statistics.mean(char_counts)
    median_chars = statistics.median(char_counts)
    stdev_chars = statistics.stdev(char_counts) if len(char_counts) > 1 else 0
    min_chars = min(char_counts)
    max_chars = max(char_counts)

    # Calculate overall percentiles - characters
    sorted_char_counts = sorted(char_counts)
    n = len(sorted_char_counts)
    overall_chars_p10 = sorted_char_counts[int(n * 0.10)]
    overall_chars_p25 = sorted_char_counts[int(n * 0.25)]
    overall_chars_p75 = sorted_char_counts[int(n * 0.75)]
    overall_chars_p90 = sorted_char_counts[int(n * 0.90)]

    # Calculate per-batch stats
    batches_words = defaultdict(list)
    batches_chars = defaultdict(list)
    for entry in entries:
        batch_num = (entry['number'] - 1) // args.batch_size + 1
        batches_words[batch_num].append(entry['word_count'])
        batches_chars[batch_num].append(entry['char_count'])

    batch_stats_words = []
    for batch_num in sorted(batches_words.keys()):
        batch_counts = batches_words[batch_num]
        sorted_counts = sorted(batch_counts)

        # Calculate percentiles
        n = len(sorted_counts)
        p10 = sorted_counts[int(n * 0.10)] if n >= 10 else sorted_counts[0]
        p25 = sorted_counts[int(n * 0.25)]
        p50 = statistics.median(batch_counts)
        p75 = sorted_counts[int(n * 0.75)]
        p90 = sorted_counts[int(n * 0.90)] if n >= 10 else sorted_counts[-1]

        batch_stats_words.append({
            'batch': batch_num,
            'entries': len(batch_counts),
            'mean': statistics.mean(batch_counts),
            'median': p50,
            'stdev': statistics.stdev(batch_counts) if len(batch_counts) > 1 else 0,
            'min': min(batch_counts),
            'max': max(batch_counts),
            'p10': p10,
            'p25': p25,
            'p75': p75,
            'p90': p90
        })

    batch_stats_chars = []
    for batch_num in sorted(batches_chars.keys()):
        batch_counts = batches_chars[batch_num]
        sorted_counts = sorted(batch_counts)

        # Calculate percentiles
        n = len(sorted_counts)
        p10 = sorted_counts[int(n * 0.10)] if n >= 10 else sorted_counts[0]
        p25 = sorted_counts[int(n * 0.25)]
        p50 = statistics.median(batch_counts)
        p75 = sorted_counts[int(n * 0.75)]
        p90 = sorted_counts[int(n * 0.90)] if n >= 10 else sorted_counts[-1]

        batch_stats_chars.append({
            'batch': batch_num,
            'entries': len(batch_counts),
            'mean': statistics.mean(batch_counts),
            'median': p50,
            'stdev': statistics.stdev(batch_counts) if len(batch_counts) > 1 else 0,
            'min': min(batch_counts),
            'max': max(batch_counts),
            'p10': p10,
            'p25': p25,
            'p75': p75,
            'p90': p90
        })

    mean_variance_words = statistics.mean([b['stdev'] for b in batch_stats_words])
    mean_variance_chars = statistics.mean([b['stdev'] for b in batch_stats_chars])
    outliers_words = [b for b in batch_stats_words if b['stdev'] > mean_variance_words * 1.5]
    outliers_chars = [b for b in batch_stats_chars if b['stdev'] > mean_variance_chars * 1.5]

    # Generate report content (used for both stdout and markdown)
    output = f"""\
# Example Sentence Statistics

Total entries: {total_entries}
Total batches: {len(batch_stats_words)}

## Word Count Analysis

Per-batch mean σ: {mean_variance_words:.2f}

| Batch   | Entries |  Mean | Median |    σ |  p25 |  p75 | Range |
|---------|---------|-------|--------|------|------|------|-------|
| Overall | {total_entries:7d} | {mean_words:5.2f} | {median_words:6.1f} | {stdev_words:4.2f} | {overall_words_p25:4d} | {overall_words_p75:4d} | {min_words}-{max_words:<3} |
"""
    for batch in batch_stats_words:
        output += f"| {batch['batch']:7d} | {batch['entries']:7d} | {batch['mean']:5.2f} | {batch['median']:6.1f} | {batch['stdev']:4.2f} | {batch['p25']:4d} | {batch['p75']:4d} | {batch['min']}-{batch['max']:<3} |\n"

    if outliers_words:
        output += f"\nHigh variance batches (>{mean_variance_words * 1.5:.2f}σ):\n"
        for batch in outliers_words:
            output += f"- Batch {batch['batch']}: σ={batch['stdev']:.2f} (range: {batch['min']}-{batch['max']} words)\n"

    output += f"""

## Character Count Analysis

Per-batch mean σ: {mean_variance_chars:.2f}

| Batch   | Entries |  Mean | Median |    σ |  p25 |  p75 | Range  |
|---------|---------|-------|--------|------|------|------|--------|
| Overall | {total_entries:7d} | {mean_chars:5.2f} | {median_chars:6.1f} | {stdev_chars:4.2f} | {overall_chars_p25:4d} | {overall_chars_p75:4d} | {min_chars}-{max_chars:<4} |
"""
    for batch in batch_stats_chars:
        output += f"| {batch['batch']:7d} | {batch['entries']:7d} | {batch['mean']:5.2f} | {batch['median']:6.1f} | {batch['stdev']:4.2f} | {batch['p25']:4d} | {batch['p75']:4d} | {batch['min']}-{batch['max']:<4} |\n"

    if outliers_chars:
        output += f"\nHigh variance batches (>{mean_variance_chars * 1.5:.2f}σ):\n"
        for batch in outliers_chars:
            output += f"- Batch {batch['batch']}: σ={batch['stdev']:.2f} (range: {batch['min']}-{batch['max']} chars)\n"

    # Print to stdout
    print()
    print("=" * 60)
    print(output, end='')
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
