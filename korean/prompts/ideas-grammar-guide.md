# Idea: Grammar Guide Generation

## Problem

Current grammar learning approach:
- Sporadic deep-dive chats on Claude web (verb conjugation, particles, etc.)
- Hard to reference later - scattered across many conversations
- No systematic organization

## Potential Solutions

1. **Classic grammar books**:

   **Korean Grammar in Use** (Darakwon) - Recommended for lookup-style reference:

   | Volume | TOPIK Level | Description |
   |--------|-------------|-------------|
   | Beginning | 1-2 | Levels 1-2 grammar, ~112 grammar points |
   | Intermediate | 3-4 | Levels 3-4 grammar, ~93 grammar points, 432 pages |
   | Advanced | 5-6 | Levels 5-6 grammar |

   Key features:
   - Organized by grammar point (not lesson-based) - good for lookup
   - Groups similar grammar points together for comparison (비교 section)
   - Real-life dialogue examples, not artificial sentences
   - MP3 audio included
   - Each grammar point is self-contained

   **For TOPIK 1 vocabulary study**: Beginning volume covers all grammar you'd encounter.

   ### Beginning Volume - Table of Contents (376 pages)

   **Introduction**: Korean Sentence Structure, Conjugation, Connecting Sentences, Honorifics

   **Getting Ready**
   - 이다, 있다, Numbers, Dates/Days, Time

   **Unit 1: Tenses**
   - -(스)ㅂ니다, -아/어요, -았/었어요, -(으)ㄹ 거예요, -고 있다, -았/었었어요

   **Unit 2: Negation**
   - 안, -지 않아요, 못, -지 못해요

   **Unit 3: Particles** (20 items)
   - 이/가, 은/는, 을/를, 와/과/(이)랑/하고, 의, 에①, 에②, 에서
   - 에서~까지/부터~까지, 에게/한테, 도, 만, 밖에, (으)로
   - (이)나①, (이)나②, 쯤, 처럼/같이, 보다, 마다

   **Unit 4: Listing/Contrast**
   - -고 (and), -거나 (or), -지만 (but)

   **Unit 5: Time Expressions**
   - -기 전에 (before), -(으)ㄴ 후에 (after), -을 때 (when), -(으)면서 (while)

   **Unit 6: Ability/Possibility**
   - -(으)ㄹ 수 있다/없다 (can/cannot), -(으)ㄹ 줄 알다/모르다 (know how to)

   **Unit 7: Obligations/Permission**
   - -아/어야 하다 (must), -(으)면 안 되다 (must not), -아/어도 되다 (may), -지 않아도 되다 (don't have to)

   **Unit 8: Hope**
   - -고 싶다 (want to), -(으)면 좋겠다 (hope/wish)

   **Unit 9: Reasons/Causes**
   - -아/어서, -(으)니까, -기 때문에

   **Unit 10: Requests/Assisting**
   - -아/어 주다 (do for someone), -아/어 주세요 (please do)

   **Unit 11: Trying/Experiences**
   - -아/어 보다 (try doing), -(으)ㄴ 적이 있다/없다 (have/haven't done)

   **Unit 12: Opinions/Suggestions**
   - -(으)ㄹ까요? (shall we?), -(으)ㅂ시다 (let's), -는 게 어때요? (how about)

   **Unit 13: Intentions/Plans**
   - -(으)ㄹ게요 (I will), -(으)려고 하다 (intend to), -(으)ㄹ 거예요②

   **Unit 14: Background Info**
   - -는데/-(으)ㄴ데 (but/background context)

   **Unit 15: Purpose**
   - -(으)러 가다/오다 (go/come to do), -(으)려고 (in order to)

   **Unit 16: Degree/Extent**
   - -기가 쉽다/어렵다 (easy/hard to), 얼마나 ~-(으)ㄴ/는지 (how much)

   **Unit 17: Comparison**
   - 만큼 (as much as), 처럼/같이 (like), 보다 더 (more than)

   **Unit 18: Conditions/Concessions**
   - -(으)면 (if), -아/어도 (even if)

   **Unit 19: State**
   - -고 있다② (wearing/state), -아/어 있다 (resultant state), -아/어지다 (become), -게 되다 (come to)

   **Unit 20: Confirming Info**
   - -(으)ㄴ/는지 (whether), -지요? (right?)

   **Unit 21: Discovery/Surprise**
   - -군요/는군요 (I see!), -네요 (oh!)

   **Unit 22: Additional Endings**
   - -(으)ㄴ가요?/나요? (wondering), -(으)ㄴ/는데요 (trailing off)

   **Unit 23: Quotations**
   - 직접 인용 (direct), 간접 인용 (indirect), -대요/-래요 (contracted)

   **Unit 24: Irregular Conjugations**
   - ㅡ, ㄹ, ㅂ, ㄷ, 르, ㅎ, ㅅ 불규칙

   Other options (less suitable for lookup):
   - **TTMIK**: More conversational/podcast-style, good for learning but less efficient for quick lookup
   - **Yonsei/Sogang**: Curriculum textbooks, lesson-based progression

2. **Consolidate existing chats**: Extract final tables/rules from web chats into markdown files
   - Example: verb conjugation tables from existing chat are quite complete

3. **Generate with Claude Code**: Easier to iterate than web chats
   - Can build incrementally in `guides/` folder
   - Version controlled
   - But: markdown not ideal for actual review/study

## Notes

- User's actual grammar knowledge is higher than "beginner" curriculum assumes
- Deep-dives include: verb conjugation (all irregulars), particles, honorifics, derivation patterns
- This could inform example sentence requirements (i+1 principle - exploit known grammar)

## Status

- Idea noted for future consideration
- **Action**: Consider buying "Korean Grammar in Use - Beginning" for lookup reference
- Note: Some patterns (partial negation, some/any/whatever, question words) may be scattered or in Intermediate volume - LLM chats fill these gaps well
