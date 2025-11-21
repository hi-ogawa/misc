# Research: Example Sentence Complexity and Learning Progression

**Created**: 2025-11-21
**Status**: Research complete, pending decision on implementation
**Related**: `requirements-example.md`, `research-example-sentences.md`, `analysis-example.md`

---

## Goal

Establish a principled basis for example sentence complexity that accounts for learner progression.

**Practical outcomes**:
1. Decide if current `requirements-example.md` (v2 style, ~5.7 words) is appropriate for all levels
2. Determine if TOPIK 2 dataset should use a different strategy than TOPIK 1
3. Inform future iterations of example generation requirements

---

## Research Question

> **How should example sentence complexity relate to learner proficiency, and how should it evolve as learners progress?**

This is not about finding a single "optimal" complexity, but understanding the relationship between learner stage and appropriate example complexity.

---

## Context

### The Development Journey

Example sentence requirements have evolved through empirical iteration:

| Generation | Words | Chars | Style | Learning Stage |
|------------|-------|-------|-------|----------------|
| Original dataset | ~2 | - | Word pairs, not sentences | Pre-study reference |
| Gen 1 | ~3 | - | Full sentences, no quality criteria | First ~100 vocab |
| Gen 2 | ~3.5 | - | Avoiding generic terms, pronouns | Next ~500 vocab |
| Gen 3 (v1) | 3.81 | 11.98 | Systematic requirements | Full dataset |
| **Gen 4 (v2)** | **5.71** | **17.02** | Rich multi-clause | Current |

### Requirements Evolution (3 major versions)

Archived versions for reference:
- `requirements-example-v1.md` - Original
- `requirements-example-v2.md` - "SIMPLE and MINIMAL"
- `requirements-example.md` - Current

**Version 1 (Original)**:
- "Keep sentences minimal: 3-4 words is ideal"
- Focus on natural, common usage
- Examples: "학교에 먼저 가요", "가벼운 가방을 샀어요"
- No explicit guidance on connectives or multi-clause

**Version 2 (1b8d66a - "improve vocabulary prompts")**:
- "Keep sentences SIMPLE and MINIMAL - one main idea only"
- ❌ Explicitly avoided compound sentences and clauses
- ❌ "Avoid clauses: 소풍 갈 때 엄마가 김밥을 싸 주셨어요"
- Added quality checklist, concrete context requirements
- Batch 7 (3.04 words) was generated under this guidance

**Version 3 (Current - multiple iterations)**:
- "STRONGLY PREFER multi-clause sentences (2+ clauses)"
- Connectives ENCOURAGED: -서, -(으)니까, -고, -지만, -을 때
- "Force evaluation through distinctive context" as core principle
- v2 examples: 5.71 words average

**Key insight**: The requirements shifted 180° from "3-4 words ideal" → "strongly prefer multi-clause". This was driven by empirical observation that richer context aids vocabulary retention—but raises the question of whether the original simpler approach was actually appropriate for earlier learning stages.

**Historical note**: The shift was not planned. Originally, minimal sentences were believed to be more effective. When LLM agents generated longer multi-clause sentences, they were initially considered "anomalies" or errors. However, upon review, these "anomalies" turned out to be more helpful at the current learning stage—leading to the requirements update.

This suggests: what's "correct" depends on where the learner is. The original minimal approach may have been right for earlier stages; the multi-clause approach became better as proficiency grew.

**Methodological note**:
- First generation processed all entries without subagent batching—quality may have degraded due to context window limitations
- Later generations introduced subagent batching (100 entries per batch, parallel processing)
- Inter-subagent variation in prompt interpretation led to different batch styles (e.g., Batch 7 minimal vs. Batch 3/6 richer)
- This variation, initially seen as inconsistency, actually enabled discovery: comparing batch styles revealed which approach worked better at current learning stage

### Key Observation

**The appropriate complexity depends on where the learner is:**

- Gen 4 examples (5.71 words) might have been **too difficult** at the start of learning
- Gen 4 examples might become **too easy** as proficiency advances
- What's "optimal" is not static—it's relative to learner stage

