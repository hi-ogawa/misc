# Dialogue Deck

Generate plot→dialogue cards. Works as production practice.

**Status**: Preliminary plan, adjustments expected.

## Core Concept

**Plot→Dialogue**: Paragraph scene description triggers full dialogue production.

- Plot is a brief paragraph describing the situation (not turn-by-turn)
- Dialogue has extra details beyond what plot describes (forces production, not translation)
- Dialogue is richer—each turn has substance, natural elaboration
- Discourse connectives drive flow (그런데, 그래서, 그럼, 왜냐면, 그래도, etc.)

Plot language (Korean vs English) may or may not matter—see TBD.

## Constraints (for this project)

Content constraints specific to the current learning objective:

- **Vocabulary**: TOPIK1 level only (simple words, complex structure)
- **Grammar coverage**: Full 112 patterns from [KGIU](../../resources/korean-grammar-in-use/toc.md)
- **Dialogue length**: 3-5 sentences (or strict 4-turn A→B→A→B—see TBD)
- **Target**: 60-80 dialogues (3-6 patterns each covers all patterns with overlap)

## Examples

### Example 1: Weather small talk

**Plot (EN)**:
Two friends talking about the cold weather. They compare it to yesterday and wonder if it will snow.

**Plot (KO)**:
두 친구가 추운 날씨에 대해 이야기한다. 어제와 비교하고 눈이 올지 궁금해한다.

**Dialogue (KO)**:
A: 오늘 진짜 춥네요. 밖에 나가기 싫어요.
B: 맞아요. 어제보다 훨씬 추워진 것 같아요. 바람도 많이 불고요.
A: 이렇게 추우면 눈이 올까요?
B: 뉴스에서 오늘 밤에 온대요. 그래서 내일 아침에 길이 미끄러울 것 같아요.

**Dialogue (EN)**:
A: It's really cold today. I don't want to go outside.
B: Right. It seems much colder than yesterday. And it's really windy too.
A: If it's this cold, will it snow?
B: The news said it'll snow tonight. So I think the roads will be slippery tomorrow morning.

**Patterns**: -네요, V-기 싫다, N보다, -아/어지다, -(으)ㄹ 것 같다, N도, -고요, -(으)ㄹ까요, -대요 (hearsay), 그래서

### Example 2: Weekend plans

**Plot (EN)**:
Two friends trying to make weekend plans. One is busy Saturday but free Sunday.

**Plot (KO)**:
두 친구가 주말 계획을 세우려고 한다. 한 명은 토요일에 바쁘지만 일요일에는 시간이 있다.

**Dialogue (KO)**:
A: 이번 주말에 뭐 할 거예요? 오랜만에 같이 뭐 하고 싶어요.
B: 토요일에는 회사 일이 있어서 못 만나요. 그런데 일요일은 완전 시간 있어요.
A: 그럼 일요일에 영화 볼까요? 요즘 재미있는 영화 많대요.
B: 좋아요! 시간 정해서 연락할게요.

**Dialogue (EN)**:
A: What are you doing this weekend? I want to do something together, it's been a while.
B: I have work on Saturday so I can't meet. But I'm completely free on Sunday.
A: Then shall we watch a movie on Sunday? I heard there are lots of good movies lately.
B: Sounds good! I'll set a time and contact you.

**Patterns**: -(으)ㄹ 거예요, 오랜만에, -고 싶다, -아/어서 (reason), 못 V, 그런데, -(으)ㄹ까요, -대요 (hearsay), -(으)ㄹ게요

### Example 3: Asking for directions

**Plot (EN)**:
Someone asking how to get to a friend's house. The friend gives subway directions.

**Plot (KO)**:
친구 집에 어떻게 가는지 물어본다. 친구가 지하철 길을 알려준다.

**Dialogue (KO)**:
A: 집에 어떻게 가요? 처음 가는 거라서 잘 모르겠어요.
B: 지하철로 오면 돼요. 3호선 타고 신사역에서 내리세요. 역에서 나와서 오른쪽으로 5분쯤 걸으면 편의점이 보여요. 거기서 전화하세요.
A: 좀 복잡하네요. 제가 길을 잘 못 찾아서 걱정돼요. 역에서 마중 나와 줄 수 있어요?
B: 그럼요. 도착하면 전화하세요. 바로 나갈게요.

