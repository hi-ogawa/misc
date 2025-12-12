# Generate Notes (TOPIK 2)

Generate related vocabulary words for the "notes" field using subagents.

## Overview

- **Input**: `input/koreantopik2-batch-{1..39}.tsv` (pre-split, ~100 entries each)
- **Output**: `output/koreantopik2/notes-{1..39}.tsv`
- **Requirements**: `prompts/requirements-notes.md`

## Subagent Prompt

Use this prompt template for each batch. Replace `N` with batch number (1-39).

````
Generate related vocabulary notes for batch N.

Read `input/koreantopik2-batch-N.tsv` and write `output/koreantopik2/notes-N.tsv`.

## CRITICAL RULES

- DO NOT write scripts or run verification commands
- DO NOT read other files besides your batch file
- Use your Korean language knowledge directly

## Output Format

TSV with columns: number, korean, notes

Example:
```
number	korean	notes
1	-가	-사, -자, -인
2	가까이	멀리
3	가꾸다	기르다
4	가난	부자, 가난하다
5	가능	불가능
```

## What to Include

For each word, add related vocabulary:
- Synonyms: 흰색 → 하얀색
- Antonyms: 높다 → 낮다
- Honorific pairs: 먹다 → 드시다
- Hanja-순우리말: 가격 → 값
- Confusables: 넣다 → 놓다

Leave blank if no meaningful relationships.

## What NOT to Include

- Morphological pairs: ❌ 닫히다 → 닫다
- Contractions: ❌ 게 → 것이

## Format

- Comma-separated: 높다, 낮다
- Parentheses for clarification: 간 (salty), 간격
````

## Execution

### Cleanup (before starting)

```bash
rm -f output/koreantopik2/notes-{1..39}.tsv output/koreantopik2/notes-all.tsv
```

### Launch subagents

Launch 39 subagents (sequentially or in parallel batches):

```
Batch 1:  input/koreantopik2-batch-1.tsv  → output/koreantopik2/notes-1.tsv
Batch 2:  input/koreantopik2-batch-2.tsv  → output/koreantopik2/notes-2.tsv
...
Batch 39: input/koreantopik2-batch-39.tsv → output/koreantopik2/notes-39.tsv
```

## Consolidation

After all batches complete:

```bash
python scripts/jq-tsv.py '.' output/koreantopik2/notes-{1..39}.tsv > output/koreantopik2/notes-all.tsv

# Verify count
wc -l output/koreantopik2/notes-all.tsv  # Should be 3874 (3873 + header)
```
