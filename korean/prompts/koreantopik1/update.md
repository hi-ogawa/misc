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
- [x] Phase 3: Backup Anki collection
- [x] Phase 4: Copy audio into Anki media
- [x] Phase 5: Update Anki Card Template
- [ ] Phase 6: Import deck

### Phase 1: Audio prep

- Vocab audio: generated `koreantopik1_korean_NNNN.mp3` (1,847 files) in `output/koreantopik1/audio/`.
- Example audio: unzipped `koreantopik1_v2_audio.zip` and renamed to `koreantopik1_example_ko_NNNN.mp3` (1,847 files) in `output/koreantopik1/audio/`.
- Verification: `generate-audio-verify.py` passed all 3,694 files; `generate-audio-stats.py` summary — files 3,694; avg 2.31s (median 2.11s); min 1.18s; max 5.59s; std dev 0.72s; total 142.11 minutes.

### Phase 2: Anki import file

`output/koreantopik1/koreantopik1_anki_import.tsv` (1847 rows) built from `koreantopik1_anki_updated.txt` with audio columns set to:
- example audio: `[sound:koreantopik1_example_ko_NNNN.mp3]`
- vocab audio: `[sound:koreantopik1_korean_NNNN.mp3]`
- Column order matches master TSV: number, korean, english, etymology, example_ko, example_en, notes, korean_audio, example_ko_audio.

### Phase 3: Backup Anki collection

Created full backup before making any changes:
- File: `koreantopik1_v1_backup.apkg`
- Export settings: Full deck with media and scheduling information
- Date: 2025-11-17

### Phase 4: Copy audio into Anki media

Copied all audio files to Anki media folder:

```bash
# Example audio
cp output/koreantopik1/audio/koreantopik1_example_ko_*.mp3 ~/.local/share/Anki2/사용자\ 1/collection.media/

# Vocab audio
cp output/koreantopik1/audio/koreantopik1_korean_*.mp3 ~/.local/share/Anki2/사용자\ 1/collection.media/
```

**Verification completed:**
- Example audio files: 1,847 ✅
- Vocabulary audio files: 1,847 ✅

### Phase 5: Update Anki Card Template

**Note Type**: Korean Vocabulary

**Goal**: Add vocabulary audio field and update card template to display both audio types (vocabulary + example).

#### Step-by-Step Instructions:

1. **Open Anki and go to Tools → Manage Note Types**

2. **Select "Korean Vocabulary" note type → Click "Fields..."**

   **Current fields** (expected):
   - number
   - korean
   - english
   - example_ko
   - example_en
   - etymology
   - notes
   - example_ko_audio (or similar name for example audio)

   **Action**: Add a new field:
   - Click "Add" button
   - Field name: `korean_audio`
   - Position: Add it before `example_ko_audio` (so it appears as the 8th field)
   - Click "OK"

3. **Update the Card Template (Tools → Manage Note Types → Korean Vocabulary → Cards...)**

   **Current Front Template**:
   ```html
   <h2>{{korean}}</h2>
   ```

   **Updated Front Template** (Option B - with vocabulary audio):
   ```html
   <h2>{{korean}}</h2>
   {{korean_audio}}
   ```

   **Back Template** (no changes needed):
   - Vocabulary audio already inherited from FrontSide
   - Example audio already present in current template

4. **Field Mapping** (to verify for Phase 6 import):

   **TSV column order** (in file):
   1. number
   2. korean
   3. english
   4. etymology
   5. example_ko
   6. example_en
   7. notes
   8. korean_audio
   9. example_ko_audio

   **Anki field order** (in note type):
   1. number
   2. korean
   3. english
   4. example_ko
   5. example_en
   6. etymology
   7. notes
   8. korean_audio (NEW - to be added)
   9. example_ko_audio

### Phase 6: Import deck

**Goal**: Import the TSV file to update all 1,847 cards with the new audio fields.

#### Step-by-Step Instructions:

1. **Open Anki and go to File → Import**

2. **Select the import file**:
   - Navigate to: `output/koreantopik1/koreantopik1_anki_import.tsv`
   - Click "Open"

3. **Configure Import Settings**:

   **Type**: Korean Vocabulary

   **Deck**: (Select your TOPIK 1 deck)

   **Update existing notes when first field matches**: ✅ CHECKED
   - This is crucial! It will update existing cards instead of creating duplicates

   **Allow HTML in fields**: ✅ CHECKED

   **Fields separated by**: Tab

4. **Map Fields** (verify the mapping):

   **IMPORTANT**: TSV column order ≠ Anki field order!

   During import, map each Anki field to the correct TSV column:

   Anki Field → TSV Column:
   ```
   number         → Field 1
   korean         → Field 2
   english        → Field 3
   example_ko     → Field 5 (NOT Field 4!)
   example_en     → Field 6 (NOT Field 5!)
   etymology      → Field 4 (NOT Field 6!)
   notes          → Field 7
   korean_audio   → Field 8
   example_ko_audio → Field 9
   ```

5. **Verify Import Preview**:
   - Check that a few sample cards look correct
   - Verify audio fields show `[sound:koreantopik1_korean_NNNN.mp3]` format
   - Make sure "Update existing notes" shows 1,847 cards will be updated

6. **Click "Import"**

7. **Verify Results**:
   - Should show: "1847 notes updated"
   - Open a few random cards and test both audio buttons work correctly

## File Naming Summary

```
koreantopik1_korean_0001.mp3     (vocabulary audio)
koreantopik1_example_ko_0001.mp3 (example audio - renamed)
...
```

## Master TSV Format (For Future Reference)

If exporting/re-importing the full deck:

```
number  korean  english  example_ko  example_en  etymology  notes  korean_audio  example_ko_audio
```

**Audio field formats**:
- `korean_audio`: `[sound:koreantopik1_korean_0001.mp3]`
- `example_ko_audio`: `[sound:koreantopik1_example_ko_0001.mp3]`

## Next Steps

1. **Copy files**: Move example + vocab audio to Anki media (Phase 4).
2. **Anki setup**: Add `korean_audio` field; update example audio field and templates.
3. **Import**: Re-import `koreantopik1_anki_import.tsv`.
4. **Test**: Verify audio plays correctly on a few cards

---

**Note**: Always backup your Anki collection before making bulk changes!
