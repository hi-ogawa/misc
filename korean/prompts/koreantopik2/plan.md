# TOPIK 2 Vocabulary Enhancement Plan (Reworked)

**Goal**: Import curated, scored TOPIK 2 vocabulary into Anki with optimal learning order.

## Current State

### Completed
- [x] Base vocabulary extraction (3,873 words)
- [x] Scoring (1-100 scale) - `output/koreantopik2/scores-singleshot100.tsv`
- [x] Curation pass 1+2 (LLM tagging) - `output/koreantopik2/curation-all.tsv` (includes etymology)

### Pending
- [x] Regenerate examples (all 3,873 words)
- [ ] ~~Regenerate notes~~ (skipped - blank for now)
- [x] Apply curation filter (remove filter=yes)
- [x] Remove duplicates vs existing Anki cards
- [x] Sort by score (learning order)
- [x] Generate audio (new numbering)
- [x] Anki import

## Pipeline Overview

```
input/koreantopik2.tsv (3,873 words)
    │
    ▼
[Phase 1: Regenerate Enhancements]
    │
    ├── Examples (subagents, 39 batches)
    │
    ▼
output/koreantopik2/examples-all.tsv
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

Regenerate examples for all 3,873 words (before filtering).

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

### 1.3 Notes (Skipped)

Notes field will be blank for initial import. Can be added later if needed.

### 1.4 Consolidate

```bash
python scripts/jq-tsv.py '.' output/koreantopik2/examples-{1..39}.tsv > output/koreantopik2/examples-all.tsv
```

---

## Phase 2: Filter & Sort

### 2.1 Merge All Data

Join all sources by `number`:

```bash
python3 -c "
import csv
import sys

def read_tsv(path, key='number'):
    with open(path) as f:
        return {row[key]: row for row in csv.DictReader(f, delimiter='\t')}

base = read_tsv('input/koreantopik2.tsv')
scores = read_tsv('output/koreantopik2/scores-singleshot100.tsv')
curation = read_tsv('output/koreantopik2/curation-all.tsv')
examples = read_tsv('output/koreantopik2/examples-all.tsv')

rows = []
for num in sorted(base.keys(), key=int):
    row = {
        'number': num,
        'korean': base[num]['korean'],
        'english': base[num]['english'],
        'score': scores.get(num, {}).get('score', ''),
        'etymology': curation.get(num, {}).get('etymology', ''),
        'category': curation.get(num, {}).get('category', ''),
        'filter': curation.get(num, {}).get('filter', ''),
        'example_ko': examples.get(num, {}).get('example_ko', ''),
        'example_en': examples.get(num, {}).get('example_en', ''),
    }
    rows.append(row)

cols = ['number', 'korean', 'english', 'score', 'etymology', 'category', 'filter', 'example_ko', 'example_en']
writer = csv.DictWriter(sys.stdout, fieldnames=cols, delimiter='\t')
writer.writeheader()
writer.writerows(rows)
" > output/koreantopik2/merged.tsv
```

**Output**: `output/koreantopik2/merged.tsv` (3874 lines = 3873 + header)

### 2.2 Apply Curation Filter

Remove words tagged `filter=yes`:

```bash
python scripts/jq-tsv.py 'select(.filter == "no")' output/koreantopik2/merged.tsv > output/koreantopik2/filtered.tsv
```

**Output**: `output/koreantopik2/filtered.tsv` (3359 lines = 3358 + header)
**Removed**: 515 words (13.3%)

### 2.3 Remove Duplicates vs Existing Anki Cards

**Note**: Many overlapping words are homonyms (different meanings) - these should be kept.

#### Step 1: Export existing Anki cards

```bash
python scripts/anki-export.py \
  --query "deck:Korean korean:_*" \
  --fields number,korean,english > output/tmp/korean-all.tsv
```

#### Step 2: Generate review file

```bash
python3 -c "
import csv
from collections import defaultdict

