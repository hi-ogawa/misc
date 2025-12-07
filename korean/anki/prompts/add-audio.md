# Add Audio to Anki Notes

**Purpose**: Generate and attach audio files to notes missing audio (typically Korean::Custom deck).

**Trigger**: User says "add audio to Custom deck" or "generate audio for N notes"

## Workflow

### 1. Export notes without audio

```bash
python scripts/anki-export.py \
  --query "deck:Korean::Custom -korean_audio:[sound:*]" \
  --fields noteId,korean,example_ko \
  --output output/tmp/custom-no-audio.tsv
```

### 2. Generate audio files

```bash
# Korean word audio
python scripts/generate-audio.py \
  --input output/tmp/custom-no-audio.tsv \
  --output output/audio/custom \
  --field korean \
  --id-field noteId \
  --prefix custom_korean_ \
  --concurrency 5

# Example sentence audio
python scripts/generate-audio.py \
  --input output/tmp/custom-no-audio.tsv \
  --output output/audio/custom \
  --field example_ko \
  --id-field noteId \
  --prefix custom_example_ko_ \
  --concurrency 5
```

### 3. Add audio columns

```bash
python scripts/jq-tsv.py \
  '. + {korean_audio: "[sound:custom_korean_\(.noteId).mp3]", example_ko_audio: "[sound:custom_example_ko_\(.noteId).mp3]"}' \
  output/tmp/custom-no-audio.tsv > output/tmp/custom-with-audio.tsv
```

### 4. Update note audio fields

```bash
python scripts/anki-update-notes.py \
  --input output/tmp/custom-with-audio.tsv \
  --fields korean_audio,example_ko_audio \
  --dry-run  # Review first, then remove --dry-run
```

### 5. Copy audio to Anki media

```bash
cp output/audio/custom/*.mp3 ~/.local/share/Anki2/"사용자 1"/collection.media/
```

### 6. Verify

```bash
python scripts/anki.py findNotes --params '{"query": "deck:Korean::Custom -korean_audio:[sound:*]"}'
# Should return empty array
```

## Notes

- Audio generation uses `edge-tts` with Korean voice
- AnkiConnect must be running (Anki open with AnkiConnect plugin)
- Using `noteId` as identifier guarantees uniqueness
