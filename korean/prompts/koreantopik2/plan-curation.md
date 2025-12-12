# TOPIK 2 Vocabulary Curation Plan

**Goal**: Filter 3,873 TOPIK 2 words down to ~1,000 high-value vocabulary items.

**Status**: 🚧 Planning phase

## Problem Statement

The raw koreantopik.com TOPIK 2 list (3,873 words) contains:

1. **Trivial English loanwords** - Zero learning value for English speakers
   - Examples: 토마토, 테니스, 아이스크림, 콜라, 케이크
   - Already known; just Hangul spelling recognition

2. **Redundant compositional compounds** - Predictable from roots
   - Examples: 감기 → 감기약, 관광 → 관광객 → 관광지
   - If you know roots + suffixes, compounds are derivable
   - Example sentences naturally teach compounds anyway

## Filtering Strategy

### Pass 1: Trivial Loanword Removal (Automatic)

**Criteria**: Remove words where English → Korean is phonetically obvious.

**Approach**:
- Romanize Korean word
- Compare to common English words
- Flag if similarity > threshold

**Exceptions to keep**:
- Loanwords with shifted meaning (아르바이트 = part-time job, not "work")
- Loanwords with Korean-specific usage patterns
- Loanwords where Korean pronunciation differs significantly

**Implementation**: `scripts/filter-loanwords.py`

### Pass 2: Compositional Compound Removal (Semi-automatic)

**Criteria**: Keep root words, remove predictable derivatives.

**Approach**:
- Morphological analysis (Korean NLP tools)
- Identify N-morpheme compounds
- Check if meaning = sum of parts
- Keep root, skip derivatives

**Exceptions to keep**:
- High-frequency compounds that function as semantic units
- Compounds with non-compositional meaning (생일 ≠ 생 + 일)
- Idiomatic compounds

**Implementation**: `scripts/filter-compounds.py`

### Pass 3: Duplicate Removal (Automatic)

**Criteria**: Remove words already in existing Anki decks (TOPIK 1, etc.)

**Approach**:
- Export existing deck's `korean` field (see `anki/prompts/check-duplicates.md`)
- Filter out exact matches from TOPIK 2 list
- Handle homonyms carefully (same korean, different english = keep)

**Note**: 105 words overlap between TOPIK 1 and TOPIK 2 per existing documentation.

**Implementation**: `scripts/filter-duplicates.py`

### Pass 4: Frequency Validation (Automatic)

**Criteria**: Prioritize words by real-world usage frequency.

**Data sources**:
- 국립국어원 (National Institute of Korean Language) Sejong Corpus
- Korean subtitle frequency lists
- "A Frequency Dictionary of Korean" (Routledge)

**Approach**:
- Cross-reference filtered words with frequency rankings
- Sort by actual usage
- Keep top 1,000-1,500

**Implementation**: `scripts/filter-by-frequency.py`

## Pipeline

```
input/koreantopik2.tsv (3,873 words)
    │
    ▼
[Pass 1: Loanword filter]
    │
    ▼
[Pass 2: Compound filter]
    │
    ▼
[Pass 3: Duplicate filter (vs existing Anki decks)]
    │
    ▼
[Pass 4: Frequency ranking]
    │
    ▼
output/koreantopik2-curated.tsv (~1,000 words)
```

## Output

**Target**: ~1,000 high-value words with:
- Core Korean vocabulary (not transparent loanwords)
- Root words or non-compositional compounds
- High frequency in actual usage
- Genuine learning value (new concept/pattern/collocation)

## Next Steps

1. [ ] Export existing Anki deck korean fields for duplicate detection
2. [ ] Find/download Korean frequency data (국립국어원 or alternative)
3. [ ] Prototype loanword detection heuristic
4. [ ] Test on sample of TOPIK 2 words
5. [ ] Iterate filters based on results
6. [ ] Generate curated list
7. [ ] Run through existing enhancement pipeline (etymology, examples, notes, audio)

## Open Questions

- What frequency threshold to use?
- How to handle borderline loanwords (partially shifted meaning)?
- How to handle homonyms in duplicate filtering (same korean, different meaning)?
- Manual review step for edge cases?

## Resources

- koreantopik.com TOPIK 2 source: https://www.koreantopik.com/2024/09/complete-topik-2-vocabulary-list-3900.html
- 국립국어원: https://www.korean.go.kr/
- Korean morphological analyzers: KoNLPy, Mecab-ko