**Dialogue (EN)**:
A: How do I get to your place? It's my first time going so I'm not sure.
B: You can take the subway. Take line 3 and get off at Sinsa station. Exit and walk right for about 5 minutes and you'll see a convenience store. Call me from there.
A: That's a bit complicated. I'm worried because I'm bad at finding directions. Can you come meet me at the station?
B: Of course. Call me when you arrive. I'll come right out.

**Patterns**: -(으)로, -(으)면 되다, N에서 내리다, -아/어서 (sequential), N쯤, -(으)세요, -네요, 못 V, -아/어서 (reason), -아/어 주다, -(으)ㄹ게요

## Data Format

TSV with fields:

| Field | Description |
|-------|-------------|
| `plot_ko` | Paragraph scene description in Korean |
| `plot_en` | Paragraph scene description in English |
| `dialogue_ko` | Full Korean dialogue |
| `dialogue_en` | Full English dialogue |
| `notes` | Grammar patterns used, usage notes |
| `plot_ko_audio` | `[sound:filename.mp3]` for plot |
| `dialogue_ko_audio` | `[sound:filename.mp3]` for dialogue |

## Anki Setup

- **Deck**: `Korean::Dialogue`
- **Note type**: "Korean Dialogue"
  - Fields: `plot_ko`, `plot_en`, `dialogue_ko`, `dialogue_en`, `notes`, `plot_ko_audio`, `dialogue_ko_audio`
  - Card layout:
      Front: `plot_en`
      Back: `dialogue_ko`

## Workflow

### 1. Generate dialogues (agent)

Generate dialogues via LLM conversation, output to TSV.

Output: `output/dialogue/dialogues.tsv`

LLM prompt template:

````
Generate Korean dialogue data for Anki cards.

## Instructions

Read ONLY: `resources/korean-grammar-in-use/toc.md` (for grammar patterns reference)

Do NOT read other files in the repository.

## Output Format

Output in YAML:

```yaml
- id: 1
  title: Weather small talk
  plot_en: Two friends talking about the cold weather. They compare it to yesterday and wonder if it will snow.
  plot_ko: 두 친구가 추운 날씨에 대해 이야기한다. 어제와 비교하고 눈이 올지 궁금해한다.
  dialogue_ko:
    - A: 오늘 진짜 춥네요. 밖에 나가기 싫어요.
    - B: 맞아요. 어제보다 훨씬 추워진 것 같아요. 바람도 많이 불고요.
    - A: 이렇게 추우면 눈이 올까요?
    - B: 뉴스에서 오늘 밤에 온대요. 그래서 내일 아침에 길이 미끄러울 것 같아요.
  dialogue_en:
    - A: It's really cold today. I don't want to go outside.
    - B: Right. It seems much colder than yesterday. And it's really windy too.
    - A: If it's this cold, will it snow?
    - B: The news said it'll snow tonight. So I think the roads will be slippery tomorrow morning.
  patterns:
    - -네요
    - V-기 싫다
    - N보다
    - -아/어지다
    - -(으)ㄹ 것 같다
    - -고요
    - -(으)ㄹ까요
    - -대요
    - 그래서
```

## Core Principle: Plot→Dialogue Production

Plot = brief paragraph describing the scene (2-3 sentences)
Dialogue = natural conversation with EXTRA DETAILS beyond plot

Key: Dialogue must contain elaboration NOT in plot. This forces genuine production,
not direct translation. The plot is a situational index, not a script.

## Dialogue Requirements

1. **Structure**: Strict 4-turn A→B→A→B
2. **Richness**: Each turn has substance—natural elaboration, not bare minimum
   - ❌ "오늘 춥네요." (too simple)
   - ✅ "오늘 진짜 춥네요. 밖에 나가기 싫어요." (elaboration)
3. **Discourse connectives**: Use naturally (그런데, 그래서, 그럼, 그래도, -고요, etc.)
4. **Extra details in dialogue**: Add specifics not mentioned in plot
   - Plot: "They wonder if it will snow"
   - Dialogue: "뉴스에서 오늘 밤에 온대요. 그래서 내일 아침에 길이 미끄러울 것 같아요."
   (news source, tonight timing, slippery roads tomorrow = extra details)

