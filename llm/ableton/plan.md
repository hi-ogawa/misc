# Ableton Live Knowledge Base - Simplified Plan

## Context
- **Goal**: Learn Ableton Live Lite for bass cover content creation
- **Problem**: LLM hallucinations when asking Ableton questions
- **Solution**: Build ground truth knowledge base from official docs

## Test Approach

**Phase 1: Official Documentation Only**
1. Collect official Ableton documentation (manual, reference guides)
2. Extract/convert to searchable markdown format
3. Test LLM retrieval accuracy with real questions
4. Verify: Can LLM answer without hallucinating?

**Phase 2: Add Well-Known Resources** (if Phase 1 works)
- Established tutorial sites
- Community-vetted guides
- Popular YouTube transcripts (if helpful)

**Phase 3: Personal Notes** (much later)
- Only add after proving official docs work
- Keep minimal - just what's not in official sources

## Minimal Structure

```
/docs/official/
  - ableton-manual-*.md         # Official manual chapters
  - keyboard-shortcuts.md       # Exported from Ableton preferences
  - glossary.md                 # Official terminology

/docs/resources/               # Well-known community resources
  (add later if needed)

/chats/
  - *.txt                       # Archived conversations with LLM
```

## Immediate Next Steps

1. **Obtain Ableton documentation**:
   - Export keyboard shortcut map from Ableton (Preferences → Export)
   - Download/extract official manual (PDF → markdown)
   - Create simple glossary of terms

2. **Test with simple questions**:
   - "What's the shortcut for creating a locator?"
   - "How does MIDI fold work?"
   - "What are warp modes?"
   - Check if LLM gives accurate answers from docs

3. **Iterate based on results**:
   - If accurate: expand with more official content
   - If still hallucinating: improve doc format/structure
   - If working well: then consider adding personal workflows

## Success Criteria
- Ask 10 Ableton questions → get accurate answers without web search
- LLM cites specific docs instead of guessing
- No need to verify answers against external sources

## Deferred (Not Now)
- ❌ Complex folder hierarchies
- ❌ Metadata/tagging systems
- ❌ Personal workflow documentation
- ❌ Ardour comparisons
- ❌ Troubleshooting database
- All of these only if official docs test succeeds
