# Tag Cards by Origin and POS

**Goal**: Add systematic tags to TOPIK 2 cards for priority-based study.

## Tags

### Origin (from existing curation category)

| Tag | Curation cat | Description |
|-----|--------------|-------------|
| `origin::native` | 7 | Pure Korean, no etymology |
| `origin::hanja` | 1 | Sino-Korean |
| `origin::compound` | 4 | Native/hybrid compound |
| `origin::derivation` | 2, 3 | Auxiliary/passive/causative |
| `origin::loanword` | 5 | Foreign borrowing |
| `origin::contraction` | 6 | Shortened form |

### POS (Part of Speech)

| Tag | Detection | Examples |
|-----|-----------|----------|
| `pos::verb` | ends in 다 (action or descriptive) | 겪다, 견디다, 굉장하다 |
| `pos::noun` | default, no verb ending | 순간, 가치 |
| `pos::adverb` | ends in 히/이/로, or standalone modifier | 확실히, 겨우, 꽤 |
| `pos::interjection` | standalone sounds | 하하, 앗 |

**Note**: Korean adjectives (형용사) conjugate like verbs, so we treat them as `pos::verb`. Both are 용언 (predicates).

## Priority Matrix

| Origin | POS | Priority | Reason |
|--------|-----|----------|--------|
| native | verb | **High** | Must learn, no alternative |
| native | adverb | **High** | Must learn, no alternative |
| native | noun | Medium | Some guessable from context |
| hanja | any | Medium | Hanja knowledge helps |
| derivation | any | Low | Predictable from root |
| loanword | any | Low | Often guessable |
| contraction | any | Low | Learn naturally |
| any | interjection | Low | Suspend |

## Data Sources

- **Curation data**: `output/koreantopik2/curation-all.tsv` (has category column)
- **Anki cards**: Export via anki-export.py

## Implementation

### Step 1: Export Anki cards

```bash
python scripts/anki-export.py \
  --query "deck:Korean::TOPIK2 -is:suspended" \
  --fields "noteId,number,korean,english" \
  --output output/tmp/topik2-cards.tsv
```

### Step 2: POS classification (subagent)

Subagent only classifies POS - category→origin mapping is done by script.

**Input**: `output/tmp/topik2-cards.tsv` (split into batches)

**Subagent prompt**:
````
Classify part of speech for Korean vocabulary batch N.

## Task

Read batch file and add `pos` column.

## POS Tags

| pos | Description | Examples |
|-----|-------------|----------|
| pos::verb | Action or descriptive, ends in 다 | 겪다, 견디다, 굉장하다 |
| pos::noun | Thing, concept, person | 순간, 가치, 경제 |
| pos::adverb | Modifies verb | 겨우, 꽤, 문득, 확실히 |
| pos::interjection | Standalone sound | 하하, 앗, 아이고 |

## Guidelines

1. Korean adjectives (형용사) → `pos::verb` (both are 용언)
2. Adverbs include 히/이/로 endings + standalone modifiers (겨우, 꽤, 막)
3. Default to `pos::noun` only if clearly a thing/concept

## Output

TSV with columns: noteId, number, korean, english, pos
````

**Output**: `output/tmp/topik2-pos.tsv`

### Step 3: Join with curation data and map origin

```bash
python3 << 'EOF'
import csv

ORIGIN_MAP = {
    '1': 'origin::hanja',
    '2': 'origin::derivation',
    '3': 'origin::derivation',
    '4': 'origin::compound',
    '5': 'origin::loanword',
    '6': 'origin::contraction',
    '7': 'origin::native',
}

# Load curation data (korean → category)
curation = {}
with open('output/koreantopik2/curation-all.tsv') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        curation[row['korean']] = row['category']

# Load POS classification
with open('output/tmp/topik2-pos.tsv') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))

# Join and map
for row in rows:
    category = curation.get(row['korean'], '')
    row['origin'] = ORIGIN_MAP.get(category, '')

# Output
with open('output/tmp/topik2-tagged.tsv', 'w') as f:
    cols = ['noteId', 'number', 'korean', 'english', 'origin', 'pos']
    writer = csv.DictWriter(f, fieldnames=cols, delimiter='\t')
    writer.writeheader()
    writer.writerows(rows)
EOF
```

### Step 4: Update Anki

```bash
# Dry run first
python scripts/anki-update-notes.py \
  --input output/tmp/topik2-tagged.tsv \
  --add-tags origin,pos \
  --dry-run

# Execute
python scripts/anki-update-notes.py \
  --input output/tmp/topik2-tagged.tsv \
  --add-tags origin,pos
```

## Usage in Anki

### Filtered deck for high-priority
```
deck:Korean::TOPIK2 tag:origin::native tag:pos::verb
```

### Custom study sessions
- Native verbs first: `tag:origin::native (tag:pos::verb OR tag:pos::adverb)`
- Skip derivations: `-tag:origin::derivation`

## Output

Final tagged file:
```
output/tmp/topik2-tagged.tsv
Columns: noteId, number, korean, english, category, pos, tags
```

## Notes

- Origin tags from existing curation data (no new LLM pass needed)
- POS tags via subagent classification (handles standalone adverbs accurately)
- Korean adjectives treated as verbs (both 용언)
