# Fix Example Sentences and Regenerate Audio

## Context
- Full TSV already imported: `output/examples-all.tsv` → Google Sheets → Anki
- When studying in Anki, you notice bad/awkward examples that need fixing
- This file tracks fixes in an ad-hoc manner (no sync back to TSV/Sheets)

**Workflow**:
1. List the corrected entry below (number, korean, example_ko, example_en)
2. Generate new audio file with `_fix` suffix
3. Update Anki card to use new audio file
4. Mark as done in Status section

**Requirements**:
- Need `output/examples-all.tsv` locally (script reads from it to generate audio)
- Download from [Google Drive](https://drive.google.com/drive/u/0/folders/1fzfewUUWmRCqEhtdHFK0wuN3PO0qnSPB) if not present
- Script uses the file as-is (no edits needed - just for audio generation)

## Fixed Examples

List of corrected entries (number, korean, example_ko, example_en):
```
24	가지다	좋은 생각을 가져요	have a good idea
457	-되다	회의가 시작되었어요	the meeting has started
```

## Process

1. **Regenerate audio** - For each fixed entry:
   ```bash
   python scripts/generate-audio.py --start 24 --end 24 --force
   ```
2. **Rename audio file** - Add `_fix` suffix (forces Anki to detect new file):
   ```bash
   mv output/audio/0024.mp3 output/audio/koreantopik1_0024_fix.mp3
   ```
3. **Copy audio to Anki**:
   ```bash
   cp output/audio/koreantopik1_0024_fix.mp3 ~/.local/share/Anki2/"User 1"/collection.media/
   ```
4. **Update Anki card** - Change audio field from `[sound:koreantopik1_0024.mp3]` to `[sound:koreantopik1_0024_fix.mp3]`

## Status
- [x] Entry 24: 가지다
- [x] Entry 457: -되다
