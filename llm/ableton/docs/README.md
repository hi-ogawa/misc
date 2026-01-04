# Documentation Directory

## Structure

```
docs/
├── README.md       # This file
└── official/       # Ableton Live 12 official manual (git-ignored)
    ├── 01-welcome-to-live.md
    ├── 02-first-steps.md
    ├── 10-editing-midi.md
    ├── 37-live-keyboard-shortcuts.md
    └── ...42 chapters total
```

## Official Documentation (git-ignored)

**Location**: `docs/official/*.md`

**Status**: ⚠️ **NOT COMMITTED TO GIT** (copyright considerations)

### How to Generate Locally

```bash
# From repository root
uv sync                              # Install dependencies
uv run scripts/fetch-manual.py       # Fetch HTML (~30 seconds, async)
uv run scripts/convert-manual.py     # Convert to markdown (~1 minute)
```

This will:
1. **Fetch**: Download 42 chapters from https://www.ableton.com/en/live-manual/12/ (async, parallel)
2. **Convert**: Extract `#chapter_content` div and convert HTML → clean markdown
3. **Output**: Save to `docs/official/*.md` with frontmatter (title, source URL, scrape date)

### Why Git-Ignored?

- **Copyright**: Ableton's documentation is their intellectual property
- **Reproducible**: Anyone can regenerate with one command
- **Up-to-date**: Re-scrape when Ableton updates docs

### Verification

After running the script, you should have:
- 42 markdown files in `docs/official/`
- Each with frontmatter (title, source URL, scrape date)
- Clean content extracted from `#chapter_content` div only

See `notes/docs-aggregation.md` for detailed documentation on the scraping process.

## Future Additions (Planned)

- `keyboard-shortcuts.md` - Exported from Ableton Preferences
- `glossary.md` - Ableton-specific terminology (if needed)
- `resources/` - Well-known community resources (if official docs prove insufficient)
