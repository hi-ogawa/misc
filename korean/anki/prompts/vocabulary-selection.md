# TOPIK 2 Vocabulary Selection Analysis

**Goal**: Assess vocabulary selection quality and identify remaining redundancy.

## Previous Curation Passes

| Pass | Target | Removed | Reference |
|------|--------|---------|-----------|
| 1+2 | Trivial loanwords, compositional compounds | 515 (13.3%) | `prompts/koreantopik2/plan-curation.md` |
| 3 | TOPIK 1 duplicates | 177 | `prompts/koreantopik2/plan.md` |
| 4 | Sino-Korean word families (하다/히/되다) | 41 | `anki/prompts/check-word-families.md` |

**Current deck**: 3,102 active cards (36 suspended by user during study)

## Current Analysis (2024-12-20)

### Sample: Next 300 Upcoming Cards (score 082-078)

| Pattern | Examples | Found | Removable |
|---------|----------|-------|-----------|
| Synonym pairs | 한국말/한국어, 더구나/더욱이, 대체/대체로 | 6 | 3 |
| Formal/informal | 마음껏/맘껏 | 2 | 1 |
| Directional pairs | 다가가다/오다, 달려가다/오다, 빠져나가다/오다 | 6 | 3 |
| Stay up cluster | 밤새/밤새다/밤새우다 | 3 | 2 |
| Interjections | 하하, 아하, 앗 | 3 | 3 |
| -적 adjective | 감동/감동적 | 2 | 1 |

**Sample result**: ~13 removable / 300 = ~4.3%

### Observations

1. **Cannot extrapolate uniformly** - Interjections (하하, 아하, 앗) cluster at score 078. Redundancy patterns may concentrate at certain score bands rather than distribute evenly.

2. **Patterns not caught by previous passes**:
   - Synonym clusters (different words, same meaning)
   - Formal/informal variants
   - Directional verb pairs (-가다/-오다)
   - Low-value interjections

3. **Score distribution hypothesis**: Lower-scored cards may be cleaner individual vocabulary items. Higher scores may have grouped "common but redundant" words together.

## Redundancy Patterns (Candidates for Next Pass)

### 1. Synonym Clusters
Same meaning, different words. Keep 1-2, suspend rest.

```
한국말 / 한국어 → keep 한국어
더구나 / 더욱이 → keep one
대체 / 대체로 → keep 대체로
```

### 2. Formal/Informal Variants
Same word, different register. Keep formal.

```
마음껏 / 맘껏 → keep 마음껏
```

### 3. Directional Verb Pairs
Base + 가다/오다. Predictable once base is known.

```
다가가다 / 다가오다 → keep 다가가다
달려가다 / 달려오다 → keep 달려가다
빠져나가다 / 빠져나오다 → keep 빠져나가다
```

### 4. Interjections
Low learning value.

```
하하, 아하, 앗 → suspend all
```

### 5. Noun + -적 Adjective Pairs
Similar to 하다/히 pattern but not caught by word-families pass.

```
감동 / 감동적 → keep 감동
일반 / 일반적 → keep 일반
```

### 6. Related Word Clusters
Multiple entries for one concept.

```
밤새 / 밤새다 / 밤새우다 → keep 밤새다
```

### 7. Too Basic for TOPIK 2
Words that slipped through curation but are TOPIK 1 level or earlier. Suspend manually when encountered.

```
한국어, 한국말 - known from day one
과학, 수학 - basic school subjects
마늘 - common food
부모 - basic family term
```

### 8. Emphatic/Formal Variants of Basic Words
TOPIK 2 words that are just "fancier" versions of TOPIK 1 vocabulary.

| TOPIK 2 | Basic alternative | Value |
|---------|-------------------|-------|
| 너무나 | 너무 | Low - just emphatic |
| 정말로 | 정말 | Low - just emphatic |
| 또한 | 도, 그리고 | Medium - formal writing |
| 오직 | 만 | Medium - literary |
| 마치 | 처럼 | Medium - literary |
| 게다가 | 그리고 | High - TOPIK essay |
| 따라서 | 그래서 | High - TOPIK essay |
| 즉 | - | High - TOPIK essay |

**Assessment**:
- Low value (너무나, 정말로): Suspend - adds nothing
- Medium/High value (따라서, 게다가, 즉): Keep - useful for reading/essays

## High Priority: Native Korean Verbs (순우리말 동사)

These are **irreplaceable** vocabulary - no Hanja to guess from, no simpler alternative to fall back on. Must learn to produce.

### From sample (cards 301-600)

| Verb | Meaning | Notes |
|------|---------|-------|
| 겪다 | experience | distinct from 경험하다 |
| 견디다 | endure | no alternative |
| 깨닫다 | realize | distinct from 알다 |
| 담다 | put into | common action |
| 맡다 | take charge | no alternative |
| 다루다 | handle, deal with | no alternative |
| 다투다 | quarrel | can't guess |
| 망설이다 | hesitate | no alternative |
| 망치다 | ruin, spoil | can't guess |
| 밟다 | step on | can't guess |
| 속다 | get deceived | can't guess |
| 아끼다 | cherish, save | unique meaning |
| 겨우 | barely | adverb, no alternative |
| 꽤 | fairly, quite | adverb, no alternative |

### Why prioritize

1. **No Hanja help** - Sino-Korean words (한자어) can often be guessed if you know Chinese/Japanese. Native Korean cannot.
2. **No fallback** - Unlike 따라서→그래서, there's no simpler way to say 망설이다.
3. **Production gap** - You may understand from context, but can't produce without learning.

### Contrast with low-priority

| Type | Example | Why lower priority |
|------|---------|-------------------|
| Emphatic variant | 너무나 | Can use 너무 |
| Formal connective | 따라서 | Can use 그래서 |
| Sino-Korean | 가능성 | Hanja helps: 可能性 |

### Implication

Focus study time on native Korean verbs/adverbs. Let Sino-Korean and formal variants come naturally through exposure.

## Next Steps

- [ ] Sample from different score bands to verify distribution hypothesis
- [ ] Build comprehensive list of candidates across full deck
- [ ] Document decision criteria for each pattern
- [ ] Execute suspension pass

## Score Band Samples (TODO)

| Range | Cards | Score | Redundancy % |
|-------|-------|-------|--------------|
| 1-300 | reviewed | 092-082 | (user suspended ~36) |
| 301-600 | upcoming | 082-078 | ~4.3% (13/300) |
| 500-600 | TODO | ~075 | ? |
| 1000-1100 | TODO | ~070 | ? |
| 2000-2100 | TODO | ~060 | ? |
