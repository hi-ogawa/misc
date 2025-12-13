# Process Fix-Tagged Cards

Workflow for processing cards tagged with `fix` that have issues requiring correction.

## Overview

Cards are tagged `fix` when they have problems. Issues are marked with `(fix: ...)` annotations in the relevant field (`example_ko`, `korean_audio`, etc.).

## Common Issues

| Pattern | Location | Example | Fix |
|---------|----------|---------|-----|
| Counter mismatch | `example_ko` | 이 개 → 두 개 | Use native Korean counters with 개 |
| Meaning mismatch | `example_ko` | English "breathe", example "rest" | Regenerate example for correct meaning |
| Grammar error | `example_ko` | (fix: description) | Follow the fix description |
| Audio issue | `korean_audio` | (fix) annotation | Regenerate audio file |

## Workflow

### 1. Export

```bash
python scripts/anki-export.py --query "tag:fix" --fields noteId,korean,english,example_ko,example_en,korean_audio,example_ko_audio --output anki/output/fix-cards.tsv
```

### 2. Correct Examples

Create `anki/output/fix-cards-fixed.tsv` with corrected sentences.

Requirements: Follow `prompts/requirements-example.md`:
- Multi-clause sentences with connectives (-서, -고, -(으)니까, etc.)
- Concrete, visualizable context
- Distinctive usage showing word's characteristic meaning

### 3. Generate Audio

```bash
# For korean audio fixes
python scripts/generate-audio.py --input anki/output/fix-cards-fixed.tsv --output output/fix-audio/ --field korean --prefix korean_fix_YYYY_MM_DD_ --id-field noteId

# For example_ko audio fixes
python scripts/generate-audio.py --input anki/output/fix-cards-fixed.tsv --output output/fix-audio/ --field example_ko --prefix example_ko_fix_YYYY_MM_DD_ --id-field noteId
```

Replace `YYYY_MM_DD` with the current date (e.g., `2025_01_15`). Run only the commands for fields that need fixing.

### 4. Add audio columns

```bash
python scripts/jq-tsv.py \
  '. + {korean_audio: "[sound:korean_fix_YYYY_MM_DD_\(.noteId).mp3]", example_ko_audio: "[sound:example_ko_fix_YYYY_MM_DD_\(.noteId).mp3]"}' \
  anki/output/fix-cards-fixed.tsv > anki/output/fix-cards-with-audio.tsv
```

Use the same `YYYY_MM_DD` date as step 3. Include only the fields that were regenerated.

### 5. Update Cards and Remove Tag

```bash
python scripts/anki-update-notes.py \
  --input anki/output/fix-cards-with-audio.tsv \
  --fields example_ko,example_en,korean_audio,example_ko_audio \
  --remove-tag fix \
  --dry-run  # Review first, then remove --dry-run
```

Adjust `--fields` to include only the fields that were fixed.

### 6. Copy to Anki Media

```bash
cp output/fix-audio/*.mp3 "$(python scripts/anki.py getMediaDirPath | tr -d '"')"
```

## Files

- `anki/output/fix-cards.tsv` - Exported cards with issues
- `anki/output/fix-cards-fixed.tsv` - Corrected examples
- `output/fix-audio/` - Generated audio files
