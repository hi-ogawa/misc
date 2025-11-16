#!/usr/bin/env python3
"""
Analyze MP3 audio duration statistics using ffprobe.
"""

import argparse
import asyncio
import json
import os
from pathlib import Path
import statistics
import sys

# Global counters (safe in single-threaded async)
completed = 0
durations = []
errors = []


async def get_duration(mp3_path: Path, total: int, timeout: float) -> tuple[Path, float | None]:
    """
    Get duration of an MP3 file using ffprobe.

    Returns:
        (mp3_path, duration_in_seconds or None)
    """
    global completed, durations, errors

    try:
        # Run ffprobe to get duration
        async def run_ffprobe():
            process = await asyncio.create_subprocess_exec(
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'json',
                str(mp3_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            return process.returncode, stdout, stderr

        returncode, stdout, stderr = await asyncio.wait_for(run_ffprobe(), timeout=timeout)

        completed += 1

        if returncode != 0:
            error_msg = stderr.decode().strip() or "ffprobe returned non-zero exit code"
            errors.append((mp3_path, error_msg))
            print(f"  [{completed}/{total}] ✗ {mp3_path.name}: {error_msg}")
            return (mp3_path, None)

        # Parse the JSON output
        try:
            data = json.loads(stdout.decode())
            duration = float(data['format']['duration'])
            durations.append(duration)
            print(f"  [{completed}/{total}] ✓ {mp3_path.name}: {duration:.2f}s")
            return (mp3_path, duration)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            errors.append((mp3_path, f"Parse error: {e}"))
            print(f"  [{completed}/{total}] ✗ {mp3_path.name}: Parse error: {e}")
            return (mp3_path, None)

    except asyncio.TimeoutError:
        completed += 1
        errors.append((mp3_path, f"Timeout after {timeout}s"))
        print(f"  [{completed}/{total}] ✗ {mp3_path.name}: Timeout after {timeout}s")
        return (mp3_path, None)
    except Exception as e:
        completed += 1
        errors.append((mp3_path, f"Unexpected error: {e}"))
        print(f"  [{completed}/{total}] ✗ {mp3_path.name}: Unexpected error: {e}")
        return (mp3_path, None)


async def analyze_all(mp3_files, concurrency, total, timeout):
    """Analyze MP3 files in chunks."""
    results = []

    # Process in chunks
    for i in range(0, len(mp3_files), concurrency):
        batch = mp3_files[i:i+concurrency]

        # Run this batch concurrently
        tasks = [
            get_duration(mp3_path, total, timeout)
            for mp3_path in batch
        ]

        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)

    return results


def main():
    global completed, durations, errors

    parser = argparse.ArgumentParser(description="Analyze MP3 audio duration statistics")
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output directory containing MP3 files"
    )
    parser.add_argument(
        "--start",
        type=int,
        default=None,
        help="Start from this file number (inclusive, e.g., 1 for 0001.mp3)"
    )
    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="End at this file number (inclusive, e.g., 100 for 0100.mp3)"
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=os.cpu_count() or 4,
        help=f"Number of concurrent analysis tasks (default: {os.cpu_count() or 4}, based on CPU cores)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Timeout in seconds for each analysis (default: 5)"
    )

    args = parser.parse_args()

    # Find all MP3 files in the output directory
    output_dir = Path(args.output)
    if not output_dir.exists():
        print(f"Error: Output directory not found: {output_dir}", file=sys.stderr)
        return 1

    mp3_files = sorted(output_dir.glob('*.mp3'))

    # Filter by range if specified
    if args.start is not None or args.end is not None:
        start = args.start if args.start is not None else 1
        end = args.end if args.end is not None else 9999

        mp3_files = [
            f for f in mp3_files
            if f.stem.isdigit() and start <= int(f.stem) <= end
        ]

    if not mp3_files:
        print(f"No MP3 files found in {output_dir}")
        if args.start or args.end:
            print(f"Range: {args.start or 1} to {args.end or 'end'}")
        return 0

    total = len(mp3_files)
    range_info = ""
    if args.start or args.end:
        range_info = f" (range: {args.start or 1}-{args.end or 'end'})"

    print(f"Found {len(mp3_files)} MP3 file(s) in {output_dir}{range_info}")
    print(f"Concurrency: {args.concurrency}")
    print(f"Analyzing...\n")

    # Reset global state
    completed = 0
    durations = []
    errors = []
    interrupted = False

    try:
        results = asyncio.run(analyze_all(mp3_files, args.concurrency, total, args.timeout))
    except KeyboardInterrupt:
        interrupted = True
        print("\n\nInterrupted by user (Ctrl-C)")
        results = []

    # Print statistics
    print()
    print("=" * 60)
    print("AUDIO DURATION STATISTICS")
    print("=" * 60)

    if durations:
        print(f"Files analyzed:  {len(durations)}/{total}")
        print(f"Total duration:  {sum(durations):.2f}s ({sum(durations)/60:.2f} minutes)")
        print(f"Average:         {statistics.mean(durations):.2f}s")
        print(f"Median:          {statistics.median(durations):.2f}s")
        print(f"Min:             {min(durations):.2f}s")
        print(f"Max:             {max(durations):.2f}s")

        if len(durations) > 1:
            print(f"Std Dev:         {statistics.stdev(durations):.2f}s")

        # Percentiles
        if len(durations) >= 10:
            sorted_durations = sorted(durations)
            p10 = sorted_durations[int(len(sorted_durations) * 0.10)]
            p25 = sorted_durations[int(len(sorted_durations) * 0.25)]
            p75 = sorted_durations[int(len(sorted_durations) * 0.75)]
            p90 = sorted_durations[int(len(sorted_durations) * 0.90)]

            print()
            print("Percentiles:")
            print(f"  10th: {p10:.2f}s")
            print(f"  25th: {p25:.2f}s")
            print(f"  75th: {p75:.2f}s")
            print(f"  90th: {p90:.2f}s")

        # Find outliers (> 10s or < 1s)
        file_durations = [(path, dur) for path, dur in results if dur is not None]
        long_files = [(path, dur) for path, dur in file_durations if dur > 10]
        short_files = [(path, dur) for path, dur in file_durations if dur < 1]

        if long_files:
            print()
            print(f"Long files (>10s): {len(long_files)}")
            for path, dur in sorted(long_files, key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {path.name}: {dur:.2f}s")
            if len(long_files) > 10:
                print(f"  ... and {len(long_files) - 10} more")

        if short_files:
            print()
            print(f"Short files (<1s): {len(short_files)}")
            for path, dur in sorted(short_files, key=lambda x: x[1])[:10]:
                print(f"  {path.name}: {dur:.2f}s")
            if len(short_files) > 10:
                print(f"  ... and {len(short_files) - 10} more")
    else:
        print("No valid durations collected")

    if errors:
        print()
        print("=" * 60)
        print(f"Errors: {len(errors)}")
        for path, error in errors[:10]:
            print(f"  {path.name}: {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")

    if interrupted:
        print("\nAnalysis incomplete (interrupted)")
        return 130  # Standard exit code for SIGINT

    return 0


if __name__ == '__main__':
    sys.exit(main())
