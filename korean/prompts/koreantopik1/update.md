# Update TOPIK 1 Deck with Dual Audio

## Current State

**TOPIK 1 Dataset**: 1,847 words already imported into Anki
- ✅ Example sentences exist
- ✅ Example audio exists: `koreantopik1_NNNN.mp3` (1,847 files in Anki media)
- ❌ Vocabulary audio missing: Need to add isolated word pronunciation

## Goal

Add vocabulary audio (isolated word pronunciation) to existing TOPIK 1 Anki deck without disrupting current cards.

## Strategy

Since the deck is already in Anki with existing cards, we need to:
1. Generate vocabulary audio for all 1,847 words
2. Update Anki cards to add the new vocabulary audio field
3. Keep existing example audio intact

## File Naming Convention

Following the TOPIK 2 dual-audio pattern:
- **Vocabulary audio**: `koreantopik1_korean_NNNN.mp3` (NEW)
- **Example audio**: `koreantopik1_example_ko_NNNN.mp3` (rename from existing `koreantopik1_NNNN.mp3`)

## Implementation Plan

### Phase 1: Generate Vocabulary Audio

#### Step 1: Generate vocabulary audio files

```bash
python scripts/generate-audio.py \
  --input input/koreantopik1.tsv \
  --field korean \
  --prefix koreantopik1_korean_ \
  --output output/koreantopik1/audio \
  --concurrency 5
```

**Result**: 1,847 files as `koreantopik1_korean_NNNN.mp3`

**Duration**: ~1 hour at concurrency=5

#### Step 2: Verify generation

```bash
# Count generated files
ls output/koreantopik1/audio/koreantopik1_korean_*.mp3 | wc -l
# Expected: 1847

# Check file sizes
du -sh output/koreantopik1/audio/
# Expected: ~50M
```

### Phase 2: Use latest example audio (v2) and rename

Source: `output/koreantopik1/koreantopik1_v2_audio.zip` (files `koreantopik1_v2_NNNN.mp3`).

**Done (staging):**
- Unzipped to `output/koreantopik1/audio/`.
- Renamed all v2 files to `koreantopik1_example_ko_NNNN.mp3` (1,847 files) in `output/koreantopik1/audio/`.

**Apply to Anki media (overwrite old example audio names):**
```bash
cp output/koreantopik1/audio/koreantopik1_example_ko_*.mp3 ~/.local/share/Anki2/"사용자 1"/collection.media/
```

**Verification** (after copying):
```bash
ls ~/.local/share/Anki2/"사용자 1"/collection.media/koreantopik1_example_ko_*.mp3 | wc -l   # expect 1847
ls ~/.local/share/Anki2/"사용자 1"/collection.media/koreantopik1_[0-9][0-9][0-9][0-9].mp3 2>/dev/null | wc -l  # expect 0 (if old names removed)
```

### Phase 3: Copy New Vocabulary Audio to Anki

```bash
# Copy new vocabulary audio files to Anki
cp output/koreantopik1/audio/koreantopik1_korean_*.mp3 ~/.local/share/Anki2/"사용자 1"/collection.media/
```

**Verification**:
```bash
ls ~/.local/share/Anki2/"사용자 1"/collection.media/koreantopik1_korean_*.mp3 | wc -l
# Expected: 1847
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

### Phase 5: Bulk Update Audio References

**Option A: Manual update in Anki**
1. Export deck as CSV
2. Find and replace in spreadsheet:
   - Find: `[sound:koreantopik1_`
   - Replace: `[sound:koreantopik1_example_ko_`
3. Add new column for vocabulary audio
4. Re-import to Anki

**Option B: SQL update (Advanced)**
Use Anki database tools to update field values programmatically.

**Option C: Add-on**
Use "Advanced Find and Replace" Anki add-on to bulk update fields.

## Alternative: Non-Breaking Approach

If you want to avoid renaming existing files in Anki:

### Keep old example audio as-is
- Leave `koreantopik1_NNNN.mp3` unchanged in Anki
- Generate vocabulary audio as `koreantopik1_korean_NNNN.mp3`
- Copy vocabulary audio to Anki
- Add new field for vocabulary audio only
- No need to update existing example audio references

**Pros**:
- Simpler - no file renaming needed
- Existing cards work without modification
- Only need to add one new field

**Cons**:
- Inconsistent naming with TOPIK 2
- File naming less explicit

## Recommended Approach

**Start with Alternative (Non-Breaking)**:
1. Generate vocabulary audio with `koreantopik1_korean_` prefix
2. Copy to Anki media directory
3. Add `korean_audio` field to note type
4. Populate field with vocabulary audio references
5. Update card template to show vocabulary audio

**Later** (optional cleanup):
- Can rename example audio files if desired for consistency
- Update references in batch
- This can be done incrementally without breaking cards

## File Naming Summary

### Current State (in Anki)
```
koreantopik1_0001.mp3 (example audio)
koreantopik1_0002.mp3 (example audio)
...
```

### After Update (Non-Breaking)
```
koreantopik1_0001.mp3           (example audio - unchanged)
koreantopik1_korean_0001.mp3    (vocabulary audio - NEW)
...
```

### After Full Migration (Optional)
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

1. **Immediate**: Generate vocabulary audio
2. **Anki setup**: Add korean_audio field
3. **Copy files**: Move vocabulary audio to Anki media
4. **Test**: Verify audio plays correctly on a few cards
5. **Bulk populate**: Fill korean_audio field for all cards
6. **Optional**: Rename example audio for consistency

---

**Note**: Always backup your Anki collection before making bulk changes!
