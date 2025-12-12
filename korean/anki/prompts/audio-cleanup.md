# Audio File Cleanup

Analysis of audio files in Anki media folder (2025-12-12).

## Summary

- **Total files**: 16,230
- **Disk usage**: 313MB
- **Stale files**: ~5,500+ (estimated)

## TOPIK 1 Audio

### korean_audio field
| Prefix | In Media | In Use | Status |
|--------|----------|--------|--------|
| `koreantopik1_korean_{NNNN}` | 1,847 | 1,847 | **keep** |

### example_ko_audio field (mixed patterns)
| Prefix | In Media | Cards Using | Status |
|--------|----------|-------------|--------|
| `koreantopik1_example_ko_{NNNN}` | 1,847 | 594 | partial use |
| `koreantopik1_example_ko_v3_{NNNN}` | 1,847 | 1,250 | partial use |
| `koreantopik1_example_ko_fix_{NNNN}` | 3 | 3 | **keep** |

**Issue**: Both `example_ko` and `example_ko_v3` patterns exist. Looks like partial migration to v3. ~1,850 orphaned files between them.

### Stale (not referenced by any card)
| Prefix | Count | Status |
|--------|-------|--------|
| `koreantopik1_{NNNN}` | 1,847 | **delete** |
| `koreantopik1_v2_{NNNN}` | 1,847 | **delete** |

## TOPIK 2 Audio

| Prefix | Count | Status |
|--------|-------|--------|
| `korean_koreantopik2_{NNN}_{NNNN}` | 3,179 | **keep** |
| `example_ko_koreantopik2_{NNN}_{NNNN}` | 3,179 | **keep** |

Format: `{prefix}_{score}_{index}.mp3`

## Other Decks

### Custom (`Korean::Custom`)
| Prefix | Count | Status |
|--------|-------|--------|
| `custom_korean_{timestamp}` | 201 | **keep** |
| `custom_example_ko_{timestamp}` | 202 | **keep** |
| `korean_extract_20251212_{NNNN}` | 41 | **keep** |
| `example_ko_extract_20251212_{NNNN}` | 41 | **keep** |
| `korean_manual_20251207_{NNNN}` | 12 | **keep** |
| `example_ko_manual_20251207_{NNNN}` | 12 | **keep** |

### Dialogue (`Korean::Dialogue`)
| Prefix | Count | Status |
|--------|-------|--------|
| `dialogue_plot_ko_{NNNN}` | 50 | **keep** |
| `dialogue_dialogue_ko_{NNNN}` | 50 | **keep** |

### Unknown
| Prefix | Count | Status |
|--------|-------|--------|
| `grammar_example_ko_{NNNN}` | 23 | check |

## Cleanup Commands

### Safe cleanup (definitely stale)

```bash
cd "$(python scripts/anki.py getMediaDirPath | tr -d '"')"

# Delete old TOPIK 1 iterations (3,694 files)
rm koreantopik1_[0-9]*.mp3
rm koreantopik1_v2_*.mp3
```

### Future: Consolidate TOPIK 1 example_ko

Option 1: Migrate all cards to v3, delete old files
Option 2: Keep both (wastes ~50MB)

To find orphaned files:
```bash
# Export all referenced audio files
python scripts/anki-export.py --query "deck:Korean" --fields korean_audio,example_ko_audio \
  | grep -oP '\[sound:\K[^\]]+' | sort -u > /tmp/referenced.txt

# Compare with actual files
cd "$(python scripts/anki.py getMediaDirPath | tr -d '"')"
ls *.mp3 | sort > /tmp/actual.txt

# Find orphaned
comm -23 /tmp/actual.txt /tmp/referenced.txt > /tmp/orphaned.txt
```
