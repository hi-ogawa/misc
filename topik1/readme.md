# TOPIK 1 Vocabulary Extraction (1847 words)

Extracted vocabulary from TOPIK 1 vocabulary list at https://www.koreantopik.com/2024/05/topik-1-vocabulary-list-1850-for.html

**Status**: ✅ Complete (18 lessons, 1847 entries)

## Output

CSV files `1.csv` through `18.csv` with format:
```
number,check,korean,english,example,translation
```

Each CSV has an empty `check` column for personal study tracking.

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

## CSV Validation

Verified all files with Python CSV parser:
```python
import csv
with open('N.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        assert len(row) == 6  # All rows have exactly 6 fields
```

✅ All 1847 entries properly formatted and escaped.

## Future Reference

For similar vocabulary extraction tasks:

1. **Try browser automation first** (Playwright MCP) - works well for clean table structures
2. **Watch for token limits** - large responses may need chunking or alternative approaches
3. **Manual text copy fallback** - reliable when automation hits limits
4. **Always validate CSV escaping** - use proper CSV parser, not simple comma splitting
5. **Key insight**: Rendered browser text is cleaner than raw minified HTML

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
