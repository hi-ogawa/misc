# Fix Single Entry - TOPIK 1

Guide for correcting individual vocabulary entries when errors are found.

## When to Use This

- Found a translation error in the original dataset
- Need to regenerate a specific example sentence
- Audio file needs to be updated for one entry

## Workflow

### Step 1: Fix the Original Input (if needed)

If the error is in `input/koreantopik1.tsv`:

```bash
# Edit the specific line (e.g., entry 549, which is line 550 with header)
sed -i '550s/\tmedal$/\tevery month/' input/koreantopik1.tsv
```

**Verify**:
```bash
grep "^549	" input/koreantopik1.tsv
```

### Step 2: Generate Corrected Example

Follow `prompts/requirements-example.md` to create a new example sentence.

**Requirements checklist**:
- ✅ Uses the actual vocabulary word (not synonym)
- ✅ Multi-clause with connective (-서, -(으)니까, -면, -지만, -(으)려고, etc.)
- ✅ Concrete context (specific time, location, objects)
- ✅ Explicit subject and object (no dropping)
- ✅ Shows characteristic/distinctive usage
- ✅ Visualizable scenario

**Example for 매달 (every month)**:
```
Korean:  아버지가 매달 월급을 받으면 저축을 하세요
English: My father saves money every month when he receives his salary
```

### Step 3: Update the Anki Import File

Edit `output/koreantopik1/koreantopik1_anki_import_v3.tsv`:

1. Read the file to check current content:
   ```bash
   grep "^549	" output/koreantopik1/koreantopik1_anki_import_v3.tsv
   ```

2. Update the entry (replace columns 3, 4, 5):
   - Column 3: English translation
   - Column 4: example_ko
   - Column 5: example_en

### Step 4: Regenerate Audio

Generate new audio for the corrected example:

```bash
python scripts/generate-audio.py \
  --input output/koreantopik1/koreantopik1_anki_import_v3.tsv \
  --field example_ko \
  --prefix koreantopik1_example_ko_v3_ \
  --output output/koreantopik1/audio \
  --start 549 \
  --end 549 \
  --force
```

**Note**: Ensure the TSV header does NOT start with `#`. If it does, remove it first:
```bash
sed -i '1s/^#//' output/koreantopik1/koreantopik1_anki_import_v3.tsv
```

### Step 5: Verify

```bash
# Check updated entry
grep "^549	" output/koreantopik1/koreantopik1_anki_import_v3.tsv

# Verify audio file exists
ls -lh output/koreantopik1/audio/koreantopik1_example_ko_v3_0549.mp3

# Test audio playback
mpv output/koreantopik1/audio/koreantopik1_example_ko_v3_0549.mp3
```

## Common Fixes

### Translation Error (Wrong English)

**Problem**: Entry 549 had 매달 (every month) translated as "medal"

**Fix**: Update input file translation
```bash
sed -i '550s/\tmedal$/\tevery month/' input/koreantopik1.tsv
```

### Confused Homophones

**Problem**: Example uses wrong homophone (e.g., 메달 instead of 매달)

**Fix**: Generate new example following requirements, ensure it uses the correct word

### Generic/Low-Quality Example

**Problem**: Example doesn't follow requirements (too generic, no connective, etc.)

**Fix**: Regenerate following the multi-clause, concrete context principles

## Validation Checklist

Before considering the fix complete:

- [ ] Input file has correct translation
- [ ] Example sentence uses the correct vocabulary word
- [ ] Example follows all quality requirements (multi-clause, concrete, etc.)
- [ ] Audio file regenerated and plays correctly
- [ ] Entry verified in koreantopik1_anki_import_v3.tsv
