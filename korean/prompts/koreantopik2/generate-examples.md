Generate natural example sentences for Korean vocabulary entries (TOPIK 2).

## Requirements

**All generation requirements are in `prompts/requirements-example.md`**

Read and follow all requirements before generating examples.

## Input/Output Format

**Input**: Pre-split batch files in `input/` directory
- Source: `input/koreantopik2.tsv` (3873 entries total)
- Pre-split into: `input/koreantopik2-batch-1.tsv` to `input/koreantopik2-batch-39.tsv`
  - Batches 1-38: 100 entries each (+ header)
  - Batch 39: 73 entries (entries 3801-3873, + header)
- Columns: number, korean, english

**Output**: TSV files (tab-separated)
- Columns: number, korean, example_ko, example_en
- Output files:
  - `output/koreantopik2/examples-1.tsv` (entries 1-100)
  - `output/koreantopik2/examples-2.tsv` (entries 101-200)
  - ...
  - `output/koreantopik2/examples-39.tsv` (entries 3801-3873)

## Process

1. Read `prompts/requirements-example.md` for complete generation requirements
2. Process input file in batches of 100 entries
3. Generate examples following all requirements
4. Write output to corresponding batch file
5. Process directly using Korean language understanding (no script-based automation)

## Execution Strategy

**Use subagents for isolated context generation:**

See `prompts/subagent-management.md` for complete guidelines on:
- Why use subagents (fresh context, parallel execution, isolation)
- Context contamination prevention (DO NOT read output files)
- What to read (requirements + assigned batch only)
- Independence and quality assurance

**Per-batch agent task:**
1. Read `prompts/requirements-example.md` (quality requirements)
2. Read `input/koreantopik2-batch-N.tsv` (assigned batch file)
3. Generate example sentences following all requirements
4. Write `output/koreantopik2/examples-N.tsv`

**CRITICAL for subagents:**
- DO NOT read any existing output files
- Generate from scratch based ONLY on requirements

**Benefits of pre-split approach:**
- Each agent reads only ~100 entries instead of full 3873-entry file
- No extraction logic needed (cleaner, faster)
- Reduces token usage per agent
- No risk of extraction errors

**Launch agents:**
- Can run sequentially (1-39) or in parallel batches
- Each agent receives identical instructions but different batch files
- No shared state between agents
