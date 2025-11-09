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
    ├─→ generate-etymology2.md  → output/topik2-etymology-*.tsv
    ├─→ generate-example3.md    → output/topik2-examples-*.tsv
    ├─→ generate-notes.md       → output/topik2-notes-*.tsv
    └─→ generate-audio.md       → output/topik2-audio/*.mp3
         ↓
    Google Sheets (combine all columns)
         ↓
    Anki Import
```

## Processing Plan

### Phase 1: Etymology Generation
**Prompt**: `prompts/generate-etymology2.md` (adapt for TOPIK 2)

- [ ] Process batches of 100 entries each
- [ ] Output files:
  - `output/topik2-etymology-1.tsv` (words 1-100)
  - `output/topik2-etymology-2.tsv` (words 101-200)
  - ...
  - `output/topik2-etymology-39.tsv` (words 3801-3900)
- [ ] Create consolidated: `output/topik2-etymology-all.tsv`

**Output format**: `number`, `korean`, `etymology`
- Sino-Korean: Show Hanja / Japanese (e.g., "希望", "價格 / 価格")
- Compounds: Show components (e.g., "눈 + 물")
- Loanwords: Show source (e.g., "computer", "アルバイト / Arbeit")
- Native Korean: Leave blank

### Phase 2: Example Sentences Generation
**Prompt**: `prompts/generate-example3.md` (adapt for TOPIK 2)

- [ ] Process batches of 100 entries each
- [ ] Output files:
  - `output/topik2-examples-1.tsv` (words 1-100)
  - `output/topik2-examples-2.tsv` (words 101-200)
  - ...
  - `output/topik2-examples-39.tsv` (words 3801-3900)
- [ ] Create consolidated: `output/topik2-examples-all.tsv`

**Output format**: `number`, `korean`, `example_ko`, `example_en`
- Natural, common usage
- Must contain the vocabulary word
- Include particles explicitly
- 3-4 words ideal

### Phase 3: Notes Generation
**Prompt**: `prompts/generate-notes.md` (adapt for TOPIK 2)

- [ ] Process batches of 100 entries each
- [ ] Output files:
  - `output/topik2-notes-1.tsv` (words 1-100)
  - `output/topik2-notes-2.tsv` (words 101-200)
  - ...
  - `output/topik2-notes-39.tsv` (words 3801-3900)
- [ ] Create consolidated: `output/topik2-notes-all.tsv`

**Output format**: `number`, `korean`, `notes`
- Related words (synonyms, antonyms)
- Family/people pairs
- Honorific pairs
- Leave blank if none

### Phase 4: Audio Generation
**Script**: `scripts/generate-audio.py` (adapt for TOPIK 2)

- [ ] Modify script to read from `output/topik2-examples-all.tsv`
- [ ] Generate audio files to `output/topik2-audio/`
- [ ] Output: `0001.mp3` to `3900.mp3` (4-digit padded)
- [ ] Voice: `ko-KR-SunHiNeural` (female)
- [ ] Add prefix: Rename to `koreantopik2_*.mp3`
- [ ] Create archive: `output/koreantopik2_audio.zip`
- [ ] Copy to Anki: `cp output/topik2-audio/koreantopik2_*.mp3 ~/.local/share/Anki2/"User 1"/collection.media/`

### Phase 5: Consolidation
- [ ] Combine all TSV files in Google Sheets
- [ ] Review and edit as needed
- [ ] Import into Anki deck

## Key Differences: TOPIK 1 vs TOPIK 2

| Aspect | TOPIK 1 | TOPIK 2 |
|--------|---------|---------|
| Words | 1,847 | 3,900 |
| Batches | 19 files (last has 47 words) | 39 files (100 each) |
| Audio prefix | `koreantopik1_` | `koreantopik2_` |
| Output files | `*-1.tsv` to `*-19.tsv` | `*-1.tsv` to `*-39.tsv` |

## Prompt Adaptations Needed

Each prompt file needs minor updates:

1. **Input path**: Change to `input/korean_english_2.tsv`
2. **Output pattern**: Change to `output/topik2-*-N.tsv`
3. **Batch count**: Update to 39 batches (instead of 19)

## File Naming Convention

```
output/
├── topik2-etymology-1.tsv
├── topik2-etymology-2.tsv
├── ...
├── topik2-etymology-39.tsv
├── topik2-etymology-all.tsv
├── topik2-examples-1.tsv
├── topik2-examples-2.tsv
├── ...
├── topik2-examples-39.tsv
├── topik2-examples-all.tsv
├── topik2-notes-1.tsv
├── topik2-notes-2.tsv
├── ...
├── topik2-notes-39.tsv
├── topik2-notes-all.tsv
└── topik2-audio/
    ├── koreantopik2_0001.mp3
    ├── koreantopik2_0002.mp3
    ├── ...
    └── koreantopik2_3900.mp3
```

## Progress Tracking

### Etymology
- [ ] Batch 1-10 (words 1-1000)
- [ ] Batch 11-20 (words 1001-2000)
- [ ] Batch 21-30 (words 2001-3000)
- [ ] Batch 31-39 (words 3001-3900)
- [ ] Consolidated all file

### Examples
- [ ] Batch 1-10 (words 1-1000)
- [ ] Batch 11-20 (words 1001-2000)
- [ ] Batch 21-30 (words 2001-3000)
- [ ] Batch 31-39 (words 3001-3900)
- [ ] Consolidated all file

### Notes
- [ ] Batch 1-10 (words 1-1000)
- [ ] Batch 11-20 (words 1001-2000)
- [ ] Batch 21-30 (words 2001-3000)
- [ ] Batch 31-39 (words 3001-3900)
- [ ] Consolidated all file

### Audio
- [ ] Generate all audio files (3900 files)
- [ ] Add prefix `koreantopik2_`
- [ ] Create zip archive
- [ ] Copy to Anki media

## Status

**Current Phase**: Planning complete, ready to start Phase 1 (Etymology)

---
*Created: 2025-11-09*
