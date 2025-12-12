# Generate Examples (TOPIK 2)

Generate example sentences for TOPIK 2 vocabulary using subagents.

## Overview

- **Input**: `input/koreantopik2-batch-{1..39}.tsv` (pre-split, ~100 entries each)
- **Output**: `output/koreantopik2/examples-{1..39}.tsv`
- **Requirements**: `prompts/requirements-example.md`

## Subagent Prompt

Use this prompt template for each batch. Replace `N` with batch number (1-39).

````
Generate example sentences for Korean vocabulary batch N.

## Task

Read `input/koreantopik2-batch-N.tsv` and generate `output/koreantopik2/examples-N.tsv`.

## CRITICAL: File Access Rules

**ONLY read these files:**
- `prompts/requirements-example.md` (quality requirements)
- `input/koreantopik2-batch-N.tsv` (your assigned batch)

**DO NOT read any other files**, especially:
- Any files in `output/` directory
- Other batch files
- Any existing examples files

Generate from scratch based only on the input batch and requirements.

## Input Format

TSV with columns: number, korean, english

## Output Format

TSV with columns: number, korean, example_ko, example_en

Write header row first, then one row per vocabulary entry.

Example output:
```
number	korean	example_ko	example_en
1	-가	그는 유명한 사진가로 활동하면서 전시회도 열어요.	He works as a famous photographer while also holding exhibitions.
2	가까이	집이 학교에서 가까우니까 걸어 다녀요.	Since my house is close to school, I walk there.
```

## Process

1. Read `prompts/requirements-example.md` first - follow ALL requirements strictly
2. Read `input/koreantopik2-batch-N.tsv`
3. For each entry, generate one example sentence pair (Korean + English)
4. Write all entries to `output/koreantopik2/examples-N.tsv`

## Key Requirements Summary

From `requirements-example.md`:
- Example MUST contain the vocabulary word (conjugated forms OK for verbs/adjectives)
- STRONGLY PREFER multi-clause sentences with connectives (-서, -(으)니까, -지만, etc.)
- Include concrete context (who, what, where, when)
- NEVER drop subjects - always explicit
- Use specific nouns, not pronouns/demonstratives
- Force evaluation: sentence should require understanding THIS specific word
````

## Execution

### Cleanup (before starting)

```bash
rm -f output/koreantopik2/examples-{1..39}.tsv output/koreantopik2/examples-all.tsv
```

### Launch subagents

Launch 39 subagents (sequentially or in parallel batches):

```
Batch 1:  input/koreantopik2-batch-1.tsv  → output/koreantopik2/examples-1.tsv
Batch 2:  input/koreantopik2-batch-2.tsv  → output/koreantopik2/examples-2.tsv
...
Batch 39: input/koreantopik2-batch-39.tsv → output/koreantopik2/examples-39.tsv
```

## Consolidation

After all batches complete:

```bash
python scripts/jq-tsv.py '.' output/koreantopik2/examples-{1..39}.tsv > output/koreantopik2/examples-all.tsv

# Verify count
wc -l output/koreantopik2/examples-all.tsv  # Should be 3874 (3873 + header)
```
