#!/usr/bin/env python3
"""
Generate Korean audio files from TSV using Edge TTS.
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


async def generate_audio(file_id: str, text: str, voice: str, output_dir: Path, skip_existing: bool, total: int, timeout: float, failed_log_path: Path, prefix: str = "") -> tuple[str, bool, str]:
    """Generate audio file for a single text entry using edge-tts CLI.

    Args:
        file_id: Identifier for the output filename
        prefix: Optional filename prefix (e.g., "vocab_" or "example_")

    Returns:
        Tuple of (file_id, success, message)
    """
    global completed, success_count

    filename = f"{prefix}{file_id}.mp3"
    output_file = output_dir / filename

    if skip_existing and output_file.exists():
        completed += 1
        message = f"Skipped {file_id} (exists)"
        print(f"  [{completed}/{total}] {message}")
        return (file_id, True, message)

    try:
        start_time = time.perf_counter()

        # Wrap subprocess execution with timeout
        async def run_tts():
            # Use --text=value format to avoid issues with text starting with hyphens
            process = await asyncio.create_subprocess_exec(
                "edge-tts", f"--voice={voice}", f"--text={text}", f"--write-media={str(output_file)}",
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
            message = f"Generated {file_id} ({duration:.2f}s): {text}"
            print(f"  [{completed}/{total}] {message}")
            return (file_id, True, message)
        else:
            error_msg = stderr.decode().strip()
            with open(failed_log_path, "a", encoding="utf-8") as f:
                f.write(f"{file_id}\tProcess error: {error_msg}\n")
            message = f"ERROR {file_id} ({duration:.2f}s): {error_msg}"
            print(f"  [{completed}/{total}] {message}")
            return (file_id, False, message)

    except asyncio.TimeoutError:
        completed += 1
        duration = time.perf_counter() - start_time
        with open(failed_log_path, "a", encoding="utf-8") as f:
            f.write(f"{file_id}\tTimeout after {timeout}s\n")
        message = f"ERROR {file_id} ({duration:.2f}s): Timeout after {timeout}s"
        print(f"  [{completed}/{total}] {message}")
        return (file_id, False, message)

    except Exception as e:
        completed += 1
        duration = time.perf_counter() - start_time
        with open(failed_log_path, "a", encoding="utf-8") as f:
            f.write(f"{file_id}\t{str(e)}\n")
        message = f"ERROR {file_id} ({duration:.2f}s): {e}"
        print(f"  [{completed}/{total}] {message}")
        return (file_id, False, message)


async def generate_all(rows_with_ids: list[tuple[str, dict]], args, output_dir: Path, total: int, failed_log_path: Path, field_name: str, prefix: str):
    """Generate audio files in batches with concurrency."""
    concurrency = args.concurrency

    for i in range(0, len(rows_with_ids), concurrency):
        batch = rows_with_ids[i:i+concurrency]

        tasks = [
            generate_audio(
                file_id,
                str(row[field_name]),
                args.voice,
                output_dir,
                not args.force,
                total,
                args.timeout,
                failed_log_path,
                prefix
            )
            for file_id, row in batch
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
        "--field",
        type=str,
        default="example_ko",
        help="TSV column to generate audio from (default: example_ko)"
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="",
        help="Filename prefix (e.g., 'koreantopik1_korean_')"
    )
    parser.add_argument(
        "--id-field",
        type=str,
        default=None,
        help="TSV column for filename ID (default: row number, zero-padded)"
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
        help="Start from this row number (1-based, inclusive, default: 1)"
    )
    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="End at this row number (inclusive, default: last row)"
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
    fieldnames = None
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = reader.fieldnames
        # Check field column exists
        if args.field not in fieldnames:
            print(f"Error: TSV must contain column: {args.field}", file=sys.stderr)
            print(f"Found columns: {list(fieldnames)}", file=sys.stderr)
            sys.exit(1)

        for row in reader:
            rows.append(row)

    # Check id-field column exists if specified
    if args.id_field and args.id_field not in fieldnames:
        print(f"Error: TSV must contain column: {args.id_field}", file=sys.stderr)
        print(f"Found columns: {list(fieldnames)}", file=sys.stderr)
        sys.exit(1)

    # Apply --start/--end range filter
    end = args.end if args.end is not None else len(rows)
    rows = [(idx, row) for idx, row in enumerate(rows, start=1) if args.start <= idx <= end]

    # Build list of (file_id, row) tuples
    # Use id-field value if specified, otherwise use zero-padded row number
    total = len(rows)
    pad_width = len(str(end))  # Pad based on end value for consistent filenames

    if args.id_field:
        rows_with_ids = [
            (row[args.id_field], row)
            for idx, row in rows
        ]
    else:
        rows_with_ids = [
            (str(idx).zfill(pad_width), row)
            for idx, row in rows
        ]

    print(f"Generating audio for rows {args.start}-{end} ({total} entries)")
    print(f"  Field: {args.field}")
    print(f"  ID: {args.id_field or f'row number (zero-padded to {pad_width} digits)'}")
    print(f"  Voice: {args.voice}")
    print(f"  Prefix: '{args.prefix}'")
    print(f"  Concurrency: {args.concurrency}")
    print(f"  Output: {output_dir}/")
    print()

    # Reset global counters
    completed = 0
    success_count = 0
    interrupted = False

    # Determine failed log path
    failed_log_path = Path(args.failed_log) if args.failed_log else output_dir / "failed.txt"

    try:
        asyncio.run(generate_all(rows_with_ids, args, output_dir, total, failed_log_path, args.field, args.prefix))

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
