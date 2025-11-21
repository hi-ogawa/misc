# Research Foundations for Vocabulary Example Sentences

**Created**: 2025-11-21
**Purpose**: Document theoretical and empirical research supporting example sentence design principles

This document synthesizes academic research on vocabulary learning, example sentence design, and memory to provide theoretical grounding for the practical requirements in `requirements-example.md`.

---

## Executive Summary

The practical requirements developed empirically align strongly with established research across multiple fields: cognitive psychology, second language acquisition, corpus linguistics, and lexicography. The "golden rule" synthesized from research:

**"Effective vocabulary examples create HIGH INVOLVEMENT through DISTINCTIVE CONCRETE CONTEXTS that show CHARACTERISTIC USAGE while maintaining sufficient GENERALIZABILITY."**

---

## Core Theoretical Frameworks

### 1. Involvement Load Hypothesis (Laufer & Hulstijn, 2001)

**Core Principle**: Retention of unfamiliar words is contingent upon the involvement load of a task—the amount of need, search, and evaluation it imposes.

**Three Components**:
- **Need**: Motivation to learn the word (intrinsic or extrinsic)
- **Search**: Looking up meaning, usage, or contextual information
- **Evaluation**: Comparing the word to context, deciding if it fits, understanding nuances

**Key Findings**:
- Higher involvement load → better retention
- **Evaluation contributes most to learning** (meta-analysis finding)
- Need contributes moderately
- Search contributes least

**Original Study Results**:
- Composition task (high evaluation) → highest retention
- Reading + fill-in (medium evaluation) → moderate retention
- Reading only (low evaluation) → lowest retention

**Application to Example Sentences**:
- Examples should force **evaluation**: "Does this show what makes THIS word different?"
- Create need through distinctive, memorable contexts
- Show characteristic usage patterns that require learners to evaluate fit

**Connection to Our Requirements**:
- ✅ "Ask: Does this example show what makes THIS word different from similar words?"
- ✅ "Show characteristic or typical usage, not just grammatically correct patterns"
- ✅ Avoiding generic patterns (주세요, 있어요) → forces evaluation of specific usage

---

### 2. Concreteness Effect & Dual Coding Theory (Paivio, 1971)

**Core Principle**: Concrete words activate BOTH verbal and imagery-based processing systems, while abstract words only activate the verbal system.

**Dual Coding Theory**:
- **Verbal system**: Processes linguistic information (all words)
- **Imagery system**: Processes nonverbal, sensory information (concrete words only)
- Concrete words benefit from dual encoding → better retention

**Research Evidence**:
- Concrete words learned faster and retained longer than abstract words
- Neural evidence: Ventral anterior fusiform gyrus (visual processing region) activates for concrete words
- L2 vocabulary learning: Concrete novel words show faster meaning acquisition
- Higher recall accuracies for concrete vs. abstract words in paired-associate learning

**Strategy for Abstract Words**:
- Concrete contexts can help abstract words by providing imagery hooks
- Embedding abstract words in specific, visualizable situations leverages imagery system

**Application to Example Sentences**:
- Use concrete, specific nouns (not pronouns or generic words)
- Add sensory details (visual, spatial, temporal)
- Create visualizable scenes even for abstract vocabulary

**Connection to Our Requirements**:
- ✅ "Use concrete, specific nouns (not pronouns/demonstratives or generic words)"
  - ❌ "이거 주세요" → ✅ "목이 말라서 물 한 잔 주세요"
- ✅ "Add concrete context elements (location/time/manner/specific object)"
  - ❌ "나비가 날아다녀요" → ✅ "봄에 나비가 꽃 사이를 날아다녀요"
- ✅ "Create content-rich, memorable examples by adding concrete details"

**Innovation in Our Approach**:
Layering concreteness through multiple dimensions:
- Generic person → specific relationship (사람 → 친구)
- Bare event → time marker (왔어요 → 어제 왔어요)
- Vague action → specific purpose (왔어요 → 놀러 왔어요)
- No location → specific place (왔어요 → 집에 왔어요)

Result: "친구가 어제 집에 놀러 왔어요" (multiple concrete anchors for visualization)

---

### 3. Context Availability Hypothesis (Schwanenflugel et al., 1988)

**Core Principle**: Words are better recalled when you can readily generate a context or circumstance for them.

