# Fix Example Sentences and Regenerate Audio

## Context
- Full TSV already imported: `output/examples-all.tsv` → Google Sheets → Anki
- Finding bad examples during practice
- Only need to update `examples-all.tsv` (not individual batch files)

## Fixed Examples

List of corrected entries (number, korean, example_ko, example_en):
```
24	가지다	좋은 생각을 가져요	have a good idea
457	-되다	회의가 시작되었어요	the meeting has started
```

## Process

1. **Edit examples-all.tsv** - Fix entries listed above
2. **Regenerate audio** - For each fixed entry:
   ```bash
   python scripts/generate-audio.py --start 24 --end 24 --force
   ```
3. **Rename audio file** - Add `_fix` suffix (forces Anki to detect new file):
   ```bash
   mv output/audio/0024.mp3 output/audio/koreantopik1_0024_fix.mp3
   ```
4. **Copy audio to Anki**:
   ```bash
   cp output/audio/koreantopik1_0024_fix.mp3 ~/.local/share/Anki2/"User 1"/collection.media/
   ```
5. **Update Anki card** - Change audio field from `[sound:koreantopik1_0024.mp3]` to `[sound:koreantopik1_0024_fix.mp3]`

## Status
- [x] Entry 24: 가지다
- [x] Entry 457: -되다
