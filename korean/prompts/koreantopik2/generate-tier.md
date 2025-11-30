# TOPIK 2 Vocabulary Tiering Strategy

## Background

After practicing TOPIK 1, key insight emerged:

- TOPIK word lists are **test-prep artifacts**, not frequency-ranked
- LLM example sentences naturally included words outside TOPIK 1 (e.g., 두르다 for 목도리)
- These "missing links" = high-frequency words that co-occur with beginner vocabulary
- TOPIK 1/2 boundary is arbitrary - some TOPIK 2 words are more useful than TOPIK 1 words

**Goal**: Filter TOPIK 2 (3873 words) to prioritize high-value words for TOPIK 1 graduates.

## Core Insight: LLM as Frequency Oracle

LLMs trained on massive Korean text have implicit knowledge of:
- Word frequency in natural text
- Co-occurrence patterns with beginner vocabulary
- Which words are "central" vs "peripheral"

Instead of:
- Finding corpus data (Option B)
- Generating 4000 example sentences (expensive)
- Manual sentence mining (slow)

**Direct approach**: Ask LLM to tier the entire vocabulary list.

## Tiering Strategy

### Tier Definitions

| Tier | Description |
|------|-------------|
| **Tier 1** | Essential everyday words, high frequency, natural with TOPIK 1 |
| **Tier 2** | Useful but less frequent, broader vocabulary |
| **Tier 3** | Specialized, academic, or low-frequency |

Let LLM decide distribution naturally - no enforced counts.

### Tier 1 Criteria (Priority)
- High frequency in spoken Korean
- Strong co-occurrence with TOPIK 1 vocabulary
- Appears in daily conversation, variety shows, dramas
- Fills "gaps" in TOPIK 1 coverage

### Tier 3 Criteria (Deprioritize)
- Academic/formal register
- Technical/specialized domains
- Literary or archaic usage
- Narrow usage contexts

## Implementation Options

### Option A: Single-shot Full List

Feed all 3873 words to LLM in one prompt:

```
Given this TOPIK 2 vocabulary list (3873 words), assign each word to a tier:

Tier 1: Essential - High frequency, everyday usage, natural co-occurrence with beginner vocabulary
Tier 2: Useful - Moderate frequency, broader but practical vocabulary
Tier 3: Specialized - Low frequency, academic, technical, or narrow usage

For a TOPIK 1 graduate, Tier 1 words should feel like "missing" beginner vocabulary.

Output: TSV with columns: number, korean, tier
```

**Pros**: Simple, fast, leverages LLM's implicit frequency knowledge
**Cons**: Single LLM's judgment, no validation

### Option B: Batch with Consensus

Split into batches, process with multiple prompts, look for consensus.

**Pros**: More robust
**Cons**: More work, may not add much value

### Option C: Validation via Example Generation

For uncertain words, ask LLM to generate example sentences using TOPIK 1 vocabulary.
- If natural sentence emerges -> Tier 1
- If sentence feels forced -> Tier 2/3

### Option D: Combined Tier + Example Generation (Recommended)

Process in ~100 word batches (like `generate-examples.md`), but generate BOTH tier and example sentence together.

**Rationale:**
- 4000 words + 4000 tier outputs in one shot is too large
- Generating an example forces LLM to "use" the word
- If natural example comes easily → reveals Tier 1
- If example feels forced/awkward → reveals Tier 2/3
- The act of generating reveals word's "naturalness" better than abstract tier judgment

**Process:**
1. Use existing batch split: `input/koreantopik2-batch-1.tsv` to `input/koreantopik2-batch-39.tsv`
2. For each batch, generate: number, korean, tier, example_ko, example_en
3. Output: `output/koreantopik2/tier-examples-N.tsv`

**Output format:**
```
number	korean	english	tier	example_ko	example_en
1	-가	professional	2	그는 유명한 음악가입니다.	He is a famous musician.
2	가까이	nearby	1	가까이 오세요.	Come closer.
...
```

**Benefits:**
- Tier decision informed by actual usage attempt
- Get examples "for free" alongside tiering
- Batch size matches existing infrastructure
- Can filter Tier 1 words later and already have examples ready

## Validation Approach

After tiering:

1. **Spot check top 50 Tier 1**: Do they feel familiar from variety shows?
2. **Cross-reference flagged unknowns**: Your ~100 unknown words from TOPIK 1 examples should mostly be Tier 1
3. **두르다 test**: Should rank high in Tier 1
4. **Sample Tier 3**: Should feel academic/specialized

## Workflow

With Option D:

1. **Generate tier + examples**: Process batches 1-39 with combined prompt
2. **Merge outputs**: Combine batch files into tier-all.tsv and examples-all.tsv
3. **Validate**: Spot-check Tier 1 results against intuition
4. **Filter Tier 1**: Extract Tier 1 words (examples already generated)
5. **Process Tier 1**: Generate notes, audio for Tier 1 words only
6. **Create "TOPIK 1.5" deck**: Import Tier 1 as priority
7. **Later**: Process Tier 2 when Tier 1 is mastered

## Output Format

With Option D (recommended), output per-batch files:

`output/koreantopik2/tier-examples-N.tsv` (N = 1-39):
```
number	korean	english	tier	example_ko	example_en
```

After all batches complete, merge into:
`output/koreantopik2/tier-all.tsv` (tier column only, for filtering)
`output/koreantopik2/examples-all.tsv` (examples, for downstream processing)

## Open Questions

1. **Refinement**: After initial tiers, allow manual adjustments?
2. **Tier criteria in prompt**: How much guidance to give LLM vs let it decide naturally?

---

**Next step**: Test Option D on batch 1 (~100 words) to validate approach.
