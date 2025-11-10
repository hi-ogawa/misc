# Find and Fix Bad Example Sentences

## Context
- Input: `input/tmp.tsv` - all TOPIK 1 example sentences (1847 entries)
- Goal: Systematically identify and fix problematic examples
- Output:
  - `output/topik1-examples-bad.tsv` - entries that need fixing
  - `output/topik1-examples-fix.tsv` - corrected versions

## Strategy for Identifying Bad Examples

### Phase 1: Critical Issue - Vocabulary Word Missing Entirely

**Focus**: Identify entries where the vocabulary word from "korean" column does NOT appear in "example_ko" at all (including conjugated or derived forms).

This is the most objective and critical issue to fix first:
- The example sentence must demonstrate the target vocabulary
- According to generate-example3.md requirements:
  - Verbs: must use verb stem in conjugated form (가지다 → 가져요, 가지고, 가진)
  - Adjectives: must use stem in some form (가볍다 → 가벼운, 가벼워요)
  - Nouns: must use the exact noun
  - NEVER substitute with synonyms

**Example of bad entry**:
```
24	가지다	have	돈이 많이 있어요	have a lot of money
```
Problem: "가지다" doesn't appear in example - uses synonym "있다" instead.

### Future Phases (not implemented yet)

Other criteria for "Bad" Examples to address later:

1. **Unnatural Korean**
   - Awkward phrasing that native speakers wouldn't use
   - Overly literal translations from English thinking
   - Missing natural Korean expressions or particles

2. **Translation Issues**
   - English translation doesn't match Korean meaning
   - Missing articles (a, the) in English
   - Broken English (e.g., "go to store often" → "I often go to the store")
   - Overly literal translations that sound unnatural in English

3. **Grammar Errors**
   - Incorrect verb conjugations
   - Missing or wrong particles (이/가, 을/를, 에, etc.)
   - Tense mismatches between Korean and English

4. **TOPIK 1 Level Appropriateness**
   - Too complex grammar for beginners
   - Uses uncommon vocabulary
   - Cultural references that need explanation

### Review Process (Phase 1)

Process input in batches of 100 entries (following project convention).

For each entry:
1. Extract the base word from "korean" column
2. Check if any form of the word appears in "example_ko"
   - For verbs ending in -다: check for stem (remove 다) in any conjugation
   - For adjectives ending in -다: check for stem in any form
   - For nouns: check for exact word
   - For compounds (e.g., 가져가다): check for any part appearing
3. Flag entries where the word is completely missing
4. Generate natural replacement example using the target word

**Important**: Use direct Korean language understanding, NOT scripts.
Process by batches manually to ensure accuracy.

### Output Format

**output/topik1-examples-bad.tsv**
```
number	korean	english	example_ko	example_en	issue
24	가지다	have	돈이 많이 있어요	have a lot of money	Word missing: uses 있다 instead of 가지다
```

**output/topik1-examples-fix.tsv**
```
number	korean	english	example_ko	example_en
24	가지다	have	좋은 생각을 가져요	have a good idea
```

### Detection Examples

**Missing word (synonym used)**:
- Entry: 가지다 → "돈이 많이 있어요" ❌ (uses 있다 instead)
- Fix: "좋은 생각을 가져요" ✓

**Missing word (different expression)**:
- Entry: 걱정하다 → "마음이 불안해요" ❌ (uses 불안하다 instead)
- Fix: "너무 걱정하지 마세요" ✓

**Correct usage (word appears in conjugated form)**:
- Entry: 가지다 → "질문이 있어요" ❌ WAIT - this is different verb 있다
- Entry: 가볍다 → "가벼운 가방을 샀어요" ✓ (가볍- stem present)
- Entry: 가다 → "학교에 먼저 가요" ✓ (가- stem present)

## Implementation Notes

- Input: `input/tmp.tsv` (1847 entries)
- Process in batches of 100 entries (following project convention)
- Use direct Korean language understanding to identify missing words
- Output both bad entries (with issue column) and fixes
- Batch outputs:
  - `output/topik1-examples-bad-1.tsv`, `bad-2.tsv`, etc. (or just one combined file)
  - `output/topik1-examples-fix-1.tsv`, `fix-2.tsv`, etc. (or just one combined file)
- Follow generate-example3.md guidelines when creating fixes
