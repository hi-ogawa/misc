# Korean Language Learning Materials

AI-assisted Korean vocabulary processing using Claude Code prompts.

## Purpose

This project uses Claude prompts to enhance Korean vocabulary learning materials with:
- Etymology information (Hanja and Japanese cognates)
- Example sentences with translations
- Audio pronunciation files
- Study notes and mnemonics

## Project Structure

```
korean/
├── prompts/          # Claude Code prompts (tracked in git)
│   ├── generate-etymology.md
│   ├── generate-etymology2.md
│   ├── generate-examples.md
│   ├── generate-example2.md
│   ├── generate-example3.md
│   ├── generate-notes.md
│   ├── generate-audio.md
│   └── generate-fix.md
├── topik1/           # TOPIK 1 vocabulary data (not tracked)
│   └── readme.md     # Detailed extraction docs (tracked)
├── input/            # Input data files (not tracked)
├── output/           # Generated content (not tracked)
├── scripts/          # Helper scripts (not tracked)
└── README.md         # This file
```

## Workflow

### 1. Vocabulary Extraction
- Source: TOPIK 1 vocabulary list (1847 words) from koreantopik.com
- Process documented in [topik1/readme.md](topik1/readme.md)
- Output: `input/korean-english.tsv` (base vocabulary file)

### 2. Enhancement via Claude Prompts
Each prompt in `prompts/` directory processes the base vocabulary:

- **Input**: `input/korean-english.tsv`
- **Prompts**: `prompts/generate-*.md` (etymology, examples, notes, audio, etc.)
- **Output**: `output/*-N.tsv` (chunked files) and `output/*-all.tsv` (consolidated)

### 3. Manual Consolidation
- Combine generated TSV files in Google Sheets
- Review and edit as needed
- Final output ready for Anki import

### 4. Anki Import
- Load consolidated vocabulary into Anki deck
- Study with enhanced content (etymology, examples, audio, notes)

### 5. Maintenance & Fixes
- During practice in Anki, you may find issues:
  - Awkward or unnatural example sentences
  - Incorrect translations
  - Audio pronunciation problems
- Use `prompts/generate-fix.md` to track fixes:
  - Document the corrected entry (number, korean, example_ko, example_en)
  - Generate new audio with `_fix` suffix
  - Update Anki card to use new audio file
- Fixes are tracked ad-hoc in the prompt file only (no sync back to source files)

## Progress

- [x] TOPIK 1 vocabulary extraction (1847 words)
- [x] Hanja and Japanese etymology columns
- [x] Consolidated all.csv file
- [x] Audio generation
- [x] Example sentences generation
- [x] Study notes generation

## Data Files

**Tracked in git:**
- `prompts/*.md` - All Claude prompts
- `topik1/readme.md` - Extraction process documentation
- `README.md` - This file

**Not tracked in git:**
- `input/korean-english.tsv` - Base vocabulary file (generated from topik1 extraction)
- `topik1/*.csv`, `topik1/*.txt` - Raw extraction files
- `output/*` - Generated enhancement files (etymology, examples, notes, etc.)
- `*.mp3` - Audio files
- `scripts/*` - Helper scripts
- Temporary/intermediate files

**Combined results:**
- All generated data combined and available on [Google Drive](https://drive.google.com/drive/u/0/folders/1fzfewUUWmRCqEhtdHFK0wuN3PO0qnSPB)

## Usage

1. Place input vocabulary in `input/`
2. Select appropriate prompt from `prompts/`
3. Run Claude Code with the prompt
4. Review generated output
5. Iterate as needed

---

**Note**: This is a personal learning project using Claude Code for vocabulary enhancement.
