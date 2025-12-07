# Manual Vocabulary Collection

Collect vocabulary from Korean content (YouTube, Instagram, etc.) and add to Anki.

## Capture (during video)

Save to `anki/input/`:

**Screenshots** (1 per vocabulary):
- Capture subtitle moment with target word highlighted/visible
- Provides visual context for Agent OCR extraction

**Notes** (`manual.md`):
- Source URLs
- Target words with `->` marker
- Full transcript (Korean | English table) for example sentence context

Example `manual.md`:
```markdown
# https://www.instagram.com/p/...

합주전 드럼 시점. 튜닝중 외로운 드럼
-> 합주, 시점

# https://www.youtube.com/watch?v=...

지금 수상 받고 왔습니다
-> 수상

| Korean | English |
| --- | --- |
| 저희가 아이돌인데도 영화제에 참석하는 게 | Even though we're idols, attending a film festival... |
| 너무 뭔가 귀한 거 같고 신기해요 | It feels so precious and amazing |
| ... | ... |
```

## Workflow

### 1. Extract vocabulary from screenshots and notes

- Agent OCR extracts highlighted vocabulary from screenshots
- Cross-reference with `->` markers in notes
- Manual verification recommended

### 2. Generate card fields

- `number`: Unique ID in format `manual_YYYYMMDD_NNN` (e.g., `manual_20251207_001`)
- `example_ko`: From original content (transcript), not generated
  - Should have enough context to provoke memory (not too short)
  - Can combine multiple lines if needed
- `example_en`: Translation of example
- `etymology`: Following `prompts/requirements-etymology.md`
- `notes`: Following `prompts/requirements-notes.md`
- Output: `anki/output/manual-cards.tsv`
- Review and iterate with user before proceeding

### 3. Generate audio files

```bash
rm -rf output/audio/custom && mkdir -p output/audio/custom

python scripts/generate-audio.py \
  --input anki/output/manual-cards.tsv \
  --output output/audio/custom \
  --field korean --id-field number --prefix korean_

python scripts/generate-audio.py \
  --input anki/output/manual-cards.tsv \
  --output output/audio/custom \
  --field example_ko --id-field number --prefix example_ko_
```

Audio filenames: `korean_manual_20251207_001.mp3`, `example_ko_manual_20251207_001.mp3`

### 4. Prepare import file with audio references

```bash
python scripts/jq-tsv.py \
  '. + {korean_audio: "[sound:korean_\(.number).mp3]", example_ko_audio: "[sound:example_ko_\(.number).mp3]"}' \
  anki/output/manual-cards.tsv > anki/output/manual-cards-import.tsv
```

### 5. Add to Anki (manual)

```bash
# Dry-run first
python scripts/anki-add-notes.py \
  --input anki/output/manual-cards-import.tsv \
  --deck "Korean::Custom" \
  --tag "manual" \
  --dry-run

# Then run without --dry-run
python scripts/anki-add-notes.py \
  --input anki/output/manual-cards-import.tsv \
  --deck "Korean::Custom" \
  --tag "manual"
```

### 6. Copy audio to Anki media (manual)

```bash
cp output/audio/custom/*.mp3 "$(python scripts/anki.py getMediaDirPath | tr -d '"')"
```

### 7. Cleanup (manual)

```bash
rm -rf anki/input/*
```

## Fields

| Field | Source |
|-------|--------|
| `korean` | Target word/phrase |
| `english` | Translation |
| `example_ko` | Original subtitle context |
| `example_en` | Translation of example |
| `etymology` | Per `requirements-etymology.md` |
| `notes` | Per `requirements-notes.md` |
| `korean_audio` | Generated TTS |
| `example_ko_audio` | Generated TTS |

## Related

- `anki/prompts/add-audio.md` - Audio generation workflow
- `prompts/requirements-etymology.md` - Etymology standards
- `prompts/requirements-notes.md` - Notes standards
