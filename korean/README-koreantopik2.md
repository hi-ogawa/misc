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
- [x] Prompts directory created (`prompts/koreantopik2/`)
- [x] Batch splitting (39 batches of ~100 words)
- [x] Etymology enhancement (all batches → `etymology-all.tsv`)
- [x] Example sentences generation (all batches → `examples-all.tsv`)
- [x] Study notes generation (all batches → `notes-all.tsv`)

### Pending
- [ ] Anki import

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

#### 2.4 Audio Generation (Dual Audio) ✅

**Prompt**: `prompts/koreantopik2/generate-audio-dual.md`

**Two audio types**:
- **Vocabulary audio** (`korean` field): Isolated word/phrase pronunciation
- **Example audio** (`example_ko` field): Example sentence pronunciation

**Progress**:
- [x] Generate vocabulary audio (3,873 files) → `koreantopik2_korean_*.mp3`
- [x] Generate example audio (3,873 files) → `koreantopik2_example_ko_*.mp3`
- [x] Total: 7,746 MP3 files (~123MB) in `output/koreantopik2/audio/`

### Phase 3: Consolidation & Import

#### 3.1 Consolidate Outputs ✅
- [x] Create `output/koreantopik2/etymology-all.tsv` (merge batches 1-39) - 3,874 lines (3,873 + header)
- [x] Create `output/koreantopik2/examples-all.tsv` (merge batches 1-39) - 3,874 lines (3,873 + header)
- [x] Create `output/koreantopik2/notes-all.tsv` (merge batches 1-39) - 3,874 lines (3,873 + header)

#### 3.2 Create Anki Import File ✅

**Goal**: Combine all enhancement outputs into a single TSV file ready for Anki import.

**Input files**:
- `input/koreantopik2.tsv` (base: number, korean, english)
- `output/koreantopik2/etymology-all.tsv` (etymology column)
- `output/koreantopik2/examples-all.tsv` (example_ko, example_en columns)
- `output/koreantopik2/notes-all.tsv` (notes column)
- Audio files: `output/koreantopik2/audio/koreantopik2_*.mp3`

**Output**: `output/koreantopik2/koreantopik2_anki_import.tsv`

**Columns** (9 total):
```
number	korean	english	example_ko	example_en	etymology	notes	korean_audio	example_ko_audio
```

**Sample row**:
```
1	-가	professional	친구가 의사가 됐어요	My friend became a doctor	-家 / -家	-사, -자, -인	[sound:koreantopik2_korean_0001.mp3]	[sound:koreantopik2_example_ko_0001.mp3]
```

**Note**: This TSV column order matches Anki field order for direct import.

**Audio field formats**:
- `korean_audio`: `[sound:koreantopik2_korean_0001.mp3]` (isolated word pronunciation)
- `example_ko_audio`: `[sound:koreantopik2_example_ko_0001.mp3]` (sentence pronunciation)

**Command**:
```bash
python scripts/create-anki-import.py koreantopik2
```

#### 3.3 Anki Import

**Goal**: Import 3,873 TOPIK 2 vocabulary entries into Anki with dual audio support.

**⚠️ ACTION REQUIRED: Deck Organization Decision** (UNDECIDED - choose before import):
- **Option A**: Single deck - merge with TOPIK 1 (e.g., "Korean Vocabulary")
- **Option B**: Separate deck - keep TOPIK 2 separate (e.g., "Korean TOPIK 2")
- **Option C**: Hierarchical - use deck hierarchy (e.g., "Korean::TOPIK 2")

**Prerequisites**:
1. Anki note type "Korean Vocabulary" with fields:
   - number
   - korean
   - english
   - example_ko
   - example_en
   - etymology
   - notes
   - korean_audio
   - example_ko_audio

2. Audio files copied to Anki media folder:
   ```bash
   cp output/koreantopik2/audio/koreantopik2_korean_*.mp3 ~/.local/share/Anki2/사용자\ 1/collection.media/
   cp output/koreantopik2/audio/koreantopik2_example_ko_*.mp3 ~/.local/share/Anki2/사용자\ 1/collection.media/
   ```

**Import Steps**:

1. **Backup Anki collection first!**
   - File → Export → Full deck with media
   - Save as: `koreantopik2_backup_YYYY-MM-DD.apkg`

2. **Copy audio files to Anki media** (see Prerequisites above)

3. **Import TSV file**:
   - File → Import
   - Select: `output/koreantopik2/koreantopik2_anki_import.tsv`
   - **Type**: Korean Vocabulary
   - **Deck**: (Select the deck you chose above)
   - **Update existing notes when first field matches**: ✅ CHECKED (if updating)
   - **Allow HTML in fields**: ✅ CHECKED
   - **Fields separated by**: Tab

4. **Map Fields** (verify the mapping):

   **IMPORTANT**: TSV column order ≠ Anki field order!

   Anki Field → TSV Column:
   ```
   number         → Field 1
   korean         → Field 2
   english        → Field 3
   example_ko     → Field 4
   example_en     → Field 5
   etymology      → Field 6
   notes          → Field 7
   korean_audio   → Field 8
   example_ko_audio → Field 9
   ```

5. **Verify Import Preview**:
   - Check that a few sample cards look correct
   - Verify audio fields show `[sound:koreantopik2_korean_NNNN.mp3]` format
   - Should show: 3,873 cards to be added/updated

6. **Click "Import"**

7. **Verify Results**:
   - Should show: "3873 notes added" (or updated)
   - Open a few random cards and test both audio buttons work correctly
   - Front: Korean word + vocabulary audio
   - Back: Translation + both audio buttons (vocabulary + example)

**Checklist**:
- [ ] Backup Anki collection
- [ ] Copy 7,746 audio files to Anki media folder
- [ ] Verify audio files copied (3,873 × 2 = 7,746)
- [ ] Import TSV file with correct field mapping
- [ ] Test sample cards for audio playback
- [ ] Begin studying!

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

**Sample row**:
```
1	-가	professional	친구가 의사가 됐어요	My friend became a doctor	-家 / -家	-사, -자, -인	[sound:koreantopik2_korean_0001.mp3]	[sound:koreantopik2_example_ko_0001.mp3]
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
| Audio files | 3,694 MP3s (korean + example_ko) | 7,746 MP3s (korean + example_ko) |
| Vocabulary level | Beginner | Intermediate-Advanced |
| File naming | `koreantopik1_korean_NNNN.mp3`<br>`koreantopik1_example_ko_NNNN.mp3` | `koreantopik2_korean_NNNN.mp3`<br>`koreantopik2_example_ko_NNNN.mp3` |
| Output directory | `output/koreantopik1/` | `output/koreantopik2/` |

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
