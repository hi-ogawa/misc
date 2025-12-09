# Update Etymology: Add Inflection Patterns

Update existing cards to add missing inflectional derivation etymology (passive/causative/nominalization) per `prompts/requirements-etymology.md`.

## Target Patterns

Words that should have inflection etymology but may be missing:

| Type | Suffixes | Example |
|------|----------|---------|
| Passive | -이/-히/-리/-기 | 보이다 → "보다 + 이 (passive)" |
| Causative | -이/-히/-리/-기/-우/-추 | 먹이다 → "먹다 + 이 (causative)" |
| -되다 passive | -되다 | 완성되다 → "완성 + 되다 (passive)" |
| -시키다 causative | -시키다 | 공부시키다 → "공부 + 시키다 (causative)" |
| Nominalization | -음/-ㅁ, -이, -기 | 걸음 → "걷다 + 음 (nominalization)" |

## Workflow

### 1. Export current data

```bash
python scripts/anki-export.py \
  --query "deck:Korean::DECK_NAME" \
  --fields noteId,number,korean,english,etymology,notes \
  --output anki/output/etymology-audit.tsv
```

### 2. Identify cards needing updates (agent)

Review each card and identify words that:
- Are passive/causative/nominalized forms
- Have empty etymology OR etymology missing the inflection info

For each identified card, provide updated etymology:
- Keep existing etymology if valid (e.g., Hanja)
- Add inflection pattern if missing
- If word has BOTH Hanja origin AND inflection, prefer the more useful one (usually inflection for derived verbs)

**Also clean up notes field:**
- If base/derived verb is in notes and now covered by etymology, remove it from notes
- Keep other related words (synonyms, antonyms, etc.)
- See `prompts/requirements-notes.md` for what belongs in notes vs etymology

Output: `anki/output/etymology-update.tsv`
- Columns: `noteId`, `korean`, `etymology`, `notes` (only rows that need changes)

### 3. Review (human)

- Verify proposed etymology changes
- Check base form accuracy (e.g., 들리다 ← 듣다, not 들다)
- Remove false positives

### 4. Update Anki

```bash
# Dry-run first
python scripts/anki-update-notes.py \
  --input anki/output/etymology-update.tsv \
  --fields etymology,notes \
  --dry-run

# Then execute
python scripts/anki-update-notes.py \
  --input anki/output/etymology-update.tsv \
  --fields etymology,notes
```

## Files

- `anki/output/etymology-audit.tsv` - Exported cards for review
- `anki/output/etymology-update.tsv` - Cards with updated etymology

## Related

- `prompts/requirements-etymology.md` - Etymology standards (section 3: Inflectional Derivations)