**Context Availability Ratings**:
- **CA (Context Availability)**: How readily a context comes to mind for a word
- **SA (Sentence Availability)**: How easy it is to think of a sentence for a word

**Research Findings on Sentence Contexts**:

1. **Low-constraint contexts**:
   - Hurt recall performance (less memorable)
   - Help recognition performance (provide some context)
   - Relative to words presented in isolation

2. **High-constraint contexts**:
   - Hurt BOTH recall and recognition
   - Too specific → not generalizable to new contexts
   - Creates overfitting to one particular usage

3. **Optimal Balance**:
   - Medium constraint with distinctive features
   - Informative but not overly specific
   - Shows typical usage across situations

**The Context Availability Trade-off**:
- Abstract words: Difficult to access prior contexts → benefit more from provided context
- Concrete words: Easy to access contexts → less benefit from additional context
- Providing context helps equalize learning between concrete and abstract words

**Application to Example Sentences**:
Balance specificity and generalizability:
- Specific enough to be memorable and distinctive
- General enough to show typical usage patterns
- Not so specific it's a one-off situation

**Connection to Our Requirements**:
- ✅ "Balance simplicity with memorable context"
- ✅ "Goal: Simple enough for TOPIK 1, but rich enough to be distinctive and memorable"
- ✅ Avoiding both extremes:
  - ❌ Too bare: "무궁화가 여름에 피어요" (lacks distinctive context)
  - ❌ Too specific: "이 빨간 스웨터가 크리스마스 선물이에요" (over-constrained)
  - ✅ Balanced: "생일 선물로 스웨터를 받았어요" (specific but common situation)

---

### 4. Contextual Diversity & Distinctive Contexts (Johns et al., 2012)

**Core Principle**: Contextual diversity (number of highly distinctive, non-redundant contexts) is a better predictor of word recognition than simple word frequency.

**Key Definitions**:
- **Contextual diversity**: Number of different contexts in which a word appears
- **Distinctive contexts**: Non-redundant contexts that show different aspects of word usage
- **Redundant contexts**: Multiple similar contexts showing same usage pattern

**Research Findings**:

1. **High diversity (distinctive contexts)**:
   - Faster word recognition
   - More accurate identification
   - Broader understanding of usage
   - Better for initial learning

2. **Low diversity (redundant contexts)**:
   - More stable semantic representations
   - Focused, coherent meaning
   - Better for reinforcement/consolidation

**The Trade-off**:
- Distinctive contexts → breadth of understanding
- Redundant contexts → depth and stability
- Both have pedagogical value at different learning stages

**Application to Example Sentences**:

**For initial learning (current focus)**:
- Use distinctive contexts that differentiate words
- Show what makes THIS word unique
- Highlight contrasts with similar vocabulary

**For review/reinforcement** (future consideration):
- Multiple examples showing same usage pattern
- Reinforces typical collocations
- Stabilizes semantic representation

**Connection to Our Requirements**:
- ✅ "Core principle: Example must help conceptualize the word through distinctive context"
- ✅ "Ask: Does this example show what makes THIS word different from similar words?"
- ✅ "Show characteristic or typical usage, not just grammatically correct patterns"
- ✅ Avoiding generic patterns that could apply to many words

**Examples of Distinctive vs. Generic Contexts**:
- ❌ Generic: "고등학생이 공부해요" (could be any student, any subject)
- ✅ Distinctive: "고등학생이 도서관에서 수학을 공부해요" (specific location, specific subject)

---

### 5. Corpus-Based Lexicography (COBUILD, 1980s+)

**Historical Context**:
- Early dictionaries: Manually compiled examples based on lexicographer intuition
- 1942: Hornby's pedagogical approach (simplified, controlled examples)
- 1980s: COBUILD pioneered corpus-driven dictionaries using Bank of English corpus
- Modern era: All major learner dictionaries are corpus-based

**Core Principles**:

1. **Authentic language patterns**:
   - Use real usage from native speakers
   - Show actual collocations and preferences
   - Avoid artificial or contrived examples

2. **Frequency-informed selection**:
   - Prioritize high-frequency collocations
   - Show typical usage environments
   - Reflect real-world language use

3. **Pedagogical adaptation**:
   - Balance authenticity with learner level
   - Simplify when necessary but preserve naturalness
   - Maintain characteristic usage patterns

