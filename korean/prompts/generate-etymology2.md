I have a Korean vocabulary list in TSV format.
Columns: number, korean, english

Your task: Generate an "etymology" column showing word origins and derivations.

Include these types:

1. SINO-KOREAN (한자어 / 日本漢字):
   - 희망 → "希望"
   - 학생 → "學生 / 学生"
   - 가격 → "價格 / 価格"

   IMPORTANT: Always show BOTH traditional Chinese and Japanese kanji when they differ.
   Examples:
   - 價格 / 価格 (NOT just 價格)
   - 簡單 / 簡単 (NOT just 簡單)
   - 經驗 / 経験 (NOT just 經驗)

2. DERIVATIONS (파생어):
   - 가져가다 → "가지다 + 가다"
   - 걸어가다 → "걷다 + 가다"

3. COMPOUNDS (합성어):
   - 눈물 → "눈 + 물"
   - 손가락 → "손 + 가락"
   - 햇빛 → "해 + 빛"
   - 강아지 → "개 + 아지" (use original root, not sound-changed form)

   IMPORTANT: For compounds with sound changes, use the ORIGINAL root form.
   - 강아지 comes from 개 (dog) + 아지, so write "개 + 아지" (NOT "강 + 아지")
   - Show the root before sound change occurred

4. LOANWORDS:
   - 컴퓨터 → "computer"
   - 아르바이트 → "アルバイト / Arbeit"
   - 빵 → "パン / pão"

   Format: Just the source word, no language labels in parentheses.
   If borrowed through another language (e.g., German → Japanese → Korean), show the path with "/"

SKIP: Pure Korean words with no clear etymology

Format: Just the etymology (minimal, no explanations)
Output ONLY: number, korean, etymology (tab-separated)
Leave blank if no etymology info.

Process input by batches of 100 entries.
Input: input/korean-english.tsv
Output:
   output/etymology-1.tsv (first 1-100)
   output/etymology-2.tsv (next 101-200)
   ...
   output/etymology-19.tsv (last 1801-1847)

IMPORTANT: Do NOT write code. Process directly using Korean language understanding.
