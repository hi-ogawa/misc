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

## Implementation Plan

### 1. Create output directory
```bash
mkdir -p output/audio-v2
```

### 2. Test with small batch (sequential first)
Start sequential to verify basic functionality:
```bash
python scripts/generate-audio.py \
  --input output/examples-v2-all.tsv \
  --output output/audio-v2 \
  --start 1 --end 10 \
  --force
```

**Expected**: ~10 seconds for 10 files (default concurrency=1)

### 3. Test with concurrency
Try with 8 concurrent tasks to test for rate limits:
```bash
python scripts/generate-audio.py \
  --input output/examples-v2-all.tsv \
  --output output/audio-v2 \
  --start 11 --end 100 \
  --concurrency 8 \
  --force
```

**Expected**: ~20-30 seconds for 90 files

Watch for errors:
- Socket timeouts
- Connection errors
- Failed generations

If no issues, proceed with full generation.

### 4. Generate all audio files
Sequential (safest):
```bash
python scripts/generate-audio.py \
  --input output/examples-v2-all.tsv \
  --output output/audio-v2
```

Or with concurrency (faster):
```bash
python scripts/generate-audio.py \
  --input output/examples-v2-all.tsv \
  --output output/audio-v2 \
  --concurrency 8
```

**Expected performance**:
- Sequential (concurrency=1): ~20 minutes
- Concurrent (concurrency=8): ~5-8 minutes
- Rate: ~300-400 files/minute with concurrency
- Speedup: 3-4x faster

### 5. Verify generation
```bash
# Count generated files
ls output/audio-v2/*.mp3 | wc -l

# Check file sizes (should be ~15KB average)
du -sh output/audio-v2/
```

## Concurrency Settings

### Sequential (default, safest)
```bash
# No flag needed - concurrency=1 by default
# Estimated time: ~20 minutes
# Risk: None
```

### Conservative
```bash
--concurrency 4
# Estimated time: ~8-10 minutes
# Risk: Very low
```

### Moderate (recommended for speed)
```bash
--concurrency 8
# Estimated time: ~5-8 minutes
# Risk: Low
```

### Aggressive (if moderate works well)
```bash
--concurrency 16
# Estimated time: ~3-5 minutes
# Risk: Medium (possible rate limiting/timeouts)
```

## Implementation Notes

**Architecture**:
- Single-threaded async using `asyncio.create_subprocess_exec()`
- Processes files in chunks of `--concurrency` size
- Global counters track progress (safe in single thread)
- Each task logs immediately upon completion
- Ctrl-C handling with graceful shutdown

**Why async subprocess?**
- More efficient than threads for I/O-bound tasks
- No thread overhead
- Can handle higher concurrency (20-50+ if needed)
- edge-tts CLI runs as subprocess (non-blocking async)

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

### Socket Timeouts / Connection Errors
If you encounter errors like `SocketTimeoutError`:
1. Reduce concurrency: `--concurrency 4` or `--concurrency 1`
2. The script continues on errors - failed files are logged
3. Re-run the same command to retry failed files (existing ones skipped)
4. Check Edge TTS service status

### Partial Generation
The script automatically skips existing files:
```bash
# Resume from where it left off
python scripts/generate-audio.py \
  --input output/examples-v2-all.tsv \
  --output output/audio-v2 \
  --concurrency 8
```

### Ctrl-C Interruption
Press Ctrl-C to stop generation:
- Shows partial progress
- Existing files are preserved
- Resume by running the same command (skips existing)

### Quality Check
Listen to random samples:
```bash
# Play random files to verify quality
mpv output/audio-v2/0001.mp3
mpv output/audio-v2/0500.mp3
mpv output/audio-v2/1000.mp3
```

## Performance Comparison

| Method | Concurrency | Time | Rate | Speedup |
|--------|-------------|------|------|---------|
| Sequential (default) | 1 | 20 min | 93/min | 1x |
| Conservative | 4 | ~10 min | 185/min | 2x |
| Moderate | 8 | ~6 min | 308/min | 3.3x |
| Aggressive | 16 | ~4 min | 462/min | 5x* |

*Aggressive setting may hit rate limits/timeouts - use with caution

## Notes
- Edge TTS is free with no API key required
- Default is sequential (concurrency=1) - safe and reliable
- Concurrency uses async subprocess for efficient I/O
- Script supports resuming (skips existing files)
- Ctrl-C interruption is handled gracefully
- Monitor for socket timeouts if using high concurrency
- Can adjust concurrency based on network stability
