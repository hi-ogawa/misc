# Script Writing Guide

Principles for writing simple, maintainable scripts in this project.

## Core Principles

### 1. Simplicity Over Abstraction

**Avoid unnecessary functions**
- Only create functions when code is actually reused
- Keep logic in `main()` when possible - linear flow is easier to understand
- Don't create abstractions "just in case"

```python
# ❌ Unnecessary abstraction
def count_words(text):
    return len(text.strip().split()) if text.strip() else 0

word_count = count_words(example_ko)

# ✅ Inline when used once
word_count = len(example_ko.strip().split()) if example_ko.strip() else 0
```

### 2. No Hardcoding

**Use argparse for all inputs**
- Reference existing scripts (e.g., `scripts/generate-audio.py`)
- Make paths configurable
- Provide sensible defaults
- Auto-derive values when reasonable (e.g., dataset name from filename)

```python
parser.add_argument("--input", required=True, help="Input TSV file")
parser.add_argument("--batch-size", type=int, default=100, help="Batch size (default: 100)")
```

### 3. Output to Stdout by Default

**Terminal output is the primary interface**
- Print results directly to stdout
- Don't create files unless explicitly needed
- Markdown formatting is fine - it's readable in terminals
- Optional file output is okay, but not the default

```python
# ✅ Stdout first
print(output)

# ❌ File output by default
with open('output.txt', 'w') as f:
    f.write(output)
```

### 4. Single Source of Truth

**Don't duplicate content generation**
- Build content once
- Reuse for different outputs (stdout, files, etc.)
- Use multiline f-strings for static sections
- Use concatenation for dynamic sections

```python
# ✅ Single source
output = f"""\
# Report
Stats: {stats}
"""
if condition:
    output += "Extra section\n"

print(output)  # stdout
# Optional: write to file
```

### 5. String Building Best Practices

**For static content: multiline f-strings**
```python
output = f"""\
# Title
Value: {value}
"""
```

**For dynamic content: concatenation**
```python
for item in items:
    output += f"- {item}\n"
```

**Use backslash to avoid leading newlines**
```python
output = f"""\
First line
"""
# Not:
output = f"""
First line
"""  # Extra newline at start
```

### 6. Focus on the Essential

**Remove features that aren't needed**
- Start with what's actually required
- Don't add "nice to have" features preemptively
- Can always add later if needed

Examples removed from `analyze-examples.py`:
- Issue tracking (not the focus)
- English sentence stats (only Korean needed)
- JSON output (stdout is sufficient)
- Complex error reporting (simple checks are enough)

### 7. Data Structures

**Use simple, built-in types**
- Lists and dicts from stdlib are usually sufficient
- `defaultdict` for grouping
- `statistics` module for stats
- Avoid external dependencies when possible

```python
from collections import defaultdict
import statistics

batches = defaultdict(list)
for entry in entries:
    batch_num = (entry['number'] - 1) // batch_size + 1
    batches[batch_num].append(entry['value'])
```

## Script Template

```python
#!/usr/bin/env python3
"""
Brief description of what this script does.
"""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Script description")
    parser.add_argument("--input", required=True, help="Input file")
    # Add more arguments as needed

    args = parser.parse_args()

    # Validate inputs
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        return 1

    # Load data
    # Process data
    # Generate output

    # Print to stdout
    print(output)

    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Reference Scripts

When writing new scripts, reference these examples:
- **`scripts/generate-audio.py`**: Argparse patterns, error handling
- **`scripts/analyze-examples.py`**: Simple data processing, stdout output

## Anti-Patterns to Avoid

- ❌ Creating helper functions that are only called once
- ❌ Building complex class hierarchies for simple tasks
- ❌ Duplicating content for stdout vs file output
- ❌ Hardcoding file paths
- ❌ Adding features "just in case"
- ❌ Writing to files by default
- ❌ Using external libraries when stdlib suffices
