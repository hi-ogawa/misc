# Anki Integration

Tools and documentation for working with Anki via AnkiConnect.

## Files

- `guide.md` - AnkiConnect API patterns and scripting
- `prompts/` - Task documentation for Anki-related automation

## Decks

- `Korean::TOPIK1` - 1847 vocabulary cards (active study)
- `Korean::TOPIK2` - 3873 vocabulary cards (pending import)
- `Korean::Custom` - manually added cards

## Note Model: Korean Vocabulary

| Field | Description |
|-------|-------------|
| `number` | Unique ID (e.g., `1`, `koreantopik2_1`) |
| `korean` | Korean word/phrase |
| `english` | English translation |
| `example_ko` | Example sentence in Korean |
| `example_en` | Example sentence translation |
| `etymology` | Hanja / Japanese cognate (e.g., `可能 / 可能`) |
| `notes` | Study notes, mnemonics, related words |
| `korean_audio` | `[sound:filename.mp3]` for word pronunciation |
| `example_ko_audio` | `[sound:filename.mp3]` for example sentence |

## Audio Naming

- TOPIK1: `koreantopik1_korean_NNNN.mp3`, `koreantopik1_example_ko_NNNN.mp3`
- TOPIK2: `koreantopik2_korean_NNNN.mp3`, `koreantopik2_example_ko_NNNN.mp3`

## Flags

| Flag | Color | Purpose |
|------|-------|---------|
| 2 | Orange | (TBD - 154 cards currently flagged) |
