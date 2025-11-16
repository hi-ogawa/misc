# Generate Dual Audio for TOPIK 2 (Vocabulary + Examples)

## Goal
Generate two sets of audio files for TOPIK 2 vocabulary:
1. **Vocabulary audio** - Pronunciation of the Korean word/phrase itself
2. **Example audio** - Pronunciation of the example sentence using the word

## Rationale
- **Vocabulary audio**: Hear isolated pronunciation clearly
- **Example audio**: Hear word in context, natural speech flow
- **Better learning**: Compare isolated vs. contextual pronunciation
- **Anki flexibility**: Use both audio types in flashcards

## Status
✅ **Example audio exists** (3,873 files as `koreantopik2_NNNN.mp3` - needs renaming)
⏳ **Vocabulary audio pending**

## Input Files
- **Vocabulary**: `input/koreantopik2.tsv` (columns: number, korean, english)
- **Examples**: `output/koreantopik2/examples-all.tsv` (columns: number, korean, example_ko, example_en)

## Output Structure
```
output/koreantopik2/audio/
├── koreantopik2_korean_0001.mp3 to koreantopik2_korean_3873.mp3
└── koreantopik2_example_ko_0001.mp3 to koreantopik2_example_ko_3873.mp3
```

Total: 7,746 MP3 files in a single directory (~100-120MB)

## Script Features
The `scripts/generate-audio.py` script supports:
- `--field`: Specify which TSV column to read (e.g., `korean` or `example_ko`)
- `--prefix`: Add filename prefix (e.g., `koreantopik2_korean_` or `koreantopik2_example_ko_`)
- `--concurrency`: Generate multiple files in parallel (default: 1, recommended: 5-10)
- `--voice`: Choose voice (default: `ko-KR-SunHiNeural` female)

## Generation Steps

### Step 0: Rename Existing Example Audio Files

The existing example audio files need to be renamed from `koreantopik2_NNNN.mp3` to `koreantopik2_example_ko_NNNN.mp3`:

```bash
cd output/koreantopik2/audio

# Rename existing example audio files
for file in koreantopik2_[0-9][0-9][0-9][0-9].mp3; do
  number="${file#koreantopik2_}"
  number="${number%.mp3}"
  mv "$file" "koreantopik2_example_ko_${number}.mp3"
done

cd -
```

**Result**: 3,873 files renamed from `koreantopik2_NNNN.mp3` to `koreantopik2_example_ko_NNNN.mp3`

**Verification**:
```bash
ls output/koreantopik2/audio/koreantopik2_example_ko_*.mp3 | wc -l
# Expected: 3873

# Verify no old files remain
ls output/koreantopik2/audio/koreantopik2_[0-9][0-9][0-9][0-9].mp3 2>/dev/null | wc -l
# Expected: 0
```

### Step 1: Generate Vocabulary Audio

```bash
python scripts/generate-audio.py \
  --input input/koreantopik2.tsv \
  --field korean \
  --prefix koreantopik2_korean_ \
  --output output/koreantopik2/audio \
  --concurrency 5
```

**Parameters**:
- `--input`: Base vocabulary file (has `korean` column)
- `--field korean`: Read from `korean` column
- `--prefix koreantopik2_korean_`: Generate files as `koreantopik2_korean_NNNN.mp3`
- `--output`: Single audio directory for all files
- `--concurrency 5`: Generate 5 files in parallel (adjust based on network)

**Duration**: ~1-2 hours for 3,873 files at concurrency=5

**Result**: `koreantopik2_korean_0001.mp3` to `koreantopik2_korean_3873.mp3` in `output/koreantopik2/audio/`

### Step 2: Generate Example Audio (Optional - Already Completed)

**Note**: Example audio files already exist (renamed in Step 0). This step is only needed if you want to regenerate them.

```bash
python scripts/generate-audio.py \
  --input output/koreantopik2/examples-all.tsv \
  --field example_ko \
  --prefix koreantopik2_example_ko_ \
  --output output/koreantopik2/audio \
  --force \
  --concurrency 5
```

**Parameters**:
- `--input`: Example sentences file
- `--field example_ko`: Read from `example_ko` column
- `--prefix koreantopik2_example_ko_`: Generate files as `koreantopik2_example_ko_NNNN.mp3`
- `--output`: Same audio directory (flat structure)
- `--force`: Overwrite existing files

**Duration**: ~1-2 hours for 3,873 files at concurrency=5

**Result**: `koreantopik2_example_ko_0001.mp3` to `koreantopik2_example_ko_3873.mp3` in `output/koreantopik2/audio/`

### Step 3: Verify Generation

