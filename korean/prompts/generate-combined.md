# Generate Combined Enhancements for TOPIK 2 Batch

Process a single batch of 100 words through all enhancement types: etymology, examples, and notes.

## Batch Range
**TODO: Specify your batch range before running**
- Batch number: `__BATCH__` (e.g., 1, 2, 3, ..., 39)
- Word range: `__START__` to `__END__` (e.g., 1-100, 101-200, ..., 3801-3900)

Example: For batch 5, set `__BATCH__=5`, `__START__=401`, `__END__=500`

## Input
- Source: `input/korean_english_2.tsv`
- Format: number, korean, english (tab-separated)
- Extract only lines for the specified range

## Output
Generate a single combined TSV file for this batch:
- `output/topik2-combined-__BATCH__.tsv`

**Format** (7 columns, tab-separated):
```
number	korean	english	etymology	example_ko	example_en	notes
```

Each row contains all enhancements for one word, keeping semantically related data together.

## Task 1: Etymology

Generate etymology column showing word origins and derivations.

### Types to Include:

**1. SINO-KOREAN (한자어 / 日本漢字):**
- 희망 → "希望"
- 학생 → "學生 / 学生"
- 가격 → "價格 / 価格"

IMPORTANT: Always show BOTH traditional Chinese and Japanese kanji when they differ.

**2. DERIVATIONS (파생어):**
- 가져가다 → "가지다 + 가다"
- 걸어가다 → "걷다 + 가다"

**3. COMPOUNDS (합성어):**
- 눈물 → "눈 + 물"
- 손가락 → "손 + 가락"
- 강아지 → "개 + 아지" (use original root before sound change)

**4. LOANWORDS:**
- 컴퓨터 → "computer"
- 아르바이트 → "アルバイト / Arbeit"

SKIP: Pure Korean words with no clear etymology

**Output format**: number, korean, etymology (tab-separated)
Leave etymology blank if no clear etymology.

## Task 2: Example Sentences

Generate natural example sentences for each entry.

### Requirements:
- **CRITICAL: Example MUST contain the vocabulary word**
  - Verbs: use conjugated form (e.g., 가다 → 가요, 가지고)
  - Adjectives: use natural form (e.g., 가볍다 → 가벼운, 가벼워요)
  - Nouns: use the exact noun (e.g., 가족 → 가족이랑)
- Avoid single-word examples (at least 2 content words)
- Prefer complete sentences over phrases
- Keep minimal: 3-4 words ideal
- **ALWAYS include particles explicitly** (가/이, 는/은, 를/을, 에, 에서, etc.)

### Examples:
- 가다 → "학교에 먼저 가요" (go to school first)
- 가볍다 → "가벼운 가방을 샀어요" (bought a light bag)
- 가족 → "가족이랑 살아요" (live with family)

**Output format**: number, korean, example_ko, example_en (tab-separated)

## Task 3: Notes

Generate a single related word for each entry.

### Relationship Types:

**1. RELATED MEANINGS (synonyms, variants):**
- 흰색 → 하얀색
- 검은색 → 까만색

**2. ANTONYMS:**
- 높다 → 낮다
- 무겁다 → 가볍다
- 오다 → 가다

**3. FAMILY/PEOPLE PAIRS:**
- 할머니 → 할아버지
- 아들 → 딸

**4. HONORIFIC PAIRS:**
- 있다 → 계시다
- 먹다 → 드시다

**Output format**: number, korean, notes (tab-separated)
Leave notes blank if no related words.

## Execution Instructions

1. Read `input/korean_english_2.tsv`
2. Extract lines __START__ to __END__ (the specified batch)
3. For each word, generate all enhancements:
   - Etymology (or blank if none)
   - Example sentence (Korean + English)
   - Notes (related word, or blank if none)
4. Write single combined TSV file: `output/topik2-combined-__BATCH__.tsv`
   - Header: `number	korean	english	etymology	example_ko	example_en	notes`
   - One row per word with all 7 columns
   - Proper TSV escaping for all fields
5. Validate output:
   - File should have exactly 100 entries (except batch 39 with 100 entries)
   - All rows have 7 columns
   - No missing line numbers in sequence

## Important Notes

- Process directly using Korean language understanding (no scripting)
- Use proper CSV/TSV escaping for fields with tabs or special characters
- Leave fields blank when no information available (don't force content)
- Each batch is independent - no need to reference other batches

---

**Status**: Ready to process batch __BATCH__ (words __START__-__END__)
