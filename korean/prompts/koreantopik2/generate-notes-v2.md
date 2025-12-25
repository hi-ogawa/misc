# Generate Notes v2 (TOPIK 2)

Generate related vocabulary notes for the notes field in Anki.

## Overview

- **Input**: Export from Anki → split into batches
- **Output**: `output/koreantopik2/notes-v2-{1..N}.tsv`
- **Requirements**: `prompts/requirements-notes.md`

## Pipeline

```
[Step 1: Export from Anki]
    python scripts/anki-export.py → topik2-export.tsv
        │
        ▼
[Step 2: Split into batches]
    python scripts/split-batches.py → notes-v2-batch-{1..N}.tsv
        │
        ▼
[Step 3: Subagent processing]
    → output/koreantopik2/notes-v2-{1..N}.tsv
        │
        ▼
[Step 4: Consolidate + Update Anki]
    → notes-v2-all.tsv → anki-update-notes.py
```

---

## Step 1: Export from Anki

```bash
python scripts/anki-export.py \
  --query "deck:Korean number:koreantopik2_*" \
  --fields noteId,korean,english,notes > output/tmp/topik2-export.tsv

wc -l output/tmp/topik2-export.tsv
# Expected: ~3900 (3899 + header)
```

---

## Step 2: Split into batches

```bash
python scripts/split-batches.py \
  --input output/tmp/topik2-export.tsv \
  --output-dir output/tmp \
  --prefix notes-v2-batch- \
  --batch-size 100
```

---

## Step 3: Subagent Processing

### Cleanup (before starting to avoid subagent output confusion)

```bash
rm -f output/koreantopik2/notes-v2-{1..99}.tsv output/koreantopik2/notes-v2-all.tsv
```

### Subagent Prompt

Use this prompt template for each batch. Replace `N` with batch number.
Avoid processing fully parallel. Use at most 5 subagents at one time.

````
Generate related vocabulary notes for batch N.

Read `prompts/requirements-notes.md` for relationship types and format.
Read `output/tmp/notes-v2-batch-N.tsv` for input data.
Write `output/koreantopik2/notes-v2-N.tsv`.

## CRITICAL RULES

- DO NOT write scripts or run verification commands
- DO NOT read other files besides requirements and your batch file
- Use your Korean language knowledge directly

## Input Format

TSV with columns: noteId, korean, english, notes

## Output Format

TSV with columns: noteId, korean, notes

Annotations describe the RELATED WORD, not the entry:
- `만 (.syn:casual)` = 만 is the casual synonym
- `신뢰 (.syn:formal)` = 신뢰 is the formal synonym

Example:
```
noteId	korean	notes
1234567890	높다	낮다 (.ant)
1234567891	오직	단지 (.syn), 만 (.syn:casual)
1234567892	즉시	바로 (.syn:casual), 곧 (.syn:native)
1234567893	믿음	신뢰 (.syn:formal)
1234567894	외로움	고독 (.syn:formal)
1234567895	먹다	드시다 (.hon), 잡수시다 (.hon)
```

Leave notes blank if no meaningful relationships exist.
````

### Launch subagents

```
Batch 1:  output/tmp/notes-v2-batch-1.tsv  → output/koreantopik2/notes-v2-1.tsv
Batch 2:  output/tmp/notes-v2-batch-2.tsv  → output/koreantopik2/notes-v2-2.tsv
...
Batch 39: output/tmp/notes-v2-batch-39.tsv → output/koreantopik2/notes-v2-39.tsv
```

---

## Step 4: Consolidate + Update Anki

### Consolidate

```bash
python scripts/jq-tsv.py '.' output/koreantopik2/notes-v2-{1..39}.tsv > output/koreantopik2/notes-v2-all.tsv

wc -l output/koreantopik2/notes-v2-all.tsv
# Expected: ~3900 (all cards, some with blank notes)
```

### Eyeball review

Check a few entries manually before updating.

### Generate update file

```bash
# Filter to only rows with non-empty notes
python3 -c "
import csv
import sys

with open('output/koreantopik2/notes-v2-all.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    rows = [row for row in reader if row['notes'].strip()]

writer = csv.DictWriter(sys.stdout, fieldnames=['noteId', 'notes'], delimiter='\t')
writer.writeheader()
for row in rows:
    writer.writerow({'noteId': row['noteId'], 'notes': row['notes']})
" > output/koreantopik2/notes-v2-update.tsv

wc -l output/koreantopik2/notes-v2-update.tsv
```

## Step 5: Update Anki

CRITICAL: Agent shouldn't run. Delegate to users for Anki update.

### Apply update

```bash
python scripts/anki-update-notes.py \
  --input output/koreantopik2/notes-v2-update.tsv \
  --fields notes --dry-run
```

---

## File Summary

| File | Description |
|------|-------------|
| `output/tmp/topik2-export.tsv` | Anki export with noteId |
| `output/tmp/notes-v2-batch-N.tsv` | Split batches for subagent |
| `output/koreantopik2/notes-v2-N.tsv` | Subagent output per batch |
| `output/koreantopik2/notes-v2-all.tsv` | Consolidated notes |
| `output/koreantopik2/notes-v2-update.tsv` | Non-empty notes for Anki update |
