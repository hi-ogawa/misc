# Find and Fix Bad Example Sentences

## Context
- Input: `input/tmp.tsv` - all TOPIK 1 example sentences (1847 entries)
- Goal: Systematically identify and fix problematic examples
- Output:
  - `output/topik1-examples-bad.tsv` - entries that need fixing
  - `output/topik1-examples-fix.tsv` - corrected versions

## Strategy for Identifying Bad Examples

### Criteria for "Bad" Examples

Review each entry for these issues:

1. **Unnatural Korean**
   - Awkward phrasing that native speakers wouldn't use
   - Overly literal translations from English thinking
   - Missing natural Korean expressions or particles

2. **Translation Issues**
   - English translation doesn't match Korean meaning
   - Missing articles (a, the) in English
   - Broken English (e.g., "go to store often" → "I often go to the store")
   - Overly literal translations that sound unnatural in English

3. **Vocabulary Usage**
   - Example doesn't clearly demonstrate the target word's meaning
   - Target word used incorrectly or in unusual context
   - Better example exists that's more common/clear

4. **Grammar Errors**
   - Incorrect verb conjugations
   - Missing or wrong particles (이/가, 을/를, 에, etc.)
   - Tense mismatches between Korean and English

5. **TOPIK 1 Level Appropriateness**
   - Too complex grammar for beginners
   - Uses uncommon vocabulary
   - Cultural references that need explanation

### Review Process

**Phase 1: Automated Detection**
- Review all entries with AI assistance
- Flag entries matching bad example criteria
- Prioritize common patterns (missing articles, broken English, etc.)

**Phase 2: Manual Review**
- Verify flagged entries
- Identify additional issues missed by automated scan
- Decide which entries truly need fixing vs. acceptable variations

**Phase 3: Generate Fixes**
- Create natural, corrected versions
- Ensure Korean and English both sound natural
- Keep sentences simple and clear for TOPIK 1 level
- Maintain the same vocabulary word being demonstrated

### Output Format

**output/topik1-examples-bad.tsv**
```
number	korean	english	example_ko	example_en	issue
2	가격	price	가격이 너무 비싸요	price is too expensive	Missing article: "the price"
```

**output/topik1-examples-fix.tsv**
```
number	korean	english	example_ko	example_en
2	가격	price	이 가격이 너무 비싸요	This price is too expensive
```

### Common Patterns to Fix

1. **Missing English articles**
   - "go to store" → "go to the store"
   - "price is expensive" → "the price is expensive"

2. **Broken English structure**
   - "meet friend sometimes" → "I sometimes meet my friend"
   - "bought new furniture" → "I bought new furniture"

3. **Unnatural Korean particles**
   - Review particle usage (은/는, 이/가, 을/를)
   - Ensure natural topic/subject marking

4. **Overly simple English**
   - Add subjects where implicit (I, you, it, etc.)
   - Add possessives where appropriate (my, your, etc.)

## Implementation Notes

- Process in batches if needed (e.g., 100 entries at a time)
- Use Claude to review and flag issues
- Keep original structure: number, korean, english, example_ko, example_en
- Document issue type for learning purposes
- Prioritize fixes that improve clarity and naturalness
