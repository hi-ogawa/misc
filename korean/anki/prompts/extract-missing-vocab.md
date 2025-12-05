# Extract Missing Vocabulary from Example Sentences

## Goal

Flagged cards (orange/flag:2) contain example sentences that use vocabulary outside the TOPIK1 dataset. Extract these "missing" words and add them as custom cards to ensure examples are self-contained.

## Context

- TOPIK1 deck: 1847 vocabulary words
- Example sentences were generated using Claude, which naturally uses words beyond the TOPIK1 list
- Orange-flagged cards: ~154 cards identified as having non-self-contained examples

## Strategy

1. **Export flagged cards**
   - Query: `deck:Korean::TOPIK1 flag:2`
   - Output: `anki/output/flag-2.tsv`

2. **Extract missing vocabulary**
   - Claude eyeballs each `example_ko`
   - Identify vocabulary clearly beyond TOPIK1 level
   - Output: `anki/output/flag-2-extract.tsv`

3. **Generate custom cards**
   - For each extracted word, create note in `Korean::Custom` deck
   - Model: "Korean Vocabulary"
   - Tag: `extracted` (to distinguish from other custom sources)
   - Fields:
     - `number`: (blank)
     - `korean`: extracted word
     - `english`: translation (Claude generates)
     - `example_ko`: original sentence (as context)
     - `example_en`: original translation
     - `etymology`: Hanja / Japanese cognate (see `prompts/generate-etymology2.md`)
     - `notes`: related words, usage hints
     - `korean_audio`, `example_ko_audio`: (skip for now)
   - Action: `addNote` via AnkiConnect

4. **Unflag processed cards**
   - After extraction complete, set flag to 0
   - Action: `setSpecificValueOfCard` with card IDs and `flags: 0`

## Files

- `anki/output/flag-2.tsv` - Exported flagged cards (number, korean, example_ko)
- `anki/output/flag-2-extract.tsv` - With extracted vocabularies (number, korean, extracted, example_ko)

## Input

- Flagged cards via AnkiConnect: `findCards` + `cardsInfo`

## Output

- List of missing vocabulary words with translations
- Custom cards added to Anki (or TSV for manual import)
