# TOPIK 2 Vocabulary Curation Plan

**Goal**: Filter 3,873 TOPIK 2 words down to ~1,000 high-value vocabulary items.

**Status**: ✅ Pass 1+2 complete (LLM tagging)

## Problem Statement

The raw koreantopik.com TOPIK 2 list (3,873 words) contains:

1. **Trivial English loanwords** - Zero learning value for English speakers
   - Examples: 토마토, 테니스, 아이스크림, 콜라, 케이크
   - Already known; just Hangul spelling recognition

2. **Redundant compositional compounds** - Predictable from roots
   - Examples: 감기 → 감기약, 관광 → 관광객 → 관광지
   - If you know roots + suffixes, compounds are derivable
   - Example sentences naturally teach compounds anyway

## Approach: LLM-based Tagging via Subagents

Similar to etymology generation, use subagents to tag each entry with pattern type.
This is more accurate than script-based heuristics for Korean linguistic analysis.

**Reference**: Pattern categories align with `prompts/requirements-etymology.md` types 4 (compounds) and 5 (loanwords).

### Categories

Each word gets tagged with one category number (from `prompts/requirements-etymology.md`):

| Cat | Name | Description |
|-----|------|-------------|
| 1 | sino-korean | Hanja-based vocabulary (희망, 학생) |
| 2 | auxiliary-compound | Verb + auxiliary (가져가다, 먹어보다) |
| 3 | derivation | Passive/causative/nominalization (보이다 ← 보다) |
| 4 | compound | Native compound (눈물, 감기약) |
| 5 | loanword | Borrowed from other languages (토마토, 아르바이트) |
| 6 | contraction | Shortened form (뭐 ← 무엇) |
| 7 | native | Pure Korean, no etymology (가다, 먹다) |

### Filter Column

LLM determines `filter` value directly based on:

| filter | When to use |
|--------|-------------|
| `yes` | Trivial loanword (meaning identical to English) |
| `yes` | Compositional compound/derivation (meaning = sum of parts, root is common) |
| `no` | Shifted loanword (Korean usage differs) |
| `no` | Semantic compound (idiomatic meaning) |
| `no` | Root word itself |
| `no` | All other cases |

### Tagging Output Format

```tsv
number	korean	english	etymology	root	category	filter
1	토마토	tomato	tomato		5	yes
2	감기약	cold medicine	감기 + 藥	감기	4	yes
3	아르바이트	part-time job	アルバイト / Arbeit		5	no
4	생각하다	to think	思考		1	no
5	눈물	tears	눈 + 물		4	no
6	가다	to go			7	no
19	가만	just as it is			7	no
20	가만있다	remain still	가만 + 있다	가만	4	yes
21	가만히	still	가만 + 히	가만	3	yes
```

**Columns**:
- `etymology`: Following `prompts/requirements-etymology.md` format
- `root`: Primary root word (for categories 2, 3, 4)
- `category`: 1-7 (clean numbers, no a/b variants)
- `filter`: `yes` or `no` (LLM determines directly)

**Benefits**:
- Etymology generated in same pass (no separate etymology generation needed)
- Filter decision made by LLM with full context (not post-hoc rule)
- Simple filter logic: `filter = yes` → remove

### Tagging Criteria

**Filter YES (loanword-trivial)**:
- English speaker already knows the meaning
- Korean pronunciation ≈ English pronunciation
- No Korean-specific usage pattern
- Examples: 토마토, 테니스, 아이스크림, 콜라, 케이크, 버스, 택시

**Filter NO (loanword-shifted)**:
- Meaning differs from source language
- Korean-specific usage
- Examples: 아르바이트 (part-time job, not general "work"), 핸드폰 (mobile phone)

**Filter YES (compound-compositional)**:
- Meaning = sum of parts
- Root word is in the list OR common TOPIK 1 vocabulary
- Examples: 감기약 (감기+약), 관광객 (관광+객), 관광지 (관광+지)

