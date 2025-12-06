# Add Audio to Anki Notes

**Purpose**: Generate and attach audio files to notes missing audio (typically Korean::Custom deck).

**Trigger**: User says "add audio to Custom deck" or "generate audio for N notes"

## Workflow

### 1. Export notes without audio

```bash
python scripts/anki-export.py \
  --query "deck:Korean::Custom -korean_audio:" \
  --fields number,korean,example_ko \
  --output output/tmp/custom-no-audio.tsv
```

### 2. Generate audio files

Generate MP3s for both `korean` and `example_ko` fields:

```bash
# Generate audio using edge-tts
python scripts/generate-audio.py \
  --input output/tmp/custom-no-audio.tsv \
  --dataset custom \
  --output-dir output/audio/custom
```

Expected output:
- `output/audio/custom/custom_korean_NNNN.mp3` (or using number field as ID)
- `output/audio/custom/custom_example_ko_NNNN.mp3`

**Naming convention** (use note identifier):
- If `number` field exists: use it (e.g., `extract_30_돌보다` → `custom_korean_extract_30_돌보다.mp3`)
- If `number` is empty: use Anki note ID (e.g., `1764563410409` → `custom_korean_1764563410409.mp3`)
- Sanitize identifiers: replace spaces/special chars with underscores for filenames

### 3. Upload audio to Anki media collection

Use AnkiConnect `storeMediaFile` action:

```bash
python scripts/anki-upload-audio.py \
  --audio-dir output/audio/custom \
  --dry-run  # Review first
```

This script should:
- Read all MP3 files from audio directory
- For each file, call `storeMediaFile` with base64-encoded audio data
- Log success/failure for each upload

AnkiConnect `storeMediaFile` format:
```json
{
  "action": "storeMediaFile",
  "version": 6,
  "params": {
    "filename": "custom_korean_0001.mp3",
    "data": "<base64-encoded-audio>"
  }
}
```

### 4. Update note audio fields

Update notes with `[sound:filename.mp3]` references:

```bash
python scripts/anki-update-audio-fields.py \
  --input output/tmp/custom-no-audio.tsv \
  --dataset custom \
  --dry-run  # Review first
```

This script should:
- For each note in input TSV, find note ID via AnkiConnect
- Construct audio filenames based on naming convention
- Update `korean_audio` and `example_ko_audio` fields via `updateNote` action

AnkiConnect `updateNote` format:
```json
{
  "action": "updateNote",
  "version": 6,
  "params": {
    "note": {
      "id": 1234567890,
      "fields": {
        "korean_audio": "[sound:custom_korean_0001.mp3]",
        "example_ko_audio": "[sound:custom_example_ko_0001.mp3]"
      }
    }
  }
}
```

### 5. Verify audio

Query Anki to verify all notes now have audio:

```bash
python scripts/anki.py findNotes --params '{"query": "deck:Korean::Custom -korean_audio:"}'
# Should return empty array
```

## Scripts to Create

### `scripts/anki-upload-audio.py`

Arguments:
- `--audio-dir`: Directory containing MP3 files
- `--dry-run`: Print what would be uploaded without uploading

### `scripts/anki-update-audio-fields.py`

Arguments:
- `--input`: TSV file with note data
- `--dataset`: Dataset name (for filename construction, e.g., "custom")
- `--deck`: Deck name for note lookup (default: "Korean::Custom")
- `--dry-run`: Print what would be updated without updating

## Notes

- Audio generation uses `edge-tts` with Korean voice (see `scripts/generate-audio.py`)
- AnkiConnect must be running (Anki open with AnkiConnect plugin)
- Consider batch processing for large numbers of notes
- Verify media files are accessible in Anki after upload
- Handle notes with empty `example_ko` gracefully (only add korean_audio)

## Implementation Details

**Identifier extraction:**
```python
def get_note_identifier(note_data: dict) -> str:
    """Get unique identifier for filename from note data."""
    number = note_data['fields']['number']['value'].strip()
    if number:
        # Sanitize: replace spaces and special chars
        return number.replace(' ', '_').replace('/', '_')
    else:
        # Use Anki note ID
        return str(note_data['noteId'])
```

**Audio filename construction:**
```python
identifier = get_note_identifier(note_data)
korean_file = f"custom_korean_{identifier}.mp3"
example_file = f"custom_example_ko_{identifier}.mp3"
```

## Edge Cases

- Notes with empty `number` field → use Anki note ID ✓ (3 notes in current Custom deck)
- Notes with empty `example_ko` → skip example_ko_audio (currently all 152 have example_ko)
- Notes that already have audio → skip by default, `--force` to overwrite
- Duplicate filenames → error (shouldn't happen with noteId fallback)
- Failed uploads → log to file and continue, report summary at end
- Failed TTS generation → log to failed.txt, continue with remaining notes
