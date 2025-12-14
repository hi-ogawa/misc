#!/usr/bin/env python3
"""Analyze vocabulary dataset for redundancy patterns.

Usage:
    python scripts/analyze-redundancy.py output/tmp/korean-all.tsv
"""

import argparse
import csv
import re
import sys
from collections import defaultdict


def load_data(filepath):
    """Load TSV with korean, english, number fields."""
    words = {}
    with open(filepath) as f:
        for row in csv.DictReader(f, delimiter='\t'):
            words[row['korean']] = row
    return words


def find_verb_auxiliaries(words):
    """Pattern 1: Verb + auxiliary (가져가다, 먹어보다)."""
    pattern = re.compile(r'(.+)(아|어|여)(가다|오다|보다|버리다|주다|놓다|두다)$')
    matches = []
    for w, v in words.items():
        m = pattern.match(w)
        if m:
            stem, connector, aux = m.groups()
            matches.append({
                'word': w,
                'english': v['english'],
                'stem': stem,
                'auxiliary': aux,
            })
    return matches


def find_compound_overlap(words):
    """Pattern 2: Root exists and root+suffix exists."""
    suffixes = ['약', '집', '객', '지', '비', '물', '증', '권', '장', '실', '관', '원', '점']
    matches = []
    for w, v in words.items():
        for suffix in suffixes:
            if len(w) > len(suffix) + 1 and w.endswith(suffix):
                root = w[:-len(suffix)]
                if root in words:
                    matches.append({
                        'word': w,
                        'english': v['english'],
                        'root': root,
                        'root_english': words[root]['english'],
                        'suffix': suffix,
                    })
                    break
    return matches


def find_passive_causative(words):
    """Pattern 3: Passive/causative derivation with base verb."""
    # Known pairs (more reliable than pattern matching)
    known_pairs = [
        ('보이다', '보다'), ('들리다', '듣다'), ('잡히다', '잡다'),
        ('읽히다', '읽다'), ('먹히다', '먹다'), ('닫히다', '닫다'),
        ('열리다', '열다'), ('팔리다', '팔다'), ('풀리다', '풀다'),
        ('끊기다', '끊다'), ('안기다', '안다'), ('쫓기다', '쫓다'),
        ('눕히다', '눕다'), ('앉히다', '앉다'), ('숨기다', '숨다'),
        ('깨우다', '깨다'), ('낮추다', '낮다'), ('높이다', '높다'),
        ('넓히다', '넓다'), ('늦추다', '늦다'), ('맞추다', '맞다'),
    ]
    matches = []
    for derived, base in known_pairs:
        if derived in words and base in words:
            matches.append({
                'word': derived,
                'english': words[derived]['english'],
                'base': base,
                'base_english': words[base]['english'],
            })
    return matches


def find_honorific_pairs(words):
    """Pattern 4: Plain/honorific verb pairs."""
    pairs = [
        ('먹다', '드시다'), ('자다', '주무시다'), ('있다', '계시다'),
        ('말하다', '말씀하시다'), ('죽다', '돌아가시다'), ('보다', '뵙다'),
        ('주다', '드리다'), ('묻다', '여쭙다'),
    ]
    matches = []
    for plain, hon in pairs:
        if plain in words and hon in words:
            matches.append({
                'plain': plain,
                'plain_english': words[plain]['english'],
                'honorific': hon,
                'honorific_english': words[hon]['english'],
            })
    return matches


def find_noun_verb_pairs(words):
    """Pattern 5: Noun X and verb X하다 both exist."""
    matches = []
    for w, v in words.items():
        # Skip if already ends with 하다
        if w.endswith('하다'):
            continue
        # Must be 2+ syllables to avoid homonym false positives (강/강하다)
        if len(w) < 2:
            continue
        verb = w + '하다'
        if verb in words:
            matches.append({
                'noun': w,
                'noun_english': v['english'],
                'verb': verb,
                'verb_english': words[verb]['english'],
            })
    return matches


def find_adverb_derivations(words):
    """Pattern 6: Adverbs derived from adjectives (히/이 suffix)."""
    matches = []
    for w, v in words.items():
        if len(w) < 2:
            continue
        # 히 adverbs - check if 하다 form exists
        if w.endswith('히'):
            hada = w[:-1] + '하다'
            if hada in words:
                matches.append({
                    'adverb': w,
                    'adverb_english': v['english'],
                    'adjective': hada,
                    'adjective_english': words[hada]['english'],
                    'type': '히',
                })
        # 이 adverbs - check if adjective base exists
        elif w.endswith('이') and len(w) >= 3:
            base = w[:-1] + '다'
            if base in words:
                matches.append({
                    'adverb': w,
                    'adverb_english': v['english'],
                    'adjective': base,
                    'adjective_english': words[base]['english'],
                    'type': '이',
                })
    return matches


