# Spontaneous Vocabulary Mining from Videos

Collect vocabulary from Korean video content (variety shows, vlogs, etc.) and add to Anki.

## Context

- Source: YouTube videos with Korean subtitles (auto or manual)
- Target: Words/phrases that seem useful but unfamiliar
- Deck: `Korean::Custom`
- Pace: ~3-10 words per 30-min video session

## Approach

**Tiering intuition** (not strict rules):
- Tier 1: Pause & lookup (blocks comprehension)
- Tier 2: Note for later (interesting but not blocking)
- Tier 3: Let go (trust re-encounter)

**Key insight**: If a word is important, Korean will show it again. Volume of exposure > precision of capture.

## Workflow (Draft)

1. **During video**: Collect words to `anki/output/video-mining.tsv`
   - Format: `korean\texample_ko` (tab-separated, minimal)
   - Example sentence = subtitle context where word appeared
   - Append as you go (no header, accumulates across sessions)

2. **Batch process** (when ready):
   - LLM generates `english` translations
   - Optionally: etymology, notes (probably skip for speed)
   - Output: `anki/output/video-mining-cards.tsv`

3. **Add to Anki**:
   - Script: `python scripts/anki-add-notes.py --input anki/output/video-mining-cards.tsv --deck "Korean::Custom"`
   - Clear `video-mining.tsv` after successful add

## Open Questions

- Screenshot workflow? (OCR extraction vs manual typing)
- Direct Anki GUI input vs file-based batch?
- How often to batch process? (daily, weekly, when file gets big?)
- Include video source/timestamp for context?

## Fields

Minimal for speed:
- `korean`: target word/phrase
- `english`: translation
- `example_ko`: subtitle context

Optional (add later if needed):
- `etymology`
- `notes`
- `example_en`

## Related

- `anki/prompts/extract-missing-vocab.md` - similar batch workflow for flagged cards
- `prompts/requirements-etymology.md`, `prompts/requirements-notes.md` - if adding those fields
