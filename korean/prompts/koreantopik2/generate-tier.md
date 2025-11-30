# TOPIK 2 Vocabulary Tiering Strategy

## Background

After practicing TOPIK 1, key insight emerged:

- TOPIK word lists are **test-prep artifacts**, not frequency-ranked
- LLM example sentences naturally included words outside TOPIK 1 (e.g., 두르다 for 목도리)
- These "missing links" = high-frequency words that co-occur with beginner vocabulary
- TOPIK 1/2 boundary is arbitrary - some TOPIK 2 words are more useful than TOPIK 1 words

**Goal**: Filter TOPIK 2 (3873 words) to prioritize high-value words for TOPIK 1 graduates.

## Core Insight: LLM as Frequency Oracle

LLMs trained on massive Korean text have implicit knowledge of:
- Word frequency in natural text
- Co-occurrence patterns with beginner vocabulary
- Which words are "central" vs "peripheral"

Instead of:
- Finding corpus data (Option B)
- Generating 4000 example sentences (expensive)
- Manual sentence mining (slow)

**Direct approach**: Ask LLM to tier the entire vocabulary list.

## Tiering Strategy

### Tier Definitions

| Tier | Description |
|------|-------------|
| **Tier 1** | Essential everyday words, high frequency, natural with TOPIK 1 |
| **Tier 2** | Useful but less frequent, broader vocabulary |
| **Tier 3** | Specialized, academic, or low-frequency |

Let LLM decide distribution naturally - no enforced counts.

### Tier 1 Criteria (Priority)
- High frequency in spoken Korean
- Strong co-occurrence with TOPIK 1 vocabulary
- Appears in daily conversation, variety shows, dramas
- Fills "gaps" in TOPIK 1 coverage

### Tier 3 Criteria (Deprioritize)
- Academic/formal register
- Technical/specialized domains
- Literary or archaic usage
- Narrow usage contexts

## Implementation Options

### Option A: Single-shot Full List

Feed all 3873 words to LLM in one prompt:

```
Given this TOPIK 2 vocabulary list (3873 words), assign each word to a tier:

Tier 1: Essential - High frequency, everyday usage, natural co-occurrence with beginner vocabulary
Tier 2: Useful - Moderate frequency, broader but practical vocabulary
Tier 3: Specialized - Low frequency, academic, technical, or narrow usage

For a TOPIK 1 graduate, Tier 1 words should feel like "missing" beginner vocabulary.

Output: TSV with columns: number, korean, tier
```

**Pros**: Simple, fast, leverages LLM's implicit frequency knowledge
**Cons**: Single LLM's judgment, no validation

### Option B: Batch with Consensus

Split into batches, process with multiple prompts, look for consensus.

**Pros**: More robust
**Cons**: More work, may not add much value

### Option C: Validation via Example Generation

For uncertain words, ask LLM to generate example sentences using TOPIK 1 vocabulary.
- If natural sentence emerges -> Tier 1
- If sentence feels forced -> Tier 2/3

### Option D: Combined Tier + Example Generation (Recommended)

Process in ~100 word batches, generating BOTH tier and example sentence together.

**Rationale:**
- 4000 words + 4000 outputs in one shot is too large (LLM gets "nervous", writes scripts instead)
- Generating an example forces LLM to "use" the word
- If natural example comes easily → reveals Tier 1
- If example feels forced/awkward → reveals Tier 2/3
- The act of generating reveals word's "naturalness" better than abstract tier judgment

**Benefits:**
- Tier decision informed by actual usage attempt
- Get examples "for free" alongside tiering
- Batch size matches existing infrastructure
- Can filter Tier 1 words later and already have examples ready

#### Subagent Prompt Template

```
**Task: Generate tier assignments AND example sentences for TOPIK 2 vocabulary batch {N}**

## Step 1: Read Requirements
Read `/home/hiroshi/code/personal/misc/korean/prompts/requirements-example.md` for example sentence quality requirements.

## Step 2: Read Input
Read `/home/hiroshi/code/personal/misc/korean/input/koreantopik2-batch-{N}.tsv`

## Step 3: For Each Word - Generate Tier + Example Together

**Key insight**: The act of generating an example reveals the word's tier.
- If a natural, everyday example comes easily → Tier 1
- If the example requires specific/moderate context → Tier 2
- If the example feels forced, academic, or narrow → Tier 3

**Tier definitions:**
- **Tier 1**: Essential - High frequency in spoken Korean, everyday dramas/variety shows. Example sentence uses common, natural patterns.
- **Tier 2**: Useful - Moderate frequency, practical but less common. Example requires more specific context.
- **Tier 3**: Specialized - Academic, technical, literary, or narrow usage. Example feels domain-specific.

**Process for each word:**
1. Try to generate a natural example sentence following requirements-example.md
2. Notice: Was this easy/natural, or did it require specialized context?
3. Assign tier based on that experience
4. Finalize the example sentence

## Step 4: Write Output
Write TSV to `/home/hiroshi/code/personal/misc/korean/output/koreantopik2/tier-examples-{N}.tsv`

**Columns**: number	korean	english	tier	example_ko	example_en

## Critical Rules
- DO NOT write scripts or code - generate directly using Korean language knowledge
- DO NOT run bash commands - just write the file and exit
- Follow ALL requirements from requirements-example.md (multi-clause preferred, concrete context, etc.)
- Process ALL entries in the batch
- Let tier assignment emerge naturally from the example generation experience
```

#### Output Format

