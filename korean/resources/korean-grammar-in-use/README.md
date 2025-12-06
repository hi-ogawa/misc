Korean Grammar in Use - Beginning

Reference material from the textbook "Korean Grammar in Use - Beginning" (112 patterns).

## Files

- `toc.md` - Table of contents with example sentences and gap markers
- `gap-analysis.md` - Analysis of gaps vs TOPIK 1 coverage
- `plan-anki-cards.md` - Plan for generating Anki cards from gaps
- `output/` - Generated files for Anki import
  - `grammar-cards.tsv` - Working file (7 columns)
  - `grammar_anki_import.tsv` - Anki import file (9 columns)
  - `audio/` - 23 MP3 files for example sentences

## Workflow

1. Dumped book's table of contents into `toc.md`
2. Agent enhanced with one-liner example sentences
3. Skimmed content and marked gaps:
   - `#` = not familiar (implies not covered in TOPIK 1)
   - `@` = explicitly not covered in TOPIK 1
4. Agent generated `gap-analysis.md` from markers

## Status

- [x] TOC with examples
- [x] Gap markers added
- [x] Review gap-analysis.md
- [x] Generate Anki cards (23 patterns)
- [x] Generate audio for example sentences
- [x] Import to Anki

## Retrospective

**What worked well:**
- Marking gaps directly in source (`#`/`@` in toc.md) - quick and intuitive
- Simplified `korean` field (`-나` vs `N(이)나`) with full notation in `notes`
- `scripts/anki-add-notes.py` now handles both extract workflow and direct import

**Future ideas:**
- Grammar → Vocab linking: Tag existing TOPIK vocab cards that use these grammar patterns
- More examples per pattern: Generate 2-3 variants for harder patterns
- Intermediate book: Same workflow for "Korean Grammar in Use - Intermediate"
- Review-driven: Flag grammar cards during review if example feels weak → regenerate
- Prompt template: Formalize grammar card generation as reusable prompt
