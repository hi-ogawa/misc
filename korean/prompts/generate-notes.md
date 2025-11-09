I have a Korean vocabulary list in TSV format.
Columns: number, korean, english

Your task: Generate a "notes" column with a single related word for each entry.

Look for these relationship types:

1. RELATED MEANINGS (synonyms, variants, semantic associations):
   - 흰색 → 하얀색
   - 검은색 → 까만색
   - 배우다 → 가르치다

2. ANTONYMS:
   - 높다 → 낮다
   - 무겁다 → 가볍다
   - 오다 → 가다
   - 학생 → 선생님

3. FAMILY/PEOPLE PAIRS:
   - 할머니 → 할아버지
   - 아저씨 → 아주머니
   - 아들 → 딸

4. HONORIFIC PAIRS:
   - 있다 → 계시다
   - 먹다 → 드시다, 잡수시다
   - 자다 → 주무시다

Output ONLY: number, korean, notes (tab-separated)
Leave blank if no related words.

Process input by batches of 100 entries.
Input: input/korean-english.tsv (all entries)
Output: 
   output/notes-1.tsv (first 1-100)
   output/notes-2.tsv (next 101-200)
   ...
   output/notes-19.tsv (last 1801-)

IMPORTANT: Use your Korean language understanding to process TSV directly.
