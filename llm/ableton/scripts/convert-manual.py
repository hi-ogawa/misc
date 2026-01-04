#!/usr/bin/env python3
"""
Convert downloaded Ableton manual HTML files to clean markdown.

Usage:
  uv run scripts/convert-manual.py                    # Convert all HTML files
  uv run scripts/convert-manual.py --test             # Test with first file only
  uv run scripts/convert-manual.py --input data/raw-html --output docs/official

Dependencies: beautifulsoup4, html2text (managed via pyproject.toml)
Output: Markdown files in docs/official/
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

try:
    from bs4 import BeautifulSoup
    import html2text
except ImportError:
    print("Error: Missing dependencies. Install with: uv sync", file=sys.stderr)
    sys.exit(1)


def extract_chapter_number(filename: str) -> int:
    """Extract chapter number from filename like '01-welcome-to-live.html'"""
    try:
        return int(filename.split('-')[0])
    except (ValueError, IndexError):
        return 0


def convert_html_to_markdown(html_file: Path, base_url: str = "https://www.ableton.com") -> tuple[bool, str, str]:
    """
    Convert a single HTML file to markdown.

    Returns:
        (success, markdown_content, error_message)
    """
    try:
        # Read HTML
        with open(html_file, 'r', encoding='utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        # Extract only the chapter content (not navigation/TOC)
        chapter_div = soup.find('div', id='chapter_content')
        if not chapter_div:
            return False, "", f"#chapter_content div not found in {html_file.name}"

        # Extract title from h1
        h1 = chapter_div.find('h1')
        if h1:
            title = h1.get_text(strip=True)
            # Remove chapter number prefix like "1. " from title
            title = title.split('.', 1)[-1].strip()
        else:
            title = html_file.stem.replace('-', ' ').title()

        # Build source URL from filename
        slug = html_file.stem.split('-', 1)[1] if '-' in html_file.stem else html_file.stem
        source_url = f"{base_url}/en/live-manual/12/{slug}/"

        # Convert HTML to markdown
        h = html2text.HTML2Text()
        h.body_width = 0  # Don't wrap lines
        h.ignore_links = False
        h.ignore_images = False
        h.base_url = source_url
        markdown_body = h.handle(str(chapter_div))

        # Create frontmatter
        frontmatter = f"""---
title: "{title}"
source: {source_url}
scraped: {datetime.now().isoformat()}
version: Live 12
---

"""

        full_markdown = frontmatter + markdown_body
        return True, full_markdown, ""

    except Exception as e:
        return False, "", f"Error processing {html_file.name}: {e}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Ableton manual HTML to markdown")
    parser.add_argument("--input", default="data/raw-html", help="Input directory with HTML files")
    parser.add_argument("--output", default="docs/official", help="Output directory for markdown files")
    parser.add_argument("--test", action="store_true", help="Test mode: convert first file only")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    # Validate input directory
    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}", file=sys.stderr)
        return 1

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all HTML files, sorted by chapter number
    html_files = sorted(
        input_dir.glob("*.html"),
        key=lambda f: extract_chapter_number(f.name)
    )

    if not html_files:
        print(f"Error: No HTML files found in {input_dir}", file=sys.stderr)
        return 1

    if args.test:
        html_files = html_files[:1]

    print("=" * 60)
    print("Ableton Manual HTML -> Markdown Converter")
    print("=" * 60)
    print(f"Input:  {input_dir}")
    print(f"Output: {output_dir}")
    print(f"Files:  {len(html_files)}")
    print()

    success_count = 0
    failed = []

    for i, html_file in enumerate(html_files, 1):
        success, markdown, error = convert_html_to_markdown(html_file)

        if success:
            # Generate output filename
            md_filename = html_file.stem + '.md'
            md_file = output_dir / md_filename

            # Write markdown
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown)

            print(f"[{i}/{len(html_files)}] OK: {md_filename}")
            success_count += 1
        else:
            print(f"[{i}/{len(html_files)}] ERROR: {html_file.name}", file=sys.stderr)
            print(f"    {error}", file=sys.stderr)
            failed.append(html_file.name)

    print()
    print("=" * 60)
    print(f"Converted: {success_count}/{len(html_files)}")
    if failed:
        print(f"Failed: {len(failed)}")
        for name in failed:
            print(f"  - {name}", file=sys.stderr)
        return 1

    print(f"\nAll files converted successfully!")
    print(f"Output: {output_dir}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
