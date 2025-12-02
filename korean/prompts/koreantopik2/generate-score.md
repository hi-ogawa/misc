# TOPIK 2 Vocabulary Scoring Strategy

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

**Direct approach**: Ask LLM to score the entire vocabulary list.

## Scoring Strategy

### Score Definition

**Numeric score (1-100)**: Higher score = more essential for a TOPIK 1 graduate

### Scoring Criteria

**High scores (80-100)**: Essential priority
- High frequency in spoken Korean
- Strong co-occurrence with TOPIK 1 vocabulary
- Appears in daily conversation, variety shows, dramas
- Fills "gaps" in TOPIK 1 coverage

**Mid scores (40-79)**: Useful but less urgent
- Moderate frequency
- Practical but less common contexts
- Broader vocabulary expansion

**Low scores (1-39)**: Specialized, low priority
- Academic/formal register
- Technical/specialized domains
- Literary or archaic usage
- Narrow usage contexts

### Morphological Family Constraint

**Critical rule**: Words in the same morphological family get **identical scores**.

Examples:
- 결정 (decision), 결정하다 (to decide), 결정적 (decisive) → all get same score
- 준비 (preparation), 준비하다 (to prepare) → all get same score
- 행복 (happiness), 행복하다 (to be happy) → all get same score

**Rationale**: If you learn one form, learning related forms is trivial. The "essentialness" judgment applies to the concept/root, not individual forms.

## Implementation Options

### Option A: Single-shot Full List

Feed all 3873 words to LLM in one prompt:

```
Given this TOPIK 2 vocabulary list (3873 words), assign each word a score (1-100):

80-100: Essential - High frequency, everyday usage, natural co-occurrence with beginner vocabulary
40-79: Useful - Moderate frequency, broader but practical vocabulary
1-39: Specialized - Low frequency, academic, technical, or narrow usage

For a TOPIK 1 graduate, high-scoring words should feel like "missing" beginner vocabulary.

Output: TSV with columns: number, korean, english, score
```

**Pros**: Simple, fast, leverages LLM's implicit frequency knowledge
**Cons**: Single LLM's judgment, no validation

### Option B: Batch with Consensus

Split into batches, process with multiple prompts, look for consensus.

**Pros**: More robust
**Cons**: More work, may not add much value

### Option C: Validation via Example Generation

For uncertain words, ask LLM to generate example sentences using TOPIK 1 vocabulary.
- If natural sentence emerges -> High score (8-10)
- If sentence feels forced -> Low score (1-5)

### Option D: Batch Scoring (Recommended)

Process in ~100 word batches, assigning numeric scores (1-100).

**Rationale:**
- 4000 words in one shot is too large for careful judgment
- Batch size matches existing infrastructure
- LLM can compare words within batch for relative scoring
- TOPIK 1 reference provides concrete anchor for "beginner vocabulary"

**Benefits:**
- Numeric scores enable flexible filtering (top 500, top 1000, etc.)
- Morphological families can be enforced by LLM during scoring
- Simpler output format (no examples)
- Can generate examples separately for high-scoring words later

#### Subagent Prompt Template

```
**Task: Assign priority scores to TOPIK 2 vocabulary batch {N}**

## Step 1: Read TOPIK 1 Reference
Read `/home/hiroshi/code/personal/misc/korean/input/koreantopik1.tsv` to anchor your judgment.

This is the beginner vocabulary a learner has mastered (~1850 words). Your task is to score TOPIK 2 words by how essential they are for someone at this level.

## Step 2: Read Input Batch
Read `/home/hiroshi/code/personal/misc/korean/input/koreantopik2-batch-{N}.tsv`

## Step 3: Assign Scores (1-100)

**Scoring criteria:**
- **80-100**: Essential - High frequency, strong co-occurrence with TOPIK 1 vocabulary, fills gaps in everyday conversation
- **40-79**: Useful - Moderate frequency, practical but less common
- **1-39**: Specialized - Academic, technical, literary, or narrow usage

**CRITICAL: Morphological family constraint**
Words in the same morphological family MUST get identical scores:
- 결정 (decision), 결정하다 (to decide), 결정적 (decisive) → same score
- 준비 (preparation), 준비하다 (to prepare) → same score
- 행복 (happiness), 행복하다 (to be happy) → same score

**Process:**
1. Identify morphological families in the batch
2. For each family, assign one score based on the concept/root
3. Apply that score to all family members
4. For standalone words, assign individual scores

**Anchoring to TOPIK 1:**
- Would this word naturally appear in sentences using TOPIK 1 vocabulary?
- Does it fill a "missing link" (e.g., 두르다 for 목도리)?
- Is it common in variety shows, dramas, daily conversation?

## Step 4: Write Output
Write TSV to `/home/hiroshi/code/personal/misc/korean/output/koreantopik2/scores-{N}.tsv`

**Columns**: number	korean	english	score

## Critical Rules
- DO NOT write scripts or code - assign scores directly using Korean language knowledge
- DO NOT run bash commands - just write the file and exit
- Process ALL entries in the batch
- ENFORCE morphological family constraint strictly
- Use full 1-100 range (don't cluster around 50)
```

