# TOPIK 2 Vocabulary Enhancement Plan (3873 words)

**Source**: TOPIK 2 vocabulary list from https://www.koreantopik.com/2024/09/complete-topik-2-vocabulary-list-3900.html

**Status**: 🚧 Planning phase - base extraction complete, enhancements pending

## Overview

Following the successful completion of TOPIK 1 (1847 words), this document outlines the plan for processing TOPIK 2 vocabulary with the same enhancement workflow.

**Scale comparison**:
- TOPIK 1: 1,847 words across 18 lessons
- TOPIK 2: 3,873 words across 39 lessons (2.1x larger)

## Current State

### Completed
- [x] Base vocabulary extraction (39 pages → CSV files)
- [x] Hanja and Japanese etymology columns added
- [x] Consolidated file: `topik2/data/csv-extra/all.csv` (documented in [topik2/readme.md](topik2/readme.md))
- [x] Converted to TSV format: `input/koreantopik2.tsv` (3873 entries)

### Pending
- [ ] Batch splitting (39 batches of ~100 words)
- [ ] Etymology enhancement
- [ ] Example sentences generation
- [ ] Study notes generation
- [ ] Audio generation
- [ ] Consolidation and Anki import

## Project Structure

```
korean/
├── input/
│   ├── koreantopik2.tsv           # Base TOPIK 2 file (3873 entries)
│   └── koreantopik2-batch-N.tsv   # Pre-split batches (1-39, pending)
├── output/topik2/                 # TOPIK 2 enhancement outputs (pending)
│   ├── etymology-N.tsv            # Etymology batches (1-39)
│   ├── examples-N.tsv             # Example sentence batches (1-39)
│   ├── notes-N.tsv                # Study notes batches (1-39)
│   ├── etymology-all.tsv          # Consolidated etymology
│   ├── examples-all.tsv           # Consolidated examples
│   ├── notes-all.tsv              # Consolidated notes
│   └── master-all.tsv             # All columns combined
├── prompts/topik2/                # TOPIK 2-specific prompts (pending)
│   ├── generate-etymology.md
│   ├── generate-examples.md
│   ├── generate-notes.md
│   └── generate-audio.md
├── topik2/                        # Original extraction work
│   ├── data/csv-extra/all.csv    # Raw extracted data with Hanja/Japanese
│   ├── readme.md                 # Extraction documentation
│   └── links.md                  # 39 lesson URLs
└── koreantopik2_*.mp3             # Audio files (pending, 3873 files)
```

## Workflow Plan

### Phase 1: Preparation & Setup

#### 1.1 Create TOPIK 2 Prompts Directory
- [ ] Create `prompts/topik2/` directory
- [ ] Adapt `generate-etymology2.md` → `prompts/topik2/generate-etymology.md`
  - Update input: `input/koreantopik2.tsv`
  - Update batches: 1-39 (instead of 1-19)
  - Update output: `output/topik2/etymology-N.tsv`
- [ ] Adapt `generate-example4.md` → `prompts/topik2/generate-examples.md`
  - Update batch count: 39 batches
  - Update output: `output/topik2/examples-N.tsv`
- [ ] Adapt `generate-notes.md` → `prompts/topik2/generate-notes.md`
  - Update batch count: 39 batches
  - Update output: `output/topik2/notes-N.tsv`
- [ ] Adapt `generate-example4-audio.md` → `prompts/topik2/generate-audio.md`
  - Update file prefix: `koreantopik2_NNNN.mp3`
  - Update entry count: 3873 files

#### 1.2 Pre-split Input File
- [ ] Create `output/topik2/` directory
- [ ] Split `input/koreantopik2.tsv` into batches:
  - [ ] `input/koreantopik2-batch-1.tsv` (entries 1-100)
  - [ ] `input/koreantopik2-batch-2.tsv` (entries 101-200)
  - [ ] ... (batches 3-38, 100 entries each)
  - [ ] `input/koreantopik2-batch-39.tsv` (entries 3801-3873, 73 entries)

### Phase 2: Enhancement Generation

#### 2.1 Etymology Enhancement
Generate Hanja and Japanese cognates for Sino-Korean words.

**Format**: `number, korean, etymology`
- Example: `32	가정	假定 / 仮定`

**Progress** (39 batches):
- [ ] `output/topik2/etymology-1.tsv` (words 1-100)
- [ ] `output/topik2/etymology-2.tsv` (words 101-200)
- [ ] ... (batches 3-38)
- [ ] `output/topik2/etymology-39.tsv` (words 3801-3873)
- [ ] Consolidate → `output/topik2/etymology-all.tsv`

#### 2.2 Example Sentences
Natural Korean example sentences with English translations.

**Format**: `number, korean, example_ko, example_en`

**Strategy**: Use subagents for parallel processing (39 independent batches)

**Progress** (39 batches):
- [ ] `output/topik2/examples-1.tsv` (words 1-100)
- [ ] `output/topik2/examples-2.tsv` (words 101-200)
- [ ] ... (batches 3-38)
- [ ] `output/topik2/examples-39.tsv` (words 3801-3873)
- [ ] Consolidate → `output/topik2/examples-all.tsv`

#### 2.3 Study Notes
Related words, antonyms, honorific pairs, etc.

