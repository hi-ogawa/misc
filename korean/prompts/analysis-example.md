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

**Output**: Two separate tables
1. Word count statistics (Korean words)
2. Character count statistics (Korean characters)

Both with overall stats and per-batch breakdown.

## Overall Results

### Word Count Analysis

**TOPIK 1** (1,847 entries, 19 batches)
- **Mean**: 3.81 words
- **Median**: 4.0 words
- **Standard deviation**: 0.83
- **IQR**: [3, 4] words (middle 50% of sentences)
- **Range**: 2-8 words
- **Per-batch mean σ**: 0.73

**TOPIK 2** (3,873 entries, 39 batches)
- **Mean**: 3.93 words
- **Median**: 4.0 words
- **Standard deviation**: 0.80
- **IQR**: [3, 4] words (middle 50% of sentences)
- **Range**: 2-9 words
- **Per-batch mean σ**: 0.74

### Character Count Analysis

**Why character count matters**:
- Word count can be misleading: "학생" (1 word, 2 chars) vs "대학생" (1 word, 3 chars)
- A 3-word sentence could be 6-15 characters depending on word complexity
- Character count may correlate better with actual reading difficulty and visual complexity

**TOPIK 1** (1,847 entries, 19 batches)
- **Mean**: 11.98 characters
- **Median**: 12.0 characters
- **Standard deviation**: 2.45
- **IQR**: [10, 14] characters (middle 50% of sentences)
- **Range**: 4-23 characters
- **Per-batch mean σ**: 2.08
- **Chars/word ratio**: ~3.14 chars/word average

**TOPIK 2** (3,873 entries, 39 batches)
- **Mean**: 12.96 characters
- **Median**: 13.0 characters
- **Standard deviation**: 2.30
- **IQR**: [11, 14] characters (middle 50% of sentences)
- **Range**: 6-25 characters
- **Per-batch mean σ**: 2.00
- **Chars/word ratio**: ~3.30 chars/word average

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

### 4. Character Count Reveals Word Complexity

**Finding**: TOPIK 2 uses more complex words (higher chars/word ratio: 3.30 vs 3.14)

**Insights**:
- Character count variance (σ ~2.0-2.5) is higher than word count variance (σ ~0.7-0.8), showing that word complexity adds another dimension beyond sentence length
- TOPIK 2 sentences are both longer (3.93 vs 3.81 words) AND use longer words (12.96 vs 11.98 chars)
- Batch 7 in both datasets shows minimal complexity in BOTH metrics:
  - TOPIK 1 Batch 7: 3.04 words, 9.18 chars (lowest in both)
  - TOPIK 2 Batch 7: 3.02 words, 10.39 chars (lowest/near-lowest in both)
- This confirms batch 7 prefers short sentences with simple vocabulary

**Interpretation**:
- Character count is a valuable complementary metric to word count
- Some batches consistently prefer simpler vocabulary (lower chars/word), not just shorter sentences
- Reading difficulty is multi-dimensional: sentence length + word complexity

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

## Visualization

**Current approach**: Markdown tables (readable in terminal, easy to generate)

**Future consideration**: Proper visualization tools
- Line charts for batch-to-batch trends
- Histograms for distribution analysis
- Box plots for comparing batches
- Tools: matplotlib, plotly, or export to CSV for external tools

**Decision**: Deferred until need is clear. Tables are sufficient for initial analysis.

## Next Steps

- [x] Implement character count analysis in `scripts/analyze-examples.py`
- [x] Run analysis on both TOPIK 1 and TOPIK 2
- [x] Update this document with character count findings
- [ ] Sample actual examples from low vs high complexity batches (e.g., batch 7 vs batch 12)
- [ ] Evaluate if sentence length differences affect learning quality in practice
- [ ] Consider whether to add explicit length guidance to requirements-example.md
- [ ] Investigate correlation between vocabulary difficulty and sentence length
- [ ] Calculate chars/word ratio per batch to identify batches with unusually simple/complex vocabulary
