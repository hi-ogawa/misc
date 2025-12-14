# Check Sino-Korean Word Families

Find cards sharing the same Sino-Korean root with different derivations (하다, 히, etc.) to reduce redundancy.

## Context

- TOPIK 2 data was pre-filtered for similar meanings during curation
  - `prompts/koreantopik2/plan-curation.md`
- This check catches a different type of redundancy: **same root, different grammatical form**
- Targets existing Anki deck (post-import)

## Goal

Identify word families like:
- 솔직하다 / 솔직히
- 확실하다 / 확실히
- 충분하다 / 충분히

These are essentially the same vocabulary item in different grammatical forms.
Bare root (e.g., 솔직) may not exist - dataset is usage-based, not systematic.

## Target Patterns

Focus on high-frequency, predictable derivations:

| Suffix | Type | Example |
|--------|------|---------|
| (bare) | Noun | 확실, 충분 |
| 하다 | Verb/Adj | 확실하다, 충분하다 |
| 히 | Adverb | 확실히, 충분히 |
| 되다 | Passive | 확인되다 |

Skip less common/different concepts: 적, 성, 화, 시키다

## Approach

1. Export all Korean words from deck
2. Extract potential Sino-Korean root by stripping suffixes:
   - 하다$ → root (솔직하다 → 솔직)
   - 히$ → root (솔직히 → 솔직)
   - 되다$ → root (확인되다 → 확인)
3. Group by extracted root
4. Filter to groups with 2+ cards (word families)
5. Review and decide: keep one form or keep all

**Note**: The bare root form (e.g., 솔직) may not exist in deck.
Dataset is hand-curated based on practical usage, not systematic.

## Usage

```bash
# Step 1: Export (with noteId for direct deletion)
python scripts/anki-export.py \
  --query "deck:Korean korean:_*" \
  --fields noteId,number,korean,english,example_ko,example_en > output/tmp/korean-all.tsv

# Step 2: Extract roots and group word families
python3 -c "
import csv
import json
from collections import defaultdict

SUFFIXES = [
    ('하다', 'verb'),
    ('되다', 'passive'),
    ('히', 'adverb'),
]

def extract_root(word):
    for suffix, stype in SUFFIXES:
        if word.endswith(suffix):
            root = word[:-len(suffix)]
            if len(root) >= 2:
                return root, stype
    return None, None

bare_words = defaultdict(list)
families = defaultdict(list)

with open('output/tmp/korean-all.tsv') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        word = row['korean']
        entry = {
            'noteId': row['noteId'],
            'number': row['number'],
            'korean': word,
            'english': row['english'],
            'example_ko': row.get('example_ko', ''),
            'example_en': row.get('example_en', ''),
        }

        root, stype = extract_root(word)
        if root:
            entry['type'] = stype
            families[root].append(entry)
        else:
            bare_words[word].append(entry)

for root, entries in list(families.items()):
    if root in bare_words:
        for bare_entry in bare_words[root]:
            bare_entry['type'] = 'bare'
            entries.insert(0, bare_entry)

result = [
    {'root': root, 'count': len(entries), 'entries': entries}
    for root, entries in sorted(families.items())
    if len(entries) >= 2
]
print(json.dumps(result, ensure_ascii=False, indent=2))
" > output/tmp/word-families.json

# Step 3: Review
jq -r '.[] | .root + ": " + ([.entries[] | .korean + "(" + .english + ")"] | join(", "))' \
  output/tmp/word-families.json

# Step 4: Manual review
# Copy to .jsonc and comment out entries to delete
cp output/tmp/word-families.json output/tmp/word-families-review.jsonc
# Edit word-families-review.jsonc, comment out entries to remove

# Step 5: Extract note IDs to delete (from commented lines)
grep -E '^\s*//' output/tmp/word-families-review.jsonc | \
  grep -oP '"noteId":\s*"\K[^"]+' > output/tmp/notes-to-delete.txt

# Step 6: Delete notes from Anki via AnkiConnect
python scripts/anki.py deleteNotes --params "{\"notes\": $(jq -Rs 'split("\n") | map(select(. != "") | tonumber)' output/tmp/notes-to-delete.txt)}"
```

## Results (2024-12-13)

**52 word families found** from 5,280 cards.

### By pattern type

| Pattern | Count | Example |
|---------|-------|---------|
| bare + 하다 | 25 | 건조 + 건조하다 |
| 히 + 하다 | 16 | 확실히 + 확실하다 |
| bare + 히 | 5 | 완전 + 완전히 |
| bare + 되다 | 2 | 당첨 + 당첨되다 |
| bare + 하다 + 히 | 2 | 가득 + 가득하다 + 가득히 |
| 하다 + 되다 | 1 | 비롯하다 + 비롯되다 |
| bare + 하다 + 되다 | 1 | 잘못 + 잘못하다 + 잘못되다 |

### Full list (with meanings)