**Research on Learner Dictionary Examples**:

**Finding 1 - Context richness**:
- Short sentences lack informativeness
- Longer sentences with context preferred for productive tasks (speaking/writing)
- More context = better understanding of usage

**Finding 2 - Authentic vs. pedagogical debate**:
- Pure authenticity can be too complex for learners
- Pure simplification can be unnatural or misleading
- Modern approach: Corpus-informed + pedagogically adapted

**Finding 3 - Recent LLM research** (2024):
- LLM-generated examples preferred to Oxford Dictionary examples 83.9% of the time
- Suggests traditional approaches can be improved
- Combination of corpus data + generation flexibility

**Application to Example Sentences**:

Use corpus linguistics principles:
- Show typical collocations from authentic usage
- Prioritize high-frequency patterns
- Demonstrate characteristic usage environments
- Balance naturalness with appropriate complexity level

**Connection to Our Requirements**:
- ✅ "Connectives and clauses are ENCOURAGED when they add learning value"
  - Shows natural language patterns (-서, -을 때, -고, -을지)
- ✅ Shift from "bare minimum" to "connectives that add context"
  - ❌ Bare: "박물관 입장이 무료예요"
  - ✅ Natural: "우리 고양이가 너무 뚱뚱해서 뛰지 못해요"
- ✅ "Use natural, conversational structures - don't artificially restrict complexity"

**Collocation Awareness**:
Show words in their typical linguistic environments:
- Verb-object pairs: 기름에 튀기다 (fry in oil)
- Adjective-noun combinations: 가벼운 가방 (light bag)
- Adverb-verb patterns: 꼭 와야 해요 (must come)

---

### 6. Depth of Processing (Craik & Lockhart, 1972)

**Core Principle**: The more deeply learners engage with new information by attaching it to meaning or context, the more likely it is to be remembered.

**Processing Levels**:
- **Shallow processing**: Physical features (how word looks/sounds)
- **Medium processing**: Phonological/orthographic patterns
- **Deep processing**: Semantic meaning, conceptual connections, contextual usage

**Related Frameworks**:

1. **Technique Feature Analysis** (Nation & Webb, 2011):
   - Analyzes specific features of vocabulary learning activities
   - Evaluates depth of processing for each technique

2. **TOPRA Model** (Barcroft, 2002):
   - Type of Processing - Resource Allocation model
   - Different processing types require different cognitive resources

**Application to Example Sentences**:

Every contextual detail forces deeper processing:

1. **Explicit subjects/objects**:
   - Forces visualization of WHO does WHAT
   - Creates mental scene with actors and actions
   - Deeper than bare verb forms

2. **Particles (가/이, 를/을, 에서, 랑)**:
   - Requires understanding grammatical relationships
   - Shows word's role in sentence structure
   - Pedagogically valuable even if less natural

3. **Time/location markers**:
   - Situational anchoring in memory
   - Creates episodic memory associations
   - Easier retrieval through context cues

4. **Causal/temporal connectives (-서, -을 때)**:
   - Requires causal reasoning
   - Shows word in relationship to other concepts
   - Deepest level of semantic processing

**Connection to Our Requirements**:
- ✅ "ALWAYS include particles explicitly for learning purposes"
- ✅ "For pedagogical purposes, prefer explicit subjects/objects over natural ellipsis"
  - ❌ "고장이 났어요" (subject dropped, shallow processing)
  - ✅ "자전거가 고장 나서 수리점에 갔어요" (explicit subject + consequence, deep processing)
- ✅ "Add enough detail to make the scene CONCRETE and VISUALIZABLE"
- ✅ "Add concrete context elements (location/time/manner/specific object)"

**Depth Through Detail**:
Each added element increases processing depth:
- "공부해요" → shallow (bare verb)
- "수학을 공부해요" → medium (adds object)
- "도서관에서 수학을 공부해요" → deeper (adds location)
- "고등학생이 도서관에서 수학을 공부해요" → deepest (adds subject, full scene)

---

## Synthesis: Alignment Between Research and Practice

### Strong Alignments

