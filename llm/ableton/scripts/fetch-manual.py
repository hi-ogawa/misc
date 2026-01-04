#!/usr/bin/env python3
"""
Fetch Ableton Live 12 manual HTML files from ableton.com

Usage:
  uv run scripts/fetch-manual.py                    # Download all 42 chapters
  uv run scripts/fetch-manual.py --test             # Test with first chapter only
  uv run scripts/fetch-manual.py --output custom/   # Custom output directory

Dependencies: aiohttp (managed via pyproject.toml)
Output: HTML files in data/raw-html/
"""

import argparse
import asyncio
import sys
from pathlib import Path
from urllib.parse import urljoin

try:
    import aiohttp
except ImportError:
    print("Error: Missing dependencies. Install with: uv sync", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://www.ableton.com"

# All chapter URLs (42 chapters)
CHAPTER_URLS = [
    "/en/live-manual/12/welcome-to-live/",
    "/en/live-manual/12/first-steps/",
    "/en/live-manual/12/live-concepts/",
    "/en/live-manual/12/working-with-the-browser/",
    "/en/live-manual/12/managing-files-and-sets/",
    "/en/live-manual/12/arrangement-view/",
    "/en/live-manual/12/session-view/",
    "/en/live-manual/12/clip-view/",
    "/en/live-manual/12/audio-clips-tempo-and-warping/",
    "/en/live-manual/12/editing-midi/",
    "/en/live-manual/12/editing-mpe/",
    "/en/live-manual/12/launching-clips/",
    "/en/live-manual/12/recording-new-clips/",
    "/en/live-manual/12/comping/",
    "/en/live-manual/12/using-grooves/",
    "/en/live-manual/12/clip-envelopes/",
    "/en/live-manual/12/automation-and-editing-envelopes/",
    "/en/live-manual/12/routing-and-i-o/",
    "/en/live-manual/12/working-with-instruments-and-effects/",
    "/en/live-manual/12/instrument-drum-and-effect-racks/",
    "/en/live-manual/12/mixing/",
    "/en/live-manual/12/using-tuning-systems/",
    "/en/live-manual/12/bounce-to-audio/",
    "/en/live-manual/12/working-with-video/",
    "/en/live-manual/12/stem-separation/",
    "/en/live-manual/12/converting-audio-to-midi/",
    "/en/live-manual/12/live-instrument-reference/",
    "/en/live-manual/12/live-audio-effect-reference/",
    "/en/live-manual/12/live-midi-effect-reference/",
    "/en/live-manual/12/midi-tools/",
    "/en/live-manual/12/max-for-live/",
    "/en/live-manual/12/max-for-live-devices/",
    "/en/live-manual/12/midi-and-key-remote-control/",
    "/en/live-manual/12/using-push-1/",
    "/en/live-manual/12/using-push-2/",
    "/en/live-manual/12/synchronizing-with-link-tempo-follower-and-midi/",
    "/en/live-manual/12/live-keyboard-shortcuts/",
    "/en/live-manual/12/accessibility-and-keyboard-navigation/",
    "/en/live-manual/12/computer-audio-resources-and-strategies/",
    "/en/live-manual/12/audio-fact-sheet/",
    "/en/live-manual/12/midi-fact-sheet/",
    "/en/live-manual/12/credits/",
]


async def fetch_chapter(session: aiohttp.ClientSession, chapter: dict, output_dir: Path) -> tuple[bool, str]:
    """Fetch a single chapter HTML"""
    url = chapter['url']
    number = chapter['number']
    slug = chapter['slug']
    filename = f"{number:02d}-{slug}.html"
    filepath = output_dir / filename

    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            response.raise_for_status()
            html = await response.text()

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        return True, filename
    except Exception as e:
        return False, f"{filename}: {e}"


async def fetch_all(chapters: list[dict], output_dir: Path) -> tuple[int, list[str]]:
    """Fetch all chapters concurrently"""
    success_count = 0
    failed = []

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_chapter(session, ch, output_dir) for ch in chapters]
        results = await asyncio.gather(*tasks)

        for (success, msg), ch in zip(results, chapters):
            if success:
                print(f"  OK: {msg}")
                success_count += 1
            else:
                print(f"  ERROR: {msg}", file=sys.stderr)
                failed.append(ch['slug'])

    return success_count, failed


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch Ableton Live 12 manual HTML files")
    parser.add_argument("--output", default="data/raw-html", help="Output directory (default: data/raw-html)")
    parser.add_argument("--test", action="store_true", help="Test mode: fetch first chapter only")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build chapter list
    chapters = []
    for i, url_path in enumerate(CHAPTER_URLS, 1):
        full_url = urljoin(BASE_URL, url_path)
        slug = url_path.rstrip('/').split('/')[-1]
        chapters.append({
            'url': full_url,
            'slug': slug,
            'number': i
        })

    if args.test:
        chapters = chapters[:1]

    print("=" * 60)
    print("Ableton Live 12 Manual Fetcher")
    print("=" * 60)
    print(f"Chapters:     {len(chapters)}")
    print(f"Output dir:   {output_dir}")
    print()
    print("Fetching HTML files (async)...")
    print("-" * 60)

    success_count, failed = asyncio.run(fetch_all(chapters, output_dir))

    print("-" * 60)
    print(f"Fetched: {success_count}/{len(chapters)}")

    if failed:
        print(f"\nFailed ({len(failed)}):")
        for slug in failed:
            print(f"  - {slug}", file=sys.stderr)
        return 1

    print(f"\nAll files fetched successfully!")
    print(f"Output: {output_dir}/")
    print(f"\nNext step: uv run scripts/convert-manual.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
