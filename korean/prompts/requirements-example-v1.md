# Example Sentence Requirements - Version 1 (Original)

**Note**: This is the original version, preserved for documentation. See `requirements-example.md` for current version.

---

I have a Korean vocabulary list in TSV format.
Columns: number, korean, english

Your task: Generate natural example sentences for each entry.

REQUIREMENTS:
- **CRITICAL: The example sentence MUST contain the vocabulary word from the "korean" column**
  - For verbs: use the verb stem in conjugated form (e.g., 가지다 → 가져요, 가지고, 가진)
  - For adjectives: use the stem in any natural form (e.g., 가볍다 → 가벼운, 가벼워요)
  - For nouns: use the exact noun (e.g., 가족 → 가족이랑)
  - NEVER substitute with synonyms or different words
- Avoid single-word examples (must have at least 2 distinct content words, not counting particles)
- Prefer complete sentences over noun phrases
- Keep sentences minimal: 3-4 words is ideal
- Show natural, common usage
- **ALWAYS include particles (가/이, 는/은, 를/을, etc.) explicitly for learning purposes**
  - Subject particles: 이/가
  - Topic particles: 은/는
  - Object particles: 을/를
  - Location particles: 에, 에서, (으)로, etc.
- Use modifying forms when the vocabulary word (especially adjectives) is more naturally used that way
  - Example: 가볍다 → "가벼운 가방을 샀어요" (not "가방이 가벼워요")
  - Example: 강하다 → "강한 바람이 불어요" (not "바람이 강해요")
- For verbs that are primarily used in action contexts, use -요 forms in complete sentences
  - Example: 가다 → "학교에 먼저 가요"
  - Example: 가르치다 → "영어를 가르쳐 주세요"
- For nouns, create natural contexts showing typical usage
  - Example: 가족 → "가족이랑 살아요"
  - Example: 강아지 → "강아지가 너무 귀여워요"

Guidelines for word types:
- **Adjectives**: Often better with modifying form + noun + verb
- **Verbs**: Use in natural sentence contexts with objects/locations
- **Nouns**: Show in typical usage contexts
- **Adverbs**: Use within natural sentences
- **Colors/descriptive nouns**: Use as modifiers in phrases

Examples:
- 가다 → "학교에 먼저 가요" (go to school first)
- 가볍다 → "가벼운 가방을 샀어요" (bought a light bag)
- 간단하다 → "간단한 질문이 있어요" (have a simple question)
- 가족 → "가족이랑 살아요" (live with family)
- 갈색 → "갈색 신발을 샀어요" (bought brown shoes)
- 강하다 → "강한 바람이 불어요" (strong wind is blowing)
- 가지다 → "좋은 생각을 가져요" (have a good idea) - NOT "좋은 생각이 있어요"

Output ONLY: number, korean, example_ko, example_en (tab-separated)

Process input by batches of 100 entries.
Input: input/korean-english.tsv (all entries)
Output:
   output/examples-1.tsv (first 1-100)
   output/examples-2.tsv (next 101-200)
   ...
   output/examples-19.tsv (last 1801-1847)

IMPORTANT: Generate the most natural, commonly-used phrase for each word. Process directly using Korean language understanding and avoid script-based automation.
