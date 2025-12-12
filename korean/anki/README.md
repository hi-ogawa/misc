# Anki Integration

Tools and documentation for working with Anki via AnkiConnect.

## Structure

```
anki/
├── guide.md                     # AnkiConnect API patterns
└── prompts/
    │
    │ # TOPIK 1 (1,847 cards)
    ├── process-fix.md           # Fix-tagged cards
    ├── update-etymology.md      # Incremental updates
    ├── update-etymology-full.md # Full regeneration
    │
    │ # TOPIK 2 (3,179 cards)
    ├── (see prompts/koreantopik2/plan.md)
    │
    │ # Custom
    ├── add-audio.md             # Add audio to notes
    ├── manual.md                # Manual vocab collection
    ├── extract-missing-vocab.md # Extract from flagged examples
    │
    │ # Dialogue (50 cards)
    ├── production-dialogues.md  # Dialogue card creation
    │
    │ # Utilities
    ├── check-duplicates.md      # Find duplicate entries
    └── audio-cleanup.md         # Audio file analysis
```

## Note Model: Korean Vocabulary

| Field | Description |
|-------|-------------|
| `number` | Unique ID (e.g., `1`, `koreantopik2_092_0001`) |
| `korean` | Korean word/phrase |
| `english` | English translation |
| `example_ko` | Example sentence in Korean |
| `example_en` | Example sentence translation |
| `etymology` | Hanja / Japanese cognate |
| `notes` | Study notes, mnemonics, related words |
| `korean_audio` | `[sound:filename.mp3]` |
| `example_ko_audio` | `[sound:filename.mp3]` |
