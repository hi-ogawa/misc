# Generate Audio for Korean Examples (v2)

## Goal
Generate audio pronunciation files for all `example_ko` entries in the updated vocabulary list using Microsoft Edge TTS with optional async concurrency.

## Status
⏳ **PLANNED** - Ready to generate

## Context
This is a regeneration of audio files following updates to example sentences. The previous version (generate-audio.md) generated 1,847 files sequentially in ~20 minutes. This version uses an async subprocess implementation with configurable concurrency for faster generation.

## Input
- Source: `output/examples-v2-all.tsv`
- Columns: number, korean, example_ko, example_en
- Total entries: 1,847 examples
- Changes: Updated example sentences with improved quality and consistency

## Output
- Location: `output/audio-v2/` (new directory to avoid overwriting v1)
- Format: `0001.mp3` to `1847.mp3` (4-digit padded)
- Total files: 1,847
- Voice: `ko-KR-SunHiNeural` (female)

## Generate

See `--help` for options:

```bash
python scripts/generate-audio.py \
  --input output/examples-v2-all.tsv \
  --output output/audio-v2 \
  --concurrency 5
```

## Verify generation

```bash
# Count generated files
ls output/audio-v2/*.mp3 | wc -l

# Check file sizes (should be ~15KB average)
du -sh output/audio-v2/

# Verify MP3 integrity using ffprobe
python scripts/generate-audio-verify.py --output output/audio-v2

# Verify specific range
python scripts/generate-audio-verify.py --output output/audio-v2 --start 1 --end 100

# Analyze audio duration statistics
python scripts/generate-audio-stats.py --output output/audio-v2
============================================================
AUDIO DURATION STATISTICS
============================================================
Files analyzed:  1847/1847
Total duration:  5471.83s (91.20 minutes)
Average:         2.96s
Median:          2.93s
Min:             1.73s
Max:             5.59s
Std Dev:         0.40s

Percentiles:
  10th: 2.50s
  25th: 2.69s
  75th: 3.22s
  90th: 3.46s
```

**Verification Strategy**:
- Uses `ffprobe` (from ffmpeg) to validate each MP3 file
- Checks: valid format, audio streams, duration > 0
- Shows progress for each file verified (✓ for valid, ✗ for broken)
- Reports broken/corrupted files with error details
- Script: `scripts/generate-audio-verify.py` (see `--help` for options)
- Supports range filtering (`--start`, `--end`)
- All files should pass validation for successful generation

**Statistics Analysis**:
- Script: `scripts/generate-audio-stats.py` (see `--help` for options)
- Provides: total duration, average, median, min, max, std dev, percentiles
- Identifies outliers (files >10s or <1s)
- Expected stats for 1847 files:
  - Average: ~3s per file
  - Total duration: ~90 minutes
  - Range: 1.5s - 6s (typical Korean sentence lengths)

## Post-Processing Steps

### 1. Rename files with prefix
```bash
cd output/audio-v2
for file in [0-9][0-9][0-9][0-9].mp3; do
  mv "$file" "koreantopik1_v2_$file"
done
```

Result: `0001.mp3` → `koreantopik1_v2_0001.mp3`

### 2. Create zip archive
```bash
cd output/audio-v2
zip -r ../koreantopik1_v2_audio.zip koreantopik1_v2_*.mp3
```

Result: `output/koreantopik1_v2_audio.zip` (24M, 1847 files)

### 3. Update Anki cards

**Context:**
- Existing Anki cards have progress/notes that should be preserved
- Need to update 3 columns: `example_ko`, `example_en`, `example_ko_audio`
- Keep existing columns: `number`, `korean`, `english`, `etymology`, `notes`
- Anki can match and update existing notes using `number` as the anchor field

**Steps:**

1. Generate update TSV with 4 columns (number + 3 fields to update):
```bash
python scripts/generate-anki-update.py \
  --input output/examples-v2-all.tsv \
  --output output/anki-update-v2.tsv
```

Output format (`output/anki-update-v2.tsv`):
```
number	example_ko	example_en	example_ko_audio
1	가게에 자주 가요	I often go to the store	[sound:koreantopik1_v2_0001.mp3]
2	가격이 너무 비싸요	The price is too expensive	[sound:koreantopik1_v2_0002.mp3]
```

2. Copy audio files to Anki media directory:
```bash
cp output/audio-v2/koreantopik1_v2_*.mp3 ~/.local/share/Anki2/"User 1"/collection.media/
```

3. Import update TSV in Anki:
- File → Import → Select `output/anki-update-v2.tsv`
- **Important settings:**
  - Field separator: Tab
  - **Field 1 (number): Set as "Field used to match existing notes"**
  - Map fields: `number` → number, `example_ko` → example_ko, `example_en` → example_en, `example_ko_audio` → example_ko_audio
  - Check "Update existing notes when first field matches"
  - Import

Anki will find existing cards by `number` and update only the 3 mapped fields, preserving all other data (korean, english, etymology, notes, review history).

## Troubleshooting

### Quality Check
Listen to random samples:
```bash
# Play random files to verify quality
mpv output/audio-v2/0001.mp3
mpv output/audio-v2/0500.mp3
mpv output/audio-v2/1000.mp3
```

## Notes
- Edge TTS is free with no API key required
- Default is sequential (concurrency=1) - safe and reliable
- Concurrency uses async subprocess for efficient I/O
- Script supports resuming (skips existing files)
- Ctrl-C interruption is handled gracefully
- Monitor for socket timeouts if using high concurrency
- Can adjust concurrency based on network stability
