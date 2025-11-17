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

### Completed
- [x] Prompts directory created (`prompts/koreantopik2/`)
- [x] Batch splitting (39 batches of ~100 words)

### Pending
- [ ] Etymology enhancement
- [ ] Example sentences generation
- [ ] Study notes generation
- [ ] Audio generation
- [ ] Consolidation and Anki import

## Project Structure

```
korean/
├── input/
│   ├── korean.tsv                 # Vocabulary reference (5720 words: TOPIK 1+2)
│   ├── koreantopik2.tsv           # Base TOPIK 2 file (3873 entries)
│   └── koreantopik2-batch-N.tsv   # Pre-split batches (1-39)
├── output/koreantopik2/           # TOPIK 2 enhancement outputs
│   ├── etymology-N.tsv            # Etymology batches (1-39)
│   ├── examples-N.tsv             # Example sentence batches (1-39)
│   ├── notes-N.tsv                # Study notes batches (1-39)
│   ├── etymology-all.tsv          # Consolidated etymology
│   ├── examples-all.tsv           # Consolidated examples
│   ├── notes-all.tsv              # Consolidated notes
│   ├── master-all.tsv             # All columns combined
│   └── audio/                     # Audio files directory (flat structure)
│       ├── koreantopik2_korean_*.mp3     # 3,873 vocabulary audio files
│       └── koreantopik2_example_ko_*.mp3 # 3,873 example audio files
├── prompts/
│   ├── requirements-etymology.md  # Etymology requirements (shared)
│   ├── requirements-example.md    # Example requirements (shared)
│   ├── requirements-notes.md      # Notes requirements (shared)
│   └── koreantopik2/              # TOPIK 2-specific generation prompts
│       ├── generate-etymology.md  # Etymology execution strategy
│       ├── generate-examples.md   # Examples execution strategy
│       ├── generate-notes.md      # Notes execution strategy
│       └── generate-audio-dual.md # Dual audio generation (vocab + example)
├── topik2/                        # Original extraction work
│   ├── data/csv-extra/all.csv     # Raw extracted data with Hanja/Japanese
│   ├── readme.md                  # Extraction documentation
│   └── links.md                   # 39 lesson URLs
└── scripts/
    ├── generate-audio.py          # Audio generation script (supports dual audio)
    └── generate-audio-verify.py   # Audio verification script
```

## Workflow Plan

### Phase 1: Preparation & Setup

#### 1.1 Create TOPIK 2 Prompts Directory
- [x] Create `prompts/koreantopik2/` directory with generation prompts:
  - [x] `generate-etymology.md` (references `requirements-etymology.md`)
  - [x] `generate-examples.md` (references `requirements-example.md`)
  - [x] `generate-notes.md` (references `requirements-notes.md`)
  - [x] `generate-audio.md` (uses `scripts/generate-audio.py`)

#### 1.2 Pre-split Input File
- [x] Vocabulary reference: `input/korean.tsv` (5720 words: TOPIK 1+2)
- [x] Create `output/koreantopik2/` directory
- [x] Split into 39 batches: `input/koreantopik2-batch-{1..39}.tsv` (3873 entries verified)

### Phase 2: Enhancement Generation

#### 2.1 Etymology Enhancement

**Prompt**: `prompts/koreantopik2/generate-etymology.md`

**Progress** (39 batches):
- [x] Batches 1-39 → `output/koreantopik2/etymology-N.tsv`
- [x] Consolidate → `output/koreantopik2/etymology-all.tsv`

#### 2.2 Example Sentences

**Prompt**: `prompts/koreantopik2/generate-examples.md`

**Progress** (39 batches):
- [x] Batches 1-39 → `output/koreantopik2/examples-N.tsv`
- [x] Consolidate → `output/koreantopik2/examples-all.tsv`

#### 2.3 Study Notes

**Prompt**: `prompts/koreantopik2/generate-notes.md`

**Progress** (39 batches):
- [x] Batches 1-39 → `output/koreantopik2/notes-N.tsv`
- [x] Consolidate → `output/koreantopik2/notes-all.tsv`

#### 2.4 Audio Generation (Dual Audio)

**Prompt**: `prompts/koreantopik2/generate-audio-dual.md`

**Two audio types**:
- **Vocabulary audio** (`korean` field): Isolated word/phrase pronunciation
- **Example audio** (`example_ko` field): Example sentence pronunciation

**Progress**:
- [ ] Generate vocabulary audio (3,873 files) → `koreantopik2_korean_*.mp3`
- [ ] Generate example audio (3,873 files) → `koreantopik2_example_ko_*.mp3`

### Phase 3: Consolidation & Import

#### 3.1 Consolidate Outputs
- [x] Create `output/koreantopik2/etymology-all.tsv` (merge batches 1-39)
- [x] Create `output/koreantopik2/examples-all.tsv` (merge batches 1-39)
- [x] Create `output/koreantopik2/notes-all.tsv` (merge batches 1-39)

#### 3.2 Create Master File