```
가득: 가득(full), 가득하다(full), 가득히(fully)
간단: 간단하다(simple), 간단히(simply)
건조: 건조(dry), 건조하다(to be dry)
공지: 공지(notice), 공지하다(to announce, notify)
관리: 관리(management), 관리하다(to manage, to maintain)
굉장: 굉장히(very, extremely), 굉장하다(wonderful, awesome)
그만: 그만(stop), 그만하다(stop)
꼼꼼: 꼼꼼하다(meticulous, careful), 꼼꼼히(carefully)
꾸준: 꾸준하다(steady), 꾸준히(steadily)
당첨: 당첨(winning), 당첨되다(to win (lottery))
당황: 당황(embarrassment), 당황하다(to be flustered, confused)
등록: 등록(registration), 등록하다(to register; to enroll)
등장: 등장(appearance), 등장하다(to appear; to enter)
똑똑: 똑똑하다(smart), 똑똑히(clearly)
마땅: 마땅하다(proper, suitable), 마땅히(rightly)
발달: 발달(develop), 발달하다(to develop, to advance)
보관: 보관(keep), 보관하다(to store, keep)
부지런: 부지런하다(diligent), 부지런히(diligently)
분명: 분명(certainly), 분명하다(clear)
비롯: 비롯하다(include, begin), 비롯되다(come from, be originated)
사과: 사과(apologize), 사과(apple), 사과하다(to apologize)
상당: 상당히(pretty), 상당하다(considerable)
소중: 소중하다(precious), 소중히(valuably)
솔직: 솔직히(honestly), 솔직하다(honest)
신고: 신고(declaration), 신고하다(to report)
실망: 실망(disappointment), 실망하다(to be disappointed)
안녕: 안녕(hi), 안녕히(bye)
안심: 안심(relief), 안심하다(to feel relieved, to be at ease)
오래: 오래(long), 오래되다(get old)
완전: 완전(perfect), 완전히(completely)
우연: 우연(accident), 우연히(by chance)
인쇄: 인쇄(printing), 인쇄하다(to print)
자세: 자세(posture), 자세히(details), 자세하다(detailed)
자연: 자연(nature), 자연히(naturally)
잘못: 잘못(wrong), 잘못되다(be wrong), 잘못하다(do wrong)
적당: 적당하다(suitable), 적당히(moderately)
정직: 정직(honesty), 정직하다(to be honest)
정확: 정확(exactness), 정확히(exactly)
제출: 제출(submission), 제출하다(to submit)
조용: 조용하다(quiet), 조용히(quietly)
참석: 참석(attendance; participation), 참석하다(to attend)
참여: 참여(participation), 참여하다(to participate)
체험: 체험(experience), 체험하다(to experience)
충분: 충분하다(enough), 충분히(fully)
토론: 토론(debate), 토론하다(to discuss, debate)
통과: 통과(pass), 통과하다(to pass (through))
특별: 특별하다(special), 특별히(especially)
화해: 화해(reconciliation), 화해하다(to make up, reconcile)
확실: 확실히(certainly), 확실하다(certain)
활발: 활발히(actively), 활발하다(animated)
후회: 후회(regret), 후회하다(to regret)
훈련: 훈련(training), 훈련하다(to train; to practice)
```

### Review notes

- 사과: Includes homonym (apple) - only 사과(apologize)+사과하다 are redundant
- 안녕/안녕히: Common greeting pair - may want to keep both
- 그만, 오래: May have distinct usage patterns

### Deletion decisions (2024-12-14)

**41 cards to delete** (koreantopik2_* only, non-koreantopik2 cards deferred)

| Deleted form | Kept form | Count | Examples |
|--------------|-----------|-------|----------|
| bare noun | 하다 verb | 25 | 건조→건조하다, 공지→공지하다, 관리→관리하다 |
| 히 adverb | 하다 verb | 9 | 꼼꼼히→꼼꼼하다, 꾸준히→꾸준하다, 충분히→충분하다 |
| 하다 verb | 히 adverb | 4 | 솔직하다→솔직히, 확실하다→확실히, 활발하다→활발히 |
| 하다 verb | bare noun | 2 | 가득하다→가득, 그만하다→그만 |
| bare noun | 되다 passive | 1 | 당첨→당첨되다 |

**Kept both forms** (13 families):
- 간단하다/간단히 - both common forms
- 굉장히/굉장하다 - different nuances (adverb=very, adj=wonderful)
- 똑똑하다/똑똑히 - different meanings (smart vs clearly)
- 마땅하다/마땅히 - both useful
- 비롯하다/비롯되다 - active vs passive voice
- 안녕/안녕히 - common greeting pair
- 오래/오래되다 - different usage patterns
- 잘못/잘못되다/잘못하다 - 3 distinct uses
- 적당하다/적당히 - both common
- 조용하다/조용히 - both very common
- 참석/참석하다 - both common
- 특별하다/특별히 - both common
- 자세(posture)/자세히 - different root meanings

## Decision Criteria

**Keep one form** when:
- Both forms exist and meanings are identical
- Example: 확실하다 + 확실히 → keep 확실하다 (can derive 확실히)

**Keep both** when:
- Different nuances or usage contexts
- One form is significantly more common in practice

## Notes

- Only targets Sino-Korean (한자어) - native Korean derivations are irregular
- 히 adverbs only work with descriptive 하다 (형용사), not action verbs
- 공부하다 → 공부히 ❌ (action verb)
- 확실하다 → 확실히 ✓ (descriptive)
