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
python scripts/generate-audio-verify.py
```

**Verification Strategy**:
- Uses `ffprobe` (from ffmpeg) to validate each MP3 file
- Checks: valid format, audio streams, duration > 0
- Reports broken/corrupted files with error details
- Script: `scripts/generate-audio-verify.py`
- All files should pass validation for successful generation

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