```bash
# Count vocabulary audio files
ls output/koreantopik2/audio/koreantopik2_korean_*.mp3 | wc -l
# Expected: 3873

# Count example audio files
ls output/koreantopik2/audio/koreantopik2_example_ko_*.mp3 | wc -l
# Expected: 3873

# Check total size
du -sh output/koreantopik2/audio/
# Expected: ~100-120M

# Verify MP3 integrity (all files)
python scripts/generate-audio-verify.py --output output/koreantopik2/audio

# Analyze duration statistics (korean)
find output/koreantopik2/audio -name "koreantopik2_korean_*.mp3" -print0 | \
  xargs -0 python scripts/generate-audio-stats.py

# Analyze duration statistics (example_ko)
find output/koreantopik2/audio -name "koreantopik2_example_ko_*.mp3" -print0 | \
  xargs -0 python scripts/generate-audio-stats.py
```

### Step 4: Create Zip Archives

```bash
cd output/koreantopik2/audio

# Vocabulary audio archive
zip -r ../koreantopik2_korean_audio.zip koreantopik2_korean_*.mp3

# Example audio archive
zip -r ../koreantopik2_example_ko_audio.zip koreantopik2_example_ko_*.mp3

# Combined archive (optional)
zip -r ../koreantopik2_audio_all.zip koreantopik2_*.mp3

cd -
```

**Result**:
- `output/koreantopik2/koreantopik2_korean_audio.zip` (~25M)
- `output/koreantopik2/koreantopik2_example_ko_audio.zip` (~50M)
- `output/koreantopik2/koreantopik2_audio_all.zip` (~75M, optional)

### Step 5: Copy to Anki Media Directory

```bash
# Copy all audio files to Anki
cp output/koreantopik2/audio/koreantopik2_*.mp3 ~/.local/share/Anki2/"User 1"/collection.media/
```

## Master File Format

The consolidated `master-all.tsv` should have **9 columns**:

```
number  korean  english  etymology  example_ko  example_en  notes  korean_audio  example_ko_audio
```

**Audio field formats**:
- `korean_audio`: `[sound:koreantopik2_korean_0001.mp3]`
- `example_ko_audio`: `[sound:koreantopik2_example_ko_0001.mp3]`

**Example row**:
```
1	-가	professional	-家 / -家	친구가 의사가 됐어요	My friend became a doctor	직업가, 작가, 음악가	[sound:koreantopik2_korean_0001.mp3]	[sound:koreantopik2_example_ko_0001.mp3]
```

## Usage in Anki

**Front of card**: Show Korean word (optionally with auto-play vocab audio)
**Back of card**: Show all fields including:
- Vocabulary audio (isolated pronunciation)
- Example sentence with audio (contextual pronunciation)
- Etymology, notes, etc.

This allows learners to:
1. Test recognition of the written word
2. Hear isolated pronunciation
3. See example in context
4. Hear natural contextual pronunciation

## Voice Settings

**Default**: `ko-KR-SunHiNeural` (female voice)
**Alternative**: `ko-KR-InJoonNeural` (male voice)

To use male voice:
```bash
python scripts/generate-audio.py --voice ko-KR-InJoonNeural ...
```

## Resuming After Interruption

If generation is interrupted (Ctrl-C or network issues):
```bash
# Script automatically skips existing files
python scripts/generate-audio.py \
  --input input/koreantopik2.tsv \
  --field korean \
  --prefix koreantopik2_korean_ \
  --output output/koreantopik2/audio \
  --concurrency 5
```

The script will skip already-generated files and continue from where it stopped.

## Regenerating Specific Ranges

To regenerate files 100-200 (useful for fixing issues):
```bash
python scripts/generate-audio.py \
  --input input/koreantopik2.tsv \
  --field korean \
  --prefix koreantopik2_korean_ \
  --output output/koreantopik2/audio \
  --start 100 \
  --end 200 \
  --force \
  --concurrency 5
```

The `--force` flag will overwrite existing files in that range.

## File Naming Convention

| Audio Type | Input File | Column | Prefix | Output Format |
|------------|------------|--------|--------|---------------|
| Vocabulary | `koreantopik2.tsv` | `korean` | `koreantopik2_korean_` | `koreantopik2_korean_NNNN.mp3` |
| Example | `examples-all.tsv` | `example_ko` | `koreantopik2_example_ko_` | `koreantopik2_example_ko_NNNN.mp3` |

## Quality Checks

After generation:
- [ ] 3,873 vocabulary audio files exist
- [ ] 3,873 example audio files exist
- [ ] All files are valid MP3 format
- [ ] File sizes reasonable (~3-30KB per file)
- [ ] Spot-check: Listen to random samples for quality
- [ ] Verify filenames match expected format

## Next Steps

After dual audio generation is complete:
1. Create master-all.tsv with both audio columns
2. Import into Google Sheets for review
3. Create Anki deck with dual-audio cards
4. Begin studying!

---

**Note**: This dual-audio approach provides maximum flexibility. You can use:
- Only vocabulary audio (focus on isolated pronunciation)
- Only example audio (focus on contextual learning)
- Both (comprehensive learning experience)

Choose based on your learning preferences when designing Anki cards.
