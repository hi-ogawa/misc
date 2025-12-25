# Import Filtered Vocab as Suspended

**Goal**: Import previously filtered-out TOPIK 2 vocabulary into Anki as suspended cards.

**Status**: ✅ Complete (2025-12-25)

## Context

During initial import, ~700 words were filtered out:
- ~515 words: `filter=yes` (trivial loanwords, compositional compounds)
- ~177 entries: duplicates vs existing Anki cards

These should still be available for reference/study, just not in active rotation.

**Scope**: Minimal import (korean/english only). No examples or audio for now.

## Approach

Derive filtered-out set by comparing:
- **Original**: `input/koreantopik2.tsv` (3,873 words)
- **Imported**: Export from Anki (koreantopik2_* cards)
- **Filtered out** = Original - Imported

## Pipeline

```
input/koreantopik2.tsv (3,873)
        │
        ├── Export current Anki koreantopik2 cards
        │
        ▼
[Step 1: Identify filtered-out words]
        │
        ▼
output/koreantopik2/suspended-candidates.tsv (~700)
        │
        ▼
[Step 2: Create import file]
        │
        ▼
output/koreantopik2/suspended-anki-import.tsv
        │
        ▼
[Step 3: Import + Suspend via AnkiConnect]
```

---

## Step 1: Identify Filtered-Out Words

### 1.1 Export current Anki cards

```bash
python scripts/anki-export.py \
  --query "deck:Korean number:koreantopik2_*" \
  --fields number,korean,english > output/tmp/koreantopik2-in-anki.tsv
```

### 1.2 Find words not in Anki

Check by korean+english pair to handle homonyms correctly.

```bash
python3 -c "
import csv

# Load Anki cards (by korean+english pair)
anki_pairs = set()
with open('output/tmp/koreantopik2-in-anki.tsv') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        anki_pairs.add((row['korean'], row['english']))

# Find original words not in Anki
with open('input/koreantopik2.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    rows = [row for row in reader if (row['korean'], row['english']) not in anki_pairs]

# Output
cols = ['number', 'korean', 'english']
writer = csv.DictWriter(__import__('sys').stdout, fieldnames=cols, delimiter='\t')
writer.writeheader()
writer.writerows(rows)
" > output/koreantopik2/suspended-candidates.tsv
```

**Expected**: ~700 words (515 curation + ~200 duplicates, minus overlap)

**Actual**: 761 words

### 1.3 Verify count

```bash
wc -l output/koreantopik2/suspended-candidates.tsv
# Should be ~700 lines (+ header)
```

---

## Step 2: Create Import File

Assign new numbers: `koreantopik2_000_NNNN` (000 = score 0, low priority)

Continue from last number in Anki to maintain unique sequence.

```bash
# Find last number in Anki
awk -F'\t' 'NR>1 {print $1}' output/tmp/koreantopik2-in-anki.tsv | grep -oP '\d{4}$' | sort -n | tail -1
# Example: 3179 → start from 3180

# Generate import file
python3 -c "
import csv
import sys

with open('output/koreantopik2/suspended-candidates.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    rows = list(reader)

start = 3180  # last Anki number + 1
for i, row in enumerate(rows):
    row['number'] = f'koreantopik2_000_{str(start + i).zfill(4)}'

cols = ['number', 'korean', 'english']
writer = csv.DictWriter(sys.stdout, fieldnames=cols, delimiter='\t', extrasaction='ignore')
writer.writeheader()
writer.writerows(rows)
" > output/koreantopik2/suspended-anki-import.tsv
```

---

## Step 3: Import + Suspend

### 3.1 Import via GUI

File → Import → select `output/koreantopik2/suspended-anki-import.tsv`
- Deck: `Korean::TOPIK 2`
- Note type: `Korean Vocabulary`
- Map columns: number, korean, english (leave other fields empty)

### 3.2 Suspend via GUI

- query by `number:koreantopik2_000_*`
- select all
- suspend

### 3.3 Verify

```bash
# Count suspended cards
python scripts/anki.py findCards \
  --params '{"query": "deck:Korean number:koreantopik2_000_* is:suspended"}' \
  | jq 'length'
# Should be 761
```

---

## Alternative: Import via AnkiConnect

Can use `addNotes` action to import directly:

```bash
python3 -c "
import csv
import json

with open('output/koreantopik2/suspended-anki-import.tsv') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))

notes = []
for row in rows:
    notes.append({
        'deckName': 'Korean::TOPIK 2',
        'modelName': 'Korean Vocabulary',
        'fields': {
            'number': row['number'],
            'korean': row['korean'],
            'english': row['english'],
        },
        'options': {'allowDuplicate': False},
        'tags': ['suspended-import'],
    })

print(json.dumps({'notes': notes}, ensure_ascii=False))
" > output/tmp/suspended-notes-payload.json

# Add notes
python scripts/anki.py addNotes --params \"\$(cat output/tmp/suspended-notes-payload.json)\"
```

Then suspend as in 3.2.

---

## Summary

| Step | Output | Status |
|------|--------|--------|
| 1. Identify filtered | `suspended-candidates.tsv` (761) | ✅ |
| 2. Create import | `suspended-anki-import.tsv` (koreantopik2_000_3180-3940) | ✅ |
| 3. Import + suspend | 761 cards in Anki (suspended) | ✅ |

---

## Future Enhancements

Can add later if needed:
- Examples (example_ko, example_en)
- Audio (korean_audio, example_ko_audio)
- Etymology
- Notes with filtering reason
