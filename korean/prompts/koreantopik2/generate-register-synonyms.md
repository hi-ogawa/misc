# Generate Register Synonym Notes (TOPIK 2)

Batch process to identify register-level synonyms and update the notes field.

**Requirements**: See `prompts/requirements-notes.md` section 6 (REGISTER VARIANTS)

## Overview

TOPIK2 contains formal/written variants of simpler TOPIK1 words. These cause higher lapse rates because learners try to memorize them as new patterns instead of linking to existing knowledge.

**Goal**: Add `[casual equivalent] (register)` to the notes field.

## Pipeline

```
[Phase 1: Identification]
    LLM analysis → candidates.tsv

[Phase 2: Anki Update]
    Export notes → merge → update via AnkiConnect
```

## Phase 1: Identification

### Input
- `output/koreantopik2/filtered-sorted.tsv` (3,179 words)

### Subagent Prompt

```
Identify register-level synonyms in this TOPIK2 vocabulary batch.

Read `prompts/requirements-notes.md` section 6 (REGISTER VARIANTS) for criteria.

For each word, determine if it has a simpler/casual equivalent:
- YES: Output the mapping
- NO: Skip (don't output)

## Output Format (TSV)

number	korean	notes_register
koreantopik2_085_0014	얼른	빨리 (formal)
koreantopik2_082_0033	즉	그러니까 (written)

Only output words that ARE register variants. Skip words that aren't.

## Vocabulary to Analyze

[BATCH_DATA]
```

### Consolidate

```bash
python scripts/jq-tsv.py '.' output/koreantopik2/register-{1..N}.tsv > output/koreantopik2/register-all.tsv
```

## Phase 2: Anki Update

### Export current notes

```bash
python scripts/anki-export.py \
  --query "deck:Korean::TOPIK\ 2" \
  --fields noteId,number,notes > output/tmp/topik2-notes.tsv
```

### Merge and generate update file

```bash
python3 -c "
import csv
import sys

# Read register synonyms
register = {}
with open('output/koreantopik2/register-all.tsv') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        register[row['number']] = row['notes_register']

# Read current notes
with open('output/tmp/topik2-notes.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    rows = list(reader)

# Merge
output = []
for row in rows:
    if row['number'] in register:
        addition = register[row['number']]
        if row['notes']:
            row['notes'] = f\"{row['notes']}; {addition}\"
        else:
            row['notes'] = addition
        output.append({'noteId': row['noteId'], 'notes': row['notes']})

writer = csv.DictWriter(sys.stdout, fieldnames=['noteId', 'notes'], delimiter='\t')
writer.writeheader()
writer.writerows(output)
" > output/koreantopik2/register-update.tsv
```

### Apply update

```bash
python scripts/anki-update-notes.py \
  --input output/koreantopik2/register-update.tsv \
  --fields notes
```

## Expected Results

Based on lapsed card analysis (62 lapsed from 420 reviewed):
- ~71% of lapses were 순우리말
- Many were register variants of TOPIK1 words

Estimate: 15-20% of TOPIK2 vocabulary may have register variant mappings.

## File Summary

| File | Description |
|------|-------------|
| `register-{N}.tsv` | Per-batch identification output |
| `register-all.tsv` | Consolidated candidates |
| `register-update.tsv` | Ready for Anki update (noteId + notes) |
