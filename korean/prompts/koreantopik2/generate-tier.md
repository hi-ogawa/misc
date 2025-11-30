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

| Tier | Description | Estimated Size |
|------|-------------|----------------|
| **Tier 1** | Essential everyday words, high frequency, natural with TOPIK 1 | ~500-800 |
| **Tier 2** | Useful but less frequent, broader vocabulary | ~1000-1500 |
| **Tier 3** | Specialized, academic, or low-frequency | ~1500-2000 |

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

### Option A: Single-shot Full List (Preferred)

Feed all 3873 words to LLM in one prompt:

```
Given this TOPIK 2 vocabulary list (3873 words), assign each word to a tier:

Tier 1: Essential - High frequency, everyday usage, natural co-occurrence with beginner vocabulary
Tier 2: Useful - Moderate frequency, broader but practical vocabulary
Tier 3: Specialized - Low frequency, academic, technical, or narrow usage

For a TOPIK 1 graduate, Tier 1 words should feel like "missing" beginner vocabulary.

Output: TSV with columns: number, korean, tier, reason (brief)
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

## Validation Approach

After tiering:

1. **Spot check top 50 Tier 1**: Do they feel familiar from variety shows?
2. **Cross-reference flagged unknowns**: Your ~100 unknown words from TOPIK 1 examples should mostly be Tier 1
3. **두르다 test**: Should rank high in Tier 1
4. **Sample Tier 3**: Should feel academic/specialized

## Workflow

1. **Generate tiers**: Run tiering prompt on full TOPIK 2 list
2. **Validate**: Spot-check results against intuition
3. **Process Tier 1 first**: Generate examples, notes, audio for ~500-800 words
4. **Create "TOPIK 1.5" deck**: Import Tier 1 as priority
5. **Later**: Process Tier 2 when Tier 1 is mastered

## Output Format

`output/koreantopik2/tier-all.tsv`:
```
number	korean	english	tier	reason
1	-가	professional	2	suffix, less common standalone
2	가까이	nearby	1	high frequency adverb
3	가꾸다	raise/cultivate	2	moderate frequency verb
...
```

## Open Questions

1. **Tier boundaries**: 500 vs 800 for Tier 1? Let LLM decide or set target?
2. **Confidence scores**: Ask for tier + confidence? Or keep simple?
3. **Context window**: Can 3873 words fit in one prompt? May need batching regardless.
4. **Refinement**: After initial tiers, allow manual adjustments?

---

**Next step**: Test tiering prompt on subset (batch 1: ~100 words) before full list.