## Constraints

- **Vocabulary**: TOPIK1 level (simple words, complex structure)
- **Grammar patterns**: Target specific patterns from Korean Grammar in Use
- **Natural flow**: Would sound natural in Korean variety show conversation

## Task

Generate [N] dialogues targeting these grammar patterns: [PATTERNS]
````

### 1b. Merge YAML batches to TSV

```bash
# Fix YAML quoting for dialogue lines with colons
for f in output/dialogue/dialogues-batch-*.yaml; do
  sed -i 's/^\(    - \)\(A:\|B:\)\(.*\)$/\1"\2\3"/g' "$f"
done

# Merge all batches and convert to TSV
yq eval-all '. as $item ireduce ([]; . + $item)' output/dialogue/dialogues-batch-*.yaml | \
  yq -o=json | \
  python3 -c "
import json, csv, sys
data = json.load(sys.stdin)
with open('output/dialogue/dialogues.tsv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(['id', 'title', 'plot_en', 'plot_ko', 'dialogue_ko', 'dialogue_en', 'patterns'])
    for d in data:
        writer.writerow([
            d.get('id', ''),
            d.get('title', ''),
            d.get('plot_en', ''),
            d.get('plot_ko', ''),
            '<br>'.join(d.get('dialogue_ko', [])),
            '<br>'.join(d.get('dialogue_en', [])),
            ', '.join(d.get('patterns', []))
        ])
"
```

### 2. Generate audio

```bash
# Plot audio
python scripts/generate-audio.py \
  --input output/dialogue/dialogues.tsv \
  --output output/dialogue/audio \
  --field plot_ko \
  --prefix dialogue_plot_ko_

# Dialogue audio
python scripts/generate-audio.py \
  --input output/dialogue/dialogues.tsv \
  --output output/dialogue/audio \
  --field dialogue_ko \
  --prefix dialogue_dialogue_ko_
```

### 3. Add audio columns

```bash
python scripts/jq-tsv.py \
  '. + {plot_ko_audio: "[sound:dialogue_plot_ko_\(.row).mp3]", dialogue_ko_audio: "[sound:dialogue_dialogue_ko_\(.row).mp3]"}' \
  output/dialogue/dialogues.tsv > output/dialogue/dialogues-with-audio.tsv
```

### 4. Create note type in Anki (manual)

Create "Korean Dialogue" note type with fields from Data Format section.

### 5. Import to Anki

```bash
python scripts/anki-add-notes.py \
  --input output/dialogue/dialogues-with-audio.tsv \
  --deck "Korean::Dialogue" \
  --model "Korean Dialogue"
```

### 6. Copy audio to Anki media

```bash
cp output/dialogue/audio/*.mp3 "$(python scripts/anki.py getMediaDirPath | tr -d '"')"
```

## Status

- [ ] Finalize grammar pattern target list
- [ ] Create first batch (20 dialogues)
- [ ] Set up Anki note type and deck

### TBD

- Plot language: `plot_en`→`dialogue_ko` or `plot_ko`→`dialogue_ko` for full Korean
- Dialogue structure: strict 4-turn A→B→A→B or flexible
- Reference [requirements-example.md](../../prompts/requirements-example.md) for dialogue generation inspiration
- LLM prompt template needs iteration

## Background

### Motivation

**Plot→Script approach**: Plot is a brief paragraph describing the scene. Dialogue provides natural realization with extra details beyond plot.

Key insight: Plot acts as situational index, not translation prompt. Dialogue has elaboration not in plot, forcing genuine production rather than direct translation. User retrieves pre-memorized dialogue chunks, not constructed translations.

### Relation to Existing System

- Complements `Korean::TOPIK1` vocab deck (same vocabulary base)
- Parallels grammar cards in `Korean::Custom` (same KGIU source)
- Different purpose: structural production vs vocabulary recognition

### Research Context

This approach is related to **Discourse Completion Tasks (DCT)** from pragmatics research (Blum-Kulka, 1980s), but extended:
- Traditional DCT: situation → single speech act
- This approach: situation → multi-turn dialogue with discourse structure
