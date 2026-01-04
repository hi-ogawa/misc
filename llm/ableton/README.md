# Ableton Live Lite Knowledge Base

Personal knowledge base for learning Ableton Live Lite, focused on bass cover production and MIDI transcription workflows.

## Purpose

**Problem**: LLM hallucinations when asking Ableton-specific questions lead to incorrect shortcuts, non-existent features, and wasted troubleshooting time.

**Solution**: Build a ground-truth knowledge base from official documentation and verified personal workflows, enabling accurate LLM-assisted lookup without external verification.

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
├── plan.md             # Detailed implementation plan
├── workflow.md         # Personal workflow notes (⚠️ partially unverified)
│                       # Mix of: Ableton-specific + general audio + personal setup
├── docs/               # (Future) Official documentation
│   └── official/       # Ableton manual, shortcuts, glossary
└── data/               # Untracked: raw chats, experiments
```

**Note**: While the primary focus is Ableton-specific documentation, `workflow.md` also contains general audio production knowledge (compression/EQ concepts) and personal workflow preferences that may be useful beyond Ableton.

## Current Status

- ✅ Initial plan created
- ✅ Personal workflow documented (mixing verified, transcription unverified)
- ⏳ Need to obtain and convert official Ableton documentation
- ⏳ Need to test LLM retrieval accuracy

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

## Next Steps

See [plan.md](plan.md) for detailed roadmap.

**Immediate:**
1. Export keyboard shortcuts from Ableton (Preferences → Export)
2. Obtain official Ableton manual
3. Convert to markdown format
4. Test with simple questions

## Note on Verification

Files marked with ⚠️ contain unverified content from LLM conversations and may include hallucinations. Only use after cross-referencing with official documentation.
