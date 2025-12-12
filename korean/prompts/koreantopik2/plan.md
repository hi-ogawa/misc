# TOPIK 2 Vocabulary Enhancement Plan (Reworked)

**Goal**: Import curated, scored TOPIK 2 vocabulary into Anki with optimal learning order.

## Current State

### Completed
- [x] Base vocabulary extraction (3,873 words)
- [x] Scoring (1-100 scale) - `output/koreantopik2/scores-singleshot100.tsv`
- [x] Curation pass 1+2 (LLM tagging) - `output/koreantopik2/curation-all.tsv` (includes etymology)

### Pending
- [ ] Regenerate examples (all 3,873 words)
- [ ] Regenerate notes (all 3,873 words)
- [ ] Apply curation filter (remove filter=yes)
- [ ] Remove duplicates vs TOPIK 1
- [ ] Sort by score (learning order)
- [ ] Generate audio (new numbering)
- [ ] Anki import

## Pipeline Overview

```
input/koreantopik2.tsv (3,873 words)
    │
    ▼
[Phase 1: Regenerate Enhancements]
    │
    ├── Examples (subagents, 39 batches)
    ├── Notes (subagents, 39 batches)
    │
    ▼
output/koreantopik2/examples-all.tsv
output/koreantopik2/notes-all.tsv
    │
    ├── scores-singleshot100.tsv (priority scores)
    ├── curation-all.tsv (filter tags + etymology)
    │
    ▼
[Phase 2: Filter & Sort]
    │
    ├── Remove filter=yes (~515 words)
    ├── Remove duplicates vs TOPIK 1 (~105 words)
    ├── Sort by score DESC
    ├── Assign new number: koreantopik2_(NNN)_(NNNN)
    │
    ▼
output/koreantopik2/filtered-sorted.tsv (~2,800 words)
    │
    ▼
[Phase 3: Audio Generation]
    │
    ├── korean_{number}.mp3
    ├── example_ko_{number}.mp3
    │
    ▼
[Phase 4: Anki Import]
    │
    ▼
output/koreantopik2/anki-import.tsv
```

## Phase 1: Regenerate Enhancements

Regenerate examples and notes for all 3,873 words (before filtering).

### 1.1 Split into Batches

Use existing batch files:
- `input/koreantopik2-batch-{1..39}.tsv`

### 1.2 Generate Examples (Subagents)

**Prompt**: `prompts/koreantopik2/generate-examples.md`

Per-batch subagent:
1. Read `prompts/requirements-example.md`
2. Read `input/koreantopik2-batch-N.tsv`
3. Write `output/koreantopik2/examples-N.tsv` (overwrites existing)

**Output columns**: number, korean, example_ko, example_en

### 1.3 Generate Notes (Subagents)

**Prompt**: `prompts/koreantopik2/generate-notes.md`

Per-batch subagent:
1. Read `prompts/requirements-notes.md`
2. Read `input/koreantopik2-batch-N.tsv`
3. Write `output/koreantopik2/notes-N.tsv` (overwrites existing)

**Output columns**: number, korean, notes

### 1.4 Consolidate

```bash
# Merge all batch outputs
cat output/koreantopik2/examples-*.tsv > examples-all.tsv
cat output/koreantopik2/notes-*.tsv > notes-all.tsv
```

---

## Phase 2: Filter & Sort

### 2.1 Merge All Data

Join all sources:

```bash
# Merge: input + scores + curation + examples + notes
# Columns: number, korean, english, score, category, filter, etymology, example_ko, example_en, notes
```

### 2.2 Apply Curation Filter

Remove words tagged `filter=yes`:

```bash
python scripts/jq-tsv.py 'select(.filter == "no")' merged.tsv > filtered.tsv
```

**Expected reduction**: ~515 words removed (13.3%)

### 2.3 Remove Duplicates vs TOPIK 1

```bash
# Export TOPIK 1 korean words
python scripts/anki-export.py \
  --query "deck:Korean::TOPIK\ 1" \
  --fields korean \
  --output output/tmp/topik1-vocab.tsv

# Filter out duplicates (by korean field)
# ~105 expected overlaps
```

### 2.4 Sort & Assign New Numbers

Sort by score DESC, assign new number format:

```bash
# Sort by score (high to low)
# Assign: koreantopik2_(NNN)_(NNNN)
# Example: koreantopik2_092_0001, koreantopik2_092_0002, koreantopik2_088_0003...
```

**Number format**: `koreantopik2_(NNN)_(NNNN)`
- `(NNN)` = priority score, 3 digits (042-092)
- `(NNNN)` = sequential index in sorted order (0001, 0002, ...)

**Output**: `output/koreantopik2/filtered-sorted.tsv` (~2,800 words)

**Columns**: number, korean, english, score, etymology, example_ko, example_en, notes

---

## Phase 3: Audio Generation

### 3.1 Generate Audio Files

```bash
# Korean word audio
python scripts/generate-audio.py \
  --input output/koreantopik2/filtered-sorted.tsv \
  --output output/koreantopik2/audio \
  --field korean \
  --id-field number \
  --prefix "korean_"

# Example sentence audio
python scripts/generate-audio.py \
  --input output/koreantopik2/filtered-sorted.tsv \
  --output output/koreantopik2/audio \
  --field example_ko \
  --id-field number \
  --prefix "example_ko_"
```

**File naming**:
- `korean_koreantopik2_085_0001.mp3`
- `example_ko_koreantopik2_085_0001.mp3`

---

## Phase 4: Anki Import

### 4.1 Generate Import File

**Output**: `output/koreantopik2/anki-import.tsv`

**Columns** (9 total):
```
number	korean	english	example_ko	example_en	etymology	notes	korean_audio	example_ko_audio
```

**Sample row**:
```
koreantopik2_092_0001	가능	possible	...	...	可能	...	[sound:korean_koreantopik2_092_0001.mp3]	[sound:example_ko_koreantopik2_092_0001.mp3]
```

### 4.2 Import Steps

```bash
# 1. Copy audio files
cp output/koreantopik2/audio/*.mp3 \
  "$(python scripts/anki.py getMediaDirPath | tr -d '"')"

# 2. Add notes via AnkiConnect
python scripts/anki-add-notes.py \
  --input output/koreantopik2/anki-import.tsv \
  --deck "Korean::TOPIK 2" \
  --model "Korean Vocabulary" \
  --dry-run
```

### 4.3 Import Order

File is pre-sorted by score, so:
1. Import in file order
2. Anki setting: "Show new cards in order added"
3. High-priority words (score 092, 090, 088...) appear first

---

## Phase 5: Maintenance

### 5.1 Fix Workflow

```bash
# Export cards needing fixes
python scripts/anki-export.py \
  --query "deck:Korean::TOPIK\ 2 tag:fix" \
  --output anki/output/topik2-fixes.tsv

# Update via anki-update-notes.py
```

---

## Subagent Strategy

Used for examples and notes regeneration (Phase 1):

- **Why**: Fresh context per batch, parallel execution, no context contamination
- **How**: 39 batches × ~100 words, each agent reads only assigned batch + requirements
- **Files**: `prompts/requirements-*.md` (shared quality requirements)

**Per-batch agent rules**:
- DO NOT read any existing output files
- Generate from scratch based ONLY on requirements + assigned batch
- No shared state between agents

---

## File Summary

| File | Description | Status |
|------|-------------|--------|
| `input/koreantopik2.tsv` | Base vocabulary (3,873) | ✅ |
| `input/koreantopik2-batch-*.tsv` | Pre-split batches (1-39) | ✅ |
| `output/koreantopik2/scores-singleshot100.tsv` | Priority scores | ✅ |
| `output/koreantopik2/curation-all.tsv` | Filter tags + etymology | ✅ |
| `output/koreantopik2/examples-all.tsv` | Regenerated examples | ⏳ Phase 1 |
| `output/koreantopik2/notes-all.tsv` | Regenerated notes | ⏳ Phase 1 |
| `output/koreantopik2/filtered-sorted.tsv` | Filtered & sorted (~2,800) | ⏳ Phase 2 |
| `output/koreantopik2/audio/` | Audio files | ⏳ Phase 3 |
| `output/koreantopik2/anki-import.tsv` | Final import file | ⏳ Phase 4 |

---

## Open Questions

1. **Duplicate handling**: Exact korean match, or also check similar meanings?
2. **Requirements updates**: Any changes to `requirements-example.md` or `requirements-notes.md`?