**Format**: `number, korean, notes`

**Progress** (39 batches):
- [ ] `output/topik2/notes-1.tsv` (words 1-100)
- [ ] `output/topik2/notes-2.tsv` (words 101-200)
- [ ] ... (batches 3-38)
- [ ] `output/topik2/notes-39.tsv` (words 3801-3873)
- [ ] Consolidate → `output/topik2/notes-all.tsv`

#### 2.4 Audio Generation
Korean pronunciation audio using edge-tts.

**Naming**: `koreantopik2_0001.mp3` through `koreantopik2_3873.mp3`

**Strategy**: Generate in chunks to avoid timeouts (e.g., 10 batches = 1000 files at a time)

**Progress**:
- [ ] Batches 1-10 (files 0001-1000)
- [ ] Batches 11-20 (files 1001-2000)
- [ ] Batches 21-30 (files 2001-3000)
- [ ] Batches 31-39 (files 3001-3873)

### Phase 3: Consolidation & Import

#### 3.1 Consolidate Outputs
- [ ] Create `output/topik2/etymology-all.tsv` (merge batches 1-39)
- [ ] Create `output/topik2/examples-all.tsv` (merge batches 1-39)
- [ ] Create `output/topik2/notes-all.tsv` (merge batches 1-39)

#### 3.2 Create Master File
- [ ] Combine all columns: `number, korean, etymology, english, example_ko, example_en, notes, audio`
- [ ] Output: `output/topik2/master-all.tsv`
- [ ] Validate: 3873 entries (+ header)

#### 3.3 Manual Review & Google Sheets
- [ ] Upload to Google Drive
- [ ] Manual review and corrections
- [ ] Final export for Anki

#### 3.4 Anki Import
- [ ] Create Anki deck: "Korean TOPIK 2"
- [ ] Import vocabulary with all enhancements
- [ ] Verify audio files work
- [ ] Begin studying

### Phase 4: Maintenance

#### 4.1 Fix Workflow
- [ ] Create `prompts/topik2/generate-fix.md` (or reuse existing)
- [ ] Track corrections during Anki practice
- [ ] Generate replacement audio with `_fix` suffix
- [ ] Update Anki cards as needed

## File Format Details

### Input Format
`input/koreantopik2.tsv` (3 columns):
```
number	korean	english
1	-가	professional
2	가까이	nearby
```

### Output Formats

**Etymology** (3 columns):
```
number	korean	etymology
1	-가	-家 / -家
5	가능	可能 / 可能
```

**Examples** (4 columns):
```
number	korean	example_ko	example_en
1	-가	그는 유명한 사진가입니다.	He is a famous photographer.
```

**Notes** (3 columns):
```
number	korean	notes
5	가능	불가능
```

**Master file** (8 columns):
```
number	korean	etymology	english	example_ko	example_en	notes	audio
```

## Key Differences from TOPIK 1

| Aspect | TOPIK 1 | TOPIK 2 |
|--------|---------|---------|
| Total words | 1,847 | 3,873 |
| Batches | 19 | 39 |
| Last batch size | 47 entries | 73 entries |
| Processing time | ~X hours | ~2X hours (est.) |
| Audio files | 1,847 MP3s | 3,873 MP3s |
| Vocabulary level | Beginner | Intermediate-Advanced |
| File prefix | `koreantopik1_` | `koreantopik2_` |
| Output directory | `output/` | `output/topik2/` |

## Strategy & Recommendations

### Processing Strategy
1. **Start small**: Process batches 1-2 end-to-end to validate workflow
2. **Parallel processing**: Use subagents for example generation (39 agents in parallel)
3. **Checkpointing**: Commit outputs after completing each enhancement type
4. **Resource monitoring**: TOPIK 2 is advanced vocabulary, may need more tokens per word

### Audio Generation Strategy
- Generate in chunks (10 batches = ~1000 files at a time)
- Verify file creation after each chunk
- Avoid overwhelming edge-tts service

### Validation Checkpoints
After each phase:
- [ ] Verify file count matches expected batch count
- [ ] Check TSV formatting (proper tabs, no CSV issues)
- [ ] Spot-check content quality
- [ ] Validate consolidated files have correct line count (3873 + header = 3874 lines)

## Pilot Run Plan

Before full processing, validate workflow with batches 1-2:

1. [ ] Split batches 1-2 from `input/koreantopik2.tsv`
2. [ ] Generate etymology for batches 1-2
3. [ ] Generate examples for batches 1-2
4. [ ] Generate notes for batches 1-2
5. [ ] Generate audio for batches 1-2 (200 MP3 files)
6. [ ] Review quality and adjust prompts if needed
7. [ ] If successful, proceed with full 39-batch processing

## Reference Links

- Original vocabulary source: [TOPIK 2 Complete List](https://www.koreantopik.com/2024/09/complete-topik-2-vocabulary-list-3900.html)
- Individual lesson links: See [topik2/links.md](topik2/links.md)
- Extraction documentation: [topik2/readme.md](topik2/readme.md)
- TOPIK 1 completed work: [topik1/readme.md](topik1/readme.md)

---

**Next step**: Begin Phase 1.2 - Split `input/koreantopik2.tsv` into 39 batch files