**Goal**: Combine all enhancement outputs into a single TSV file ready for Anki import.

**Input files**:
- `input/koreantopik2.tsv` (base: number, korean, english)
- `output/koreantopik2/etymology-all.tsv` (etymology column)
- `output/koreantopik2/examples-all.tsv` (example_ko, example_en columns)
- `output/koreantopik2/notes-all.tsv` (notes column)
- Audio files: `output/koreantopik2/audio/koreantopik2_*.mp3`

**Output**: `output/koreantopik2/master-all.tsv`

**Columns** (9 total):
```
number	korean	english	example_ko	example_en	etymology	notes	korean_audio	example_ko_audio
```

**Note**: This TSV column order matches Anki field order for direct import.

**Audio field formats**:
- `korean_audio`: `[sound:koreantopik2_korean_0001.mp3]` (isolated word pronunciation)
- `example_ko_audio`: `[sound:koreantopik2_example_ko_0001.mp3]` (sentence pronunciation)

**Steps**:
1. [ ] Join all TSV files on `number` column
2. [ ] Add `korean_audio` column with format `[sound:koreantopik2_korean_{number:04d}.mp3]`
3. [ ] Add `example_ko_audio` column with format `[sound:koreantopik2_example_ko_{number:04d}.mp3]`
4. [ ] Validate: 3873 entries (+ header = 3874 lines)
5. [ ] Verify all audio file references exist

**Quality checks**:
- All rows must have matching number across all source files
- No missing columns (empty strings are OK)
- Audio file path formats must be exact:
  - Vocabulary: `[sound:koreantopik2_korean_NNNN.mp3]`
  - Example: `[sound:koreantopik2_example_ko_NNNN.mp3]`

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
- [ ] Create `prompts/koreantopik2/generate-fix.md` (adapted from TOPIK 1 version)
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

**Master file** (9 columns):
```
number	korean	english	example_ko	example_en	etymology	notes	korean_audio	example_ko_audio
```

**Note**: Column order matches Anki field order for direct import.

Audio field formats:
- `korean_audio`: `[sound:koreantopik2_korean_0001.mp3]`
- `example_ko_audio`: `[sound:koreantopik2_example_ko_0001.mp3]`

## Key Differences from TOPIK 1

| Aspect | TOPIK 1 | TOPIK 2 |
|--------|---------|---------|
| Total words | 1,847 | 3,873 |
| Batches | 19 | 39 |
| Last batch size | 47 entries | 73 entries |
| Processing time | ~X hours | ~2X hours (est.) |
| Audio files | 1,847 MP3s | 7,746 MP3s (korean + example_ko) |
| Audio structure | Single audio | Dual audio (korean + example_ko) |
| Vocabulary level | Beginner | Intermediate-Advanced |
| File naming | `koreantopik1_NNNN.mp3` | `koreantopik2_korean_NNNN.mp3`<br>`koreantopik2_example_ko_NNNN.mp3` |
| Output directory | `output/` | `output/koreantopik2/` |
| Prompts directory | `prompts/` | `prompts/koreantopik2/` |
| Requirements | `prompts/requirements-*.md` | Same (shared) |

## Strategy & Recommendations

### Subagent Architecture

All enhancement generation uses isolated subagents for clean, parallel processing.

**See `prompts/subagent-management.md` for complete guidelines.**

### Processing Strategy
1. **Start small**: Process batches 1-2 end-to-end to validate workflow
2. **Parallel processing**: Use subagents for all enhancement types (39 agents in parallel)
   - **Etymology**: Each agent reads batch file (100 entries)
   - **Examples**: Each agent reads batch file (100 entries)
   - **Notes**: Each agent reads vocab reference (5720 words) + batch file (100 entries)
3. **Checkpointing**: Commit outputs after completing each enhancement type
4. **Resource monitoring**: TOPIK 2 is advanced vocabulary, may need more tokens per word
5. **Requirements reuse**: All prompts reference shared `requirements-*.md` files

### Audio Generation Strategy (Dual Audio)
- **Two sets**: Vocabulary audio (isolated) + Example audio (contextual)
- Generate in chunks with concurrency (5-10 concurrent tasks recommended)
- Verify file creation after each generation
- Edge TTS is free and reliable, but respect rate limits
- Total storage: ~100-120MB for 7,746 MP3 files

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

## Prompt Architecture

**Separation of concerns:**
- **Requirements files** (`prompts/requirements-*.md`): Define WHAT makes good content
  - Shared across TOPIK 1 and TOPIK 2
  - Focus on quality criteria
  - Dataset-agnostic
- **Generation files** (`prompts/koreantopik2/generate-*.md`): Define HOW to execute
  - TOPIK 2 specific (batch counts, file paths)
  - Execution strategy (subagents, parallelization)
  - Input/output formats

**Benefits:**
- Clean reuse of quality requirements
- Easy to adapt for future datasets
- Clear separation between quality and execution

---

**Next step**: Begin Phase 1.2 - Split `input/koreantopik2.tsv` into 39 batch files
