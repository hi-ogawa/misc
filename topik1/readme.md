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
Format (7 fields):
```
number,check,korean,japanese,english,example,translation
```

Both versions have an empty `check` column for personal study tracking.
The `extra/` files include an empty `japanese` column for annotating Japanese equivalents, especially useful for Sino-Korean words (e.g., 가격 → 価格).

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