def output_tsv(results, words, outfile=None):
    """Output families as TSV for review - each row is one form in a family."""
    import io
    out = io.StringIO() if outfile is None else open(outfile, 'w')

    # Header: family_id groups related words
    print("family_id\tpattern\trole\tword\tenglish\texample_ko\texample_en\tnumber", file=out)

    family_id = 0
    seen_families = set()

    for name, matches in results.items():
        for m in matches:
            # Determine family members based on pattern
            if name == '1_verb_aux':
                members = [
                    ('compound', m['word']),
                ]
                family_key = m['word']
            elif name == '2_compound':
                members = [
                    ('root', m['root']),
                    ('compound', m['word']),
                ]
                family_key = (m['root'], m['word'])
            elif name == '3_passive':
                members = [
                    ('base', m['base']),
                    ('derived', m['word']),
                ]
                family_key = (m['base'], m['word'])
            elif name == '4_honorific':
                members = [
                    ('plain', m['plain']),
                    ('honorific', m['honorific']),
                ]
                family_key = (m['plain'], m['honorific'])
            elif name == '5_noun_verb':
                members = [
                    ('noun', m['noun']),
                    ('verb', m['verb']),
                ]
                family_key = (m['noun'], m['verb'])
            elif name == '6_adverb':
                members = [
                    ('adjective', m['adjective']),
                    ('adverb', m['adverb']),
                ]
                family_key = (m['adjective'], m['adverb'])
            else:
                continue

            if family_key in seen_families:
                continue
            seen_families.add(family_key)
            family_id += 1

            # Output each member of the family
            for role, word in members:
                entry = words.get(word, {})
                num = entry.get('number', '')
                eng = entry.get('english', '')
                ex_ko = entry.get('example_ko', '')
                ex_en = entry.get('example_en', '')
                print(f"{family_id}\t{name}\t{role}\t{word}\t{eng}\t{ex_ko}\t{ex_en}\t{num}", file=out)

    if outfile is None:
        return out.getvalue()
    out.close()
    return family_id  # return number of families


def main():
    parser = argparse.ArgumentParser(description='Analyze vocabulary redundancy patterns')
    parser.add_argument('input', help='Input TSV file (korean, english columns)')
    parser.add_argument('--pattern', choices=['all', '1', '2', '3', '4', '5', '6'],
                        default='all', help='Which pattern to analyze')
    parser.add_argument('--tsv', help='Output TSV file for review')
    args = parser.parse_args()

    words = load_data(args.input)
    print(f"Loaded {len(words)} words", file=sys.stderr)

    results = {}

    if args.pattern in ('all', '1'):
        results['1_verb_aux'] = find_verb_auxiliaries(words)
    if args.pattern in ('all', '2'):
        results['2_compound'] = find_compound_overlap(words)
    if args.pattern in ('all', '3'):
        results['3_passive'] = find_passive_causative(words)
    if args.pattern in ('all', '4'):
        results['4_honorific'] = find_honorific_pairs(words)
    if args.pattern in ('all', '5'):
        results['5_noun_verb'] = find_noun_verb_pairs(words)
    if args.pattern in ('all', '6'):
        results['6_adverb'] = find_adverb_derivations(words)

    # TSV output
    if args.tsv:
        output_tsv(results, words, args.tsv)
        print(f"Wrote TSV to {args.tsv}", file=sys.stderr)

    # Print summary
    print("\n" + "=" * 60)
    print("REDUNDANCY ANALYSIS SUMMARY")
    print("=" * 60)

    for name, matches in results.items():
        print(f"\n{name}: {len(matches)} matches")
        print("-" * 40)

        if name == '1_verb_aux':
            for m in matches:
                print(f"  {m['word']} ({m['english']}) = {m['stem']}+{m['auxiliary']}")

        elif name == '2_compound':
            for m in matches:
                print(f"  {m['word']} ({m['english']}) = {m['root']}+{m['suffix']} ({m['root_english']})")

        elif name == '3_passive':
            for m in matches:
                print(f"  {m['word']} ({m['english']}) ← {m['base']} ({m['base_english']})")

        elif name == '4_honorific':
            for m in matches:
                print(f"  {m['plain']} ({m['plain_english']}) / {m['honorific']} ({m['honorific_english']})")

        elif name == '5_noun_verb':
            for m in matches:
                print(f"  {m['noun']} ({m['noun_english']}) / {m['verb']} ({m['verb_english']})")

        elif name == '6_adverb':
            for m in matches:
                print(f"  {m['adverb']} ({m['adverb_english']}) ← {m['adjective']} ({m['adjective_english']})")

    # Deduplication count
    all_words = set()
    for name, matches in results.items():
        for m in matches:
            if name == '1_verb_aux':
                all_words.add(m['word'])
            elif name == '2_compound':
                all_words.add(m['word'])
            elif name == '3_passive':
                all_words.add(m['word'])
            elif name == '4_honorific':
                all_words.add(m['honorific'])
            elif name == '5_noun_verb':
                all_words.add(m['noun'])
            elif name == '6_adverb':
                all_words.add(m['adverb'])

    # Total
    raw_total = sum(len(m) for m in results.values())
    print(f"\n{'=' * 60}")
    print(f"Raw total: {raw_total}")
    print(f"Unique words flagged: {len(all_words)}")
    print(f"Dataset size: {len(words)}")
    print(f"Potential reduction: {len(all_words) / len(words) * 100:.1f}%")


if __name__ == '__main__':
    main()
