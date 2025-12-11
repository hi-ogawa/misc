# Check Duplicate Cards

Find cards with the same `korean` field to identify true homonyms vs actual duplicates.

## Usage

```bash
# Export all cards with korean and english fields
python scripts/anki-export.py \
  --query "deck:Korean korean:_*" \
  --fields number,korean,english > output/tmp/korean-all.tsv

# Find duplicates grouped by korean field
python scripts/jq-tsv.py -s --json \
  'group_by(.korean) | map(select(length > 1)) | map({korean: .[0].korean, entries: map({number, english})})' \
  output/tmp/korean-all.tsv > output/tmp/duplicates.json

# View duplicates
jq '.' output/tmp/duplicates.json
```

## Interpretation

Review duplicates to distinguish:

**True homonyms** (different meanings - keep all):
- 배: belly / ship / pear / times
- 쓰다: write / wear / use / bitter
- 차다: be full / kick / wear (watch) / cold
- 따르다: to pour / to follow

**Actual duplicates** (same meaning - consider merging):
- 구하다: extract_1325 vs extract_1757 (both "to obtain")
- 옮기다: extract_1128 vs extract_1437 (both "to move")

## Notes

- Query `korean:_*` filters out cards with empty korean field
- Homonyms are expected and valid - Korean has many
- True duplicates often come from overlapping extraction batches
