# TOPIK 1 — vocabulary extraction (1850 words)

This folder will hold the saved HTML pages, extraction scripts, and CSV outputs for the TOPIK 1 1850-word vocabulary list from https://www.koreantopik.com.

- list of 1850 is found in https://www.koreantopik.com/2024/05/topik-1-vocabulary-list-1850-for.html
  - each 100 words are on separate lesson pages (18 total)

Goal
 - Extract vocabulary from all 18 lesson pages directly using Playwright MCP browser automation.
 - Generate CSV files `1.csv`, `2.csv`, … `18.csv` with checklist format.
 - Verify the final combined set contains 1850 unique entries.

Current strategy (SUCCESSFUL: Playwright MCP)
 1. Use Playwright MCP to directly extract vocabulary from web pages via browser automation
 2. Navigate to each lesson URL using `mcp__playwright__browser_navigate`
 3. Use `mcp__playwright__browser_evaluate` with JavaScript to query the vocabulary table (CSS selector: `table[border="1"]`)
 4. Extract all table rows with 5 cells (number, korean, english, example, translation)
 5. Write directly to CSV with columns: `number,check,korean,english,example,translation`
 6. Verify the combined CSV contains 1850 unique entries

Alternative approach (FAILED: HTML parsing)
 - Downloading HTML files and parsing with Python HTMLParser failed due to heavily minified HTML with complex nested tags
 - Created `extract.py` but it could not extract data from the minified HTML structure
 - Playwright MCP is the superior approach as it renders pages in a real browser and allows DOM queries

Progress
 - [x] Create `topik1` folder (this README lives here)
 - [x] Add this `readme.md` summarizing strategy and tracking progress
 - [x] Downloaded main TOC page and extracted all 18 lesson URLs
 - [x] Set up Playwright MCP for browser automation
 - [x] Successfully extracted lesson 1 vocabulary (100 entries) using Playwright MCP
 - [x] Created `1.csv` with checklist format (number, check, korean, english, example, translation)
 - [ ] Extract remaining lessons 2-18 using Playwright MCP
 - [ ] Verify the combined CSV contains 1850 unique entries

Lesson URLs (18 total)
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
 18. Words 1701-1850: https://www.koreantopik.com/2024/03/the-17011850th-topik-1-vocabulary-words.html

Files in this folder
 - `topik1/readme.md` — this file, documents the extraction strategy and progress
 - `topik1/1.csv` — CSV checklist with 100 vocabulary entries (columns: number, check, korean, english, example, translation)
 - (future) `topik1/2.csv` … `topik1/18.csv` — remaining lesson CSVs

Assumptions and notes
 - The source post links 18 lesson pages (each ~100 words except the last which has 150).
 - All pages have consistent table structure: `<table border="1">` with 5 columns (number, vocab, meaning, example, translation).
 - Playwright MCP successfully extracts vocabulary by querying the DOM with JavaScript in a real browser context.
 - The minified HTML structure makes direct parsing difficult, but browser rendering normalizes it perfectly.

Next steps (short)
 1. Use Playwright MCP to navigate to each of the remaining 17 lesson URLs (lessons 2-18).
 2. Extract vocabulary tables using the same JavaScript query: `table[border="1"]` → filter rows with 5 cells.
 3. Write each lesson's data to corresponding CSV files: `2.csv` … `18.csv`.
 4. Verify the combined CSV contains 1850 unique entries and update this README with the verification result.

JavaScript extraction code used:
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

----
Created: automatic by assistant
