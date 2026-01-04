# Ableton Live Lite Knowledge Base

Personal knowledge base for learning Ableton Live Lite, focused on bass cover production and MIDI transcription workflows.

## Purpose

**Problem**: LLM hallucinations when asking Ableton-specific questions lead to incorrect shortcuts, non-existent features, and wasted troubleshooting time.

**Solution**: Build a ground-truth knowledge base from official documentation and verified personal workflows, enabling accurate LLM-assisted lookup without external verification.

## ⚠️ Regenerating Documentation

**Official docs are NOT committed to git** (copyright considerations).

To regenerate locally:
```bash
uv sync                              # Install dependencies
uv run scripts/fetch-manual.py       # Fetch HTML (~30 sec)
uv run scripts/convert-manual.py     # Convert to markdown (~1 min)
```

See `docs/README.md` and `notes/docs-aggregation.md` for details.

---

## Approach

### Phase 1: Official Documentation (Current)
- Collect and convert official Ableton documentation to markdown
- Test LLM retrieval accuracy with real questions
- Verify: Can LLM answer accurately without hallucinating?

### Phase 2: Trusted Resources (Future)
- Add well-known community resources if Phase 1 succeeds
- Expand coverage of advanced topics

### Phase 3: Personal Workflows (Later)
- Document personal discoveries and workflows
- Only add what's not in official sources
- Keep minimal and verified

## Repository Structure

```
/
├── README.md           # This file
├── workflow.md         # Personal workflow notes (✅ VERIFIED against official docs)
│                       # Mix of: Ableton-specific + general audio + personal setup
├── docs/               # Documentation (see docs/README.md)
│   ├── README.md       # Documentation structure and reproduction instructions
│   └── official/       # ⚠️ GIT-IGNORED: Official Ableton docs (regenerate locally)
│       ├── 01-welcome-to-live.md
│       ├── 10-editing-midi.md
│       ├── 37-live-keyboard-shortcuts.md
│       └── ...42 chapters (use scripts/scrape-manual.py to generate)
├── scripts/            # Documentation scraping/conversion scripts
│   ├── scrape-manual.py
│   └── convert-manual.py
└── notes/              # Planning and documentation notes
    └── docs-aggregation.md
```

**Note**: While the primary focus is Ableton-specific documentation, `workflow.md` also contains general audio production knowledge (compression/EQ concepts) and personal workflow preferences that may be useful beyond Ableton.

## Current Status

- ✅ Initial plan created
- ✅ Official Ableton Live 12 documentation scraped and converted (42 chapters)
- ✅ Personal workflow documented and **VERIFIED** against official docs
- ✅ LLM retrieval accuracy validated (successfully corrected 8+ hallucinations in workflow.md)
- ✅ **PROOF OF CONCEPT COMPLETE** - approach works as intended

## Context

- **Background**: Linux audio production (Ardour, JACK, PipeWire)
- **Current setup**: Windows 11 + Ableton Live Lite + Focusrite Scarlett
- **Use case**: Bass cover recording, mixing, and manual MIDI transcription
- **Learning philosophy**: Manual transcription as ear training practice

## Success Criteria

- Ask 10 Ableton questions → get accurate answers from knowledge base
- LLM cites specific docs instead of guessing
- No need to verify answers against external sources
- Faster learning without re-discovering forgotten shortcuts

## What Worked

✅ **Successfully validated the approach**:
1. Scraped all 42 chapters from official Ableton Live 12 manual
2. Converted to clean markdown with metadata preservation
3. Used docs to verify and fix `workflow.md` - caught 8+ hallucinations:
   - Fixed incorrect keyboard shortcuts (`F`, `A`, `Ctrl+L`, `Alt+Space`)
   - Identified PerforModule-only shortcuts (locators: `/`, `,`, `.`)
   - Corrected default Ableton behavior vs. third-party templates

**Result**: LLM can now accurately answer Ableton questions by referencing official docs instead of hallucinating.

## Next Steps (Optional)

**Nice to have** (not required for basic usage):
1. Export keyboard shortcuts from Ableton Preferences for quick reference
2. Test with more complex questions to validate edge cases
3. Add glossary of Ableton-specific terminology if needed

**For future use**:
- Re-scrape docs when Ableton releases updates
- Add community resources if official docs prove insufficient
- Document personal workflow discoveries not in official manual

## Deferred / Out of Scope

The following are intentionally NOT included (minimalist approach):
- Complex folder hierarchies beyond current structure
- Metadata/tagging systems
- Troubleshooting database
- Community resources (unless official docs prove insufficient)

**Philosophy**: Keep it simple - official docs + verified personal workflows only.
