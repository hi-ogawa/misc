# Generate Audio for Korean Examples

## Goal
Generate audio pronunciation files for all `example_ko` entries in the vocabulary list using Microsoft Edge TTS.

## Status
✅ **COMPLETED** - 1847/1847 audio files generated successfully (2025-11-09)

## Input
- Source: `output/examples-all.tsv`
- Columns: number, korean, example_ko, example_en
- Total entries: 1,847 examples

## Output
- Location: `output/audio/`
- Format: `0001.mp3` to `1847.mp3` (4-digit padded)
- Total files: 1,847
- Total size: 28MB
- Average file size: ~15KB per file
- Voice used: `ko-KR-SunHiNeural` (female)

## Implementation Steps

### 1. Install Edge TTS
```bash
uv tool install edge-tts
```

### 2. Test Korean Voices
Available Korean voices:
- `ko-KR-SunHiNeural` (female)
- `ko-KR-InJoonNeural` (male)

Test command:
```bash
edge-tts --voice ko-KR-SunHiNeural --text "가게에 자주 가요" --write-media test.mp3
```

### 3. Created Python Script
Created: `scripts/generate-audio.py`

Features:
- Reads `output/examples-all.tsv` using Python's csv module
- Calls edge-tts CLI via subprocess for each entry
- Generates audio as `output/audio/{number:04d}.mp3` (4-digit padding)
- Skips existing files by default (allows resuming)
- Supports range selection with `--start` and `--end` flags
- Error handling and progress reporting

## Usage

### Generate all audio files
```bash
python scripts/generate-audio.py
```

### Generate specific range
```bash
# First 10 examples
python scripts/generate-audio.py --start 1 --end 10

# Examples 100-200
python scripts/generate-audio.py --start 100 --end 200
```

### Force regenerate (overwrite existing)
```bash
python scripts/generate-audio.py --force
```

### Use different voice
```bash
python scripts/generate-audio.py --voice ko-KR-InJoonNeural
```

## Voice Selection
Default: `ko-KR-SunHiNeural` (female, clear pronunciation)
Alternative: `ko-KR-InJoonNeural` (male)

## Results & Performance

### Generation Stats
- Total time: ~20 minutes for all 1,847 files
- Rate: ~93 files/minute
- No errors during generation
- All files validated and playable

### File Statistics
- Individual file size: 13-15KB per phrase
- Total storage used: 28MB
- Format: MP3 audio
- Sample rate: 24kHz (Edge TTS default)

## Post-Processing Steps

### 1. Rename files with prefix
Added `koreantopik1_` prefix to all files for better organization:
```bash
cd output/audio
for file in [0-9][0-9][0-9][0-9].mp3; do
  mv "$file" "koreantopik1_$file"
done
```

Result: `0001.mp3` → `koreantopik1_0001.mp3`

### 2. Create zip archive
Created compressed archive for backup/sharing:
```bash
cd output/audio
zip -r ../koreantopik1_audio.zip koreantopik1_*.mp3
```

**Archive details:**
- File: `output/koreantopik1_audio.zip`
- Size: 16MB (compressed from 28MB)
- Compression: ~43% reduction
- Contents: 1,847 files

### 3. Copy to Anki media directory
Integrated audio files into Anki for flashcard use:
```bash
cp output/audio/koreantopik1_*.mp3 ~/.local/share/Anki2/"User 1"/collection.media/
```

**To use in Anki cards:**
```
[sound:koreantopik1_0001.mp3]
```

The audio files are now available in all Anki decks and will sync across devices.

## Notes
- Edge TTS is free with no API key required
- No rate limiting issues encountered
- Can regenerate specific files by deleting and re-running the script
- Script automatically resumes from where it left off (skips existing files)
- For fixing examples and regenerating audio, see `prompts/generate-fix.md`
