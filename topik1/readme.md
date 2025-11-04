# TOPIK 1 Vocabulary Extraction (1847 words)

Extracted vocabulary from TOPIK 1 vocabulary list at https://www.koreantopik.com/2024/05/topik-1-vocabulary-list-1850-for.html

**Status**: ✅ Complete (18 lessons, 1847 entries)

## Output

### Original Files: `1.csv` through `18.csv`
Format (6 fields):
```
number,check,korean,english,example,translation
```

### Enhanced Files: `extra/1.csv` through `extra/18.csv`
Format (8 fields):
```
number,check,korean,hanja,japanese,english,example,translation
```

Both versions have an empty `check` column for personal study tracking.
The `extra/` files include `hanja` and `japanese` columns for Sino-Korean word etymology:
- `hanja`: Traditional Chinese characters used in Korean (e.g., 가격 → 價格)
- `japanese`: Japanese kanji equivalents (e.g., 가격 → 価格)
- Example: 가격, 價格, 価格 showing Korean → Hanja → Japanese

## Extraction Strategy

### Method 1: Playwright MCP (Lessons 1-7)
Used for initial lessons when token limits were manageable.

1. Navigate to lesson URL: `mcp__playwright__browser_navigate`
2. Extract table data via JavaScript: `mcp__playwright__browser_evaluate`
   ```javascript
   const table = document.querySelector('table[border="1"]');
   const rows = table.querySelectorAll('tr');
   const data = [];
   for (let i = 0; i < rows.length; i++) {
     const cells = rows[i].querySelectorAll('td');
     if (cells.length === 5) {
       const rowData = Array.from(cells).map(cell => cell.textContent.trim());
       if (rowData[0] !== '#' && /^\d+$/.test(rowData[0])) {
         data.push(rowData);
       }
     }
   }
   ```
3. Write to CSV with proper escaping (quote fields containing commas)

### Method 2: Manual Text Copy (Lessons 8-18)
Switched to this method to avoid token limits from large browser responses.

1. Manually copy rendered HTML table text from browser → save as `N.txt`
2. Parse text structure by eyeballing the 5-column pattern
3. Write CSV manually, ensuring proper escaping for commas

## Adding Japanese Column (Migration Strategy)

**Goal**: Add `japanese` column after `korean` column for tracking Japanese equivalents, especially Sino-origin words (e.g., 가격 → 価格).

**Options:**

### Option A: In-place modification
- Modify all 18 CSV files directly in current directory
- Git history preserves original 6-field format
- Pros: Clean directory structure, single source of truth
- Cons: Need to checkout previous commit to see original format

### Option B: Backup directory
- Copy current state to `topik1_6col/` or `backup/`
- Modify files in current directory
- Pros: Easy side-by-side comparison, both formats accessible
- Cons: Data duplication, takes up space

### Option C: New directory for modified files
- Keep current files as-is
- Create `topik1_7col/` with modified files
- Pros: Original files untouched, clear separation
- Cons: Unclear which is "current", need to choose going forward

**Chosen approach**: Option D - Create `extra/` subdirectory
- Original files remain in `topik1/*.csv` (6 fields)
- Enhanced files in `topik1/extra/*.csv` (7 fields with japanese column)
- Pros: Originals untouched, clear naming, easy to maintain both versions
- Going forward: Use `extra/` for study with Japanese annotations

**Implementation:**
1. Create `topik1/extra/` directory
2. For each file 1.csv through 18.csv:
   - Read with Python csv module
   - Insert `japanese` column after `korean` (at index 3: number,check,korean,japanese,english,example,translation)
   - Insert empty string for japanese field in all data rows
   - Write to `extra/N.csv` with proper CSV escaping
3. Validate all files have 7 fields per row

**Script:**
```python
import csv, os
os.makedirs('extra', exist_ok=True)
for i in range(1, 19):
    with open(f'{i}.csv') as f:
        rows = list(csv.reader(f))
    rows[0].insert(3, 'japanese')  # Insert header
    for row in rows[1:]:
        row.insert(3, '')  # Insert empty japanese field
    with open(f'extra/{i}.csv', 'w', newline='') as f:
        csv.writer(f).writerows(rows)
```

## Filling Hanja and Japanese Columns

**Status**: 🚧 In Progress (Restarting with new 8-field format)

**Method**: Manual "eyeballing" - reading each CSV file and adding both Hanja and Japanese for Sino-Korean words.

**Approach**:
1. **Hanja column**: Traditional Chinese characters (Hanzi) as used in Korean
   - Example: 가격 → 價格
   - Example: 학교 → 學校

2. **Japanese column**: Japanese kanji equivalents
   - Example: 가격 → 価格 (simplified from 價格)
   - Example: 학교 → 学校 (simplified from 學校)

3. **Native Korean words**: Leave both `hanja` and `japanese` columns empty
   - Examples: 가다, 먹다, 좋다, 예쁘다