### Concrete Example: Connectives

Current v2 examples heavily use multi-clause sentences with connectives:
- -서 (cause/reason)
- -(으)니까 (cause/reason)
- -고 (sequential)
- -지만 (contrast)
- -을 때 (temporal)

**Problem**: A true beginner may not have learned these grammar patterns yet.

If learner doesn't know -서, then:
- ❌ "목이 마르**서** 물을 마셨어요" → incomprehensible structure
- The example fails as vocabulary learning aid—it becomes a grammar puzzle

**Implication**: Example sentence complexity has dependencies on grammar knowledge, not just vocabulary size. Multi-clause examples assume grammatical readiness.

### Hypothesis: Natural Frequency-Complexity Alignment

There may be a natural alignment between vocabulary frequency and appropriate sentence complexity:

| Vocabulary Type | Frequency | Learner Stage | Grammar Knowledge | Appropriate Structure |
|-----------------|-----------|---------------|-------------------|----------------------|
| Simple/common | High | Early | Basic (subject + verb + -요) | Simple single-clause |
| Intermediate | Medium | Mid | Connectives emerging | Single or simple multi-clause |
| Rare/specialized | Low | Later | Connectives fluent | Rich multi-clause |

**Key insight**: Multi-clause examples for rare vocabulary serve dual purpose:
1. **Richer context** needed because rare words are harder to remember
2. **Scaffolding**: One clause uses already-learned simple vocabulary, helping decode the new word

**Example**:
- Learning 시달리다 (to suffer from, be tormented by):
- "요즘 일이 많아서 스트레스에 **시달려요**"
- Clause 1: uses 요즘, 일, 많다 (common, already learned)
- Clause 2: introduces 시달리다 (less frequent, nuanced)
- The familiar context (lots of work + stress) scaffolds understanding of the new verb

**If true**: Complexity scaling may happen naturally if examples are generated in vocabulary frequency order, without explicit proficiency-based rules.

### What We Know

From `research-example-sentences.md`, we have theoretical support for **why** richer context helps:

1. **Dual Coding Theory**: Concrete, visualizable contexts activate both verbal and imagery systems
2. **Depth of Processing**: More contextual detail forces deeper semantic processing
3. **Involvement Load Hypothesis**: Distinctive contexts require evaluation, improving retention
4. **Context Availability**: Provided context helps learners access word meaning

### What We Haven't Investigated

1. **Complexity-proficiency relationship**: How should example complexity scale with learner level?
2. **Ceiling and floor effects**: Is there a minimum/maximum useful complexity at each stage?
3. **Progression model**: Should examples get more complex as learners advance, or stay constant?
4. **Regeneration strategy**: Should examples be regenerated as learners outgrow them?

---

## Sub-Questions

### 1. Complexity-Proficiency Relationship

- How does optimal example complexity scale with learner proficiency?
- Is the relationship linear, logarithmic, or stepped (by level)?
- What frameworks exist for calibrating input complexity to proficiency?

### 2. Cognitive Load Dynamics

- How does working memory capacity for L2 change with proficiency?
- At what point does added complexity become noise rather than signal?
- Does vocabulary difficulty interact with sentence complexity (harder word → simpler sentence)?

### 3. Comprehensible Input (i+1)

- How does Krashen's i+1 apply to example sentence design?
- What counts as "+1" in sentence complexity terms?
- Does i+1 imply complexity should always be slightly ahead of current level?

### 4. Static vs. Dynamic Examples

- Should examples remain constant (learn same material at deeper levels)?
- Or should examples evolve with learner (regenerate as proficiency grows)?
- What are the trade-offs of each approach?

---

## Hypotheses to Investigate

### H1: Complexity Should Track Proficiency
Optimal example complexity is relative to learner stage. What's too complex early becomes too simple later. Examples should scale.

### H2: Inverted-U at Each Stage
At any given proficiency level, there's an optimal complexity range. Too simple = not memorable, too complex = cognitive overload. The "sweet spot" shifts upward with proficiency.

