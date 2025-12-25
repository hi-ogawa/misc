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

  5. **CONFUSABLE PAIRS** (easily confused words):
     - Homophones: 간 (liver) → 간 (.cf), 간격 (.cf)
     - Near-homophones: 넣다 → 놓다 (.cf)
     - Similar spellings: 걷다 → 걸다 (.cf), 걸리다 (.cf)
     - Phonetic clusters: 굳다 → 굵다 (.cf), 굽다 (.cf)

  6. **REGISTER VARIANTS** (formal/written ↔ casual/spoken):
     Words with same meaning but different register (formality level).
     The simpler/casual form is typically TOPIK1 level; the formal/written form is TOPIK2.

     - 얼른 → 빨리 (.syn:formal)
     - 그저 → 그냥 (.syn:written)
     - 요새 → 요즘 (.syn:casual)
     - 한참 → 오래 (.syn:formal)
     - 즉 → 그러니까 (.syn:written)
     - 게다가 → 그리고 (.syn:written)
     - 몹시 → 매우 (.syn:literary)

- **Output format:**

  Use parenthetical tags to indicate relationship type:

  | Type | Tag | Example |
  |------|-----|---------|
  | Antonym | `(.ant)` | `불가능 (.ant)` |
  | Synonym | `(.syn)` | `감추다 (.syn)` |
  | Register (casual) | `(.syn:casual)` | `그런데 (.syn:casual)` |
  | Register (formal) | `(.syn:formal)` | `빨리 (.syn:formal)` |
  | Register (written) | `(.syn:written)` | `그러니까 (.syn:written)` |
  | Register (literary) | `(.syn:literary)` | `매우 (.syn:literary)` |
  | Hanja-native | `(.syn:native)` | `값 (.syn:native)` |
  | Honorific | `(.hon)` | `드시다 (.hon)` |
  | Confusable | `(.cf)` | `놓다 (.cf)` |

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