| Practical Requirement | Supporting Research | Strength |
|----------------------|---------------------|----------|
| "Show characteristic/typical usage" | Corpus linguistics, collocations | ⭐⭐⭐ Very Strong |
| "Add concrete details for visualization" | Concreteness effect, dual coding theory | ⭐⭐⭐ Very Strong |
| "Avoid generic patterns (주세요, 있어요)" | Distinctive contexts, contextual diversity | ⭐⭐⭐ Very Strong |
| "Use specific nouns, not pronouns" | Concreteness effect, context availability | ⭐⭐⭐ Very Strong |
| "Add time/location/manner context" | Context availability, memorable encoding | ⭐⭐⭐ Very Strong |
| "Connectives encouraged (-서, -을 때)" | Depth of processing, involvement load | ⭐⭐⭐ Very Strong |
| "Balance simplicity with distinctiveness" | Context constraint research | ⭐⭐⭐ Very Strong |
| "Never drop subjects/objects" | Pedagogical clarity, depth of processing | ⭐⭐ Strong (pedagogical choice) |
| "Create visualizable scenes" | Dual coding, episodic memory | ⭐⭐⭐ Very Strong |

### Novel Insights from Research

#### 1. The Evaluation Component is Key

**Research Insight**: In the Involvement Load Hypothesis, **evaluation** contributes most to vocabulary retention.

**Application**:
Current approach already emphasizes evaluation through:
- "Does this show what makes THIS word different?"
- Showing characteristic vs. atypical usage
- Domain-specific contexts

**Potential Enhancement**:
- Explicitly track semantic contrasts in notes field
- Show word in context of similar words (synonyms, antonyms)
- Highlight typical vs. atypical collocations

**Example**:
For 고장 나다:
- Current: "자전거가 고장 나서 수리점에 갔어요" ✅
- Enhanced notes: "vs. 망가지다 (completely broken), vs. 작동이 안 되다 (not working)"

#### 2. Context Constraint Balance

**Research Warning**: High-constraint contexts hurt both recall and recognition.

**What to Watch For**:
- ❌ Too many specifics: "이 빨간 스웨터가 크리스마스 선물이에요"
  - Specific color + specific occasion → overfitting
  - Hard to generalize to other uses of "스웨터"

- ✅ Specific but general: "생일 선물로 스웨터를 받았어요"
  - Specific situation (birthday) but common/relatable
  - Shows typical context for receiving gifts
  - Generalizable to other occasions

**Guideline**: Aim for **medium constraint with distinctive features**
- Specific enough: Memorable, visualizable, distinctive
- General enough: Shows typical usage, transferable to other contexts

#### 3. Redundant Contexts Have Value Too

**Research Finding**: While distinctive contexts aid initial learning, redundant contexts create more stable semantic representations.

**Two-Stage Learning Strategy**:

**Stage 1 - Initial Learning** (current focus):
- Use distinctive contexts
- Show what makes word unique
- Differentiate from similar vocabulary
- Build breadth of understanding

**Stage 2 - Consolidation** (future consideration):
- Multiple examples showing same pattern
- Reinforce typical collocations
- Stabilize semantic representation
- Build depth of understanding

**Example for 가볍다**:
- Distinctive: "가벼운 가방을 사서 여행에 가져갔어요" (shows portability context)
- Redundant 1: "등산할 때 가벼운 배낭이 필요해요" (reinforces portability)
- Redundant 2: "가벼운 운동화를 신으면 오래 걸을 수 있어요" (reinforces portability)

This could inform a fix/enhancement workflow for commonly confused words.

#### 4. Frequency-Based Context Selection

**Corpus Research**: High-frequency collocations aid learning more than low-frequency ones.

**Application**:
When choosing contexts, prioritize:
- Common verb-object pairings
- Typical adjective-noun combinations
- Frequent grammatical patterns
- Real-world usage frequencies

**Potential Tool**: Use Korean corpus data (예: 세종 말뭉치) to validate collocation frequencies.

**Example for 가르치다**:
- Check corpus: "영어를 가르치다" (very common)
- vs. "체조를 가르치다" (less common)
- Prioritize high-frequency patterns for better transfer

---

## The Golden Rule: Unified Framework

Synthesizing all research findings into a single actionable principle:

### **"Effective vocabulary examples create HIGH INVOLVEMENT through DISTINCTIVE CONCRETE CONTEXTS that show CHARACTERISTIC USAGE while maintaining sufficient GENERALIZABILITY."**

**Breaking Down Each Component**:

