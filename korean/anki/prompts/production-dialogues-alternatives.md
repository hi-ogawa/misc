# Dialogue Alternatives

Experimental extension to [production-dialogues.md](production-dialogues.md) - adding one alternative dialogue per card.

**Status**: Hypothesis testing phase

## Hypothesis

One alternative dialogue is sufficient to break false rigidity ("only one way to say this") without cognitive overload.

### Why This Might Work

1. **Stage-dependent effectiveness**: Learner already has passive exposure to variant expressions (못해 vs 할 수가 없어) but hasn't explicitly recognized them as interchangeable. Alternative makes implicit equivalence explicit.

2. **Dialogue is a safe testing ground**: Unlike vocabulary example sentences (which require specific word + grammar pattern), dialogue already expects variance. Plot→dialogue is situational, not translation.

3. **Binary comparison is cognitively clean**: "I said X, they show Y and Z" → simple validation without decision paralysis of 5 variants.

### Counterarguments to Address

- **Selection bias**: How to choose which alternative? Must be equally natural, not rare/unusual.
- **Directionality**: For production (plot→dialogue), showing alternatives validates learner's variance. For recognition, might be unnecessary.
- **Assessment ambiguity**: User self-grades whether their production matches primary, alternative, or is a valid third option.

## What Makes a Good Alternative

**Include:**
- Different discourse connective (그런데 vs 근데 vs 그래도)
- Different elaboration (same meaning, different extra details)
- Structural variance (못 만나요 vs 만날 수 없어요)
- Lexical variance at same register (진짜 vs 정말)

**Exclude:**
- Formality shifts (반말↔존댓말)
- Significantly different content
- Rare/unusual phrasings
- Grammatically correct but pragmatically odd

## Data Format

Extends existing TSV with one additional field:

| Field | Description |
|-------|-------------|
| `alt_dialogue_ko` | Alternative Korean dialogue (same structure, natural variance) |

## Card Template Update

Front: (unchanged)
```
{{plot_ko}}<br><br>{{plot_ko_audio}}
```

Back:
```html
{{FrontSide}}
<hr id=answer>
{{dialogue_ko}}<br><br>{{dialogue_ko_audio}}

<details><summary>Alternative</summary>
{{alt_dialogue_ko}}
</details>

<br><details><summary>English</summary>{{dialogue_en}}</details>
<br><small>{{patterns}}</small>
```

## Workflow

### Phase 1: Prototype (5-10 dialogues)

Generate alternatives for existing dialogues to test:
- Is generating meaningful alternatives tractable?
- Do alternatives feel useful during review?
- Can LLM produce natural variants without explicit guidance?

```yaml
# Input: existing dialogue
- id: 2
  dialogue_ko:
    - A: 이번 주말에 뭐 할 거예요? 오랜만에 같이 뭐 하고 싶어요.
    - B: 토요일에는 회사 일이 있어서 못 만나요. 그런데 일요일은 완전 시간 있어요.
    - A: 그럼 일요일에 영화 볼까요? 요즘 재미있는 영화 많대요.
    - B: 좋아요! 시간 정해서 연락할게요.
  dialogue_en:
    - A: What are you doing this weekend? I want to do something together, it's been a while.
    - B: I have work on Saturday so I can't meet. But I'm completely free on Sunday.
    - A: Then shall we watch a movie on Sunday? I heard there are lots of good movies lately.
    - B: Sounds good! I'll set a time and contact you.

# Output: alternative
  alt_dialogue_ko:
    - A: 이번 주말에 시간 있어요? 오랜만에 만나고 싶어요.
    - B: 토요일은 회사 일 때문에 안 돼요. 근데 일요일은 괜찮아요.
    - A: 그러면 일요일에 영화 어때요? 요즘 좋은 영화 많다던데.
    - B: 좋아요! 나중에 시간 알려 줄게요.
```

Variance types in this example:
- 뭐 할 거예요 → 시간 있어요 (different question framing)
- 같이 뭐 하고 싶어요 → 만나고 싶어요 (specific→general)
- 있어서 못 만나요 → 때문에 안 돼요 (connector + verb)
- 그런데 → 근데 (discourse marker)
- 완전 시간 있어요 → 괜찮아요 (different expression)
- 그럼 → 그러면 (connector variant)
- 볼까요 → 어때요 (suggestion form)
- 많대요 → 많다던데 (hearsay variant)
- 정해서 연락할게요 → 알려 줄게요 (different verb)

### Phase 2: Evaluate

After 1-2 weeks of using prototype cards:
- Did seeing alternatives change production confidence?
- Did it reduce "tip of tongue" moments?
- Was self-grading ambiguous or clear?

### Phase 3: Scale (if validated)

Generate alternatives for full dialogue set (60-80 cards).

## LLM Prompt for Alternative Generation

```
Given this Korean dialogue, generate ONE natural alternative.

Requirements:
- Same 4-turn A→B→A→B structure
- Same overall meaning and situation
- Natural variance in: discourse connectives, verb choices, elaboration style
- Same formality level (존댓말)
- All variants should be equally common/natural (no rare phrasings)

Original:
A: 이번 주말에 뭐 할 거예요? 오랜만에 같이 뭐 하고 싶어요.
B: 토요일에는 회사 일이 있어서 못 만나요. 그런데 일요일은 완전 시간 있어요.
A: 그럼 일요일에 영화 볼까요? 요즘 재미있는 영화 많대요.
B: 좋아요! 시간 정해서 연락할게요.

Generate alternative:
```

## Open Questions

- Should alternative have audio? (Probably not for prototype - adds complexity)
- How to handle cases where original is already the most natural? (Skip alternative)
- Should variance types be tracked/annotated? (Maybe for analysis, not for cards)

## Related

- [production-dialogues.md](production-dialogues.md) - Base dialogue system
- [../../prompts/requirements-example.md](../../prompts/requirements-example.md) - Contrast: tightly constrained examples (not suitable for alternatives)
