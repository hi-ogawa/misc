# Dialogue Deck

Generate plot→dialogue cards. Works as production practice.

**Status**: Preliminary plan, adjustments expected.

## Core Concept

**Plot→Dialogue**: Turn-by-turn plot triggers full dialogue production.

- Plot describes each speaker's intent (A→B→A→B)
- Dialogue realizes intent with natural conversational flow
- Discourse connectives drive flow (그런데, 그래서, 그럼, 왜냐면, 그래도, etc.)

Plot language (Korean vs English) may or may not matter—see TBD.

## Constraints (for this project)

Content constraints specific to the current learning objective:

- **Vocabulary**: TOPIK1 level only (simple words, complex structure)
- **Grammar coverage**: Full 112 patterns from [KGIU](../../resources/korean-grammar-in-use/toc.md)
- **Dialogue length**: 3-5 sentences (or strict 4-turn A→B→A→B—see TBD)
- **Target**: 60-80 dialogues (3-6 patterns each covers all patterns with overlap)

## Examples

### Example 1

**Plot (EN)**:
Weekend plans + availability conflict
A: Ask about weekend plans.
B: Busy Saturday (work), but free Sunday.
A: Suggest movie on Sunday.
B: Agree, will contact later.

**Dialogue (KO)**:
A: 이번 주말에 뭐 할 거예요?
B: 토요일에는 일해야 돼서 못 만나요. 그런데 일요일은 시간 있어요.
A: 그럼 일요일에 영화 볼까요?
B: 좋아요! 연락할게요.

**Patterns**: -아/어야 되다, -아/어서 (reason), 그런데, -(으)ㄹ까요, -(으)ㄹ게요

### Example 2

**Plot (EN)**:
Explaining absence + resolution
A: Ask if homework is done.
B: No, was too sick yesterday. Planning to do it today.
A: Ask when it's due.
B: Tomorrow, but think can finish today.

**Dialogue (KO)**:
A: 숙제 다 했어요?
B: 아니요, 어제 너무 아파서 못 했어요. 그래서 오늘 하려고 해요.
A: 언제까지 내야 돼요?
B: 내일까지인데 오늘 끝낼 수 있을 것 같아요.

**Patterns**: 못 V, -아/어서 (reason), 그래서, -(으)려고 하다, -는데, -(으)ㄹ 것 같다

### Example 3

**Plot (EN)**:
Giving directions
A: Ask how to get to friend's place.
B: Take subway, exit and turn right, walk 5min to convenience store, house nearby.
A: Sounds complicated, offer to meet at station.
B: It's okay, will call when arriving.

**Dialogue (KO)**:
A: 집에 어떻게 가요?
B: 지하철로 오면 돼요. 역에서 나와서 오른쪽으로 걸으면 편의점이 보여요. 거기서 5분쯤 더 가면 우리 집이에요.
A: 복잡하네요. 제가 마중 나갈까요?
B: 괜찮아요. 도착하면 전화할게요.

**Patterns**: -(으)로, -(으)면, -아/어서 ①, N쯤, -네요, -(으)ㄹ까요, -(으)ㄹ게요

## Data Format

TSV with fields:

| Field | Description |
|-------|-------------|
| `plot_ko` | Turn-by-turn plot in Korean (title as first line) |
| `plot_en` | Turn-by-turn plot in English (title as first line) |
| `dialogue_ko` | Full Korean dialogue |
| `dialogue_en` | Full English dialogue |
| `notes` | Grammar patterns used, usage notes |
| `plot_ko_audio` | `[sound:filename.mp3]` for plot |
| `dialogue_ko_audio` | `[sound:filename.mp3]` for dialogue |

## Anki Setup

- **Deck**: `Korean::Dialogue`
- **Note type**: "Korean Dialogue"
  - Fields: `plot_ko`, `plot_en`, `dialogue_ko`, `dialogue_en`, `notes`, `plot_ko_audio`, `dialogue_ko_audio`
  - Card layout: see TBD

## Workflow

### 1. Generate dialogues (agent)

Generate dialogues via LLM conversation, output to TSV.

Output: `output/dialogue/dialogues.tsv`

LLM prompt template: TBD - needs iteration

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
- Dialogue structure: flexible 3-5 sentences or strict 4-turn A→B→A→B
- Reference [requirements-example.md](../../prompts/requirements-example.md) for dialogue generation inspiration
- LLM prompt template needs iteration

## Background

### Motivation

**Plot→Script approach**: Plot describes turn-by-turn intent, dialogue provides natural realization with discourse connectives.

Key insight: Plot acts as situational index, not translation prompt. User retrieves pre-memorized dialogue chunks, not constructed translations.

### Relation to Existing System

- Complements `Korean::TOPIK1` vocab deck (same vocabulary base)
- Parallels grammar cards in `Korean::Custom` (same KGIU source)
- Different purpose: structural production vs vocabulary recognition

### Research Context

This approach is related to **Discourse Completion Tasks (DCT)** from pragmatics research (Blum-Kulka, 1980s), but extended:
- Traditional DCT: situation → single speech act
- This approach: situation → multi-turn dialogue with discourse structure