#### 1. HIGH INVOLVEMENT
**Source**: Involvement Load Hypothesis (Laufer & Hulstijn, 2001)

**Operationalized as**:
- **Evaluation**: Requires thinking "What makes THIS word different?"
- **Need**: Creates motivation through memorable, relevant contexts
- **Search** (optional): May prompt looking up related words or patterns

**In Practice**:
- Avoid generic patterns that work for any word
- Show distinctive usage that requires evaluation
- Create contexts worth remembering

#### 2. DISTINCTIVE
**Source**: Contextual Diversity (Johns et al., 2012)

**Operationalized as**:
- Non-redundant contexts (at initial learning stage)
- Shows contrast with similar words
- Highlights what makes word unique
- Avoids patterns that could apply to many words

**In Practice**:
- ❌ "주세요" patterns (too generic)
- ✅ Specific actions/contexts characteristic of that word

#### 3. CONCRETE
**Source**: Dual Coding Theory (Paivio, 1971), Concreteness Effect

**Operationalized as**:
- Specific nouns (not pronouns: 이거, 그것, 사람)
- Visualizable scenes (who, what, where, when)
- Sensory details (temporal, spatial, manner)
- Explicit grammatical elements (subjects, objects, particles)

**In Practice**:
- Multiple layers of concreteness
- Create mental images
- Activate both verbal and imagery systems

#### 4. CHARACTERISTIC USAGE
**Source**: Corpus Linguistics, Collocation Research

**Operationalized as**:
- Typical collocations from authentic usage
- Natural grammatical patterns
- Real-world contexts where word commonly appears
- Frequency-informed examples

**In Practice**:
- Show what you DO with the word
- Demonstrate typical environments
- Use natural connectives and structures

#### 5. SUFFICIENT GENERALIZABILITY
**Source**: Context Availability Hypothesis (Schwanenflugel et al., 1988)

**Operationalized as**:
- Medium constraint (not too specific, not too bare)
- Common/relatable situations
- Transferable to other contexts
- Shows range of applicability

**In Practice**:
- Avoid overly specific one-off situations
- Use common scenarios learners will encounter
- Balance memorability with transferability

---

## Practical Implications

### Current Strengths

The empirically-derived requirements already embody most research-supported principles:

✅ **High involvement through evaluation**
- "Does this show what makes THIS word different?"

✅ **Concreteness through multiple layers**
- Specific nouns, time, location, manner
- Explicit subjects/objects

✅ **Distinctive contexts**
- Avoiding generic patterns
- Showing characteristic usage

✅ **Corpus-informed naturalness**
- Natural connectives
- Authentic grammatical structures

✅ **Appropriate constraint level**
- Balance of simplicity and distinctiveness

### Potential Enhancements

Based on research not yet fully incorporated:

#### 1. Collocation Tracking
**What**: Systematically track and use high-frequency collocations
**How**:
- Use Korean corpus data (세종 말뭉치, 고려대 한국어 대사전)
- Prioritize frequent patterns in examples
- Document typical collocations in notes field

**Example Addition to Notes Field**:
- 가볍다: Common collocations: 가벼운 가방, 가벼운 마음, 가벼운 운동

#### 2. Semantic Contrast Documentation
**What**: Explicitly show how word differs from synonyms/related words
**How**:
- Add semantic contrast notes for commonly confused words
- Show typical context differences
- Highlight usage restrictions or preferences

**Example**:
- 고장 나다 vs. 망가지다 vs. 작동이 안 되다
- Notes field could include: "고장 나다: repairable malfunction (vs. 망가지다: broken beyond repair)"

#### 3. Two-Stage Example Strategy
**What**: Recognize different needs for initial learning vs. consolidation
**How**:
- Current approach: Distinctive contexts (perfect for initial learning)
- Future fix workflow: Could add redundant contexts for difficult words
- Anki could show both types across spaced repetition

**Implementation**:
- Initial card: One distinctive example
- Review/difficult cards: Add 2-3 redundant examples showing same pattern
- Builds both breadth (distinctive) and depth (redundant)

#### 4. Involvement Load Scoring
**What**: Rate examples by involvement load to ensure high evaluation
**How**:
- Quick self-check: Does this example require evaluation?
- Does learner need to think about word meaning to understand context?
- Does context show something specific about this word?

