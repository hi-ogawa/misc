# Extract Missing Vocabulary from Example Sentences

Extract vocabulary from flagged cards (flag:2) that use words outside the TOPIK1 dataset (1847 words). Add as custom cards to ensure examples are self-contained.

**Incremental**: Export queries current `flag:2` cards → process batch → unflag → repeat. Files overwrite each run.

## Workflow

1. **Export flagged cards**
   - Script: `python scripts/anki-export.py --query "deck:Korean::TOPIK1 flag:2" --fields number,korean,example_ko,example_en --output anki/output/flag-2.tsv`

2. **Extract missing vocabulary**
   - LLM reviews each `example_ko` using language understanding (not rule-based)
   - Identify vocabulary beyond TOPIK1 level
   - Output: `anki/output/flag-2-extract.tsv` (number, korean, extracted, example_ko)
   - Note: `extracted` may have multiple words comma-separated

3. **Review extractions** (human)
   - Review `flag-2-extract.tsv`
   - Remove false positives, add missed words

4. **Prepare card data**
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
     - With `--unflag`: sets flag to 0 on source cards after all notes added successfully
   - Deck: `Korean::Custom`
   - Model: "Korean Vocabulary"
   - Tag: `extracted`
   - Fields: number, korean, english, example_ko, example_en, etymology, notes

## Files

- `anki/output/flag-2.tsv` - Exported flagged cards
- `anki/output/flag-2-extract.tsv` - With extracted vocabularies
- `anki/output/flag-2-cards.tsv` - Final card data