### H3: Content vs. Structure Independence
Contextual richness (concrete details) and structural complexity (clause count, connectives) are separable dimensions. Early learners may benefit from rich content in simpler structures.

### H4: Asymptotic Benefit
Beyond a threshold, added complexity provides diminishing returns. There's a "good enough" level at each stage, beyond which effort is better spent elsewhere.

### H5: Static Examples Are Sufficient
If examples are well-designed for vocabulary learning (not grammar), the same example serves across proficiency levels—learners extract different value at different stages.

---

## Research Areas to Explore

### Academic Literature

- [ ] Cognitive load theory in L2 vocabulary acquisition
- [ ] Comprehensible input research (Krashen's i+1, VanPatten)
- [ ] Graded reader complexity calibration studies
- [ ] Learner dictionary example sentence research
- [ ] Working memory development in L2 acquisition
- [ ] Scaffolding theory and gradual complexity increase

### Practical Frameworks

- [ ] CEFR level descriptors for input complexity (A1→C2 progression)
- [ ] Graded reader leveling systems (how complexity is calibrated per level)
- [ ] Learner dictionary standards by level (Oxford, Cambridge, COBUILD)
- [ ] Spaced repetition and complexity (does Anki research address this?)

### Korean-Specific

- [ ] Korean readability formulas/research
- [ ] Korean L2 textbook sentence complexity by level
- [ ] TOPIK exam sentence complexity progression (1급→6급)
- [ ] Korean graded readers (if they exist)

---

## Findings

### Finding 1: Comprehensible Input Must Be 95-98% Known

**Source**: Krashen's i+1 hypothesis, supported by subsequent research

**Key insights**:
- Input should be 95-98% comprehensible for optimal acquisition
- The "distance" between i and i+1 cannot be too great
- If input is too far beyond (i+2, i+3), acquisition stalls
- Cognitive load becomes too high when <90% comprehensible

**Implication for our approach**:
- Multi-clause sentences with unfamiliar connectives (-서, -(으)니까) may push beginners below 95% comprehension
- For early learners: simpler structures ensure the vocabulary item is the "+1", not the grammar
- As grammar knowledge grows, complex structures become comprehensible, freeing capacity for vocabulary

### Finding 2: CEFR Progression Shows Clear Complexity Scaling

**Source**: CEFR level descriptors, text complexity research

**Key insights**:
- **A1**: Very short sentences, present tense only, few hundred words
- **A2**: Subordinate clauses introduced, 600-1000 words
- **B1**: Embedded clauses, conditional statements, ~2000 words
- **A2→B1 transition is significant**: requires comfort with embedded clauses and nuanced conditions
- Sentence length alone is not a good discriminator; clause complexity matters more

**Implication for our approach**:
- TOPIK 1 (≈A1-A2) learners may not be ready for embedded clauses
- Multi-clause examples (current v3) may be more appropriate for TOPIK 2 (≈B1+)
- The original "3-4 words" approach aligns with A1-A2 expectations

### Finding 3: Graded Readers Use Frequency + Structural Complexity Together

**Source**: Fountas & Pinnell, Lexile, graded reader research

**Key insights**:
- Leveling considers BOTH vocabulary frequency AND sentence complexity
- "Simpler, more natural sentences are easier to process"
- "Embedded and conjoined clauses make text more difficult"
- Vocabulary limited by frequency headword counts:
  - Level 1: 200 headwords
  - Level 6: 1200 headwords
- Higher levels permit more complex clause structures

**Implication for our approach**:
- Supports the frequency-complexity alignment hypothesis
- Early vocabulary (high frequency) → simple structures
- Later vocabulary (lower frequency) → more complex structures permitted
- Complexity should scale with vocabulary frequency, not be uniform

### Finding 4: High-Constraining Context Benefits Vocabulary Learning

**Source**: L2 vocabulary acquisition research

**Key insights**:
- "High-constraining contexts generate more robust learning than low-constraining contexts"
- Low-frequency words benefit from contextual clues in text
- Word frequency correlates strongly with perceived difficulty
- Prior knowledge affects contextual learning effectiveness

**Implication for our approach**:
- Richer context (multi-clause) IS beneficial for vocabulary learning
- BUT the learner must be able to comprehend the context (95%+ known)
- For beginners: context richness limited by grammar knowledge
- For intermediate+: richer context becomes accessible and beneficial

### Finding 5: Syntactic Complexity Adds Processing Load

**Source**: L2 reading comprehension research

**Key insights**:
- "Syntactically complex texts present greater difficulty in both L1 and L2 reading"
- L2 learners rely more on lexical/semantic cues than syntactic cues (shallow-structure hypothesis)
- Clause complexity significantly affects paragraph comprehension

**Implication for our approach**:
- Complex structures add cognitive load beyond vocabulary
- If learner is still processing grammar, less capacity for vocabulary acquisition
- Simpler structures for beginners = more capacity for vocabulary focus

---

## Implications for Requirements

### Research-Based Conclusions

**The frequency-complexity alignment hypothesis is supported by research:**

1. **CEFR/graded readers confirm**: Complexity should scale with proficiency
2. **i+1 principle**: Input must be 95-98% comprehensible; grammar counts toward this
3. **Cognitive load**: Complex structures consume processing capacity needed for vocabulary
4. **Rich context helps**: BUT only when the context itself is comprehensible

### Revised Understanding

| Stage | Vocab Frequency | Grammar Knowledge | Appropriate Structure |
|-------|-----------------|-------------------|----------------------|
| Early (TOPIK 1 초급) | High frequency | Basic (-요 endings) | Simple: 3-4 words, single clause |
| Mid (TOPIK 1 중급) | Medium frequency | Some connectives | Moderate: 4-5 words, simple connectives |
| Later (TOPIK 2) | Lower frequency | Connectives fluent | Rich: 5-6+ words, multi-clause |

**Key insight**: The original "3-4 words" wasn't wrong—it was appropriate for early stages. The current "multi-clause" isn't wrong either—it's appropriate for intermediate+ stages. Both are valid at different points.

### Recommended Strategy

**Tiered approach based on vocabulary position/frequency:**

1. **For TOPIK 1 (beginner vocabulary)**:
   - Return to simpler structures (v1/v2 style)
   - Single clause, 3-5 words
   - Avoid connectives learner hasn't acquired yet
   - Focus: vocabulary is the "+1", not grammar

2. **For TOPIK 2 (intermediate vocabulary)**:
   - Use current rich approach (v3 style)
   - Multi-clause with connectives
   - 5-6+ words
   - Focus: richer context aids retention of harder words

3. **Alternative: Vocabulary-frequency-based complexity**
   - Rather than TOPIK level, base complexity on word frequency
   - High-frequency words → simpler examples
   - Low-frequency words → richer context for scaffolding

### Questions Resolved

| Question | Answer |
|----------|--------|
| Should complexity scale with proficiency? | **Yes** - supported by CEFR, graded readers, i+1 |
| Was original "3-4 words" appropriate? | **Yes, for beginners** - aligns with A1-A2 expectations |
| Is current "multi-clause" appropriate? | **Yes, for intermediate+** - aligns with B1+ expectations |
| Should TOPIK 2 use different strategy? | **Yes** - research supports different complexity levels |

---

## Remaining Open Questions

1. How to operationalize "connectives the learner knows" in prompt requirements?
2. Should TOPIK 1 v2 examples (5.71 words) be regenerated with simpler approach?
3. What specific connectives are appropriate at each TOPIK sub-level?
4. How do commercial apps (Duolingo, Memrise) handle complexity progression?

---

## Next Steps

- [x] Search academic literature on complexity progression in L2
- [x] Review Krashen's i+1 for specific guidance on calibration
- [x] Examine CEFR complexity descriptors by level
- [x] Look at graded reader leveling methodologies
- [ ] Define specific requirements for TOPIK 1 vs TOPIK 2 example generation
- [ ] Decide: regenerate TOPIK 1 with simpler approach, or keep current v2?
- [ ] Create `requirements-example-topik1.md` and `requirements-example-topik2.md` if tiered approach adopted
