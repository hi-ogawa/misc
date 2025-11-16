#!/usr/bin/env python3
"""
Verify MP3 files using ffprobe to detect broken or corrupted audio files.
"""

import argparse
import asyncio
import json
import os
from pathlib import Path
import sys

# Global counters (safe in single-threaded async)
completed = 0
valid_count = 0


async def verify_mp3(mp3_path: Path, total: int, timeout: float) -> tuple[Path, bool, str]:
    """
    Verify an MP3 file using ffprobe.

    Returns:
        (mp3_path, is_valid, error_message)
    """
    global completed, valid_count

    try:
        # Run ffprobe to get file info
        async def run_ffprobe():
            process = await asyncio.create_subprocess_exec(
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration,size',
                '-show_entries', 'stream=codec_type,codec_name',
                '-of', 'json',
                str(mp3_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            return process.returncode, stdout, stderr

        returncode, stdout, stderr = await asyncio.wait_for(run_ffprobe(), timeout=timeout)

        completed += 1

        # If ffprobe returns non-zero, the file is likely broken
        if returncode != 0:
            error_msg = stderr.decode().strip() or "ffprobe returned non-zero exit code"
            print(f"  [{completed}/{total}] ✗ {mp3_path.name}: {error_msg}")
            return (mp3_path, False, error_msg)

        # Parse the JSON output
        try:
            data = json.loads(stdout.decode())
        except json.JSONDecodeError:
            error_msg = "Failed to parse ffprobe output"
            print(f"  [{completed}/{total}] ✗ {mp3_path.name}: {error_msg}")
            return (mp3_path, False, error_msg)

        # Check if we have format information
        if 'format' not in data:
            error_msg = "No format information found"
            print(f"  [{completed}/{total}] ✗ {mp3_path.name}: {error_msg}")
            return (mp3_path, False, error_msg)

        # Check duration
        duration = float(data['format'].get('duration', 0))
        if duration <= 0:
            error_msg = f"Invalid duration: {duration}"
            print(f"  [{completed}/{total}] ✗ {mp3_path.name}: {error_msg}")
            return (mp3_path, False, error_msg)

        # Check if we have audio streams
        streams = data.get('streams', [])
        audio_streams = [s for s in streams if s.get('codec_type') == 'audio']

        if not audio_streams:
            error_msg = "No audio streams found"
            print(f"  [{completed}/{total}] ✗ {mp3_path.name}: {error_msg}")
            return (mp3_path, False, error_msg)

        # Valid file
        valid_count += 1
        print(f"  [{completed}/{total}] ✓ {mp3_path.name}")
        return (mp3_path, True, "OK")

    except asyncio.TimeoutError:
        completed += 1
        error_msg = f"ffprobe timeout after {timeout}s"
        print(f"  [{completed}/{total}] ✗ {mp3_path.name}: {error_msg}")
        return (mp3_path, False, error_msg)
    except FileNotFoundError:
        completed += 1
        error_msg = "ffprobe not found - please install ffmpeg"
        print(f"  [{completed}/{total}] ✗ {mp3_path.name}: {error_msg}")
        return (mp3_path, False, error_msg)
    except Exception as e:
        completed += 1
        error_msg = f"Unexpected error: {str(e)}"
        print(f"  [{completed}/{total}] ✗ {mp3_path.name}: {error_msg}")
        return (mp3_path, False, error_msg)


async def verify_all(mp3_files, concurrency, total, timeout):
    """Verify MP3 files in chunks."""
    results = []

    # Process in chunks
    for i in range(0, len(mp3_files), concurrency):
        batch = mp3_files[i:i+concurrency]

        # Run this batch concurrently
        tasks = [
            verify_mp3(mp3_path, total, timeout)
            for mp3_path in batch
        ]

        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)

    return results


def main():
    global completed, valid_count

    parser = argparse.ArgumentParser(description="Verify MP3 files using ffprobe")
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
        help=f"Number of concurrent verification tasks (default: {os.cpu_count() or 4}, based on CPU cores)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Timeout in seconds for each verification (default: 5)"
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
    print(f"Verifying...\n")

    # Reset global counters
    completed = 0
    valid_count = 0
    interrupted = False

    try:
        results = asyncio.run(verify_all(mp3_files, args.concurrency, total, args.timeout))
    except KeyboardInterrupt:
        interrupted = True
        print("\n\nInterrupted by user (Ctrl-C)")
        results = []

    # Collect broken files from results
    broken_files = [(path, error) for path, is_valid, error in results if not is_valid]

    # Print summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Valid files:  {valid_count}/{total}")
    print(f"  Broken files: {len(broken_files)}/{total}")

    if broken_files:
        print(f"\n{'='*60}")
        print("Broken files:")
        for path, error in broken_files:
            print(f"  - {path.name}")
            print(f"    Error: {error}")
        return 1
    elif interrupted:
        print("\nVerification incomplete (interrupted)")
        return 130  # Standard exit code for SIGINT
    else:
        print("\nAll MP3 files are valid!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
