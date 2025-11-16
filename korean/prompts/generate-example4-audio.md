# Generate Audio for Korean Examples (v2)

## Goal
Generate audio pronunciation files for all `example_ko` entries in the updated vocabulary list using Microsoft Edge TTS with parallelization.

## Status
⏳ **PLANNED** - Ready to generate

## Context
This is a regeneration of audio files following updates to example sentences. The previous version (generate-audio.md) generated 1,847 files sequentially in ~20 minutes. This version uses the newly parallelized script for faster generation.

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

## Implementation Plan

### 1. Create output directory
```bash
mkdir -p output/audio-v2
```

### 2. Test parallel generation with small batch
Start conservative to test for rate limits:
```bash
python scripts/generate-audio.py \
  --input output/examples-v2-all.tsv \
  --output output/audio-v2 \
  --start 1 --end 100 \
  --workers 8 \
  --force
```

**Expected**: ~30-60 seconds for 100 files (vs ~60-80 seconds sequential)

### 3. Monitor for rate limiting
Watch for errors during the test batch:
- HTTP 429 errors
- Connection timeouts
- Failed generations

If no issues, proceed with full generation.

### 4. Generate all audio files
```bash
python scripts/generate-audio.py \
  --input output/examples-v2-all.tsv \
  --output output/audio-v2 \
  --workers 8
```

**Expected performance**:
- Workers: 8 (default)
- Estimated time: 5-8 minutes (vs 20 minutes sequential)
- Rate: ~300-400 files/minute
- Speedup: 3-4x faster

### 5. Verify generation
```bash
# Count generated files
ls output/audio-v2/*.mp3 | wc -l

# Check file sizes (should be ~15KB average)
du -sh output/audio-v2/
```

## Parallelization Settings

### Conservative (recommended start)
```bash
--workers 4
# Estimated time: ~8-10 minutes
# Risk: Very low
```

### Default (recommended)
```bash
--workers 8
# Estimated time: ~5-8 minutes
# Risk: Low
```

### Aggressive (if default works well)
```bash
--workers 16
# Estimated time: ~3-5 minutes
# Risk: Medium (possible rate limiting)
```

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

### 3. Copy to Anki media directory
```bash
cp output/audio-v2/koreantopik1_v2_*.mp3 ~/.local/share/Anki2/"User 1"/collection.media/
```

**To use in Anki cards:**
```
[sound:koreantopik1_v2_0001.mp3]
```

## Migration from v1 to v2

### Option 1: Keep both versions
- v1: `koreantopik1_*.mp3`
- v2: `koreantopik1_v2_*.mp3`
- Allows comparison and gradual migration

### Option 2: Replace v1
```bash
# Backup v1 first
cd ~/.local/share/Anki2/"User 1"/collection.media/
mkdir -p ~/backup/anki-audio-v1
cp koreantopik1_[0-9]*.mp3 ~/backup/anki-audio-v1/

# Remove v1 and rename v2
rm koreantopik1_[0-9]*.mp3
for file in koreantopik1_v2_*.mp3; do
  mv "$file" "${file/koreantopik1_v2_/koreantopik1_}"
done
```

## Troubleshooting

### Rate Limiting
If you encounter errors:
1. Reduce workers: `--workers 4`
2. Add delays between batches (process in chunks)
3. Check Edge TTS service status

### Partial Generation
The script automatically skips existing files:
```bash
# Resume from where it left off
python scripts/generate-audio.py \
  --input output/examples-v2-all.tsv \
  --output output/audio-v2 \
  --workers 8
```

### Quality Check
Listen to random samples:
```bash
# Play random files to verify quality
mpv output/audio-v2/0001.mp3
mpv output/audio-v2/0500.mp3
mpv output/audio-v2/1000.mp3
```

## Performance Comparison

| Method | Workers | Time | Rate | Speedup |
|--------|---------|------|------|---------|
| v1 (Sequential) | 1 | 20 min | 93/min | 1x |
| v2 (Parallel, conservative) | 4 | ~10 min | 185/min | 2x |
| v2 (Parallel, default) | 8 | ~6 min | 308/min | 3.3x |
| v2 (Parallel, aggressive) | 16 | ~4 min | 462/min | 5x* |

*Aggressive setting may hit rate limits - use with caution

## Notes
- Edge TTS is free with no API key required
- Parallelization significantly improves generation time
- Script supports resuming (skips existing files)
- Monitor first batch for any rate limiting issues
- Can adjust worker count based on performance/errors
