# TOPIK 2 Processing Strategy

## Context

Following the TOPIK 1 workflow documented in [README.md](README.md), we'll enhance TOPIK 2 vocabulary with etymology, examples, notes, and audio.

**Already completed:**
- ✅ TOPIK 1: 1847 words fully processed (etymology, examples, notes, audio)

**Current task:**
- Process TOPIK 2: 3900 words using the same workflow

## Input

- **File**: `input/korean_english_2.tsv`
- **Format**: 3 columns (tab-separated): `number`, `korean`, `english`
- **Count**: 3900 words (TOPIK 2 vocabulary)

## Workflow Overview

```
input/korean_english_2.tsv (base)
    ↓
    generate-combined.md → output/topik2-combined-*.tsv
    (etymology + examples + notes in one file per batch)
    ↓
    Consolidate → output/topik2-combined-all.tsv
    ↓
    generate-audio.md → output/topik2-audio/*.mp3
    ↓
    Google Sheets (review/edit)
    ↓
    Anki Import
```

## Processing Plan

### Phase 1: Combined Enhancement Generation
**Prompt**: `prompts/generate-combined.md`

**Strategy**: Manual multi-terminal processing for context isolation
- Open multiple Claude Code terminals
- Each terminal processes one batch independently
- Edit prompt to specify batch number and range

**Output**: One TSV file per batch with all enhancements combined
- `output/topik2-combined-1.tsv` (words 1-100)
- `output/topik2-combined-2.tsv` (words 101-200)
- ...
- `output/topik2-combined-39.tsv` (words 3801-3900)

**Format** (7 columns):
```
number	korean	english	etymology	example_ko	example_en	notes
```

**Content per row:**
- **etymology**: Sino-Korean hanja/kanji, compounds, loanwords (blank for native Korean)
- **example_ko**: Natural sentence containing the word with particles
- **example_en**: English translation of example
- **notes**: Related word, antonym, or honorific pair (blank if none)

### Phase 2: Consolidation
- [ ] Concatenate all 39 batch files into `output/topik2-combined-all.tsv`
- [ ] Validate: Should have 3901 lines (1 header + 3900 entries)
- [ ] All rows have 7 columns

### Phase 3: Audio Generation
**Script**: `scripts/generate-audio.py` (adapt for TOPIK 2)

- [ ] Modify script to read `example_ko` column from `output/topik2-combined-all.tsv`
- [ ] Generate audio files to `output/topik2-audio/`
- [ ] Output: `0001.mp3` to `3900.mp3` (4-digit padded)
- [ ] Voice: `ko-KR-SunHiNeural` (female)
- [ ] Add prefix: Rename to `koreantopik2_*.mp3`
- [ ] Create archive: `output/koreantopik2_audio.zip`
- [ ] Copy to Anki: `cp output/topik2-audio/koreantopik2_*.mp3 ~/.local/share/Anki2/"User 1"/collection.media/`

### Phase 4: Final Review
- [ ] Import `output/topik2-combined-all.tsv` into Google Sheets
- [ ] Review and edit as needed
- [ ] Import into Anki deck

## Key Differences: TOPIK 1 vs TOPIK 2

| Aspect | TOPIK 1 | TOPIK 2 |
|--------|---------|---------|
| Words | 1,847 | 3,900 |
| Batches | 19 files (last has 47 words) | 39 files (100 each) |
| Audio prefix | `koreantopik1_` | `koreantopik2_` |
| Output files | `*-1.tsv` to `*-19.tsv` | `*-1.tsv` to `*-39.tsv` |

## File Naming Convention

```
output/
├── topik2-combined-1.tsv      # Batch 1 (words 1-100)
├── topik2-combined-2.tsv      # Batch 2 (words 101-200)
├── ...
├── topik2-combined-39.tsv     # Batch 39 (words 3801-3900)
├── topik2-combined-all.tsv    # Consolidated (all 3900 words)
└── topik2-audio/
    ├── koreantopik2_0001.mp3
    ├── koreantopik2_0002.mp3
    ├── ...
    └── koreantopik2_3900.mp3
```

## Progress Tracking

### Combined Enhancement (Etymology + Examples + Notes)
- [ ] Batch 1-10 (words 1-1000)
- [ ] Batch 11-20 (words 1001-2000)
- [ ] Batch 21-30 (words 2001-3000)
- [ ] Batch 31-39 (words 3001-3900)
- [ ] Consolidated all file: `topik2-combined-all.tsv`

### Audio
- [ ] Generate all audio files (3900 files)
- [ ] Add prefix `koreantopik2_`
- [ ] Create zip archive
- [ ] Copy to Anki media

## Status

**Current Phase**: Planning complete, ready to start Phase 1 (Combined Enhancement)

**Approach**: Manual multi-terminal processing using `prompts/generate-combined.md`

---
*Created: 2025-11-09*