**Benefits of dual columns**:
- Shows etymological connection between Korean Hanja and Japanese kanji
- Reveals simplification differences (e.g., 價格 vs 価格)
- Useful for learners of both Korean and Japanese
- Native Korean words clearly identifiable by empty cells

**Progress by file (8-field format with hanja + japanese):**
- [x] extra/1.csv (words 1-100)
- [x] extra/2.csv (words 101-200)
- [x] extra/3.csv (words 201-300)
- [x] extra/4.csv (words 301-400)
- [x] extra/5.csv (words 401-500)
- [x] extra/6.csv (words 501-600)
- [x] extra/7.csv (words 601-700)
- [x] extra/8.csv (words 701-800)
- [x] extra/9.csv (words 801-900)
- [x] extra/10.csv (words 901-1000)
- [x] extra/11.csv (words 1001-1100)
- [x] extra/12.csv (words 1101-1200)
- [x] extra/13.csv (words 1201-1300)
- [ ] extra/14.csv (words 1301-1400)
- [ ] extra/15.csv (words 1401-1500)
- [ ] extra/16.csv (words 1501-1600)
- [ ] extra/17.csv (words 1601-1700)
- [ ] extra/18.csv (words 1701-1847)

## CSV Validation

### Original files (6 fields):
```python
import csv
with open('N.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        assert len(row) == 6  # All rows have exactly 6 fields
```

### Extra files (7 fields):
```python
import csv
for i in range(1, 19):
    with open(f'extra/{i}.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            assert len(row) == 7  # All rows have exactly 7 fields
```

✅ All 1847 entries properly formatted and escaped in both versions.

**CSV Escaping Fixes**:
During the migration to add the `japanese` column, discovered and fixed CSV escaping issues in 1.csv and 5.csv:
- 1.csv line 64: `translation` field had unquoted comma → changed to semicolon "lie; tell a lie"
- 5.csv: 7 rows with unquoted commas in `english` field → manually quoted each field

**Important lesson**: Manual "eyeballing" and fixing with the Edit tool was far more robust than automated Python scripts. Multiple attempts at automated fixing kept combining wrong fields or misidentifying the issue. Reading the file directly and manually editing each problematic line was faster and more reliable.

## Future Reference

For similar vocabulary extraction tasks:

1. **Try browser automation first** (Playwright MCP) - works well for clean table structures
2. **Watch for token limits** - large responses may need chunking or alternative approaches
3. **Manual text copy fallback** - reliable when automation hits limits
4. **Always validate CSV escaping** - use proper CSV parser, not simple comma splitting
5. **Fix data quality issues by eyeballing** - manual inspection and Edit tool is more reliable than automated scripts for fixing escaping issues
6. **Key insight**: Rendered browser text is cleaner than raw minified HTML

## Lesson URLs

<details>
<summary>18 lesson pages (click to expand)</summary>

1. Words 1-100: https://www.koreantopik.com/2022/10/official-topik-1-vocabulary-list-for.html
2. Words 101-200: https://www.koreantopik.com/2023/08/1850-topik-i-vocabulary-words-for.html
3. Words 201-300: https://www.koreantopik.com/2023/08/1850-topik-i-vocabulary-words-for_26.html
4. Words 301-400: https://www.koreantopik.com/2023/09/the-301-400th-topik-1-vocabulary-words.html
5. Words 401-500: https://www.koreantopik.com/2023/09/the-401500th-topik-1-vocabulary-words.html
6. Words 501-600: https://www.koreantopik.com/2023/09/the-501600th-topik-1-vocabulary-words.html
7. Words 601-700: https://www.koreantopik.com/2023/10/the-601700th-topik-1-vocabulary-words.html
8. Words 701-800: https://www.koreantopik.com/2023/10/the-701800th-topik-1-vocabulary-words.html
9. Words 801-900: https://www.koreantopik.com/2023/11/the-801900th-topik-1-vocabulary-words.html
10. Words 901-1000: https://www.koreantopik.com/2023/11/the-9011000th-topik-1-vocabulary-words.html
11. Words 1001-1100: https://www.koreantopik.com/2023/12/the-10011100th-topik-1-vocabulary-words.html
12. Words 1101-1200: https://www.koreantopik.com/2023/12/the-11011200th-topik-1-vocabulary-words.html
13. Words 1201-1300: https://www.koreantopik.com/2024/01/the-12011300th-topik-1-vocabulary-words.html
14. Words 1301-1400: https://www.koreantopik.com/2024/01/the-13011400th-topik-1-vocabulary-words.html
15. Words 1401-1500: https://www.koreantopik.com/2024/02/the-14011500th-topik-1-vocabulary-words.html
16. Words 1501-1600: https://www.koreantopik.com/2024/02/the-15011600th-topik-1-vocabulary-words.html
17. Words 1601-1700: https://www.koreantopik.com/2024/03/the-16011700th-topik-1-vocabulary-words.html
18. Words 1701-1847: https://www.koreantopik.com/2024/03/the-17011850th-topik-1-vocabulary-words.html

</details>

---
*Note: Original source claimed 1850 words, but actual count is 1847 (verified by counting all CSV entries).*