**Quality Check Questions**:
- [ ] Does this force evaluation of word meaning?
- [ ] Is context distinctive (not generic)?
- [ ] Can I visualize the scene?
- [ ] Does this show typical usage?
- [ ] Is it generalizable to other contexts?

---

## Research References

### Primary Sources

**Involvement Load Hypothesis**:
- Hulstijn, J., & Laufer, B. (2001). Some empirical evidence for the Involvement Load Hypothesis in vocabulary acquisition. *Language Learning, 51*(3), 539-558.
- Laufer, B., & Hulstijn, J. (2001). Incidental vocabulary acquisition in a second language: The construct of task-induced involvement. *Applied Linguistics, 22*(1), 1-26.

**Concreteness Effect & Dual Coding**:
- Paivio, A. (1971). *Imagery and Verbal Processes*. New York: Holt, Rinehart, and Winston.
- De Groot, A. M. B., & Keijzer, R. (2000). What is hard to learn is easy to forget: The roles of word concreteness, cognate status, and word frequency in foreign-language vocabulary learning and forgetting. *Language Learning, 50*(1), 1-56.

**Context Availability**:
- Schwanenflugel, P. J., Harnishfeger, K. K., & Stowe, R. W. (1988). Context availability and lexical decisions for abstract and concrete words. *Journal of Memory and Language, 27*(5), 499-520.
- Schwanenflugel, P. J., & Shoben, E. J. (1983). Differential context effects in the comprehension of abstract and concrete verbal materials. *Journal of Experimental Psychology: Learning, Memory, and Cognition, 9*(1), 82-102.

**Contextual Diversity**:
- Johns, B. T., Gruenenfelder, T. M., Pisoni, D. B., & Jones, M. N. (2012). Contextual diversity facilitates learning new words in the classroom. *PLOS ONE, 7*(6), e0179004.
- Adelman, J. S., Brown, G. D., & Quesada, J. F. (2006). Contextual diversity, not word frequency, determines word-naming and lexical decision times. *Psychological Science, 17*(9), 814-823.

**Corpus Linguistics & Lexicography**:
- Sinclair, J. (1991). *Corpus, Concordance, Collocation*. Oxford: Oxford University Press.
- Hanks, P. (2012). The corpus revolution in lexicography. *International Journal of Lexicography, 25*(4), 398-436.

**Depth of Processing**:
- Craik, F. I., & Lockhart, R. S. (1972). Levels of processing: A framework for memory research. *Journal of Verbal Learning and Verbal Behavior, 11*(6), 671-684.
- Nation, I. S. P., & Webb, S. (2011). Researching and analyzing vocabulary. Boston: Heinle Cengage Learning.

**Collocations in L2 Learning**:
- Gablasova, D., Brezina, V., & McEnery, T. (2017). Collocations in corpus‐based language learning research: Identifying, comparing, and interpreting the evidence. *Language Learning, 67*(S1), 155-179.

### General Vocabulary Learning

- Nation, I. S. P. (2001). *Learning Vocabulary in Another Language*. Cambridge: Cambridge University Press.
- Laufer, B., & Nation, P. (1995). Vocabulary size and use: Lexical richness in L2 written production. *Applied Linguistics, 16*(3), 307-322.
- Schmitt, N. (2010). *Researching Vocabulary: A Vocabulary Research Manual*. Basingstoke: Palgrave Macmillan.

---

## Conclusion

The empirically-derived practical requirements demonstrate strong alignment with established research across multiple theoretical frameworks. The iterative refinement process based on personal learning experience has independently discovered many core principles from cognitive psychology, SLA research, and corpus linguistics.

**Key Strengths**:
1. High involvement through distinctive contexts
2. Concreteness through layered detail
3. Natural usage patterns from authentic language
4. Appropriate balance of specificity and generalizability

**Opportunities for Enhancement**:
1. Systematic collocation tracking using corpus data
2. Explicit semantic contrast documentation
3. Two-stage example strategy (distinctive → redundant)
4. Involvement load quality checks

The "golden rule" provides a unified framework that synthesizes all research findings into actionable guidance: create examples with high involvement, distinctive concrete contexts, characteristic usage, and sufficient generalizability.

---

**Document Status**: Initial research synthesis
**Next Steps**:
- Potential integration of corpus data for collocation validation
- Development of semantic contrast documentation for confusable words
- Consideration of two-stage example strategy for review/fix workflow