#### Output Format

Per-batch: `output/koreantopik2/scores-{N}.tsv`
```
number	korean	english	score
1	-가	professional	25
2	가까이	nearby	85
3	가능	possible	92
4	가능하다	to be possible	92
5	가능성	possibility	92
```

## Validation Approach

After scoring:

1. **Spot check top 50 scores**: Do they feel familiar from variety shows?
2. **Cross-reference flagged unknowns**: Your ~100 unknown words from TOPIK 1 examples should have high scores
3. **두르다 test**: Should score high (80+)
4. **Sample low scores (<40)**: Should feel academic/specialized
5. **Morphological family check**: Verify related words have identical scores

## Output Files

**Per-batch outputs** (39 files):
- `output/koreantopik2/scores-{1-39}.tsv`

**Consolidated scores**:
```bash
# Merge all batches (use {1..39} for correct numeric order, not *.tsv)
cat output/koreantopik2/scores-{1..39}.tsv | awk 'NR==1 || !/^number/' > output/koreantopik2/scores-all.tsv
```

**Sort by score** (descending):
```bash
# Sort by score (highest first), skip header
(head -n 1 output/koreantopik2/scores-all.tsv && tail -n +2 output/koreantopik2/scores-all.tsv | sort -t$'\t' -k4 -nr) > output/koreantopik2/scores-sorted.tsv
```

**Score distribution**:
```bash
# Count words by score ranges
python3 scripts/jq-tsv.py -s 'group_by(if (.score | tonumber) >= 80 then "80-100" elif (.score | tonumber) >= 40 then "40-79" else "1-39" end) | map({range: .[0] | if (.score | tonumber) >= 80 then "80-100" elif (.score | tonumber) >= 40 then "40-79" else "1-39" end, count: length})' output/koreantopik2/scores-all.tsv
```

**Filter top N words**:
```bash
# Top 500 words
head -n 501 output/koreantopik2/scores-sorted.tsv > output/koreantopik2/top-500.tsv

# Top 1000 words
head -n 1001 output/koreantopik2/scores-sorted.tsv > output/koreantopik2/top-1000.tsv
```

## Execution Status

**Status**: Not yet started (planning phase)

**Next actions**:
1. Run scoring for all 39 batches using Option D subagent prompt
2. Consolidate into `scores-all.tsv`
3. Sort by score descending → `scores-sorted.tsv`
4. Analyze score distribution
5. Decide cutoff for priority deck (e.g., top 500, top 1000, or score >= 80)

## Creating Priority Anki Deck

### Goal
After scoring is complete, create a filtered Anki deck of high-priority words.

### Workflow (TBD after scoring)

**Option 1: Score-based cutoff**
- Filter words with score >= 80
- Use existing examples and audio from `koreantopik2_anki_import.tsv`

**Option 2: Top N words**
- Take top 500 or top 1000 from `scores-sorted.tsv`
- Use existing examples and audio

**Option 3: Generate new examples for priority words**
- After identifying priority words (by score or count)
- Generate fresh examples optimized for those specific words
- Generate new audio

**Deferred decision**: Wait until scoring reveals distribution and count of high-scoring words.

## Next Steps

1. **Immediate**: Run scoring for all 39 batches
2. Analyze score distribution
3. Decide priority deck cutoff (score threshold or top N)
4. Generate examples for priority words (if needed)
5. Create filtered Anki import file
6. Import to Anki as "TOPIK 1.5" or similar deck
