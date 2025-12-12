# Update Etymology: Full Regeneration

Regenerate all etymology for a deck using updated `prompts/requirements-etymology.md`.

## When to Use

- Requirements have been significantly updated
- Existing etymology is inconsistent or incomplete
- Easier than identifying individual cards to fix

## Workflow

### 1. Export current data

```bash
python scripts/anki-export.py \
  --query "deck:Korean::DECK_NAME" \
  --fields noteId,number,korean,english \
  --output anki/output/DECK-etymology-audit.tsv
```

### 2. Split into batches

```bash
python scripts/split-batches.py \
  --input anki/output/DECK-etymology-audit.tsv \
  --output-dir anki/output/DECK-etymology-batches \
  --prefix batch- \
  --batch-size 100
```

### 3. Generate etymology (agent per batch)

See `prompts/subagent-management.md` for complete guidelines on subagent execution.

**Subagent prompt:**

```
Generate etymology for Korean vocabulary batch N.

Steps:
1. Read `prompts/requirements-etymology.md` for etymology standards
2. Read `anki/output/DECK-etymology-batches/batch-N.tsv` (your assigned batch)
3. For each entry, generate etymology following the requirements
4. Write output to `anki/output/DECK-etymology-batches/etymology-N.tsv`

Output format:
- TSV with columns: noteId, korean, etymology
- Include ALL rows from input (leave etymology blank if no etymology applies)
- Do NOT add explanations or labels - just the etymology value

CRITICAL:
- DO NOT read other batch files or output files
- Generate based ONLY on requirements + your assigned batch
```

**CRITICAL for agents:**
- DO NOT read other batch files or output files
- Generate based ONLY on requirements + assigned batch

### 4. Combine batches

```bash
python scripts/jq-tsv.py '.' anki/output/DECK-etymology-batches/etymology-*.tsv > anki/output/DECK-etymology-all.tsv
```

### 5. Review (human)

Compare new etymology against current:

```bash
# Join current and new etymology by noteId
python scripts/jq-tsv.py '{noteId, korean, old: .etymology}' anki/output/DECK-etymology-audit.tsv > output/tmp/old.tsv
python scripts/jq-tsv.py '{noteId, korean, new: .etymology}' anki/output/DECK-etymology-all.tsv > output/tmp/new.tsv

# Show differences (where old != new)
# TODO: join script or manual review
```

Review focus:
- Entries where etymology changed significantly
- Entries where etymology was added (old empty, new has value)
- Entries where etymology was removed (old has value, new empty) - potential regression

### 6. Update Anki

```bash
# Dry-run first
python scripts/anki-update-notes.py \
  --input anki/output/DECK-etymology-all.tsv \
  --fields etymology \
  --dry-run

# Then execute
python scripts/anki-update-notes.py \
  --input anki/output/DECK-etymology-all.tsv \
  --fields etymology
```

## Files

- `anki/output/DECK-etymology-audit.tsv` - Exported cards
- `anki/output/DECK-etymology-batches/` - Split batches and generated etymology
- `anki/output/DECK-etymology-all.tsv` - Combined etymology for import

## TOPIK1 Specifics

- 1,847 cards → 19 batches (18 × 100 + 1 × 47)
- Current state: 1,049 with etymology, 800 empty

## Related

- `prompts/requirements-etymology.md` - Etymology standards
- `prompts/subagent-management.md` - Subagent execution guidelines
- `anki/prompts/update-etymology.md` - Incremental update workflow
