# Update TOPIK 1 Deck - Example Sentence Regeneration (v3)

## Goal

Regenerate all 1,847 example sentences using updated `requirements-example.md` that produces richer, multi-clause sentences.

## Analysis Results

**Before (old examples)**:
- Mean: 3.81 words, 11.98 chars
- Batch 7 was problematic: 3.04 words (bare minimum style)

**After (v3 examples)**:
- Mean: 5.71 words, 17.02 chars (+50%)
- Consistent across batches: 5.23-6.09 words
- Multi-clause sentences with connectives (-서, -(으)니까, -고, etc.)

## Files

**Source files**:
- Existing anki import: `output/tmp/koreantopik1_anki_import.tsv` (1848 lines)
- New v3 examples: `output/examples-v3-combined.tsv` (1848 lines)

**Output file**:
- `output/koreantopik1/koreantopik1_anki_import_v3.tsv`

## Anki Import Format

**Columns** (9 total, matches TOPIK 2 structure):
```
number	korean	english	example_ko	example_en	etymology	notes	korean_audio	example_ko_audio
```

**Sample row**:
```
1	가게	store	동네 가게에서 우유를 사고 집에 돌아왔어요	I bought milk at the neighborhood store and came home.	상점	[sound:koreantopik1_korean_0001.mp3]	[sound:koreantopik1_example_ko_0001.mp3]
```

**Note**: TOPIK 1 uses unprefixed numbers (1, 2, 3...) while TOPIK 2 uses prefixed (`koreantopik2_1`).

## Implementation Plan

- [x] Phase 1: Generate new example sentences (19 batches, parallel)
- [x] Phase 2: Combine batch files into `examples-v3-combined.tsv`
- [x] Phase 3: Analyze new examples (confirmed 5.71 avg words)
- [x] Phase 4: Merge v3 examples into anki import file
- [x] Phase 5: Generate new audio for v3 examples (1847 files, 116 min total, 44MB)
- [ ] Phase 6: Copy audio to Anki media folder
- [ ] Phase 7: Import updated TSV into Anki

### Phase 4: Merge v3 examples into anki import

Merge new `example_ko` and `example_en` columns from v3 into existing anki import (preserving number, korean, english, etymology, notes, audio columns).

```bash
python scripts/merge-examples.py \
  --base output/tmp/koreantopik1_anki_import.tsv \
  --examples output/examples-v3-combined.tsv \
  --output output/koreantopik1/koreantopik1_anki_import_v3.tsv
```

### Phase 5: Generate new audio for v3 examples

Since example sentences changed, need to regenerate example audio only (vocabulary audio unchanged).

```bash
python scripts/generate-audio.py \
  --input output/koreantopik1/koreantopik1_anki_import_v3.tsv \
  --field example_ko \
  --prefix koreantopik1_example_ko_ \
  --output output/koreantopik1/audio \
  --concurrency 5 \
  --force
```

**Expected output**: 1,847 files `koreantopik1_example_ko_0001.mp3` to `koreantopik1_example_ko_1847.mp3`

**Duration**: ~30-60 min at concurrency=5

**Verification**:
```bash
# Count files
ls output/koreantopik1/audio/koreantopik1_example_ko_*.mp3 | wc -l
# Expected: 1847

# Verify MP3 integrity
python scripts/generate-audio-verify.py --output output/koreantopik1/audio

# Check duration stats
python scripts/generate-audio-stats.py --output output/koreantopik1/audio
```

### Phase 6: Copy audio to Anki

```bash
cp output/koreantopik1/audio/koreantopik1_example_ko_*.mp3 ~/.local/share/Anki2/사용자\ 1/collection.media/
```

### Phase 7: Import into Anki

1. Open Anki
2. File -> Import -> select `output/koreantopik1/koreantopik1_anki_import.tsv`
3. Ensure "Update existing notes when first field matches" is checked
4. Import
