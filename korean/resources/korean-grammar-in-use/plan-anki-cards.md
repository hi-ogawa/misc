# Plan: Anki Cards for Grammar Gaps

Generate Anki cards for the 21 grammar patterns identified in `gap-analysis.md`.

## Overview

- **Source**: `gap-analysis.md` (21 patterns marked `#` or `@`)
- **Target**: `Korean::Custom` deck with `grammar` tag
- **Note model**: Existing "Korean Vocabulary" model

## File Structure

```
resources/korean-grammar-in-use/
├── gap-analysis.md              # Source: 21 gap patterns
├── output/
│   ├── grammar-cards.tsv        # Step 1: Extracted patterns with examples
│   └── audio/                   # Step 2: Generated audio
│       └── grammar_example_ko_*.mp3
└── plan-anki-cards.md           # This file
```

## Field Mapping

| Field | Content | Example |
|-------|---------|---------|
| `number` | `grammar_01`, `grammar_02`, ... | `grammar_01` |
| `korean` | Pattern | `N(이)나` |
| `english` | Meaning (disambiguate if needed) | or (choice between options) |
| `example_ko` | Korean sentence | 시간이 없어서 커피나 차를 빨리 골라야 해요 |
| `example_en` | English translation | I don't have time so I need to quickly choose coffee or tea |
| `etymology` | (empty) | |
| `notes` | Related/contrasting patterns | `N처럼` |

## TSV Format

**Output**: `output/grammar-cards.tsv` (7 columns, tab-separated)

```
number	korean	english	example_ko	example_en	etymology	notes
grammar_01	N(이)나	or (choice between options)	시간이 없어서 커피나 차를 빨리 골라야 해요	I don't have time so I need to quickly choose coffee or tea
grammar_02	N(이)나	as many as (large quantity)	...	...
```

## Example Sentence Guidelines

Reference `prompts/requirements-example.md`:
- Multi-clause sentences (reason, time, purpose connectives)
- Concrete, visualizable context
- Explicit subjects/objects (no ellipsis)
- Show characteristic usage of the grammar pattern

## Notes Field Guidelines

Reference `prompts/requirements-notes.md` for inspiration. For grammar patterns:
- Similar patterns: `N같이` → `N처럼`
- Contrasting patterns: `A/V-겠어요 (intention)` vs `A/V-겠어요 (conjecture)`
- Related suggestions: `V-(으)ㅂ시다` → `V-(으)ㄹ까요?`
- Leave blank if no meaningful association

## Audio Generation

**Script**: `scripts/generate-audio.py`

**Command**:
```bash
python scripts/generate-audio.py \
  --input resources/korean-grammar-in-use/output/grammar-cards.tsv \
  --output resources/korean-grammar-in-use/output/audio \
  --field example_ko \
  --prefix grammar_example_ko_
```

**Output**: 21 files → `grammar_example_ko_0001.mp3` ... `grammar_example_ko_0021.mp3`

**Audio fields**:
- `korean_audio`: (empty - pattern notation not TTS-friendly)
- `example_ko_audio`: `[sound:grammar_example_ko_0001.mp3]`

## Anki Import

> **⚠️ DRAFT** - This section is incomplete. Revisit when ready to import.

1. Copy audio to Anki media folder
2. Import TSV to `Korean::Custom` deck with `grammar` tag
3. TBD: exact commands/steps

## Steps

1. [ ] Extract 21 patterns from `gap-analysis.md` to `output/grammar-cards.tsv`
2. [ ] Generate example sentences following guidelines
3. [ ] Generate audio: `scripts/generate-audio.py`
4. [ ] Copy audio to Anki media folder
5. [ ] Import to Anki via AnkiConnect or manual import
6. [ ] Verify cards in Anki

## Source Patterns

From `gap-analysis.md`:

| # | Pattern | Meaning | Page |
|---|---------|---------|------|
| 01 | N(이)나 | or (choice) | 105 |
| 02 | N(이)나 | as many as | 107 |
| 03 | N쯤 | about/around | 110 |
| 04 | N처럼, N같이 | like | 112 |
| 05 | A/V-거나 | or (alternative actions) | 123 |
| 06 | V-(으)ㄴ 지 | since (time elapsed) | 157 |
| 07 | V-아/어 주시겠어요? | please do (polite) | 198 |
| 08 | V-(으)니까 | when/upon | 235 |
| 09 | V-기로 하다 | decide to | 248 |
| 10 | V-(으)려면 | if you want to | 255 |
| 11 | A/V-겠어요 | must be (conjecture) | 260 |
| 12 | A-아/어하다 | emotion verb pattern | 281 |
| 13 | V-아/어 있다 | resultant state | 287 |
| 14 | A/V-지요? | right? (confirmation) | 301 |
| 15 | A/V-군요/는군요 | I see! (discovery) | 304 |
| 16 | A-(으)ㄴ가요?, V-나요? | question form | 310 |
| 17 | Indirect Quotation Contracted | shortened reported speech | 322 |
| 18 | A/V-지 않아도 되다 | don't need to | 179 |
| 19 | A/V-았/었으면 좋겠다 | I hope/wish | 184 |
| 20 | V-(으)ㄴ 적이 있다/없다 | have done before | 207 |
| 21 | V-(으)ㅂ시다 | let's (formal) | 214 |
| 22 | V-(으)시겠어요? | would you like? | 217 |
| 23 | A/V-겠어요 | I will (intention) | 222 |
