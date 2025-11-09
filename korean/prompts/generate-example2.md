I have a Korean vocabulary list in TSV format.
Columns: number, korean, english

Your task: Generate natural 2-3 word example phrases for each entry.

REQUIREMENTS:
- Keep it minimal: 2-3 words maximum
- Show natural, common usage
- Prefer -요 form when using verbs/adjectives in sentences
- Use whatever form is most natural (modifying forms, compounds, etc. are fine)

Examples:
- 가다 → "학교에 가요"
- 높다 → "건물이 높아요" 
- 학생 → "학생이 공부해요"
- 사과 → "빨간 사과"
- 간단하다 → "간단한 설명"

Output ONLY: number, korean, example_ko, example_en (tab-separated)

Process input by batches of 100 entries.
Input: input/korean-english.tsv (all entries)
Output: 
   output/examples-1.tsv (first 1-100)
   output/examples-2.tsv (next 101-200)
   ...
   output/examples-19.tsv (last 1801-1847)

IMPORTANT: Generate the most natural, commonly-used phrase for each word. Process directly using Korean language understanding and avoid script-based automation.
