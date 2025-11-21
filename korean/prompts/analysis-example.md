# Example Sentence Analysis

Analysis of example sentence quality and consistency across TOPIK 1 and TOPIK 2 datasets.

## Tool

**Script**: `scripts/analyze-examples.py`

```bash
# Analyze TOPIK 1
python scripts/analyze-examples.py --input output/koreantopik1_anki_import.tsv

# Analyze TOPIK 2
python scripts/analyze-examples.py --input output/koreantopik2/koreantopik2_anki_import.tsv
```

**Output**: Korean word count statistics with per-batch breakdown

## Overall Results

### TOPIK 1 (1,847 entries, 19 batches)
- **Mean**: 3.81 words
- **Median**: 4.0 words
- **Standard deviation**: 0.83
- **IQR**: [3, 4] words (middle 50% of sentences)
- **Range**: 2-8 words
- **Per-batch mean σ**: 0.73

### TOPIK 2 (3,873 entries, 39 batches)
- **Mean**: 3.93 words
- **Median**: 4.0 words
- **Standard deviation**: 0.80
- **IQR**: [3, 4] words (middle 50% of sentences)
- **Range**: 2-9 words
- **Per-batch mean σ**: 0.74

## Key Findings

### 1. Excellent Intra-Batch Consistency

**Finding**: Each subagent generates internally consistent examples
- Per-batch σ ranges from 0.55 to 0.98 (average ~0.73)
- Low variance within each batch confirms each subagent maintains consistent style

**Interpretation**:
- Subagents follow requirements-example.md reliably
- No "quality drift" within a single batch
- Isolated subagent processing works well

### 2. Notable Inter-Batch Variation

**Finding**: Different batches have different mean sentence lengths

**TOPIK 1 outlier batches**:
- **Low complexity**: Batch 7 (mean=3.04), Batch 16 (mean=3.33)
- **High complexity**: Batch 12 (mean=4.57), Batch 11 (mean=4.41)
- **Range**: 3.04 → 4.57 words (50% difference)

**TOPIK 2 outlier batches**:
- **Low complexity**: Batch 7 (mean=3.02), Batch 2 (mean=3.59)
- **High complexity**: Batch 38 (mean=4.75), Batch 22 (mean=4.40)
- **Range**: 3.02 → 4.75 words (57% difference)

**Interpretation**:
- Different subagents interpret "appropriate sentence length" differently
- This is **not** a quality problem (all follow requirements-example.md)
- This **is** a consistency/calibration problem across batches

### 3. Appropriate Difficulty Progression

**Finding**: TOPIK 2 sentences are slightly longer on average (3.93 vs 3.81 words)

**Interpretation**:
- Matches expected difficulty level (beginner → intermediate/advanced)
- Natural progression in vocabulary complexity

## Implications for Learning

### Noticeable Complexity Jumps

As a learner progresses through batches, they will encounter:
- **Minimal example batches** (mean ~3 words): "나는 학생이다"
- **Contextual example batches** (mean ~4.5 words): "우리는 내일 서울에 갈 거예요"

This creates **inconsistent cognitive load** across study sessions.

### Current Study Progress

User is around batch 7 (one of the most minimal batches), so will experience complexity increase in later batches (especially batches 11-12).

## Understanding Statistics

### Standard Deviation (σ)
- Measures spread/variance of data
- Low σ (< 1.0) = sentences are consistently similar in length
- High σ (> 1.5) = wide variation in sentence lengths

### Percentiles
- **p25 (25th percentile)**: 25% of sentences have ≤ this many words
- **p50 (median)**: Half of sentences have ≤ this many words
- **p75 (75th percentile)**: 75% of sentences have ≤ this many words
- **IQR (Interquartile Range)**: [p25, p75] contains middle 50% of data

Example: TOPIK 1 overall IQR = [3, 4]
- 25% of sentences have ≤3 words
- 50% of sentences have 3-4 words
- 25% of sentences have ≥4 words

## Open Questions

1. **Is this variation acceptable?**
   - Pro: Provides natural diversity in example styles
   - Con: Inconsistent learning experience across batches

2. **Should requirements-example.md be more specific?**
   - Could add explicit target: "3-4 words for TOPIK 1, 4-5 words for TOPIK 2"
   - Trade-off: Less flexibility for subagents to adapt to vocabulary complexity

3. **Does vocabulary difficulty correlate with sentence length?**
   - Need to investigate: Do harder words naturally require longer contextual examples?
   - Check: Are high-mean batches teaching inherently more complex vocabulary?

## Next Steps

- [ ] Sample actual examples from low vs high complexity batches
- [ ] Evaluate if sentence length differences affect learning quality
- [ ] Consider whether to add explicit length guidance to requirements-example.md
- [ ] Investigate correlation between vocabulary difficulty and sentence length
