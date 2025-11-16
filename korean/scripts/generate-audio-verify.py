#!/usr/bin/env python3
"""
Verify MP3 files using ffprobe to detect broken or corrupted audio files.
"""

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
    # Find all MP3 files in the current directory and subdirectories
    mp3_files = sorted(Path('.').rglob('*.mp3'))

    if not mp3_files:
        print("No MP3 files found in the current directory.")
        return 0

    print(f"Found {len(mp3_files)} MP3 file(s). Verifying...\n")

    broken_files = []
    valid_count = 0

    for mp3_path in mp3_files:
        is_valid, message = verify_mp3(mp3_path)

        if is_valid:
            valid_count += 1
            print(f"✓ {mp3_path}")
        else:
            broken_files.append((mp3_path, message))
            print(f"✗ {mp3_path}: {message}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Valid files:  {valid_count}/{len(mp3_files)}")
    print(f"  Broken files: {len(broken_files)}/{len(mp3_files)}")

    if broken_files:
        print(f"\n{'='*60}")
        print("Broken files:")
        for path, error in broken_files:
            print(f"  - {path}")
            print(f"    Error: {error}")
        return 1
    else:
        print("\nAll MP3 files are valid!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
