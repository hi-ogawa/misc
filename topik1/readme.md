# TOPIK 1 — vocabulary extraction (1850 words)

This folder will hold the saved HTML pages, extraction scripts, and CSV outputs for the TOPIK 1 1850-word vocabulary list from https://www.koreantopik.com.

Goal
 - Fetch each lesson page (18 lessons) and save as `1.html`, `2.html`, … `18.html` inside this folder.
 - Parse each saved HTML and extract vocabulary rows to `1.csv`, `2.csv`, … `18.csv`.
 - Verify the final combined set contains 1850 unique entries.

Current strategy
 1. Fetch pages and save the fetched HTML as-is to `N.html` (temporary) so we keep an exact copy of the source for reproducibility and debugging.
 2. Optionally create a cleaned version (table-only) for manual edits; but the extractor should be able to parse the raw `N.html` files directly.
 3. Write a small extractor script (`extract.py`) that reads `N.html` and writes `N.csv`.
 4. CSV columns will be: `number,check,korean,english,example,translation` (the checklist format you requested). Some fields may be empty depending on source layout.
 5. After extraction, run a quick verification script to count entries and check for duplicates.

Progress
 - [x] Create `topik1` folder (this README lives here)
 - [x] Add this `readme.md` summarizing strategy and tracking progress
 - [x] Saved lesson 1 as `1.html` and created `1.csv` (100 entries)
 - [ ] Fetch remaining pages and save as `2.html` … `18.html`
 - [ ] (optional) Implement `extract.py` to parse saved HTML files automatically
 - [ ] Run extraction/verification to confirm 1850 unique words

Files added so far
 - `topik1/1.html` — lesson page 1 (1–100) saved for offline parsing
 - `topik1/1.csv` — CSV checklist (columns: number, check, korean, english, example, translation)

Assumptions and notes
 - The source post links 18 lesson pages (each ~100 words except the last which has 150). We'll save each lesson as a separate HTML file.
 - HTML structure may vary slightly between lesson pages; the extractor should be tolerant (use selectors + fallback regex if needed).
 - If any pages are blocked or contain anti-scraping protections, we will save them manually or fall back to a single combined HTML.

Next steps (short)
 1. Fetch and save the 18 lesson pages as raw files: `1.html` … `18.html` (these are temporary full HTML copies).
 2. Implement and run `extract.py` to generate CSVs `1.csv` … `18.csv` (format: number,check,korean,english,example,translation).
 3. Verify the combined CSV contains 1850 unique entries and update this README with the verification result.

If you want me to proceed, I'll fetch the 18 lesson pages next and save them under this folder.

----
Created: automatic by assistant
