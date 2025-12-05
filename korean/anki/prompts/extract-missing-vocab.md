# Extract Missing Vocabulary from Example Sentences

## Goal

Flagged cards (orange/flag:2) contain example sentences that use vocabulary outside the TOPIK1 dataset. Extract these "missing" words and add them as custom cards to ensure examples are self-contained.

## Context

- TOPIK1 deck: 1847 vocabulary words
- Example sentences were generated using Claude, which naturally uses words beyond the TOPIK1 list
- Orange-flagged cards: cards identified as having non-self-contained examples

## Incremental Processing

Process is designed to run incrementally:
- Export always queries current `flag:2` cards
- After processing a batch, unflag those cards
- Next run sees only remaining unprocessed cards
- Files overwrite each run (represent current batch, not history)

## Strategy

1. **Export flagged cards**
   - Query: `deck:Korean::TOPIK1 flag:2`
   - Output: `anki/output/flag-2.tsv` (number, korean, example_ko, example_en)

2. **Extract missing vocabulary**
   - Claude eyeballs each `example_ko`
   - Identify vocabulary clearly beyond TOPIK1 level
   - Output: `anki/output/flag-2-extract.tsv` (number, korean, extracted, example_ko)
   - Note: `extracted` may have multiple words comma-separated

3. **Manual review** (human)
   - Review `flag-2-extract.tsv`
   - Remove false positives (words that are actually basic)
   - Add any missed words

4. **Prepare card data**
   - Flatten: one row per extracted word
   - Generate for each word:
     - `english`: translation
     - `etymology`: see `prompts/requirements-etymology.md`
     - `notes`: see `prompts/requirements-notes.md`
   - Output: `anki/output/flag-2-cards.tsv`
   - Columns: korean, english, example_ko, example_en, etymology, notes

5. **Review card data** (human)
   - Review `flag-2-cards.tsv`
   - Fix translations, etymology, notes as needed

6. **Add notes to Anki**
   - Deck: `Korean::Custom`
   - Model: "Korean Vocabulary"
   - Tag: `extracted`
   - Action: `addNote` via AnkiConnect
   - Fields: number (blank), korean, english, example_ko, example_en, etymology, notes
   - Skip: korean_audio, example_ko_audio

7. **Unflag processed cards**
   - After cards added, set flag to 0
   - Action: `setSpecificValueOfCard` with card IDs and `flags: 0`

## Files

- `anki/output/flag-2.tsv` - Exported flagged cards (number, korean, example_ko, example_en)
- `anki/output/flag-2-extract.tsv` - With extracted vocabularies (number, korean, extracted, example_ko)
- `anki/output/flag-2-cards.tsv` - Final card data ready for import (korean, english, example_ko, example_en, etymology, notes)

## Input

- Flagged cards via AnkiConnect: `findCards` + `cardsInfo`

## Output

- List of missing vocabulary words with translations
- Custom cards added to Anki (or TSV for manual import)
