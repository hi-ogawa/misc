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

  6. **REGISTER VARIANTS** (formal/written ↔ casual/spoken):
     Words with same meaning but different register (formality level).
     The simpler/casual form is typically TOPIK1 level; the formal/written form is TOPIK2.

     - Adverbs:
       - 얼른 → = 빨리 (formal)
       - 그저 → = 그냥 (written)
       - 요새 → = 요즘 (variant)
       - 한참 → = 오래 (formal)
       - 어쩌면 → = 아마 (formal)
       - 오직 → = 만 (literary)
       - 몹시 → = 매우 (literary)
       - 마침 → = 딱 (written)

     - Connectives/discourse markers:
       - 즉 → = 그러니까 (written)
       - 게다가 → = 그리고 (written)
       - 따라서 → = 그래서 (written)

     Format: `[casual equivalent] ([register])`
     - Register labels: `formal`, `written`, `literary`, `variant`

- **Output format:**
  - Single word: `notes: 하얀색`
  - Multiple words: `notes: 간 (salty), 간격`
  - Register variant: `notes: = 빨리 (formal)`
  - Combined: `notes: = 빨리 (formal), 느리다`
  - No related words: `notes: ` (blank)

- **What NOT to include:**
  - Base/derived verb pairs from inflection (passive, causative, nominalization)
    - ❌ 닫히다 → 닫다 (morphological derivation, not related vocabulary)
    - ❌ 옮기다 → 옮다 (same - causative derivation)
  - Contractions/abbreviations
    - ❌ 게 → 것이, 뭐 → 무엇 (phonological fusion, not related vocabulary)
  - These are structural relationships, not semantic relationships

- **Prioritization:**
  - No strict priority - include all relevant relationships
  - For confusables, provide context in parentheses if needed to distinguish meanings
  - Aim for practical usefulness over completeness
