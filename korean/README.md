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

### 1. Source Data
- TOPIK 1 vocabulary list: 1847 words from koreantopik.com
- Extraction details: See [topik1/readme.md](topik1/readme.md)

### 2. Enhancement Pipeline
1. **Etymology**: Add Hanja (漢字) and Japanese cognates for Sino-Korean words
2. **Examples**: Generate example sentences with translations
3. **Audio**: Create pronunciation audio files using edge-tts
4. **Notes**: Add study notes and memory aids

### 3. Claude Prompts
All prompts are in `prompts/` directory. Each handles a specific transformation:
- Input: TSV/CSV vocabulary files
- Output: Enhanced files with additional columns
- Processing: Automated via Claude Code

## Progress

- [x] TOPIK 1 vocabulary extraction (1847 words)
- [x] Hanja and Japanese etymology columns
- [x] Consolidated all.csv file
- [x] Audio generation
- [x] Example sentences generation
- [x] Study notes generation

## Data Files

Data files (CSV, TSV, MP3, TXT) are **not tracked in git**:
- Input vocabulary files
- Generated audio
- Intermediate processing files
- Output files

Only prompts and documentation are version controlled.

## Usage

1. Place input vocabulary in `input/`
2. Select appropriate prompt from `prompts/`
3. Run Claude Code with the prompt
4. Review generated output
5. Iterate as needed

---

**Note**: This is a personal learning project using Claude Code for vocabulary enhancement.
