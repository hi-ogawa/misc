# Dataset Reduction Strategies

Mechanical pattern-based approaches to reduce vocabulary redundancy without per-word LLM processing.

## Context

**Already implemented**:
- LLM curation tagging (prompts/koreantopik2/plan-curation.md) - filtered ~13%
- Word families: 하다/히/되다 variants (check-word-families.md) - 52 families

**Goal**: Find additional mechanical patterns detectable via regex/cross-reference.

## Approach 1: Verb Auxiliary Compounds

Compound verbs formed by verb stem + auxiliary verb. Meaning is predictable if you know both parts.

**Pattern**: `(아|어|여)(가다|오다|보다|버리다|주다|놓다|두다)$`

| Auxiliary | Meaning | Example |
|-----------|---------|---------|
| 가다 | away/continuing | 가져가다 (take away) |
| 오다 | toward/becoming | 가져오다 (bring) |
| 보다 | try | 먹어보다 (try eating) |
| 버리다 | completely | 잊어버리다 (forget completely) |
| 주다 | for someone | 만들어주다 (make for someone) |
| 놓다/두다 | in advance | 써놓다 (write down) |

**Detection**:
```bash
# Extract potential auxiliary compounds
grep -E '(아|어|여)(가다|오다|보다|버리다|주다|놓다|두다)$' input.tsv
```

**Filter criteria**: Keep if root verb also exists in dataset? Or always filter?

## Approach 2: Root + Compound Overlap

If both a root word and its compound exist, the compound may be redundant.

**Common compound suffixes**:
| Suffix | Type | Example |
|--------|------|---------|
| 약 | medicine | 감기약 ← 감기 |
| 집 | place/shop | 빵집 ← 빵 |
| 객 | person | 관광객 ← 관광 |
| 지 | place | 관광지 ← 관광 |
| 비 | cost | 교통비 ← 교통 |
| 물 | thing | 음식물 ← 음식 |

**Detection**:
```python
# Cross-reference: find words where root exists in dataset
roots = set(words)
compounds = [(w, suffix) for w in words
             for suffix in ['약', '집', '객', '지', '비', '물']
             if w.endswith(suffix) and w[:-len(suffix)] in roots]
```

**Filter criteria**: Compound meaning = root + suffix meaning → filter

## Approach 3: Passive/Causative Pairs

Korean passive/causative formed by suffix. If active verb exists, derived form may be redundant.

**Patterns**:
| Suffix | Type | Example |
|--------|------|---------|
| 이다 | passive/causative | 보이다 ← 보다 |
| 히다 | passive/causative | 읽히다 ← 읽다 |
| 리다 | passive/causative | 들리다 ← 듣다 |
| 기다 | passive/causative | 안기다 ← 안다 |
| 우다 | causative | 깨우다 ← 깨다 |
| 추다 | causative | 낮추다 ← 낮다 |

**Detection**:
```bash
# Find potential passive/causative forms
grep -E '(이다|히다|리다|기다)$' input.tsv
```

**Complication**: Not all -이다/-히다 endings are derivations (e.g., 이다 copula, 좋아하다).

**Filter criteria**: Only if base verb exists in dataset.

## Approach 4: Adverb from Adjective

Adverbs derived from adjectives via 히 or 이 suffix.

**Patterns**:
- 형용사 + 히 → 부사: 확실하다 → 확실히
- 형용사 + 이 → 부사: 같다 → 같이

**Note**: Partially covered by word-families.md (하다/히 pairs). This extends to non-하다 adjectives.

**Detection**:
```bash
# Adverbs ending in 히 or 이
grep -E '(히|이)$' input.tsv | grep -v '하다$'
```

## Approach 5: Honorific Pairs

Known pairs where honorific and plain form both exist.

**Known pairs** (finite list):
| Plain | Honorific |
|-------|-----------|
| 먹다 | 드시다 |
| 자다 | 주무시다 |
| 있다 | 계시다 |
| 말하다 | 말씀하시다 |
| 죽다 | 돌아가시다 |

**Detection**: Direct lookup against known list.

**Filter criteria**: If both exist, keep one (probably plain form).

## Approach 6: Noun/Verb Pairs (Sino-Korean)

Many Sino-Korean nouns have corresponding 하다 verbs.

**Pattern**: `X` (noun) + `X하다` (verb)

**Examples**:
- 공부 / 공부하다
- 운동 / 운동하다
- 여행 / 여행하다

**Detection**:
```python
# Find noun/verb pairs
nouns = set(words)
pairs = [(w, w+'하다') for w in nouns if w+'하다' in nouns]
```

