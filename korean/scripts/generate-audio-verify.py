#!/usr/bin/env python3
"""
Verify MP3 files using ffprobe to detect broken or corrupted audio files.
"""

import argparse
import subprocess
import json
from pathlib import Path
import sys


def verify_mp3(mp3_path: Path) -> tuple[bool, str]:
    """
    Verify an MP3 file using ffprobe.

    Returns:
        (is_valid, error_message)
    """
    try:
        # Run ffprobe to get file info
        result = subprocess.run(
            [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration,size',
                '-show_entries', 'stream=codec_type,codec_name',
                '-of', 'json',
                str(mp3_path)
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        # If ffprobe returns non-zero, the file is likely broken
        if result.returncode != 0:
            error_msg = result.stderr.strip() or "ffprobe returned non-zero exit code"
            return False, error_msg

        # Parse the JSON output
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            return False, "Failed to parse ffprobe output"

        # Check if we have format information
        if 'format' not in data:
            return False, "No format information found"

        # Check duration
        duration = float(data['format'].get('duration', 0))
        if duration <= 0:
            return False, f"Invalid duration: {duration}"

        # Check if we have audio streams
        streams = data.get('streams', [])
        audio_streams = [s for s in streams if s.get('codec_type') == 'audio']

        if not audio_streams:
            return False, "No audio streams found"

        return True, "OK"

    except subprocess.TimeoutExpired:
        return False, "ffprobe timeout"
    except FileNotFoundError:
        return False, "ffprobe not found - please install ffmpeg"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"


def main():
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

    range_info = ""
    if args.start or args.end:
        range_info = f" (range: {args.start or 1}-{args.end or 'end'})"
    print(f"Found {len(mp3_files)} MP3 file(s) in {output_dir}{range_info}")
    print(f"Verifying...\n")

    broken_files = []
    valid_count = 0

    for mp3_path in mp3_files:
        is_valid, message = verify_mp3(mp3_path)

        if is_valid:
            valid_count += 1
            print(f"✓ {mp3_path.name}")
        else:
            broken_files.append((mp3_path, message))
            print(f"✗ {mp3_path.name}: {message}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Valid files:  {valid_count}/{len(mp3_files)}")
    print(f"  Broken files: {len(broken_files)}/{len(mp3_files)}")

    if broken_files:
        print(f"\n{'='*60}")
        print("Broken files:")
        for path, error in broken_files:
            print(f"  - {path.name}")
            print(f"    Error: {error}")
        return 1
    else:
        print("\nAll MP3 files are valid!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
