# Language Learning Framework & Philosophy

Personal notes on language learning approaches and the rationale behind this project's design.

## The Problem with Existing Frameworks

### Traditional Vocabulary Lists (TOPIK, textbooks)
- Organized by test level, not actual usage/frequency
- Treat morphological variants as separate entries (가능/가능하다/가능성)
- Often include specialized/academic words to hit target counts
- Missing high-frequency colloquial words
- **Good for**: Passing specific tests
- **Bad for**: Natural acquisition, practical communication

### Frequency-Based Lists
- Corpus-driven (e.g., top 5000 most common words)
- Better alignment with real usage
- **Problem**: Still treats words as atomic units, ignores morphology
- Examples: Anki frequency decks, various "most common words" lists

### Textbook Progression
- Thematic organization (food, travel, weather)
- Grammar-driven (introduce words needed for grammar points)
- Often arbitrary ordering within themes
- **Good for**: Structured classroom learning
- **Bad for**: Self-directed learners, optimizing for efficiency

### Input-Based Approaches (Comprehensible Input / Krashen)
- Learn through massive exposure to understandable content
- Vocabulary emerges naturally from context
- No explicit "lists" - you acquire what you need when you need it
- **Good for**: Natural acquisition, long-term retention
- **Bad for**: Slow initial progress, requires lots of content at right level

### Sentence Mining (AJATT, Refold, etc.)
- Extract sentences from real content you're consuming
- Learn words in context, not isolation
- Build deck from your actual media exposure
- **Good for**: Contextual learning, motivation (content you care about)
- **Bad for**: Inefficient (might encounter rare words before common ones)

## This Project's Approach

**Hybrid philosophy**: Start with test-prep list, but fix its flaws.

### Core Principles

1. **Use TOPIK as scaffold**
   - Provides structure and curriculum
   - Aligned to standardized proficiency test
   - Widely recognized benchmark
   - BUT: Don't trust the ordering blindly

2. **Add contextual richness**
   - Etymology (Hanja, Japanese cognates) - connects to prior knowledge
   - Example sentences - demonstrate actual usage
   - Audio - pronunciation reference
   - Study notes - mnemonics and usage tips

3. **Re-prioritize by utility**
   - Score vocabulary by value for TOPIK 1 graduate
   - Identify "missing links" (high-frequency words naturally used in beginner contexts)
   - Filter out specialized/low-frequency words
   - See: `prompts/koreantopik2/generate-score.md`

4. **Acknowledge morphological families**
   - Treat related forms (가능/가능하다/가능성) as learning units
   - Score families identically
   - Avoid false sense of progress from trivial derivations

5. **Optimize for comprehensible input**
   - Example sentences follow i+1 principle
   - Grammar should be within TOPIK 1 knowledge
   - Target vocabulary is the "+1", not grammar complexity
   - See: `prompts/research-sentence-complexity.md`

### What This Optimizes For

- **Goal**: Practical Korean usage (reading, listening, conversation)
- **Prior knowledge**: TOPIK 1 vocabulary (~1850 words)
- **Time constraint**: Self-study with Anki (20-30 cards/day)
- **Learning style**: Explicit study (flashcards) + input (media consumption)
- **Motivation**: Intrinsic interest in Korean media/culture

### What Makes This Different

**Compared to blindly following TOPIK 2:**
- Filters 3873 words → prioritized subset based on actual utility
- Provides richer context (etymology, audio, examples)
- Acknowledges morphological redundancy

**Compared to pure frequency lists:**
- Still test-aligned (useful for standardized assessment)
- Manually curated examples (not raw corpus sentences)
- Korean-specific considerations (Hanja etymology, Japanese cognates)

**Compared to pure immersion/mining:**
- More structured and efficient for beginners
- Ensures coverage of essential vocabulary
- Provides explicit learning aids (etymology, notes)

## Key Insights from Practice

### The "Missing Link" Problem

**Observation**: LLM-generated example sentences for TOPIK 1 words naturally included words outside TOPIK 1.

**Example**: 목도리 (scarf) naturally co-occurs with 두르다 (to wear around neck/shoulders).