**Filter NO (compound-semantic)**:
- Meaning is idiomatic or non-obvious
- Examples: 생일 (birthday, not just "birth+day"), 눈물 (tears, specific meaning)

## Pipeline

```
input/koreantopik2.tsv (3,873 words)
    │
    ▼
[Pass 1+2: LLM tagging (loanword + compound patterns)]
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

### Pass 1+2: LLM Tagging (Combined)

**Execution**: Subagents process batches (same as etymology generation)
- Input: `input/koreantopik2-batch-{1..39}.tsv`
- Output: `output/koreantopik2/curation-{1..39}.tsv`

**Subagent prompt**:

````
Generate curation tags for Korean vocabulary batch N.

## Task

Read `input/koreantopik2-batch-N.tsv` and generate `output/koreantopik2/curation-N.tsv`.

## CRITICAL: File Access Rules

**ONLY read these files:**
- `input/koreantopik2-batch-N.tsv` (your assigned batch)
- `prompts/requirements-etymology.md` (etymology format reference)

**DO NOT read any other files**, especially:
- Any files in `output/` directory
- Other batch files
- Any existing curation files

Generate from scratch based only on the input batch and requirements.

## Input Format

TSV with columns: number, korean, english

## Output Format

TSV with columns: number, korean, english, etymology, root, category, filter

Example output:
```tsv
number	korean	english	etymology	root	category	filter
1	토마토	tomato	tomato		5	yes
2	감기약	cold medicine	감기 + 藥	감기	4	yes
3	아르바이트	part-time job	アルバイト / Arbeit		5	no
4	생각하다	to think	思考		1	no
5	눈물	tears	눈 + 물		4	no
6	가다	to go			7	no
```

**IMPORTANT**: Use numeric category (1-7), NOT text names.

## Etymology Format

Follow `prompts/requirements-etymology.md` format:
- Sino-Korean: Show Hanja (希望, 學生 / 学生)
- Compounds: Show roots (눈 + 물, 감기 + 藥)
- Loanwords: Show source (tomato, アルバイト / Arbeit)
- Derivations: Show base + suffix (보다 + 이 (passive))
- Native words with no etymology: leave blank

## Root Column

For categories 2, 3, 4: Extract the primary root word.
- 감기약 → root: 감기
- 가만있다 → root: 가만
- 가만히 → root: 가만
- 보이다 → root: 보다
- 가져가다 → root: 가지다

Leave blank for categories 1, 5, 6, 7.

## Categories (from requirements-etymology.md)

Assign exactly ONE category per entry:

| Cat | Name | When to use |
|-----|------|-------------|
| 1 | sino-korean | Hanja-based vocabulary (희망, 학생, 가능) |
| 2 | auxiliary-compound | Verb + auxiliary verb (가져가다, 먹어보다, 잊어버리다) |
| 3 | derivation | Passive/causative/nominalization (보이다, 먹이다, 걸음) |
| 4 | compound | Native/hybrid compound (눈물, 감기약, 가만있다) |
| 5 | loanword | Borrowed from other languages (토마토, 아르바이트) |
| 6 | contraction | Shortened form (뭐, 난, 걸) |
| 7 | native | Pure Korean, no clear etymology (가다, 먹다, 예쁘다) |

## Filter Column

Determine `filter` value directly:

| filter | When to use |
|--------|-------------|
| `yes` | Trivial loanword - meaning identical to English (토마토, 버스) |
| `yes` | Compositional - meaning = sum of parts, root is common (감기약, 가만있다) |
| `no` | Shifted loanword - Korean usage differs (아르바이트, 핸드폰) |
| `no` | Semantic compound - idiomatic meaning (눈물, 생일) |
| `no` | Root word itself (감기, 가만, 보다) |
| `no` | All other cases (sino-korean, native, contraction) |

## Guidelines

1. **Default to `filter=no` (keep the word)**:
   - Only use `filter=yes` when confident the word has low learning value
   - Loanwords: only filter if meaning is truly identical to English
   - Compounds/derivations: only filter if meaning is obviously predictable from parts
   - When uncertain → `filter=no`

2. Always extract root for categories 2, 3, 4:
   - Use the base form (dictionary form for verbs)

3. Err on the side of keeping words - we can always filter more later, but missing good words is worse.

## Process

1. Read `input/koreantopik2-batch-N.tsv`
2. For each entry: determine etymology, root, category, and filter
3. Write all entries to `output/koreantopik2/curation-N.tsv`
````

### Pass 1+2 Results

**Completed**: 2025-12-12

**Output files**:
- `output/koreantopik2/curation-{1..39}.tsv` (batch files)
- `output/koreantopik2/curation-all.tsv` (consolidated, 3,873 entries)

**Filter distribution**:
| filter | count | % |
|--------|-------|---|
| yes | 515 | 13.3% |
| no | 3,358 | 86.7% |

**Category distribution**:
| category | count | % |
|----------|-------|---|
| 1 sino-korean | 2,052 | 53% |
| 7 native | 749 | 19% |
| 4 compound | 513 | 13% |
| 3 derivation | 199 | 5% |
| 2 auxiliary-compound | 191 | 5% |
| 5 loanword | 160 | 4% |
| 6 contraction | 9 | <1% |

**Notes**:
- Categories normalized to numeric (1-7) in curation-all.tsv
- ~13% filtered is reasonable - keeps 3,358 words before duplicate/frequency filtering

### Pass 3: Duplicate Removal

**Criteria**: Remove words already in existing Anki decks (TOPIK 1, etc.)

**Approach**:
- Export existing deck's `korean` field (see `anki/prompts/check-duplicates.md`)
- Filter out exact matches from curated list
- Handle homonyms carefully (same korean, different english = keep)

**Note**: 105 words overlap between TOPIK 1 and TOPIK 2 per existing documentation.

### Pass 4: Frequency Validation

**Criteria**: Prioritize remaining words by real-world usage frequency.

**Data sources** (to investigate):
- 국립국어원 (National Institute of Korean Language) Sejong Corpus
- Korean subtitle frequency lists
- "A Frequency Dictionary of Korean" (Routledge)

**Approach**:
- Cross-reference filtered words with frequency rankings
- Sort by actual usage
- Keep top 1,000-1,500

## Output

**Target**: ~1,000 high-value words with:
- Core Korean vocabulary (not transparent loanwords)
- Root words or non-compositional compounds
- High frequency in actual usage
- Genuine learning value (new concept/pattern/collocation)

## Next Steps

1. [x] Run sample batch through LLM tagging to validate categories
2. [x] Review distribution of patterns (how many filter=yes?)
3. [x] Iterate tagging criteria based on results
4. [x] Run full tagging (39 batches)
5. [x] Fix parsing issues (batch 26 had extra tab, batch 39 had ideographic spaces)
6. [x] Normalize category column (text → numeric in curation-all.tsv)
7. [ ] Export existing Anki deck for duplicate detection
8. [ ] Apply duplicate filter (Pass 3)
9. [ ] Find/download Korean frequency data
10. [ ] Apply frequency filter (Pass 4)
11. [ ] Generate final curated list
12. [ ] Run through enhancement pipeline (examples, notes, audio)

## Open Questions

- ~~Is the pattern taxonomy complete? Missing categories?~~ → Yes, 7 categories sufficient
- ~~How strict on compound-compositional?~~ → ~13% filter rate seems reasonable
- Frequency data source - which is most accessible?
- Target word count: With ~3,365 after Pass 1+2, need Pass 3+4 to reach ~1,000-1,500

## Resources

- koreantopik.com TOPIK 2 source: https://www.koreantopik.com/2024/09/complete-topik-2-vocabulary-list-3900.html
- 국립국어원: https://www.korean.go.kr/
- Etymology patterns: `prompts/requirements-etymology.md`
