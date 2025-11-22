# Regenerate TOPIK 1 Example Sentences (v3)

## Goal

Regenerate all 1,847 example sentences using the updated `prompts/requirements-example.md` that produces:
- Multi-clause sentences with diverse connectives (-서, -(으)니까, -고, -을 때, -지만, -(으)려고, etc.)
- Concrete, visualizable contexts (specific locations, times, objects)
- Distinctive usage that forces vocabulary evaluation
- Explicit subjects/objects for pedagogical clarity

## Input/Output Files

**Input**:
- Vocabulary: `input/koreantopik1.tsv` (1,847 entries + header = 1,848 lines)
- Columns: `number`, `korean`, `english`

**Output**:
- Batch files: `output/koreantopik1/examples-1.tsv` to `examples-19.tsv`
  - Batches 1-18: 100 entries each
  - Batch 19: 47 entries (1,801-1,847)
- Combined: `output/koreantopik1/examples-all.tsv`
- Columns: `number`, `korean`, `example_ko`, `example_en`

**Final Anki Import**:
- File: `output/koreantopik1/koreantopik1_anki_import_v3.tsv`
- Columns (9 total): `number`, `korean`, `english`, `example_ko`, `example_en`, `etymology`, `notes`, `korean_audio`, `example_ko_audio`

**Note**: Header line commented with `#` for Anki import compatibility.

## Implementation Plan

### Phase 0: Pre-split Input File (PREREQUISITE)

Split `input/koreantopik1.tsv` into 19 batch files for parallel processing.

```bash
python scripts/split-batches.py \
  --input input/koreantopik1.tsv \
  --output-dir input \
  --prefix koreantopik1-batch- \
  --batch-size 100
```

**Output**:
- `input/koreantopik1-batch-1.tsv` to `input/koreantopik1-batch-19.tsv`
- Each with header row + entries (batches 1-18: 100 entries, batch 19: 47 entries)

### Phase 1: Generate Example Sentences

**Step 1: Generate batches (19 batches)**

Use subagents with fresh context (see `prompts/subagent-management.md`)

**Per-batch task**:
1. Read `prompts/requirements-example.md` (quality requirements)
2. Read `input/koreantopik1-batch-N.tsv` (assigned batch ONLY)
3. Generate examples following ALL requirements
4. Write `output/koreantopik1/examples-N.tsv`

**Launch agents** (can run in parallel or sequential):
```
Launch 19 agents, each processing one batch independently
```

**Critical**:
- Each agent reads ONLY requirements + assigned batch
- DO NOT read existing output files
- Generate from scratch for consistency

**Step 2: Combine batch files**

```bash
# Extract header from first batch
head -1 output/koreantopik1/examples-1.tsv > output/koreantopik1/examples-all.tsv

# Concatenate all batch files (skip headers)
for i in {1..19}; do
  tail -n +2 output/koreantopik1/examples-$i.tsv >> output/koreantopik1/examples-all.tsv
done
```

**Result**: `examples-all.tsv` with 1,847 entries + header

**Verify**:
```bash
wc -l output/koreantopik1/examples-all.tsv
# Expected: 1848 (1 header + 1847 entries)
```

**Note**: Consider creating `scripts/combine-batches.py` for cleaner workflow.

**Step 3: Analyze quality**

```bash
python scripts/analyze-examples.py \
  --input output/koreantopik1/examples-all.tsv
```

**Check for**:
- Average words per sentence (target: 5-7)
- Connective diversity (not just -서/-(으)니까)
- Generic pattern detection
- Subject/object presence

### Phase 2: Generate Audio for New Examples

**IMPORTANT: Audio filename versioning**
- When updating example sentences, audio filenames MUST include version suffix
- This forces Anki to recognize them as new media files
- Without version suffix, Anki keeps playing old audio even when text changes
- Format: `koreantopik1_example_ko_NNNN_v3.mp3` (note the `_v3` suffix)

**Step 1: Generate audio files**

Regenerate only example audio (vocabulary audio unchanged).

```bash
python scripts/generate-audio.py \
  --input output/koreantopik1/koreantopik1_anki_import_v3.tsv \
  --field example_ko \
  --prefix koreantopik1_example_ko_ \
  --suffix _v3 \
  --output output/koreantopik1/audio \
  --concurrency 5 \
  --force
```

**Output**: 1,847 files `koreantopik1_example_ko_0001_v3.mp3` to `koreantopik1_example_ko_1847_v3.mp3`
**Duration**: ~30-60 min at concurrency=5
**Size**: ~35-45MB

**Step 2: Verify audio quality**

```bash
# Count files
ls output/koreantopik1/audio/koreantopik1_example_ko_*_v3.mp3 | wc -l
# Expected: 1847

# Verify MP3 integrity
python scripts/generate-audio-verify.py \
  --input output/koreantopik1/audio

# Check duration stats
python scripts/generate-audio-stats.py \
  --input output/koreantopik1/audio \
  --pattern "koreantopik1_example_ko_*_v3.mp3"
```

**Step 3: Create zip archive**

```bash
cd output/koreantopik1/audio
zip -r ../koreantopik1_example_ko_v3_audio.zip koreantopik1_example_ko_*_v3.mp3
cd -
```

**Result**: `output/koreantopik1/koreantopik1_example_ko_v3_audio.zip`

---

## Anki Import (Manual)

### Phase 3: Merge into Anki Import File

Merge new examples with existing deck data (preserving etymology, notes, vocabulary audio):

```bash
python scripts/merge-examples.py \
  --base output/koreantopik1/koreantopik1_anki_import_v2.tsv \
  --examples output/koreantopik1/examples-all.tsv \
  --output output/koreantopik1/koreantopik1_anki_import_v3.tsv
```

**Note**: Uses v2 as base to preserve all current deck edits (etymology, notes, audio references).

**IMPORTANT**: After merging, update audio references in the TSV file:
- Find: `[sound:koreantopik1_example_ko_NNNN.mp3]`
- Replace: `[sound:koreantopik1_example_ko_NNNN_v3.mp3]`

This ensures Anki recognizes the new audio files.

### Phase 4: Import into Anki

1. Backup current deck (export as .apkg or .txt)
2. Copy audio files to Anki media folder (use `*_v3.mp3` pattern)
3. Import `koreantopik1_anki_import_v3.tsv` into Anki
4. Verify examples and audio playback

**Note**: The TSV file must reference the versioned audio filenames in the `example_ko_audio` column (e.g., `[sound:koreantopik1_example_ko_0001_v3.mp3]`)

---

## Summary Checklist

- [ ] Phase 0: Pre-split input file into 19 batches
- [ ] Phase 1: Generate example sentences
  - [ ] Step 1: Generate batches (19 subagents)
  - [ ] Step 2: Combine batch files
  - [ ] Step 3: Analyze quality
- [ ] Phase 2: Generate audio for new examples
  - [ ] Step 1: Generate audio files (1,847 MP3s, ~30-60min)
  - [ ] Step 2: Verify audio quality
  - [ ] Step 3: Create zip archive
- [ ] Phase 3: Merge into Anki import file (update audio references)
- [ ] Phase 4: Import into Anki (manual)

**Estimated Total Time**: 1-2 hours (mostly audio generation)