**Implication**: TOPIK word lists have gaps - high-frequency words that naturally appear in beginner contexts but aren't in beginner lists.

**Solution**: Prioritize TOPIK 2 words that fill these gaps (score them high in priority ranking).

### Morphological Redundancy

**Observation**: Test-prep lists treat trivial derivations as separate entries.

**Example**:
- 가능 (possibility, noun)
- 가능하다 (to be possible, verb)
- 가능성 (possibility, abstract noun)

These are essentially the same learning unit, but counted as 3 separate "words."

**Solution**: Morphological family constraint - score related forms identically, study as unit.

### TOPIK 1/2 Boundary is Arbitrary

**Observation**: Some TOPIK 2 words are more useful than some TOPIK 1 words.

**Example**: 가까이 (nearby, adverb) is TOPIK 2, but it's a natural derivation of 가깝다 (close, TOPIK 1) and appears frequently in everyday Korean.

**Solution**: Re-score/re-rank based on utility, not test level.

## Related Research & Concepts

### Comprehensible Input (i+1)
- Input should be 95-98% comprehensible for optimal acquisition
- The "+1" should be vocabulary, not grammar complexity
- See: `prompts/research-sentence-complexity.md`

### Spaced Repetition
- Forgetting curve is real - requires systematic review
- Anki implementation with customized cards
- See: Audio generation, example sentences for each word

### Context-Rich Learning
- Words learned in isolation are harder to retain
- Example sentences provide usage context
- Etymology provides conceptual context (Hanja, Japanese)
- Notes provide mnemonic context

### Graded Readers / Leveled Content
- Complexity should scale with proficiency
- TOPIK 1 → TOPIK 2 represents natural progression
- But within TOPIK 2, not all words are equally accessible

## Open Questions

1. **Optimal deck size**: How many words should Tier 1 / high-score subset contain?
   - Too small: Miss essential vocabulary
   - Too large: Defeat purpose of filtering

2. **Morphological families**: Should they be separate Anki cards or combined?
   - Current: Separate cards with identical priority
   - Alternative: Single card with all forms listed

3. **Example sentence quality**: Generated vs. corpus-extracted?
   - Current: LLM-generated following i+1 principles
   - Trade-off: Artificially simple vs. naturally messy

4. **Audio utility**: How much does pronunciation audio actually help?
   - Intuition: Useful for Korean (different phonology from English/Japanese)
   - But: Time investment vs. benefit?

5. **Long-term validation**: After studying high-priority subset, does real Korean media feel more accessible?
   - This is the ultimate test of framework effectiveness
   - Need to measure: Comprehension % before/after

## Future Directions

### Potential Enhancements

1. **Frequency corpus integration**
   - Cross-reference TOPIK list with Korean subtitle corpus
   - Validate/adjust priority scores with actual frequency data

2. **Grammar scaffolding**
   - Identify grammar patterns needed for TOPIK 2
   - Generate examples that introduce grammar in i+1 fashion
   - See: `prompts/ideas-grammar-guide.md`

3. **Content-based filtering**
   - Filter vocabulary by genre (news, drama, variety shows)
   - Allow learner to optimize for specific media interests

4. **Adaptive deck**
   - Track unknown words encountered in real content
   - Dynamically adjust priorities based on learner's gaps

### What NOT to Build

- ❌ Complex spaced-repetition algorithm (Anki already handles this)
- ❌ Grammar explanations (other resources cover this well)
- ❌ Full textbook replacement (this complements textbook study)
- ❌ Speaking/writing practice (different skill, different tools)

## References

### External Resources
- Krashen's Input Hypothesis (comprehensible input)
- Nation's vocabulary research (frequency, learning burden)
- CEFR framework (proficiency levels)
- Korean learning communities (r/Korean, HowtoStudyKorean)

### Internal Documentation
- `prompts/research-sentence-complexity.md` - i+1 application to examples
- `prompts/ideas-grammar-guide.md` - grammar scaffolding concepts
- `prompts/koreantopik2/generate-score.md` - priority scoring strategy
- `prompts/requirements-example.md` - example sentence quality criteria

---

**Last updated**: 2025-01-02

**Note**: This is a living document. As insights emerge from practice, update this to reflect evolved understanding.
