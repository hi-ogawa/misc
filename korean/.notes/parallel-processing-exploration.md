# Exploring Claude Code Subagent Parallel Processing for TOPIK 2

*Discussion Date: 2025-11-09*

## Context

Processing TOPIK 2 vocabulary (3900 words) requires:
- 39 batches of 100 words each
- 3 enhancement types: etymology, examples, notes
- 117 total processing tasks (39 × 3)

**Goal**: Explore parallel processing with Claude Code subagents for better context management and efficiency.

## Current Sequential Approach (TOPIK 1)

What we did for TOPIK 1:
- Single conversation context
- Process all batches sequentially
- Context grows with each batch
- One failure could disrupt flow

## Parallel Processing Benefits

1. **True parallelism**: Process multiple batches simultaneously
2. **Context isolation**: Each agent only loads its batch context
3. **Failure resilience**: One batch failure doesn't affect others
4. **Progress monitoring**: Track completion independently
5. **Resume capability**: Restart only failed batches

## Proposed Architectures

### Option A: Batch-Level Parallelism (Recommended)
Launch agents per batch, each handling all enhancements for that batch:
- Agent 1: Batch 1 (words 1-100) → etymology + examples + notes
- Agent 2: Batch 2 (words 101-200) → etymology + examples + notes
- ...
- Agent 39: Batch 39 (words 3801-3900) → etymology + examples + notes

**Pros**:
- Simpler coordination
- All data for a batch stays together
- Natural unit of work

**Cons**:
- Each agent does more work
- Less granular parallelism

### Option B: Enhancement-Type Parallelism
Launch 39 agents per enhancement type:
- 39 etymology agents (one per batch)
- 39 example agents (one per batch)
- 39 notes agents (one per batch)

**Pros**:
- Maximum parallelism (theoretically 117 agents)
- Specialized per enhancement type

**Cons**:
- More complex coordination
- Need to manage 117 agents

### Option C: Chunked Parallelism (Balanced)
Launch 10 agents at a time, each handling 4 batches:
- Round 1: Agents 1-10 process batches 1-10 (etymology)
- Round 2: Agents 1-10 process batches 11-20 (etymology)
- Repeat for examples and notes

**Pros**:
- Controlled parallelism
- Manageable agent count

**Cons**:
- Still has sequential rounds
- Less efficient than full parallelism

## Agent Task Structure

Each agent would receive a prompt like:

```markdown
Task: Process TOPIK 2 Batch N for [enhancement-type]

Input: input/korean_english_2.tsv
Range: Words [start]-[end] (e.g., 101-200)
Output: output/topik2-[type]-N.tsv

[Include relevant rules from prompts/generate-[type].md]

Steps:
1. Read input TSV
2. Extract lines for this batch
3. Process each word according to rules
4. Write output TSV with proper escaping
5. Report completion status
```

## Questions to Explore

1. **Practical limits**: How many agents can Claude Code launch in parallel?
2. **Batching strategy**: Should we launch all at once or in groups?
3. **Starting point**: Which enhancement type to test first? (etymology seems simplest)
4. **Progress tracking**: How to monitor 39 concurrent agents?
5. **Error handling**: What happens if some agents fail?
6. **Output validation**: How to verify all outputs are correct?

## Proposed Test Phases

### Phase 0: Small Test (3-5 agents)
- Test with batches 1-5 for etymology only
- Learn the mechanics of launching/monitoring agents
- Validate output quality

### Phase 1: Medium Test (10 agents)
- Process batches 1-10 for etymology
- Assess practical limits and performance
- Refine coordination approach

### Phase 2: Full Etymology (39 agents)
- Launch all 39 etymology agents
- Monitor completion and handle failures
- Create consolidated etymology-all.tsv

### Phase 3: Examples and Notes
- Repeat for examples (39 agents)
- Repeat for notes (39 agents)
- Create consolidated files

### Phase 4: Audio Generation
- Possibly parallel audio generation
- Or traditional sequential approach (already fast)

## Open Questions

- Should each agent create its own output file, or coordinate through main?
- How to handle consolidation into `-all.tsv` files?
- Should we create a master tracking file/dashboard?
- What's the optimal agent model? (haiku for speed vs sonnet for quality)

## Next Steps

**Decision needed**: Which test approach to start with?
- A) Small test (3-5 agents, batches 1-5, etymology only)
- B) Medium test (10 agents, batches 1-10, etymology only)
- C) Full parallel (all 39 agents, etymology only)

**Preference**: Start small, learn, scale up

---

## Final Decision

**Date**: 2025-11-09

### Key Insight
The real value is **context isolation**, not speed from parallelism. Each batch (100 words) is a "natural unit of work" that should be processed independently to:
- Keep context small and focused
- Allow independent progress tracking
- Enable easy resume of failed batches

### Chosen Approach: Manual Multi-Terminal Processing

**Implementation**: `prompts/generate-combined.md`

Instead of automated subagent orchestration, use manual control:
1. Create a combined prompt that processes all 3 enhancements for one batch
2. Open multiple Claude Code terminals manually
3. Edit the prompt in each terminal to specify batch range
4. Run independently in parallel (user controls how many)

**Example workflow:**
- Terminal 1: Process batch 1 (words 1-100)
- Terminal 2: Process batch 2 (words 101-200)
- Terminal 3: Process batch 3 (words 201-300)
- etc.

Each terminal produces 1 combined file:
- `output/topik2-combined-N.tsv`

**Format**: `number, korean, english, etymology, example_ko, example_en, notes` (7 columns)

All enhancements for each word stay together in one row, maintaining semantic connection.

### Why This Approach?

**Advantages:**
1. **Simple**: No complex subagent orchestration needed
2. **Flexible**: User controls parallelism (run 1, 5, or 39 terminals)
3. **Transparent**: Easy to see what's running and what's done
4. **Recoverable**: Just re-run specific batches if needed
5. **Context-efficient**: Each session only loads 100 words + prompt

**Trade-offs:**
- More manual setup (copy/paste and edit batch number)
- No automated progress tracking (but easy to check output/ directory)

### Implementation Complete

Created `prompts/generate-combined.md` with:
- Combined etymology + examples + notes processing
- Template placeholders for batch range (`__BATCH__`, `__START__`, `__END__`)
- All rules from individual prompts consolidated
- Clear execution instructions

**Next step**: Test with batch 1, then scale to multiple terminals.

---
*Status: Decision made, prompt created, ready to test*
