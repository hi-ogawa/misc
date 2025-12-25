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

## Subagent Response Format

**Subagents must return ONLY status information, not generated content.**

When a subagent completes its task, its response flows back to the orchestrator's context. If subagents include full generated content in their responses, this:
- Bloats orchestrator context unnecessarily
- Could inadvertently influence instructions for subsequent batches
- Defeats the purpose of isolated generation

**Correct response format:**
```
✅ Wrote 100 entries to output/koreantopik2/etymology-3.tsv
   - Batch: 3
   - Entries processed: 100
   - Status: Complete
```

**Incorrect response format:**
```
❌ Here are the 100 etymology entries I generated:
   1. 가격 (價格): Sino-Korean from 價 "price" + 格 "standard"...
   2. 가능 (可能): Sino-Korean from 可 "can" + 能 "ability"...
   [... 98 more entries ...]
```

**Add to subagent prompts:**
> After writing the output file, respond ONLY with batch number, entries processed count, and file path. Do NOT include generated content in your response.

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

## Model Selection

**IMPORTANT: Manager must confirm model choice with user before launching subagents**

**Model selection considerations:**

| Task Type | Recommended Model | Reasoning |
|-----------|------------------|-----------|
| **Etymology** | Haiku (confirm first) | Mechanical/factual lookup task, clear right/wrong answers |
| **Examples** | Sonnet (confirm first) | Creative generation requiring language nuance and quality |
| **Notes** | Sonnet (confirm first) | Semantic analysis across 5,720 words, subjective relationships |

**Before launching subagents:**
1. ✅ Review the generation task requirements
2. ✅ Propose a model choice with reasoning
3. ✅ **Ask user to confirm** before proceeding
4. ✅ Show user the exact subagent prompt that will be used
5. ✅ Launch subagents only after user approval

**Factors to consider:**
- **Task complexity**: Mechanical vs creative/semantic
- **Quality requirements**: Formulaic vs nuanced
- **Cost vs quality tradeoff**: Total entries × model cost
- **Error tolerance**: Easy to verify vs subjective quality

**Pilot run recommendation:**
- Process 1-2 batches with proposed model
- User reviews quality
- Adjust model choice if needed before full run

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

## Manager Verification (Orchestration Level)

**What the orchestrating agent SHOULD verify:**
- ✅ File creation: Does the output file exist?
- ✅ Basic structure: Correct line count (~100-101 entries including header)?
- ✅ Format check: Valid TSV with proper tabs and expected columns?

**What the orchestrating agent should NOT do:**
- ❌ Read and verify content quality of all entries
- ❌ Judge whether generated content meets quality standards
- ❌ Compare outputs against requirements in detail

**Rationale:**
- Reading all outputs defeats the purpose of isolated generation (token overhead, context contamination risk)
- If requirements are good and subagents follow them, outputs should be good
- Trust subagents to execute their task based on requirements
- Detailed quality review happens later in the workflow (manual review phase)
- Easy to regenerate individual batches if issues are found later

**Regeneration is safe:**
- Delete problematic batch output
- Re-run subagent for that batch only
- No impact on other batches

**Quality contract:**
The requirements files are the quality contract. Manager oversees process execution, not content quality.
