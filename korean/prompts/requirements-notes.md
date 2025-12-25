Goal: Generate related vocabulary words for the "notes" field to help distinguish and contextualize each vocabulary item.

REQUIREMENTS:
- **Core principle: Provide words that help learners differentiate or understand this word better**
  - Related words should create meaningful connections (semantic, phonetic, or conceptual)
  - Multiple related words can be provided (comma-separated)
  - Leave blank if no meaningful related words exist

- **Relationship types to consider:**

  1. **RELATED MEANINGS** (synonyms, variants, semantic associations):
     - Color variants: 흰색 → 하얀색 (.syn)
     - Action pairs: 배우다 → 가르치다 (.ant)
     - Similar concepts: 가게 → 상점 (.syn)

  2. **ANTONYMS/PAIRS** (opposite or complementary meanings):
     - Descriptive: 높다 → 낮다 (.ant), 무겁다 → 가볍다 (.ant)
     - Directional: 오다 → 가다 (.ant)
     - Relational: 학생 → 선생님 (.ant)
     - Family: 할머니 → 할아버지 (.ant), 아들 → 딸 (.ant)

  3. **HONORIFIC PAIRS** (plain ↔ honorific forms):
     - 있다 → 계시다 (.hon)
     - 먹다 → 드시다 (.hon), 잡수시다 (.hon)
     - 자다 → 주무시다 (.hon)

  4. **HANJA-순우리말 PAIRS** (Sino-Korean ↔ native Korean):
     - 가격 → 값 (.syn:native)
     - 장소 → 곳 (.syn:native)
     - 시간 → 때 (.syn:native)
     - Only include if 순우리말 equivalent is commonly used

  5. **REGISTER VARIANTS** (formal/written ↔ casual/spoken):
     Words with same meaning but different formality level.
     Annotate what register THE RELATED WORD belongs to.
     Often correlates with hanja (formal) vs native Korean (casual).

     Entry (formal/hanja) → related word is casual/native:
     - 오직 → 만 (.syn:casual)
     - 즉시 → 바로 (.syn:casual)
     - 감정 → 기분 (.syn:casual)

     Entry (casual/native) → related word is formal/hanja:
     - 믿음 → 신뢰 (.syn:formal)
     - 외로움 → 고독 (.syn:formal)
     - 주고받다 → 교환하다 (.syn:formal)

- **Output format:**

  Annotate each related word to describe what IT is:

  | Relationship | Tag | Meaning |
  |--------------|-----|---------|
  | Antonym | `(.ant)` | related word is opposite |
  | Synonym | `(.syn)` | related word is synonym |
  | Casual synonym | `(.syn:casual)` | related word is casual/colloquial |
  | Formal synonym | `(.syn:formal)` | related word is formal/written/literary |
  | Native Korean | `(.syn:native)` | related word is 순우리말 |
  | Honorific | `(.hon)` | related word is honorific form |

  - Multiple: `낮다 (.ant), 짧다 (.syn)`
  - No related words: leave blank

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
