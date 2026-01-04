# Scripting Principles

Simple, practical guidelines for scripts in this project.

## Core Principles

### 1. Simplicity Over Abstraction
- Keep logic in `main()` when possible - linear flow is easier to understand
- Only create functions when code is actually reused
- Don't create abstractions "just in case"

```python
# ❌ Unnecessary abstraction (used once)
def fetch_chapter(url):
    return requests.get(url).text

html = fetch_chapter(chapter_url)

# ✅ Inline when used once
html = requests.get(chapter_url).text
```

### 2. No Hardcoding
- Use argparse for all inputs
- Make paths configurable
- Provide sensible defaults
- Auto-derive values when reasonable

```python
parser.add_argument("--output", default="docs/official", help="Output directory")
parser.add_argument("--delay", type=int, default=1, help="Delay between requests (seconds)")
```

### 3. Output to Stdout by Default
- Print results directly to stdout
- Don't create files unless explicitly needed for the task
- Markdown formatting is fine - it's readable in terminals
- Optional file output with `--output` flag is okay

### 4. Type Annotations
Always use type hints for function signatures:
```python
def scrape_chapter(url: str, output_dir: Path) -> bool:
    ...
```

### 5. Focus on the Essential
- Start with what's actually required
- Don't add "nice to have" features preemptively
- Can always add later if needed

## Script Template

```python
#!/usr/bin/env python3
"""
Brief description of what this script does.

Usage: uv run scripts/script-name.py [options]
Dependencies: managed via pyproject.toml
Output: where output goes
"""

import argparse
import sys
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser(description="Script description")
    parser.add_argument("--input", required=True, help="Input file")
    args = parser.parse_args()

    # Validate inputs
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        return 1

    # Load data
    # Process data
    # Print to stdout or save to files

    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Naming Conventions

**Format**: `verb-noun.py`

Examples:
- `scrape-manual.py` - scrapes Ableton manual
- `convert-html.py` - converts HTML to markdown
- `validate-docs.py` - validates documentation

## Dependencies

**Use pyproject.toml + uv**:
```toml
[project]
dependencies = [
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.0",
]
```

Install: `uv sync`
Run: `uv run scripts/script-name.py`

## Output Organization

**Scripts write to organized locations**:
```
scripts/
  scrape-manual.py          # Script

docs/
  official/
    *.md                    # Generated docs (tracked)

data/                       # Raw/cache (add to .gitignore)
  raw-html/
  cache/
```

## Error Handling & Progress

**For long-running scripts**:
- Show progress: "Processing 5/35..."
- Print errors to stderr
- Summary at end: "35 succeeded, 2 failed"
- Exit with non-zero on error

```python
for i, item in enumerate(items, 1):
    print(f"[{i}/{len(items)}] Processing {item['name']}")
    try:
        process(item)
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        failed.append(item)
```

## When NOT to Script

Don't script if:
- Task is truly one-time
- Manual execution is clearer
- Script would be more complex than manual process

Examples: GUI actions, initial setup, exploratory analysis

## Anti-Patterns to Avoid

- ❌ Creating helper functions that are only called once
- ❌ Building complex class hierarchies for simple tasks
- ❌ Hardcoding file paths
- ❌ Adding features "just in case"
- ❌ Using external libraries when stdlib suffices
