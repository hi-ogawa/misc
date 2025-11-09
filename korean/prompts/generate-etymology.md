I have a Korean vocabulary list in TSV format.
Columns: number, korean, english

Your task: Generate an "etymology" column showing word origins and derivations.

Include these types:

1. SINO-KOREAN (한자어 / 日本漢字):
   - 희망 → "希望"
   - 학생 → "學生 / 学生"
   - 가격 → "價格 / 価格"

2. DERIVATIONS (파생어):
   - 가져가다 → "가지다 + 가다"
   - 걸어가다 → "걷다 + 가다"

3. COMPOUNDS (합성어):
   - 눈물 → "눈 + 물"
   - 손가락 → "손 + 가락"
   - 햇빛 → "해 + 빛"

4. LOANWORDS:
   - 컴퓨터 → "computer (English)"
   - 아르바이트 → "アルバイト / Arbeit (German)"
   - 빵 → "パン / pão (Portuguese)"

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