**Filter criteria**: Keep verb form only? Or noun only? (Debatable)

## Priority Order

1. **Verb auxiliaries** - Clear pattern, high confidence
2. **Root + compound overlap** - Requires cross-reference
3. **Passive/causative pairs** - Needs base verb check
4. **Noun/verb pairs** - Many exist, decision needed on which to keep
5. **Honorific pairs** - Small fixed list, easy
6. **Adverb derivation** - Partially covered by word-families

## Implementation

Script: `scripts/analyze-redundancy.py`

```bash
# Summary output
python scripts/analyze-redundancy.py output/tmp/korean-all.tsv

# Specific pattern only
python scripts/analyze-redundancy.py output/tmp/korean-all.tsv --pattern 2

# Export to TSV for manual review
python scripts/analyze-redundancy.py output/tmp/korean-all.tsv \
  --tsv output/tmp/redundancy-candidates.tsv
```

Output TSV columns: `family_id, pattern, role, word, english, example_ko, example_en, number`

Family structure - related forms share same `family_id`:
```
30  2_compound  root      감기    cold          감기에 걸렸어요...
30  2_compound  compound  감기약  cold medicine 감기약을 먹었어요...
```

## Analysis Results (2025-12-14)

Dataset: 5,046 words (Korean deck)

| # | Pattern | Count | Notes |
|---|---------|-------|-------|
| 1 | Verb auxiliaries | 29 | Many semantically distinct |
| 2 | Root+compound | 73 | Highest yield |
| 3 | Passive/causative | 21 | Known pairs only |
| 4 | Honorific pairs | 5 | Small fixed list |
| 5 | Noun/verb pairs | 28 | 2+ syllables filter |
| 6 | Adverb derivations | 27 | Overlaps word-families |
| **Total** | | **183** | **3.6%** |

Plus existing word-families (52) = ~235 candidates total.

### Pattern 1: Verb Auxiliaries (29)

**Keep most** - Many have distinct meanings beyond composition:
- 돌아가다 (return) ≠ 돌다 (turn) + 가다 (go)
- 알아보다 (recognize/inquire) ≠ 알다 (know) + 보다 (try)

**Consider removing**:
- 잃어버리다/잊어버리다 - 버리다 just adds "regretfully"
- 들어주다/알아주다 - 주다 just adds "for someone"

### Pattern 2: Root+Compound (73)

**Highest value** - Most are compositional:

Good candidates (meaning = root + suffix):
- 감기약 (cold medicine) = 감기 + 약
- 교통비 (transportation fee) = 교통 + 비
- 관광객/관광지 = 관광 + 객/지

Keep (semantic shift):
- 화장실 (restroom) ≠ 화장 (makeup) + 실 (room)
- 도서관 (library) - 도서 less common than 책

### Pattern 3: Passive/Causative (21)

Uses known-pairs approach (more reliable than regex).
All 21 are valid derivation pairs. Decision: keep base verb only?

Examples:
- 보이다 ← 보다
- 들리다 ← 듣다
- 열리다 ← 열다

### Pattern 4: Honorific Pairs (5)

Small list, all valid:
- 자다/주무시다, 있다/계시다, 보다/뵙다, 주다/드리다, 묻다/여쭙다

Decision: Keep plain form only? Or both for comprehension?

### Pattern 5: Noun/Verb Pairs (28)

Filtered to 2+ syllable nouns (avoids homonym false positives).

**Overlaps with word-families** - 가득/가득하다, 그만/그만하다 etc.

Unique to this pattern:
- 참석/참석하다, 참여/참여하다
- 등록/등록하다, 제출/제출하다

### Pattern 6: Adverb Derivations (27)

**Mostly overlaps with word-families.md** (하다/히 pairs).

Unique finds (이 suffix, 없다 base):
- 똑같이 ← 똑같다
- 정신없이 ← 정신없다
- 틀림없이 ← 틀림없다

## Overlap Analysis

Significant overlap between patterns:
- Pattern 5 + 6 overlap with existing word-families check
- Net new candidates: ~150 (after deduplication)

## Recommendations

1. **Run word-families first** (existing check-word-families.md)
2. **Pattern 2 (compounds)** - Manual review, highest yield
3. **Pattern 3 (passive/causative)** - Clear derivations, safe to filter
4. **Pattern 1 (verb aux)** - Conservative, keep most
5. **Skip patterns 4-6** - Small count or overlaps word-families

## Notes

- Output candidates for manual review (don't auto-delete)
- Track which pattern flagged each word
- Final decision: manual review of flagged candidates
