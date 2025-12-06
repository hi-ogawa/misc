# Plan: Anki Cards for Grammar Gaps

Generate Anki cards for the 23 grammar patterns identified in `gap-analysis.md`.

## Overview

- **Source**: `gap-analysis.md` (patterns marked `#` or `@`)
- **Target**: `Korean::Custom` deck with `grammar` tag
- **Note model**: Existing "Korean Vocabulary" model

## File Structure

```
resources/korean-grammar-in-use/
├── gap-analysis.md              # Source: gap patterns
├── output/
│   ├── grammar-cards.tsv        # Working file (7 columns)
│   ├── grammar_anki_import.tsv  # Anki import file (9 columns)
│   └── audio/                   # Generated audio
│       └── grammar_example_ko_*.mp3 (23 files)
└── plan-anki-cards.md           # This file
```

## Field Mapping

| Field | Content | Example |
|-------|---------|---------|
| `number` | `grammar_01`, `grammar_02`, ... | `grammar_01` |
| `korean` | Pattern (clean, no A/V/N prefix) | `-나` |
| `english` | Meaning (disambiguate if needed) | or (choice between options) |
| `example_ko` | Korean sentence | 시간이 없으니까 커피나 주스 중에서 빨리 골라 주세요 |
| `example_en` | English translation | I don't have time, so please quickly choose between coffee or juice |
| `etymology` | (empty) | |
| `notes` | Full notation + related patterns | N(이)나, -하고, -거나 |
| `korean_audio` | (empty - pattern not TTS-friendly) | |
| `example_ko_audio` | Sound reference | `[sound:grammar_example_ko_0001.mp3]` |

## Example Sentence Guidelines

Reference `prompts/requirements-example.md`:
- Multi-clause sentences (reason, time, purpose connectives)
- Concrete, visualizable context
- Explicit subjects/objects (no ellipsis)
- Show characteristic usage of the grammar pattern

## Notes Field Guidelines

Reference `prompts/requirements-notes.md` for inspiration. For grammar patterns:
- Full notation: `-나` → `N(이)나`
- Similar patterns: `-같이` → `-처럼`
- Formal/casual pairs: `-시다` → `-자 (casual)`
- Related patterns: `-시다` → `-(으)ㄹ까요?`

## Audio Generation

**Script**: `scripts/generate-audio.py`

**Command**:
```bash
python scripts/generate-audio.py \
  --input resources/korean-grammar-in-use/output/grammar-cards.tsv \
  --output resources/korean-grammar-in-use/output/audio \
  --field example_ko \
  --prefix grammar_example_ko_
```

**Output**: 23 files → `grammar_example_ko_0001.mp3` ... `grammar_example_ko_0023.mp3`

## Anki Import

### Step 1: Copy audio files

```bash
cp resources/korean-grammar-in-use/output/audio/*.mp3 \
   ~/.local/share/Anki2/사용자\ 1/collection.media/
```

### Step 2: Import notes

**Option A**: Manual Anki import (recommended)
1. File → Import → select `grammar_anki_import.tsv`
2. Set deck to `Korean::Custom`
3. Add `grammar` tag after import

**Option B**: AnkiConnect via `scripts/anki-add-notes.py`

```bash
# Verify Anki is running
python scripts/anki.py deckNames

# Dry run first
python scripts/anki-add-notes.py \
  --input resources/korean-grammar-in-use/output/grammar_anki_import.tsv \
  --deck "Korean::Custom" \
  --tag grammar \
  --dry-run

# If dry-run looks good, run without --dry-run
python scripts/anki-add-notes.py \
  --input resources/korean-grammar-in-use/output/grammar_anki_import.tsv \
  --deck "Korean::Custom" \
  --tag grammar
```

### Step 3: Verify

```bash
# Check notes were added
python scripts/anki.py findNotes --params '{"query": "deck:Korean::Custom tag:grammar"}'
```

## Steps

- [x] Extract 23 patterns from `gap-analysis.md` to `output/grammar-cards.tsv`
- [x] Generate example sentences following guidelines
- [x] Generate audio: `scripts/generate-audio.py`
- [x] Create `grammar_anki_import.tsv` with audio references
- [x] Copy audio to Anki media folder
- [x] Import notes via `scripts/anki-add-notes.py`
- [x] Verify cards in Anki
