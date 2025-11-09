I have a Korean vocabulary TSV with the following columns:
number, todo, ok, korean, hanja, japanese, english, example_ko, example_en

## CRITICAL RULES:
1. ALL examples must be at least 2 words: [subject/object] + [verb/adjective in -요 form]
2. Use 현재형 (-요 form), NEVER 기본형 (-다 form)
3. Output ONLY 3 columns: number, example_ko, example_en

## Three types of conversions:

### TYPE A: Single-word
**Identification:** example_ko is just a single word without a verb

**Action:** Generate a NEW 2-3 word phrase using the korean word
- Format: [korean word][particle][simple verb/adjective in -요 form]
- Choose natural, contextual verbs

**Examples:**
- 가수 → "가수가 불러요" (singer sings)
- 개 → "개가 짖어요" (dog barks)
- 가을 → "가을이 와요" (autumn comes)

### TYPE B: Phrases ending in -다 form
**Identification:** example_ko ends with -다

**Action:** Convert the final verb/adjective from -다 to -요 form
- Keep everything before the verb unchanged
- Apply irregular conjugation rules

**Examples:**
- "가게에 가다" → "가게에 가요"
- "거리가 가깝다" → "거리가 가까워요" (ㅂ irregular)
- "그림을 걷다" → "그림을 걸어요" (ㄷ irregular)

### TYPE C: Already complete phrases
**Identification:** Multi-word phrase that does NOT end in -다

**Action:** KEEP EXACTLY AS IS

**Pattern recognition:**
- Modifying forms ending in -ㄴ/은/는: "간단한 설명", "게으른 사람"
- Noun phrases with counters: "사과 한 개", "몇 가지"
- Nominalizers ending in -ㄹ 것: "먹을 것"
- Multi-word compounds: "컴퓨터 게임", "안과 겉"

## Process for each row:
1. **Identify the type:**
   - Does it end in -다? → TYPE B
   - Is it a single-word category label? → TYPE A
   - Is it already a natural phrase (not ending in -다)? → TYPE C

2. **Apply the conversion:**
   - TYPE A: Create new 2-word phrase
   - TYPE B: Convert -다 to -요
   - TYPE C: Keep unchanged

3. **Update example_en:** Keep it simple, 2-3 words matching the Korean

4. **Verify:** ALL results must have at least 2 words in example_ko

## Common mistakes to AVOID:
❌ Creating 1-word examples → ✓ Always use 2+ words
❌ Changing TYPE C phrases → ✓ Keep multi-word non-다 phrases as-is
❌ Wrong irregular conjugation → ✓ 가깝다 → 가까워요 (NOT 가깝어요)

---

## Task execution:

**Input:** input/test.tsv
**Output:** output/test-examples.tsv

**Output format:** TSV with 3 columns (tab-separated):
```
number	example_ko	example_en
1	가게에 가요	go to store
2	가격이 비싸요	price is expensive
```

## IMPORTANT NOTES:
1. **Do NOT write Python code or scripts** - This is a language/translation task
2. **Process directly** - Use your Korean language understanding to convert each row
3. **Output only 3 columns** - Do NOT copy korean, hanja, japanese, english columns
4. **Preserve row numbers** - Keep the same number from input
5. **Use tabs** - Separate columns with tabs, not spaces
6. **All examples must be 2+ words** - Single-word phrases are not acceptable
