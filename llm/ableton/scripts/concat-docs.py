#!/usr/bin/env python3
"""
Concatenate all Ableton documentation into a single markdown file.

Usage:
  uv run scripts/concat-docs.py                    # Output to data/custom-instructions/
  uv run scripts/concat-docs.py --output custom.md # Custom output path
  uv run scripts/concat-docs.py --include-workflow # Include workflow.md

Output: Single markdown file with all documentation concatenated
"""

import argparse
from pathlib import Path
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Concatenate Ableton docs into single file")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/custom-instructions/ableton-docs-full.md"),
        help="Output file path",
    )
    parser.add_argument(
        "--include-workflow",
        action="store_true",
        help="Include workflow.md at the beginning",
    )
    args = parser.parse_args()

    # Setup paths
    repo_root = Path(__file__).parent.parent
    docs_dir = repo_root / "docs" / "official"
    workflow_file = repo_root / "workflow.md"
    output_file = args.output if args.output.is_absolute() else repo_root / args.output

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Check if docs exist
    if not docs_dir.exists():
        print(f"Error: {docs_dir} does not exist. Run 'uv run scripts/fetch-manual.py' first.")
        return 1

    # Get all markdown files sorted by filename
    doc_files = sorted(docs_dir.glob("*.md"))
    if not doc_files:
        print(f"Error: No markdown files found in {docs_dir}")
        return 1

    print(f"Found {len(doc_files)} documentation files")

    # Write concatenated output
    with output_file.open("w", encoding="utf-8") as out:
        # Write header
        out.write("# Ableton Live 12 Documentation\n\n")
        out.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"**Source**: Official Ableton Live 12 Manual\n")
        out.write(f"**Files**: {len(doc_files)} chapters\n\n")
        out.write("---\n\n")

        # Include workflow.md if requested
        if args.include_workflow and workflow_file.exists():
            print(f"Including: {workflow_file.name}")
            out.write("# Personal Workflow\n\n")
            out.write(workflow_file.read_text(encoding="utf-8"))
            out.write("\n\n---\n\n")

        # Concatenate all docs
        for i, doc_file in enumerate(doc_files, 1):
            print(f"Processing {i}/{len(doc_files)}: {doc_file.name}")
            
            content = doc_file.read_text(encoding="utf-8")
            
            # Write chapter separator
            out.write(f"# Chapter {i}: {doc_file.stem}\n\n")
            out.write(content)
            out.write("\n\n---\n\n")

    print(f"\n✅ Successfully created: {output_file}")
    print(f"📊 File size: {output_file.stat().st_size / 1024:.1f} KB")

    return 0


if __name__ == "__main__":
    exit(main())
