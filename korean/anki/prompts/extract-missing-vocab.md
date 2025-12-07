# Extract Missing Vocabulary from Example Sentences

**Agent workflow**: Process flagged cards (flag:2) to identify and extract vocabulary from example sentences that looks difficult or worth learning as dedicated entries. Create custom cards for these words to make examples more self-contained.

**Trigger**: User says "start extract workflow" or "process N flagged cards"

**Process**: Manual batches (e.g., 10 cards at a time) - export current `flag:2` cards → agent processes requested batch → human reviews → unflag processed cards → repeat. Output files overwrite each run.

## Workflow

1. **Export flagged cards**
   - Script: `python scripts/anki-export.py --query "deck:Korean::TOPIK1 flag:2" --fields number,korean,example_ko,example_en --output anki/output/flag-2.tsv`

2. **Extract missing vocabulary** (agent)
   - Review each `example_ko` sentence and identify OTHER words (not the card's target `korean` word) that appear difficult or worth learning as dedicated entries
   - Use linguistic judgment to assess which vocabulary would be useful to extract (no scripts, no external data - just language understanding)
   - Output: `anki/output/flag-2-extract.tsv` (number, korean, extracted, example_ko)
   - Include ALL flagged cards in output (leave `extracted` empty if none found - user flagged for a reason)
   - Note: `extracted` may have multiple words comma-separated

3. **Review extractions** (human)
   - Review `flag-2-extract.tsv`
   - Remove false positives, add missed words

4. **Prepare card data** (agent)
   - Flatten: one row per extracted word
   - Generate for each word:
     - `english`: translation
     - `etymology`: see `prompts/requirements-etymology.md`
     - `notes`: see `prompts/requirements-notes.md`
   - Output: `anki/output/flag-2-cards.tsv`
   - Columns: source_number, korean, english, example_ko, example_en, etymology, notes

5. **Review card data** (human)
   - Review `flag-2-cards.tsv`
   - Fix translations, etymology, notes as needed

6. **Add notes to Anki**
   - Script: `python scripts/anki-add-notes.py --input anki/output/flag-2-cards.tsv [--unflag] [--dry-run]`
     - `--dry-run`: checks for duplicates before adding (run first to catch issues)
     - `--unflag`: sets flag to 0 on source cards after all notes added successfully
   - Deck: `Korean::Custom`
   - Model: "Korean Vocabulary"
   - Tag: `extracted`
   - Fields: number, korean, english, example_ko, example_en, etymology, notes

## Files

- `anki/output/flag-2.tsv` - Exported flagged cards
- `anki/output/flag-2-extract.tsv` - With extracted vocabularies
- `anki/output/flag-2-cards.tsv` - Final card data
