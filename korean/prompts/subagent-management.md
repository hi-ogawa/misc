# Subagent Management Guidelines

This document defines best practices for using subagents in batch processing workflows.

## Why Use Subagents

**Key benefits:**
1. **Fresh context per batch**: Each agent starts with clean context, ensuring consistent quality across all batches
2. **Parallel execution**: Multiple batches can run simultaneously for faster processing
3. **Isolation**: No cross-contamination between batches or enhancement types
4. **Scalability**: Easy to regenerate individual batches without affecting others

## Critical: Context Contamination Prevention

**DO NOT read existing output files**

Subagents must NEVER read files in output directories

**Why this is critical:**
- Output directories may contain **garbage data from past trial-and-error experiments**
- Reading contaminated files will **corrupt generation with bad examples and incorrect patterns**
- Subagents might inadvertently learn from low-quality or incorrect outputs
- This defeats the purpose of having standardized requirements

**What happens if you read contaminated files:**
- Inconsistent quality across batches (some follow good examples, others follow bad ones)
- Propagation of errors and anti-patterns
- Difficult to trace where quality degradation originated
- May require regenerating all batches

## What Subagents Should Read

**ONLY read these files:**

1. **Requirements file** (always required):
   - `prompts/requirements-etymology.md` for etymology generation
   - `prompts/requirements-example.md` for example generation
   - `prompts/requirements-notes.md` for notes generation
   - These define WHAT makes good content

2. **Assigned batch file** (always required):
   - Your specific batch file as indicated in the generation prompt
   - Contains ~100 entries to process
   - Provides explicit list of entries for this agent

**Exception for notes generation:**
- Notes agents also read the vocabulary reference file (all vocabulary for cross-referencing)
- This enables finding related words, antonyms, honorific pairs across the full dataset
- Etymology and examples agents do NOT need this

## Subagent Task Template

Each subagent should follow this structure:

1. **Read requirements**: Load quality standards for this enhancement type
2. **Read assigned batch**: Load the specific entries to process
3. **Generate from scratch**: Create content based ONLY on requirements, not existing outputs
4. **Write output**: Save to designated batch file

**Notes generation adds one step:**
- After step 1, also read the vocabulary reference file for cross-referencing

## Independence and Fresh Context

**Each agent must:**
- Work independently with no shared state
- Generate from scratch based purely on requirements
- Have no dependency on quality of previous outputs
- Not look at other batches for inspiration or reference

**Benefits:**
- Consistent quality across all batches
- Deterministic regeneration (same inputs → same outputs)
- Easy debugging (isolate issues to specific batches)
- No cascading failures

## Parallel Execution

Subagents can run:
- **Sequentially**: Process batches one at a time
- **In parallel batches**: Process multiple batches simultaneously
- **Mixed approach**: Pilot run (small subset), then parallel for remainder

**No coordination required:**
- Each agent receives identical instructions
- Different batch numbers are the only variable
- Outputs go to separate files (no conflicts)

## File Naming Convention

File naming follows a consistent pattern across datasets:

**Input batches:**
- `input/{dataset}-batch-N.tsv` (where N is the batch number)

**Output files:**
- Etymology: `output/{dataset}/etymology-N.tsv`
- Examples: `output/{dataset}/examples-N.tsv`
- Notes: `output/{dataset}/notes-N.tsv`

## Quality Assurance

After batch completion:
- Verify file count matches expected batch count
- Check TSV formatting (proper tabs, no CSV issues)
- Spot-check content quality against requirements
- Regenerate individual batches if issues found

**Regeneration is safe:**
- Delete contaminated batch output
- Re-run subagent for that batch only
- No impact on other batches
