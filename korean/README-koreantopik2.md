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
│   └── koreantopik2-batch-N.tsv   # Pre-split batches (1-39, pending)
├── output/koreantopik2/           # TOPIK 2 enhancement outputs (pending)
│   ├── etymology-N.tsv            # Etymology batches (1-39)
│   ├── examples-N.tsv             # Example sentence batches (1-39)
│   ├── notes-N.tsv                # Study notes batches (1-39)
│   ├── etymology-all.tsv          # Consolidated etymology
│   ├── examples-all.tsv           # Consolidated examples
│   ├── notes-all.tsv              # Consolidated notes
│   ├── master-all.tsv             # All columns combined
│   └── audio/                     # Audio files directory
│       └── koreantopik2_*.mp3     # Audio files (3873 files)
├── prompts/
│   ├── requirements-etymology.md  # Etymology requirements (shared)
│   ├── requirements-example.md    # Example requirements (shared)
│   ├── requirements-notes.md      # Notes requirements (shared)
│   └── koreantopik2/              # TOPIK 2-specific generation prompts
│       ├── generate-etymology.md  # Etymology execution strategy
│       ├── generate-examples.md   # Examples execution strategy
│       ├── generate-notes.md      # Notes execution strategy
│       └── generate-audio.md      # Audio generation procedure
├── topik2/                        # Original extraction work
│   ├── data/csv-extra/all.csv     # Raw extracted data with Hanja/Japanese
│   ├── readme.md                  # Extraction documentation
│   └── links.md                   # 39 lesson URLs
└── scripts/
    ├── generate-audio.py          # Audio generation script
    └── generate-audio-verify.py   # Audio verification script
```

## Workflow Plan

### Phase 1: Preparation & Setup

#### 1.1 Create TOPIK 2 Prompts Directory
- [x] Create `prompts/koreantopik2/` directory
- [x] Create `prompts/koreantopik2/generate-etymology.md`
  - References: `prompts/requirements-etymology.md` (shared)
  - Input: `input/koreantopik2-batch-N.tsv` (39 batches)
  - Output: `output/koreantopik2/etymology-N.tsv`
  - Strategy: Subagent-based parallel execution
- [x] Create `prompts/koreantopik2/generate-examples.md`
  - References: `prompts/requirements-example.md` (shared)
  - Input: `input/koreantopik2-batch-N.tsv` (39 batches)
  - Output: `output/koreantopik2/examples-N.tsv`
  - Strategy: Subagent-based parallel execution
- [x] Create `prompts/koreantopik2/generate-notes.md`
  - References: `prompts/requirements-notes.md` (shared)
  - Input 1: `input/korean.tsv` (5720 words for cross-referencing)
  - Input 2: `input/koreantopik2-batch-N.tsv` (batch files)
  - Output: `output/koreantopik2/notes-N.tsv`
  - Strategy: Two-step input (vocab reference + explicit batch)
- [x] Create `prompts/koreantopik2/generate-audio.md`
  - Input: `output/koreantopik2/examples-all.tsv`
  - Output: `output/koreantopik2/audio/koreantopik2_NNNN.mp3`
  - Uses: `scripts/generate-audio.py`

#### 1.2 Pre-split Input File
- [x] Vocabulary reference: `input/korean.tsv` (already exists)
  - Contains: 5720 Korean words (TOPIK 1 + TOPIK 2)
  - Format: Single column, one word per line, no header
  - Used by notes generation for cross-referencing
- [x] Create `output/koreantopik2/` directory
- [x] Split `input/koreantopik2.tsv` into batches:
  - [x] `input/koreantopik2-batch-1.tsv` through `input/koreantopik2-batch-39.tsv`
  - Batches 1-38: 100 entries each (+ header)
  - Batch 39: 73 entries (entries 3801-3873, + header)
  - Total: 3873 entries verified

### Phase 2: Enhancement Generation

#### 2.1 Etymology Enhancement
Generate Hanja and Japanese cognates for Sino-Korean words.

**Format**: `number, korean, etymology`
- Example: `32	가정	假定 / 仮定`

**Progress** (39 batches):
- [ ] `output/koreantopik2/etymology-1.tsv` (words 1-100)
- [ ] `output/koreantopik2/etymology-2.tsv` (words 101-200)
- [ ] ... (batches 3-38)
- [ ] `output/koreantopik2/etymology-39.tsv` (words 3801-3873)
- [ ] Consolidate → `output/koreantopik2/etymology-all.tsv`

#### 2.2 Example Sentences
Natural Korean example sentences with English translations.

**Format**: `number, korean, example_ko, example_en`

**Strategy**: Use subagents for parallel processing (39 independent batches)

**Progress** (39 batches):
- [ ] `output/koreantopik2/examples-1.tsv` (words 1-100)
- [ ] `output/koreantopik2/examples-2.tsv` (words 101-200)
- [ ] ... (batches 3-38)
- [ ] `output/koreantopik2/examples-39.tsv` (words 3801-3873)
- [ ] Consolidate → `output/koreantopik2/examples-all.tsv`

#### 2.3 Study Notes
Related words, antonyms, honorific pairs, etc.

**Format**: `number, korean, notes`

**Strategy**: Two-step input for better cross-referencing
- Input 1: Vocabulary reference (`input/korean.tsv` - 5720 words: TOPIK 1+2)
- Input 2: Batch file (`input/koreantopik2-batch-N.tsv` - 100 entries)
- Output: Only entries from batch file
- Rationale: Vocab reference enables finding antonyms/pairs across all TOPIK vocabulary

**Progress** (39 batches):
- [ ] `output/koreantopik2/notes-1.tsv` (words 1-100)
- [ ] `output/koreantopik2/notes-2.tsv` (words 101-200)
- [ ] ... (batches 3-38)
- [ ] `output/koreantopik2/notes-39.tsv` (words 3801-3873)
- [ ] Consolidate → `output/koreantopik2/notes-all.tsv`

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
- [ ] Create `output/koreantopik2/etymology-all.tsv` (merge batches 1-39)
- [ ] Create `output/koreantopik2/examples-all.tsv` (merge batches 1-39)
- [ ] Create `output/koreantopik2/notes-all.tsv` (merge batches 1-39)

#### 3.2 Create Master File
- [ ] Combine all columns: `number, korean, etymology, english, example_ko, example_en, notes, audio`
- [ ] Output: `output/koreantopik2/master-all.tsv`
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
| Output directory | `output/` | `output/koreantopik2/` |
| Prompts directory | `prompts/` | `prompts/koreantopik2/` |
| Requirements | `prompts/requirements-*.md` | Same (shared) |

## Strategy & Recommendations

### Processing Strategy
1. **Start small**: Process batches 1-2 end-to-end to validate workflow
2. **Parallel processing**: Use subagents for all enhancement types (39 agents in parallel)
   - **Etymology**: Each agent reads batch file (100 entries)
   - **Examples**: Each agent reads batch file (100 entries)
   - **Notes**: Each agent reads vocab reference (5720 words) + batch file (100 entries)
3. **Checkpointing**: Commit outputs after completing each enhancement type
4. **Resource monitoring**: TOPIK 2 is advanced vocabulary, may need more tokens per word
5. **Requirements reuse**: All prompts reference shared `requirements-*.md` files

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
