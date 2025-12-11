# Extract Missing Vocabulary from Example Sentences

Extract vocabulary from flagged cards' example sentences that looks difficult or worth learning as dedicated entries.

**Trigger**: User says "start extract workflow" or "process extract"

**Process**: Manual batches (e.g., 10 cards at a time) - export current `flag:2` cards → agent processes requested batch → human reviews → unflag processed cards → repeat. Output files overwrite each run.

## Workflow

### 1. Export flagged cards

```bash
python scripts/anki-export.py \
  --query "(deck:Korean::TOPIK1 OR deck:Korean::Custom) flag:2" \
  --fields number,korean,example_ko,example_en \
  --output anki/output/flag-2.tsv
```

### 2. Extract missing vocabulary (agent)

- Review each `example_ko` and identify OTHER words (not the target `korean`) worth learning.
- Use linguistic judgment (no scripts, no external data).
- Output: `anki/output/flag-2-extract.tsv` (number, korean, extracted, example_ko)
- Include ALL flagged cards (leave `extracted` empty if none found)
- `extracted` may have multiple words comma-separated

### 3. Review extractions (human)

- Review `flag-2-extract.tsv`
- Remove false positives, add missed words

### 4. Prepare card data (agent)

- Flatten: one row per extracted word
- Generate for each word:
  - `number`: Unique ID in format `extract_YYYYMMDD_NNN` (e.g., `extract_20251212_001`)
  - `english`: translation
  - `example_ko`: fresh example sentence (see `prompts/requirements-example.md`)
  - `example_en`: translation of example
  - `etymology`: see `prompts/requirements-etymology.md`
  - `notes`: see `prompts/requirements-notes.md`
- Output: `anki/output/flag-2-cards.tsv`
- Columns: number, korean, english, example_ko, example_en, etymology, notes

### 5. Review card data (human)

- Review `flag-2-cards.tsv`
- Fix translations, etymology, notes as needed

### 6. Generate audio

```bash
python scripts/generate-audio.py \
  --input anki/output/flag-2-cards.tsv \
  --output output/audio/extracted \
  --field korean --id-field number --prefix korean_ \
  --concurrency 5 --force

python scripts/generate-audio.py \
  --input anki/output/flag-2-cards.tsv \
  --output output/audio/extracted \
  --field example_ko --id-field number --prefix example_ko_ \
  --concurrency 5 --force
```

### 7. Add audio columns

```bash
python scripts/jq-tsv.py \
  '. + {korean_audio: "[sound:korean_\(.number).mp3]", example_ko_audio: "[sound:example_ko_\(.number).mp3]"}' \
  anki/output/flag-2-cards.tsv > anki/output/flag-2-cards-import.tsv
```

### 8. Add notes to Anki

```bash
# Dry-run first
python scripts/anki-add-notes.py \
  --input anki/output/flag-2-cards-import.tsv \
  --deck "Korean::Custom" \
  --tag "extracted" \
  --dry-run

# Then run without --dry-run
python scripts/anki-add-notes.py \
  --input anki/output/flag-2-cards-import.tsv \
  --deck "Korean::Custom" \
  --tag "extracted"
```

### 9. Copy audio to Anki media

```bash
cp output/audio/extracted/*.mp3 "$(python scripts/anki.py getMediaDirPath | tr -d '"')"
```

## Files

| File | Description |
|------|-------------|
| `anki/output/flag-2.tsv` | Exported flagged cards |
| `anki/output/flag-2-extract.tsv` | With extracted vocabularies |
| `anki/output/flag-2-cards.tsv` | Card data with content |
| `anki/output/flag-2-cards-import.tsv` | Final import file with audio refs |
| `output/audio/extracted/` | Generated audio files |
