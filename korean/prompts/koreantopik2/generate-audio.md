# Generate Audio for Korean Examples (TOPIK 2)

## Goal
Generate audio pronunciation files for all `example_ko` entries in the TOPIK 2 vocabulary list using Microsoft Edge TTS.

## Status
⏳ **PLANNED** - Ready to generate after examples are complete

## Input
- Source: `output/koreantopik2/examples-all.tsv` (consolidated from batches 1-39)
- Columns: number, korean, example_ko, example_en
- Total entries: 3,873 examples

## Output
- Location: `output/koreantopik2/audio/`
- Format: `0001.mp3` to `3873.mp3` (4-digit padded)
- Total files: 3,873
- Voice: `ko-KR-SunHiNeural` (female)

## Generate

```bash
python scripts/generate-audio.py \
  --input output/koreantopik2/examples-all.tsv \
  --output output/koreantopik2/audio \
  --concurrency 5
```

**Notes:**
- Edge TTS is free with no API key required
- Default is sequential (concurrency=1) - safe and reliable
- Concurrency uses async subprocess for efficient I/O
- Script supports resuming (skips existing files)
- Ctrl-C interruption is handled gracefully
- Can adjust concurrency based on network stability

## Verify generation

```bash
# Count generated files
ls output/koreantopik2/audio/*.mp3 | wc -l

# Check file sizes (should be ~15KB average)
du -sh output/koreantopik2/audio/

# Verify MP3 integrity using ffprobe
python scripts/generate-audio-verify.py --output output/koreantopik2/audio

# Analyze audio duration statistics
python scripts/generate-audio-stats.py --output output/koreantopik2/audio
```

## Post-Processing Steps

### 1. Rename files with prefix
```bash
cd output/koreantopik2/audio
for file in [0-9][0-9][0-9][0-9].mp3; do
  mv "$file" "koreantopik2_$file"
done
```

Result: `0001.mp3` → `koreantopik2_0001.mp3`

### 2. Create zip archive
```bash
cd output/koreantopik2/audio
zip -r ../koreantopik2_audio.zip koreantopik2_*.mp3
```

Result: `output/koreantopik2/koreantopik2_audio.zip` (~50M, 3873 files)

### 3. Copy audio files to Anki media directory

```bash
cp output/koreantopik2/audio/koreantopik2_*.mp3 ~/.local/share/Anki2/"User 1"/collection.media/
```

This copies all 3,873 audio files to Anki's media folder so they can be referenced in cards.
