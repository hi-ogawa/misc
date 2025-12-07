# Process Fix-Tagged Cards

Workflow for processing cards tagged with `fix` that have issues requiring correction.

## Overview

Cards are tagged `fix` when they have problems (usually grammar/usage issues in examples). The issue description is embedded in the `example_ko` field as `(fix: ...)` annotations.

## Common Issues

| Pattern | Example | Fix |
|---------|---------|-----|
| Counter mismatch | 이 개 → 두 개 | Use native Korean counters with 개 |
| Meaning mismatch | English "breathe", example "rest" | Regenerate example for correct meaning |
| Grammar error | (fix: description) | Follow the fix description |

## Workflow

### 1. Export

```bash
python scripts/anki-export.py --query "tag:fix" --fields noteId,korean,english,example_ko,example_en --output anki/output/fix-cards.tsv
```

### 2. Correct Examples

Create `anki/output/fix-cards-fixed.tsv` with corrected sentences.

Requirements: Follow `prompts/requirements-example.md`:
- Multi-clause sentences with connectives (-서, -고, -(으)니까, etc.)
- Concrete, visualizable context
- Distinctive usage showing word's characteristic meaning

### 3. Generate Audio

```bash
python scripts/generate-audio.py --input anki/output/fix-cards-fixed.tsv --output output/fix-audio/ --field example_ko --prefix koreantopik1_example_ko_fix_ --id-field noteId
```

### 4. Copy to Anki Media

```bash
cp output/fix-audio/*.mp3 ~/.local/share/Anki2/"사용자 1"/collection.media/
```

### 5. Update Cards and Remove Tag

```bash
python scripts/anki-update-notes.py \
  --input anki/output/fix-cards-fixed.tsv \
  --fields example_ko,example_en \
  --example-audio koreantopik1_example_ko_fix_ \
  --remove-tag fix \
  --dry-run  # Review first, then remove --dry-run
```

## Files

- `anki/output/fix-cards.tsv` - Exported cards with issues
- `anki/output/fix-cards-fixed.tsv` - Corrected examples
- `output/fix-audio/` - Generated audio files
