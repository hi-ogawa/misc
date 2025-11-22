# Data Validation - TOPIK 1

Guide for validating the dataset for common errors.

## Known Issues

### Entry 549: 매달 (every month) vs 메달 (medal)

**Problem**: Original dataset had:
```
549	매달	medal
```

**Issue**: 매달 means "every month" (매 = every, 달 = month), not "medal" (메달)

**Status**: ✅ Fixed in `input/koreantopik1.tsv`

## Common Error Types

### 1. Translation Errors

**Symptoms**:
- English doesn't match Korean meaning
- Confused homophones
- Wrong hanja/etymology

**How to find**:
- Manual review of alphabetically similar entries
- Check entries with similar pronunciation
- Verify hanja matches meaning

### 2. Confused Homophones

**Watch for**:
- 매달 (every month) / 메달 (medal)
- 내일 (tomorrow) / 네일 (nail)
- 눈 (eye/snow) - context-dependent
- 밤 (night/chestnut) - context-dependent

### 3. Example Sentence Errors

**Symptoms**:
- Example uses wrong word (synonym or homophone)
- Example doesn't contain the vocabulary word
- Too generic/doesn't show distinctive usage

**How to find**:
- Spot check random entries
- Look for very short examples (<4 words)
- Check examples that don't use connectives

## Validation Checklist

### Input File (`input/koreantopik1.tsv`)

- [ ] All entries have number, korean, english columns
- [ ] Numbers are sequential (1-1847)
- [ ] No duplicate entries
- [ ] English translations match Korean meanings
- [ ] No confused homophones

### Examples File (`output/koreantopik1/examples-all.tsv`)

- [ ] All entries have example_ko and example_en
- [ ] Each example contains the vocabulary word
- [ ] Examples meet quality standards (see `prompts/requirements-example.md`)
- [ ] Average sentence length ~5-7 words
- [ ] Multi-clause sentences prevalent

### Anki Import File (`output/koreantopik1/koreantopik1_anki_import_v3.tsv`)

- [ ] All 9 columns present
- [ ] Audio references use v3 format: `[sound:koreantopik1_example_ko_v3_NNNN.mp3]`
- [ ] No missing fields
- [ ] Header format compatible with scripts (no `#` if using generate-audio.py)

## Quick Validation Commands

### Check for missing examples
```bash
# Should output nothing if all entries have examples
awk -F'\t' 'NR>1 && ($4 == "" || $5 == "")' output/koreantopik1/koreantopik1_anki_import_v3.tsv
```

### Check example length distribution
```bash
python scripts/analyze-examples.py --input output/koreantopik1/examples-all.tsv
```

### Verify audio file count
```bash
ls output/koreantopik1/audio/koreantopik1_example_ko_v3_*.mp3 | wc -l
# Expected: 1847
```

### Find entries with very short examples (potential issues)
```bash
awk -F'\t' 'NR>1 {
  split($4, words, " ");
  if (length(words) <= 3) print NR-1 "\t" $2 "\t" $4
}' output/koreantopik1/koreantopik1_anki_import_v3.tsv
```

### Check for examples not using the vocabulary word
```bash
# This is complex - best done with manual review
# Look at random samples:
shuf -n 10 output/koreantopik1/koreantopik1_anki_import_v3.tsv | cut -f1,2,4
```

## Systematic Review Process

### Phase 1: Input File Validation

1. Check for translation errors in similar-sounding words
2. Verify hanja/etymology matches meaning
3. Look for common homophone confusions

### Phase 2: Example Quality Spot Check

1. Random sample 50 entries
2. Verify each contains vocabulary word
3. Check for multi-clause usage
4. Ensure concrete context present

### Phase 3: Audio Verification

1. Verify file count matches entry count
2. Spot check audio quality (5-10 random samples)
3. Check file naming matches references in TSV

## Fixing Found Issues

See `prompts/koreantopik1/fix-single-entry.md` for detailed fix workflow.
