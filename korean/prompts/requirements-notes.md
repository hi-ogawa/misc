Goal: Generate related vocabulary words for the "notes" field to help distinguish and contextualize each vocabulary item.

REQUIREMENTS:
- **Core principle: Provide words that help learners differentiate or understand this word better**
  - Related words should create meaningful connections (semantic, phonetic, or conceptual)
  - Multiple related words can be provided (comma-separated)
  - Leave blank if no meaningful related words exist

- **Relationship types to consider:**

  1. **RELATED MEANINGS** (synonyms, variants, semantic associations):
     - Color variants: 흰색 → 하얀색
     - Action pairs: 배우다 → 가르치다
     - Similar concepts: 가게 → 상점

  2. **ANTONYMS/PAIRS** (opposite or complementary meanings):
     - Descriptive: 높다 → 낮다, 무겁다 → 가볍다
     - Directional: 오다 → 가다
     - Relational: 학생 → 선생님
     - Family: 할머니 → 할아버지, 아들 → 딸

  3. **HONORIFIC PAIRS** (plain ↔ honorific forms):
     - 있다 → 계시다
     - 먹다 → 드시다, 잡수시다
     - 자다 → 주무시다

  4. **HANJA-순우리말 PAIRS** (Sino-Korean ↔ native Korean):
     - 가격 (價格) → 값
     - 장소 (場所) → 곳
     - 시간 (時間) → 때
     - Only include if 순우리말 equivalent is commonly used

  5. **CONFUSABLE PAIRS** (easily confused words):
     - Homophones: 간 (liver) → 간 (salty), 간격 (space)
     - Near-homophones: 넣다 (put in) → 놓다 (put down)
     - Similar spellings: 걷다 (walk) → 걸다 (hang), 걸리다 (take time)
     - Phonetic clusters: 굳다 (harden) → 굵다 (thick), 굽다 (bend/bake)

  6. **CONTRACTIONS/ABBREVIATIONS** (full form ↔ shortened form):
     - 것이 ↔ 게
     - 무엇 ↔ 뭐
     - 나는 ↔ 난, 너는 ↔ 넌
     - 것을 ↔ 걸
     - 이것 ↔ 이거, 그것 ↔ 그거, 저것 ↔ 저거
     - 아이 ↔ 애

- **Output format:**
  - Single word: `notes: 하얀색`
  - Multiple words: `notes: 간 (salty), 간격`
  - No related words: `notes: ` (blank)

- **Prioritization:**
  - No strict priority - include all relevant relationships
  - For confusables, provide context in parentheses if needed to distinguish meanings
  - Aim for practical usefulness over completeness
