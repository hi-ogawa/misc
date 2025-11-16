# Update TOPIK 1 Deck with Dual Audio

## Current State

**TOPIK 1 Dataset**: 1,847 words already imported into Anki
- ✅ Example sentences exist
- ✅ Latest example audio available as `koreantopik1_example_ko_NNNN.mp3` (renamed from v2 zip)
- ✅ Vocabulary audio ready as `koreantopik1_korean_NNNN.mp3`

## Goal

Add vocabulary audio (isolated word pronunciation) to existing TOPIK 1 Anki deck without disrupting current cards.

## Strategy

Use the v2 example audio (renamed to `koreantopik1_example_ko_*.mp3`) and the generated vocab audio (`koreantopik1_korean_*.mp3`), then import a unified TSV with both audio references and update the card templates.

## File Naming Convention

Following the TOPIK 2 dual-audio pattern:
- **Vocabulary audio**: `koreantopik1_korean_NNNN.mp3` (NEW)
- **Example audio**: `koreantopik1_example_ko_NNNN.mp3` (rename from existing `koreantopik1_NNNN.mp3`)

## Implementation Plan

- [x] Phase 1: Audio prep
- [x] Phase 2: Anki import file
- [ ] Phase 3: Copy audio into Anki media
- [ ] Phase 4: Update Anki Card Template
- [ ] Phase 5: Import deck

### Phase 1: Audio prep

- Vocab audio: generated `koreantopik1_korean_NNNN.mp3` (1,847 files) in `output/koreantopik1/audio/`.
- Example audio: unzipped `koreantopik1_v2_audio.zip` and renamed to `koreantopik1_example_ko_NNNN.mp3` (1,847 files) in `output/koreantopik1/audio/`.
- Verification: `generate-audio-verify.py` passed all 3,694 files; `generate-audio-stats.py` summary — files 3,694; avg 2.31s (median 2.11s); min 1.18s; max 5.59s; std dev 0.72s; total 142.11 minutes.

### Phase 2: Anki import file

`output/koreantopik1/koreantopik1_anki_import.tsv` (1847 rows) built from `koreantopik1_anki_updated.txt` with audio columns set to:
- example audio: `[sound:koreantopik1_example_ko_NNNN.mp3]`
- vocab audio: `[sound:koreantopik1_korean_NNNN.mp3]`
- Column order matches master TSV: number, korean, english, etymology, example_ko, example_en, notes, korean_audio, example_ko_audio.

### Phase 3: Copy audio into Anki media

```bash
# Example audio (overwrite old names)
cp output/koreantopik1/audio/koreantopik1_example_ko_*.mp3 ~/.local/share/Anki2/"사용자 1"/collection.media/

# Vocab audio
cp output/koreantopik1/audio/koreantopik1_korean_*.mp3 ~/.local/share/Anki2/"사용자 1"/collection.media/
```

**Verification:**
```bash
ls ~/.local/share/Anki2/"사용자 1"/collection.media/koreantopik1_example_ko_*.mp3 | wc -l   # expect 1847
ls ~/.local/share/Anki2/"사용자 1"/collection.media/koreantopik1_korean_*.mp3 | wc -l       # expect 1847
```

### Phase 4: Update Anki Card Template

**Current card structure** (assumed):
- Front: Korean word
- Back: English, example sentence, example audio (`[sound:koreantopik1_NNNN.mp3]`)

**New card structure**:
- Front: Korean word (optionally with vocabulary audio button)
- Back: English, vocabulary audio, example sentence, example audio

#### Required Changes in Anki:

1. **Add new field to note type**:
   - Field name: `korean_audio`
   - Populate with: `[sound:koreantopik1_korean_{{number}}.mp3]`

2. **Update existing example audio field**:
   - Old reference: `[sound:koreantopik1_{{number}}.mp3]`
   - New reference: `[sound:koreantopik1_example_ko_{{number}}.mp3]`

3. **Update card template** to display both audio types

### Phase 5: Import deck

1. Backup Anki collection.
2. Ensure both audio sets are present in media (Phase 2).
3. Import `output/koreantopik1/koreantopik1_anki_import.tsv` (tab-delimited). Map fields to the note type, including new `korean_audio` and updated `example_ko_audio`.

## File Naming Summary

```
koreantopik1_korean_0001.mp3     (vocabulary audio)
koreantopik1_example_ko_0001.mp3 (example audio - renamed)
...
```

## Master TSV Format (For Future Reference)

If exporting/re-importing the full deck:

```
number  korean  english  etymology  example_ko  example_en  notes  korean_audio  example_ko_audio
```

**Audio field formats**:
- `korean_audio`: `[sound:koreantopik1_korean_0001.mp3]`
- `example_ko_audio`: `[sound:koreantopik1_example_ko_0001.mp3]` (or `[sound:koreantopik1_0001.mp3]` if not renamed)

## Next Steps

1. **Anki setup**: Add `korean_audio` field; update example audio field and templates.
2. **Copy files**: Move example + vocab audio to Anki media (Phase 3).
3. **Import**: Re-import `koreantopik1_anki_import.tsv`.
4. **Test**: Verify audio plays correctly on a few cards

---

**Note**: Always backup your Anki collection before making bulk changes!
