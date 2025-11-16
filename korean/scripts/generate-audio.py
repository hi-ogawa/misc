#!/usr/bin/env python3
"""
Generate Korean audio files from example sentences using Edge TTS.
"""

import argparse
import asyncio
import csv
import sys
import time
from pathlib import Path

# Global counters (safe in single-threaded async)
completed = 0
success_count = 0


async def generate_audio(number: int, text: str, voice: str, output_dir: Path, skip_existing: bool, total: int, timeout: float, concurrency: int, failed_log_path: Path) -> tuple[int, bool, str]:
    """Generate audio file for a single text entry using edge-tts CLI.

    Returns:
        Tuple of (number, success, message)
    """
    global completed, success_count

    output_file = output_dir / f"{number:04d}.mp3"

    if skip_existing and output_file.exists():
        completed += 1
        message = f"Skipped {number:04d} (already exists)"
        print(f"  [{completed}/{total}] {message}")
        return (number, True, message)

    try:
        start_time = time.perf_counter()

        # Wrap subprocess execution with timeout
        async def run_tts():
            process = await asyncio.create_subprocess_exec(
                "edge-tts", "--voice", voice, "--text", text, "--write-media", str(output_file),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            return process.returncode, stdout, stderr

        returncode, stdout, stderr = await asyncio.wait_for(run_tts(), timeout=timeout)

        duration = time.perf_counter() - start_time
        completed += 1

        if returncode == 0:
            success_count += 1
            message = f"Generated {number:04d} ({duration:.2f}s): {text}"
            print(f"  [{completed}/{total}] {message}")
            return (number, True, message)
        else:
            error_msg = stderr.decode().strip()
            with open(failed_log_path, "a", encoding="utf-8") as f:
                f.write(f"{number}\tProcess error: {error_msg}\n")
            message = f"ERROR {number:04d} ({duration:.2f}s): {error_msg}"
            print(f"  [{completed}/{total}] {message}")
            return (number, False, message)

    except asyncio.TimeoutError:
        completed += 1
        duration = time.perf_counter() - start_time
        with open(failed_log_path, "a", encoding="utf-8") as f:
            f.write(f"{number}\tTimeout after {timeout}s\n")
        message = f"ERROR {number:04d} ({duration:.2f}s): Timeout after {timeout}s"
        print(f"  [{completed}/{total}] {message}")
        return (number, False, message)

    except Exception as e:
        completed += 1
        duration = time.perf_counter() - start_time
        with open(failed_log_path, "a", encoding="utf-8") as f:
            f.write(f"{number}\t{str(e)}\n")
        message = f"ERROR {number:04d} ({duration:.2f}s): {e}"
        print(f"  [{completed}/{total}] {message}")
        return (number, False, message)


async def generate_all(filtered_rows, args, output_dir, total, failed_log_path):
    """Generate audio files in chunks."""
    concurrency = args.concurrency

    # Process in chunks
    for i in range(0, len(filtered_rows), concurrency):
        batch = filtered_rows[i:i+concurrency]

        # Run this batch concurrently
        tasks = [
            generate_audio(
                int(row["number"]),
                str(row["example_ko"]),
                args.voice,
                output_dir,
                not args.force,
                total,
                args.timeout,
                concurrency,
                failed_log_path
            )
            for row in batch
        ]

        await asyncio.gather(*tasks)


def main():
    global completed, success_count

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
    parser.add_argument(
        "--concurrency",
        type=int,
        default=1,
        help="Number of concurrent tasks (default: 1)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Timeout in seconds for each generation (default: 10)"
    )
    parser.add_argument(
        "--failed-log",
        type=str,
        default=None,
        help="Log file for failed generations (default: <output>/failed.txt)"
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
    print(f"Concurrency: {args.concurrency}")
    print(f"Output: {output_dir}/")
    print()

    # Reset global counters
    completed = 0
    success_count = 0
    interrupted = False

    # Determine failed log path
    failed_log_path = Path(args.failed_log) if args.failed_log else output_dir / "failed.txt"

    try:
        asyncio.run(generate_all(filtered_rows, args, output_dir, total, failed_log_path))

    except KeyboardInterrupt:
        interrupted = True
        print("\n\nInterrupted by user (Ctrl-C)")

    print()
    if interrupted:
        print(f"Partially completed: {success_count}/{total} files generated before interruption")
        print(f"To resume, run the same command again (existing files will be skipped)")
    else:
        print(f"Completed: {success_count}/{total} files generated successfully")

    # Report if there were failures
    if failed_log_path.exists():
        print(f"Failed entries logged to: {failed_log_path}")

    if interrupted:
        sys.exit(130)  # Standard exit code for SIGINT

    if success_count < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