Per-batch: `output/koreantopik2/tier-examples-{N}.tsv`
```
number	korean	english	tier	example_ko	example_en
1	-가	professional	3	유명한 음악가가 콘서트에서 피아노를 연주했어요.	A famous musician played piano at the concert.
2	가까이	nearby	1	위험하니까 가까이 오지 마세요.	Don't come close because it's dangerous.
```

## Validation Approach

After tiering:

1. **Spot check top 50 Tier 1**: Do they feel familiar from variety shows?
2. **Cross-reference flagged unknowns**: Your ~100 unknown words from TOPIK 1 examples should mostly be Tier 1
3. **두르다 test**: Should rank high in Tier 1
4. **Sample Tier 3**: Should feel academic/specialized

## Output Files

**Per-batch outputs** (39 files):
- `output/koreantopik2/tier-examples-{1-39}.tsv`

**Merged by tier** (using `scripts/jq-tsv.py`):
```bash
# Use {1..39} for correct numeric order (not *.tsv which gives 1,10,11,...,2,...)
python3 scripts/jq-tsv.py 'select(.tier == "1")' output/koreantopik2/tier-examples-{1..39}.tsv > output/koreantopik2/tier-1-examples.tsv
python3 scripts/jq-tsv.py 'select(.tier == "2")' output/koreantopik2/tier-examples-{1..39}.tsv > output/koreantopik2/tier-2-examples.tsv
python3 scripts/jq-tsv.py 'select(.tier == "3")' output/koreantopik2/tier-examples-{1..39}.tsv > output/koreantopik2/tier-3-examples.tsv
```

**Tier counts**:
```bash
python3 scripts/jq-tsv.py -s 'group_by(.tier) | map({tier: .[0].tier, count: length})' output/koreantopik2/tier-examples-*.tsv
```

## Execution Status

**Completed**: All 39 batches processed with Option D.

**Final Distribution**:
| Tier | Count | % | Description |
|------|-------|---|-------------|
| Tier 1 | 1,049 | 27% | Essential - "TOPIK 1.5" priority deck |
| Tier 2 | 2,052 | 53% | Useful - learn after Tier 1 |
| Tier 3 | 772 | 20% | Specialized - lowest priority |

**Output files created**:
- `tier-examples-{1-39}.tsv` - per-batch with tier + examples
- `tier-1-examples.tsv` - 1,049 essential words
- `tier-2-examples.tsv` - 2,052 useful words
- `tier-3-examples.tsv` - 772 specialized words

## Creating Tier 1 Anki Import

### Goal
Create `koreantopik2_tier1_anki_import.tsv` - a filtered deck of 1,049 essential words.

### Naming Convention
- `koreantopik2_tier1_N` for card IDs (not `koreantopik2_N`)
- Audio files: `koreantopik2_tier1_korean_NNNN.mp3`, `koreantopik2_tier1_example_ko_NNNN.mp3`

### Data Sources
1. **Tier assignment**: `tier-examples-{1..39}.tsv` (number, tier)
2. **Base content**: `koreantopik2_anki_import.tsv` (etymology, notes, existing examples)

### Approach Options

#### Option A: Reuse Existing Examples + Audio
- Filter `koreantopik2_anki_import.tsv` to tier 1 words
- Keep original examples (already have audio)
- Renumber: `koreantopik2_1` → `koreantopik2_tier1_1`
- Rename audio references accordingly
- **Pro**: No new audio generation needed
- **Con**: Examples weren't optimized for tier assessment

#### Option B: Use Tier-Generated Examples
- Use `example_ko`, `example_en` from `tier-examples-*.tsv`
- Keep etymology, notes from original
- Generate new audio for tier examples
- **Pro**: Examples naturally demonstrate word's "essentialness"
- **Con**: Requires new audio generation (~2100 files)

#### Option C: Hybrid
- Keep original examples + audio
- Add tier examples as secondary field (for review/comparison)
- **Pro**: Best of both worlds
- **Con**: More complex card structure

### Recommended: Option B (tier-generated examples are the point)

```bash
# Step 1: Extract tier 1 with examples (already done)
python3 scripts/jq-tsv.py 'select(.tier == "1")' \
  output/koreantopik2/tier-examples-{1..39}.tsv \
  > output/koreantopik2/tier-1-examples.tsv

# Step 2: Join with anki import to get etymology/notes, renumber
python3 scripts/create-tier1-anki-import.py \
  --tier output/koreantopik2/tier-1-examples.tsv \
  --anki output/koreantopik2/koreantopik2_anki_import.tsv \
  --prefix koreantopik2_tier1

# Step 3: Generate audio for tier examples
python3 scripts/generate-audio.py output/koreantopik2/koreantopik2_tier1_anki_import.tsv
```

### Output Structure
Same columns as `koreantopik2_anki_import.tsv`:
```
number	korean	english	example_ko	example_en	etymology	notes	korean_audio	example_ko_audio
koreantopik2_tier1_1	가까이	nearby	...	...	...	...	[sound:koreantopik2_tier1_korean_0001.mp3]	...
```

## Next Steps

1. ~~Generate tier + examples~~ ✓ Complete
2. ~~Merge by tier~~ ✓ Complete
3. **Create tier1 anki import**: Filter and renumber (Option A)
4. **Copy/rename audio files**: Map original audio to tier1 naming
5. **Import to Anki**: Create "TOPIK 1.5" deck
6. **Later**: Process Tier 2 when Tier 1 is mastered

## Open Questions

1. **Refinement**: After initial tiers, allow manual adjustments?
2. **Audio strategy**: Reuse existing (Option A) or regenerate for tier examples (Option B)?
