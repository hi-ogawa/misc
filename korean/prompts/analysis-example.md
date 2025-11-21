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
- Root cause identified: Batch 7 over-optimized for "SIMPLE and MINIMAL" guidance in requirements
- Batch 3/6 used connectives (-서, -을 때) which violated requirements but produced better learning outcomes
- **Action taken**: Updated `requirements-example.md` to encourage batch 3/6 style and discourage batch 7's bare minimum approach

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

### Current Study Progress & User Feedback

User is around batch 7 (one of the most minimal batches).

**From actual Anki practice experience:**
- **Preferred style**: Batch 3/6 examples with connectives and richer context
  - Batch 3 (4.22 words): "동생이 그저께 서울에서 돌아왔어요" (time + location)
  - Batch 6 (4.30 words): "우리 고양이가 너무 뚱뚱해서 뛰지 못해요" (-서 connective)
- **Less preferred**: Batch 7's minimal style
  - Batch 7 (3.04 words): "무궁화가 여름에 피어요" (bare minimum)

**Learning insight**: Richer context with connectives (-서, -을 때, -을지) aids memorization and understanding, even if sentences are longer.

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

1. **~~Should requirements-example.md be more specific?~~** ✅ **RESOLVED**
   - User feedback confirmed batch 3/6 style (with connectives) is preferred over batch 7's minimal style
   - Updated requirements to encourage connectives (-서, -을 때, -을지) that add learning value
   - Batch 7 examples now explicitly shown as "BARE MINIMUM" to avoid

2. **Is variation still acceptable with updated requirements?**
   - Some variation (3.5-4.5 words) may still occur and could be beneficial for diversity
   - Extreme minimalism (batch 7 style) now discouraged by updated requirements
   - Future batches should converge toward batch 3/6 style

3. **Does vocabulary difficulty correlate with sentence length?**
   - Batch 7 vocabulary was equally basic as other batches (무겁다, 무릎, 문 vs 어리다, 어머니, 얼굴)
   - Variation is in example generation style, not vocabulary complexity
   - No correlation found between vocabulary difficulty and sentence length

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
- [x] Sample actual examples from low vs high complexity batches (batches 3, 6, 7)
- [x] Evaluate if sentence length differences affect learning quality (user feedback: batch 3/6 preferred)
- [x] Update requirements-example.md based on findings (encourage connectives, discourage bare minimum)
- [x] Investigate correlation between vocabulary difficulty and sentence length (no correlation found)
- [ ] Calculate chars/word ratio per batch to identify batches with unusually simple/complex vocabulary
- [ ] Consider if batch 7 should be regenerated with updated requirements (low priority - examples are functional)
