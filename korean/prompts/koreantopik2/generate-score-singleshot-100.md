# Single-Shot Scoring Prompt for TOPIK 2 Vocabulary (1-100 scale)

**Context**: Score all 3873 TOPIK 2 words in one pass to maintain consistent scoring baseline.

**Score scale**: 1-100 (revised from 1-10 for better granularity)

---

## Task

Assign priority scores (1-100) to all TOPIK 2 vocabulary words based on their value for a TOPIK 1 graduate.

---

## Step 1: Read TOPIK 1 Reference

Read `input/koreantopik1.tsv` (korean column).

This is the beginner vocabulary (~1850 words) the learner has already mastered. Use this as your anchor.

---

## Step 2: Read TOPIK 2 Input

Read `input/koreantopik2.tsv` - all 3873 words.

**Important**: Read the entire file (it's ~4000 lines). If needed, use offset/limit parameters to read in multiple passes, but keep ALL words in memory before scoring to maintain consistent baseline.

---

## Step 3: Scoring Guidelines

### Score Ranges

**80-100: Essential priority**
- High frequency in spoken Korean
- Strong co-occurrence with TOPIK 1 vocabulary
- Common in variety shows, dramas, daily conversation
- Fills "missing links" in beginner vocabulary (e.g., 두르다 for 목도리)
- Natural next step after TOPIK 1

**40-79: Useful expansion**
- Moderate frequency
- Practical but less common contexts
- Broader vocabulary building
- Not critical for daily conversation

**1-39: Specialized/low priority**
- Academic or formal register
- Technical/domain-specific
- Literary or archaic
- Narrow usage contexts

### Morphological Family Constraint

**CRITICAL RULE**: Words in the same morphological family get **identical scores**.

Examples:
- 결정 (decision), 결정하다 (to decide), 결정적 (decisive) → same score
- 준비 (preparation), 준비하다 (to prepare) → same score
- 행복 (happiness), 행복하다 (to be happy) → same score
- 가능 (possible), 가능하다 (be possible), 가능성 (possibility) → same score

**Why**: If you learn one form, learning related forms is trivial. Score the concept/root, not individual forms.

### Scoring Process

1. **Scan the full list** (3873 words) to get overall sense of vocabulary range
2. **Identify morphological families** across the entire list
3. **For each family**:
   - Decide score based on the concept/root
   - Apply same score to ALL family members
4. **For standalone words**: Score individually
5. **Use the full 1-100 range**: Spread scores naturally across the range, don't cluster around 50-70
6. **Anchoring questions** for each word/family:
   - Would this naturally appear in sentences using TOPIK 1 vocabulary?
   - Is it common in Korean media (variety shows, dramas, news)?
   - Would a TOPIK 1 graduate feel this is a "missing piece"?

---

## Step 4: Output Format

**IMPORTANT**: Score all 3873 words first, then write output in batches to avoid token limits.

Write output in 8 parts (each with header), 500 entries per part:
- `output/koreantopik2/scores-singleshot100-0001-0500.tsv` - rows 1-500
- `output/koreantopik2/scores-singleshot100-0501-1000.tsv` - rows 501-1000
- `output/koreantopik2/scores-singleshot100-1001-1500.tsv` - rows 1001-1500
- `output/koreantopik2/scores-singleshot100-1501-2000.tsv` - rows 1501-2000
- `output/koreantopik2/scores-singleshot100-2001-2500.tsv` - rows 2001-2500
- `output/koreantopik2/scores-singleshot100-2501-3000.tsv` - rows 2501-3000
- `output/koreantopik2/scores-singleshot100-3001-3500.tsv` - rows 3001-3500
- `output/koreantopik2/scores-singleshot100-3501-3873.tsv` - rows 3501-3873

**Columns**: `number	korean	english	score`

**Example** (all parts have same format):
```
number	korean	english	score
1	-가	professional	[score]
2	가까이	nearby	[score]
3	가능	possible	[score]
4	가능하다	to be possible	[score]
5	가능성	possibility	[score]
...
```

Note: Morphological families (e.g., 가능/가능하다/가능성) must have identical scores across all parts.

---

## Critical Rules

1. **DO NOT write scripts or code** - assign scores directly using your Korean language knowledge
2. **DO NOT use bash/python** - just read the files and write output
3. **DO NOT use Task/subagents** - process all words yourself to maintain consistent baseline
4. **Process ALL 3873 entries** - no truncation, read entire file even if requires multiple Read calls
5. **ENFORCE morphological family constraint strictly** - scan full list to identify all families
6. **Use full 1-100 range** - spread scores naturally, don't cluster around 50
7. **Maintain consistency** - this is the key advantage of single-shot scoring

---

## Why Single-Shot?

**Problem with batches**: Each batch establishes its own baseline. Batch 1 might score 두르다 as 90, while batch 20 scores an equally essential word as 70 due to different local context.

**Single-shot advantage**: Consistent baseline across all 3873 words. You can compare any two words directly and maintain relative ordering.

---

## Results

Output: `output/koreantopik2/scores-singleshot100.tsv`

### Overall Statistics
| Metric | Value |
|--------|-------|
| Total words | 3,873 |
| Min score | 42 |
| Max score | 92 |
| Mean score | 72.5 |

### Tier Breakdown
| Tier | Count | % |
|------|-------|---|
| 80-100 (Essential) | 517 | 13.3% |
| 40-79 (Useful) | 3,356 | 86.7% |
| 1-39 (Specialized) | 0 | 0% |

### Score Distribution (24 unique values)
```
42 | 1
45 | 1
48 | 2
52 | 11
55 |█ 27
56 | 1
58 |████████ 136
60 | 1
62 |██████████ 175
64 | 10
65 |████████████████ 276
68 |████████████████████████████████████ 608
70 |█ 20
72 |██████████████████████████████████████████████████ 839
74 | 2
75 |███████████████████████████████████████████ 732
76 | 3
78 |██████████████████████████████ 511
80 |███ 60
82 |█████████████████ 288
85 |██████ 117
88 |██ 48
90 | 1
92 | 3
```

### Highest Scored (92)
- 가능, 가능성, 두르다

### Lowest Scored (42-52)
- 가뭄 (drought) - 42
- -가 (professional suffix) - 45
- 가로막다 (obstruct), 강수량 (precipitation) - 48

### Observations
- **Narrow range**: Only 24 unique values, clustered 58-85 (not using full 1-100)
- **No low-priority words**: Nothing scored below 42
- **Morphological families**: 가능/가능성 correctly share score (92)