anki = defaultdict(list)
with open('output/tmp/korean-all.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        anki[row['korean']].append(row['english'])

topik2 = defaultdict(list)
with open('output/koreantopik2/filtered.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        topik2[row['korean']].append(row['english'])

print('korean\tanki_meanings\ttopik2_meanings')
for k in sorted(set(anki.keys()) & set(topik2.keys())):
    a = ' / '.join(anki[k])
    t2 = ' / '.join(topik2[k])
    print(f'{k}\t{a}\t{t2}')
" > output/koreantopik2/duplicates-review.tsv
```

**Output**: `output/koreantopik2/duplicates-review.tsv` (229 unique overlapping words)

#### Step 2b: Auto-detect duplicates vs homonyms

```bash
python3 -c "
import csv
from collections import defaultdict

anki = defaultdict(list)
with open('output/tmp/korean-all.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        anki[row['korean']].append(row['english'].lower())

topik2 = defaultdict(list)
with open('output/koreantopik2/filtered.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        topik2[row['korean']].append(row['english'].lower())

def meanings_overlap(list1, list2):
    for m1 in list1:
        words1 = set(m1.replace(',', ' ').replace('/', ' ').split())
        for m2 in list2:
            words2 = set(m2.replace(',', ' ').replace('/', ' ').split())
            common = words1 & words2
            if [w for w in common if len(w) > 2]:
                return True
            if m1 in m2 or m2 in m1:
                return True
    return False

print('korean\tanki_meanings\ttopik2_meanings\tduplicate')
for k in sorted(set(anki.keys()) & set(topik2.keys())):
    is_dup = 'yes' if meanings_overlap(anki[k], topik2[k]) else 'no'
    print(f'{k}\t{\" / \".join(anki[k])}\t{\" / \".join(topik2[k])}\t{is_dup}')
" > output/koreantopik2/duplicates-review.tsv
```

Auto-detection logic: marks as duplicate if meanings share any word >2 chars or one is substring of other.

#### Step 3: Manual review

Review `duplicates-review.tsv` and mark `duplicate` column as `yes` (remove) or `no` (keep).
Save as `output/koreantopik2/duplicates-remove.tsv`.

#### Step 4: Apply removal

```bash
python3 -c "
import csv
import sys

remove = set()
with open('output/koreantopik2/duplicates-remove.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        if row['duplicate'] == 'yes':
            remove.add(row['korean'])

with open('output/koreantopik2/filtered.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    rows = [row for row in reader if row['korean'] not in remove]

cols = reader.fieldnames
writer = csv.DictWriter(sys.stdout, fieldnames=cols, delimiter='\t')
writer.writeheader()
writer.writerows(rows)
" > output/koreantopik2/deduped.tsv
```

**Stats**:
- Overlapping words reviewed: 229
- Marked as duplicate (same meaning): 157
- Marked as homonym (different meaning): 72
- Entries removed: 177 (some words had multiple TOPIK 2 entries)

**Output**: `output/koreantopik2/deduped.tsv` (3180 lines = 3179 + header)

### 2.4 Sort & Assign New Numbers

```bash
python3 -c "
import csv
import sys

with open('output/koreantopik2/deduped.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    rows = list(reader)

rows.sort(key=lambda r: int(r['score']), reverse=True)

for i, row in enumerate(rows, 1):
    score = row['score'].zfill(3)
    idx = str(i).zfill(4)
    row['number'] = f'koreantopik2_{score}_{idx}'

cols = ['number', 'korean', 'english', 'score', 'etymology', 'example_ko', 'example_en']
writer = csv.DictWriter(sys.stdout, fieldnames=cols, delimiter='\t', extrasaction='ignore')
writer.writeheader()
writer.writerows(rows)
" > output/koreantopik2/filtered-sorted.tsv
```

**Number format**: `koreantopik2_(NNN)_(NNNN)`
- `(NNN)` = priority score, 3 digits (042-092)
- `(NNNN)` = sequential index in sorted order (0001, 0002, ...)

**Output**: `output/koreantopik2/filtered-sorted.tsv` (3180 lines = 3179 + header)

**Columns**: number, korean, english, score, etymology, example_ko, example_en

**Sample**:
```
koreantopik2_092_0001  가능      possible    92
koreantopik2_092_0002  가능성    possibility 92
koreantopik2_090_0003  확실히    certainly   90
...
koreantopik2_042_3179  가뭄      drought     42
```

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
  --prefix "korean_" \
  --concurrency 10

# Example sentence audio
python scripts/generate-audio.py \
  --input output/koreantopik2/filtered-sorted.tsv \
  --output output/koreantopik2/audio \
  --field example_ko \
  --id-field number \
  --prefix "example_ko_" \
  --concurrency 10
```

**File naming**:
- `korean_koreantopik2_085_0001.mp3`
- `example_ko_koreantopik2_085_0001.mp3`

---

## Phase 4: Anki Import

### 4.1 Generate Import File

```bash
python3 -c "
import csv
import sys

with open('output/koreantopik2/filtered-sorted.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    rows = list(reader)

for row in rows:
    num = row['number']
    row['korean_audio'] = f'[sound:korean_{num}.mp3]'
    row['example_ko_audio'] = f'[sound:example_ko_{num}.mp3]'

cols = ['number', 'korean', 'english', 'example_ko', 'example_en', 'etymology', 'korean_audio', 'example_ko_audio']
writer = csv.DictWriter(sys.stdout, fieldnames=cols, delimiter='\t', extrasaction='ignore')
writer.writeheader()
writer.writerows(rows)
" > output/koreantopik2/anki-import.tsv
```

**Output**: `output/koreantopik2/anki-import.tsv` (3180 lines = 3179 + header)

**Columns** (8 total):
```
number	korean	english	example_ko	example_en	etymology	korean_audio	example_ko_audio
```

**Sample row**:
```
koreantopik2_092_0001	가능	possible	...	...	可能	[sound:korean_koreantopik2_092_0001.mp3]	[sound:example_ko_koreantopik2_092_0001.mp3]
```

### 4.2 Import Steps

```bash
# 1. Copy audio files to Anki media folder
cp output/koreantopik2/audio/*.mp3 \
  "$(python scripts/anki.py getMediaDirPath | tr -d '"')"
```

2. In Anki GUI: File → Import → select `output/koreantopik2/anki-import.tsv`
   - Deck: `Korean::TOPIK 2`
   - Note type: `Korean Vocabulary`
   - Field mapping: match columns to fields

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

Used for examples regeneration (Phase 1):

- **Why**: Fresh context per batch, parallel execution, no context contamination
- **How**: 39 batches × ~100 words, each agent reads only assigned batch + requirements
- **Files**: `prompts/requirements-example.md` (quality requirements)

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
| `output/koreantopik2/examples-all.tsv` | Regenerated examples | ✅ |
| `output/koreantopik2/notes-all.tsv` | ~~Regenerated notes~~ | ⏭️ Skipped |
| `output/koreantopik2/filtered-sorted.tsv` | Filtered & sorted (3,179) | ✅ |
| `output/koreantopik2/audio/` | Audio files (6,358) | ✅ |
| `output/koreantopik2/anki-import.tsv` | Final import file | ✅ |

---

## Open Questions

1. **Duplicate handling**: Exact korean match, or also check similar meanings?
