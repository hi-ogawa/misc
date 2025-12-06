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
**Cons**: Single LLM's judgment, risk of hallucinations/typos

#### Validation Steps

After generating output, verify data integrity:

```bash
# 1. Extract sorted Korean words from input
python scripts/jq-tsv.py -s 'map(.korean) | sort' input/koreantopik2.tsv > output/tmp/input-korean-sorted.json

# 2. Extract sorted Korean words from output
python scripts/jq-tsv.py -s 'map(.korean) | sort' output/koreantopik2/scores-singleshot.tsv > output/tmp/output-korean-sorted.json

# 3. Find hallucinations (words in output but not in input)
jq -n --slurpfile a output/tmp/input-korean-sorted.json --slurpfile b output/tmp/output-korean-sorted.json '($b[0] - $a[0])'

# 4. Find missing words (words in input but not in output)
jq -n --slurpfile a output/tmp/input-korean-sorted.json --slurpfile b output/tmp/output-korean-sorted.json '($a[0] - $b[0])'
```

**Expected result**: Both commands should return `[]` (empty array).

**Common issues found:**
- **Hallucinations**: LLM adds words to complete morphological families (e.g., adding 가능하다 to complete 가능/가능성/가능하다 family, even though 가능하다 wasn't in input)
- **Typos**: LLM misremembers spelling (e.g., 지겹다 → 지겁다)

**If errors found:**
- Document the discrepancies
- Decide whether to manually fix or re-run with stricter prompt constraints

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

**Status**: Completed using Option A (single-shot scoring)

**Approach**: Single-shot full list with 1-10 score scale (changed from original 1-100 for practicality)

**Files**:
- Raw output: `output/koreantopik2/scores-singleshot.tsv` (had validation issues)
- Fixed output: `output/koreantopik2/scores-singleshot_edit.tsv` (canonical version)

**Validation Issues Found**:
1. **Hallucination**: 가능하다 added at row 7 (completing morphological family not in input)
2. **Typo**: 지겹다 → 지겁다
3. Fixed using jq-tsv.py transformation (see validation steps in Option A)

**Score Distribution** (3873 words):
```
Score 9: 113 words (2.9%) - Essential
Score 8: 1045 words (27.0%) - High priority
Score 7: 2052 words (53.0%) - Useful
Score 6: 551 words (14.2%) - Moderate
Score 5: 107 words (2.8%) - Lower priority
Score 4: 5 words (0.1%) - Specialized
```

**Statistics**:
- Range: 4-9 (no scores 1-3 or 10 assigned)
- Mean: 7.13
- Median: 7

**Sample Words by Score**:

Score 9 (Essential - 113 words):
- 가능 (possible), 가능성 (possibility)
- 검색 (search)
- 결국 (finally)
- 경우 (case)
- 그래도 (anyway), 그렇지 (right)
- 근데 (however)
- 기본 (basics)

Score 8 (High priority - 1045 words):
- 가까이 (nearby)
- 가스 (gas)
- 가정 (family)
- 가져다주다 (bring)
- 가치 (value)
- 각 (each), 각자 (each person)
- 갈수록 (increasingly)
- 감정 (emotion)

Score 5 (Lower priority - 107 words):
- 가꾸다 (raise/cultivate)
- 가로 (length)
- 가뭄 (drought)
- 가정 (assumption)
- 가톨릭 (Catholic)
- 각국 (each country)
- 간 (liver)
- 간접적 (indirect)

Score 4 (Specialized - 5 words):
- 강수량 (precipitation/rainfall)
- 경복궁 (Gyeongbokgung)
- 남미 (South America)
- 북미 (North America)
- 아프리카 (Africa)

**Key Observations**:
- LLM avoided extreme scores (1-3, 10) and clustered around 6-8
- Morphological families correctly received identical scores
- Geographic/specialized terms (continents, palaces) scored lowest
- High-frequency functional words (근데, 경우, 결국) scored highest
- Distribution suggests ~1200 words (scores 8-9) as priority tier

### 1-100 Scale Attempt (Second Run)

**Status**: Completed

**Files**:
- Output: `output/koreantopik2/scores-singleshot100.tsv` (canonical version)

**Score Distribution** (3873 words):
- Range: 42-92 (only 50 out of 100 points used)
- Mean: 72.5, Median: 72

**Heavy clustering around 4 scores**:
- Score 72: 839 words (21.7%)
- Score 75: 732 words (18.9%)
- Score 68: 608 words (15.7%)
- Score 78: 511 words (13.2%)
- **Total: 69% of all words in just 4 scores**

**By tier**:
- 85-100 (Essential): 169 words (4.4%)
- 75-84 (High): 1594 words (41.2%)
- 65-74 (Mid): 1745 words (45.1%)
- 55-64 (Lower): 350 words (9.0%)
- 1-54 (Specialized): 15 words (0.4%)

**Key Observations**:
- 1-100 scale didn't solve clustering problem (just shifted from 6-8 → 65-78)
- LLMs naturally avoid extremes and cluster around "safe" middle values
- Morphological families correctly received identical scores
- No hallucinations or typos (validation passed)

## Post-Processing: Further Subdivision of Clusters

**Problem**: Both 1-10 and 1-100 scales resulted in heavy clustering. For practical deck management, we want ~100-word batches with alphabetical variety.

**Goal**: Split large score clusters (e.g., score 72 with 839 words) into smaller groups of ~100 words each, while:
- Maintaining alphabetical variety within each group
- Keeping morphological families together (never split 가능/가능성 across groups)

### Approach: Morphological Family-Aware Binning

**Algorithm**:
1. **Group by morphological family** (shared stem/root)
   - Heuristic: shared first 2-3 characters, or dictionary-based stems
   - Examples: {가능, 가능성}, {개인, 개인적}, {간신히}

2. **Sort families alphabetically** (by first word in family)
   - Ensures natural alphabetical spread across bins

3. **Pack families into bins of ~100 words**
   - Bin-packing algorithm: greedily assign families to bins until ~100 words
   - Never split a family across bins
   - Some bins may have 90-110 words (acceptable variation)

4. **Assign sub-scores**:
   - Score 72 (839 words) → 72.1 (~100), 72.2 (~100), ..., 72.9 (~39)
   - Score 75 (732 words) → 75.1 (~100), 75.2 (~100), ..., 75.8 (~32)

**Result**:
- ~40 buckets total across all scores
- Each bucket: ~100 words with alphabetical variety
- Morphological families intact for easier studying

**Implementation** (TBD):
- Write Python script for morphological family detection
- Use bin-packing algorithm for assignment
- Output: `scores-singleshot100-subdivided.tsv` with additional `subscore` column

**Status**: Not yet implemented (potential future enhancement)

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

1. ✅ **Complete**: Single-shot scoring of all 3873 words
2. ✅ **Complete**: Score distribution analysis
3. **Decide priority deck approach**:
   - Option A: Score >= 8 (1158 words - top 30%)
   - Option B: Score == 9 only (113 words - top 3%)
   - Option C: Top N (e.g., 500, 1000 words)
4. **Generate examples for priority subset** (if going with filtered approach)
   - Reuse existing examples from `output/koreantopik2/notes-*.tsv`
   - Or generate fresh examples optimized for high-priority words
5. **Create filtered Anki import file**
   - Join scores with existing notes/examples/audio
   - Filter to priority subset
6. **Import to Anki** as "TOPIK 1.5" or "TOPIK 2 Essential" deck
