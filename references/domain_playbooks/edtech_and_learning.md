# Domain Playbook: EdTech & Interactive Learning Platforms
1. **Sub-Second Progressive Quiz & Card Streaming:** Retrieve and stream **Question/Card #1 in <800ms** into a pre-built React `<QuizCard/>` or `<Flashcard/>` component. Pre-fetch Questions #2–#10 asynchronously into `sessionStorage` while the learner reads Question #1.
2. **Non-Repeating Pool & Mastery State:** Track `seen_chunk_ids`, `seen_question_hashes`, and concept mastery scores in `IndexedDB` / PostgreSQL so quizzes never repeat stale questions across Timed/Untimed study modes.
3. **Nightly Curriculum Dreaming:** Batch-analyze student wrong answers and thumbs-downs out-of-band to identify ambiguous questions or missing syllabus coverage.
