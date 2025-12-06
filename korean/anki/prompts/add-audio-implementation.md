# Add Audio to Custom Deck - Implementation Plan

## Current Status

**Korean::Custom deck**: 152 notes, 0 have audio
- 149 from extract-missing-vocab workflow (tagged "extracted", have `number` field)
- 3 manually added (no `number` field, will use noteId)
- All 152 have both `korean` and `example_ko` fields ✓

## Scripts Needed

### 1. Create: `scripts/anki-export.py`
Export notes from Anki to TSV.

**Arguments:**
- `--query`: AnkiConnect query (e.g., `"deck:Korean::Custom -korean_audio:"`)
- `--fields`: Comma-separated field names to export
- `--output`: Output TSV file path

**Implementation:**
- Use `findNotes` to get note IDs matching query
- Use `notesInfo` to get full note data
- Write TSV with requested fields + noteId

### 2. Create: `scripts/generate-audio-anki.py`
Generate audio files from Anki note data (TSV with noteId).

**Arguments:**
- `--input`: TSV file with notes (must have `noteId`, `korean`, `example_ko` fields)
- `--output-dir`: Directory for generated MP3s
- `--dataset`: Dataset prefix (e.g., "custom")
- `--voice`: TTS voice (default: ko-KR-SunHiNeural)
- `--force`: Regenerate existing files
- `--concurrency`: Number of concurrent generations

**Implementation:**
- Read TSV and extract identifier from `number` field or `noteId`
- For each note, generate 2 files:
  - `{dataset}_korean_{identifier}.mp3` (from `korean` field)
  - `{dataset}_example_ko_{identifier}.mp3` (from `example_ko` field)
- Use edge-tts like existing `generate-audio.py`
- Log failures to `{output-dir}/failed.txt`

**Alternative:** Modify existing `generate-audio.py` to support field-based naming

### 3. Create: `scripts/anki-upload-audio.py`
Upload MP3 files to Anki media collection via AnkiConnect.

**Arguments:**
- `--audio-dir`: Directory containing MP3 files
- `--pattern`: Glob pattern for files (default: `*.mp3`)
- `--dry-run`: Print without uploading

**Implementation:**
- Find all MP3 files in directory
- For each file:
  - Read file and base64 encode
  - Call AnkiConnect `storeMediaFile` with filename and data
  - Print status
- Report summary (uploaded, skipped, failed)

### 4. Create: `scripts/anki-update-audio-fields.py`
Update note audio fields with `[sound:...]` references.

**Arguments:**
- `--input`: TSV file with note data (must have `noteId` and identifier fields)
- `--dataset`: Dataset prefix for constructing filenames (e.g., "custom")
- `--dry-run`: Print without updating

**Implementation:**
- Read TSV with note data
- For each note:
  - Get identifier from `number` field or `noteId`
  - Construct audio filenames:
    - `korean_audio`: `[sound:{dataset}_korean_{identifier}.mp3]`
    - `example_ko_audio`: `[sound:{dataset}_example_ko_{identifier}.mp3]`
  - Call AnkiConnect `updateNote` with noteId and new field values
  - Print status
- Report summary (updated, failed)

## Workflow

### Step 1: Export notes without audio
```bash
python scripts/anki-export.py \
  --query "deck:Korean::Custom -korean_audio:" \
  --fields noteId,number,korean,example_ko \
  --output output/tmp/custom-no-audio.tsv
```

Expected: 152 rows

### Step 2: Generate audio files
```bash
python scripts/generate-audio-anki.py \
  --input output/tmp/custom-no-audio.tsv \
  --output-dir output/audio/custom \
  --dataset custom \
  --concurrency 3
```

Expected: 304 MP3 files (152 × 2)

### Step 3: Upload audio to Anki
```bash
# Dry run first
python scripts/anki-upload-audio.py \
  --audio-dir output/audio/custom \
  --dry-run

# Then actual upload
python scripts/anki-upload-audio.py \
  --audio-dir output/audio/custom
```

### Step 4: Update note fields
```bash
# Dry run first
python scripts/anki-update-audio-fields.py \
  --input output/tmp/custom-no-audio.tsv \
  --dataset custom \
  --dry-run

# Then actual update
python scripts/anki-update-audio-fields.py \
  --input output/tmp/custom-no-audio.tsv \
  --dataset custom
```

### Step 5: Verify
```bash
# Should return 0
python scripts/anki.py findNotes --params '{"query": "deck:Korean::Custom -korean_audio:"}' | jq 'length'

# Should return 152
python scripts/anki.py findNotes --params '{"query": "deck:Korean::Custom korean_audio:"}' | jq 'length'
```

## Testing Strategy

1. Test with 1-2 notes first:
   ```bash
   # Export just 2 notes for testing
   head -n 3 output/tmp/custom-no-audio.tsv > output/tmp/custom-test.tsv

   # Run full workflow with test file
   # ... (same commands but with custom-test.tsv)
   ```

2. Verify in Anki:
   - Check notes have audio field values
   - Play audio to verify files are accessible
   - Check media folder for actual files

3. Run full workflow on all 152 notes

## Implementation Order

1. **anki-export.py** - needed for all subsequent steps
2. **generate-audio-anki.py** - can test with existing notes data
3. **anki-upload-audio.py** - test with a few generated files
4. **anki-update-audio-fields.py** - final step, test with dry-run

## Notes

- All scripts follow `prompts/guide-script.md` principles
- Use existing `scripts/anki.py` wrapper for AnkiConnect calls
- Test with `--dry-run` flags before actual operations
- Keep intermediate files in `output/tmp/` for debugging
