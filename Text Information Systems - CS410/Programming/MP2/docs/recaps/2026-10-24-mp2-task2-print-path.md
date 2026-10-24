# CS410 MP2 Task 2 print path

**Date:** 2026-10-24
**Type:** implementation

## TL;DR

Task 2 is done. `main.py` now prints a yellow 500-character snippet of each retrieved article before a green answer. Retrieval and generation are unchanged. The same three Task 1 questions were re-run in Ghostty, and the screenshots are in `docs/Task2/`.

## Context & Goal

CS410 MP2 Task 2 asks for at least two user-facing improvements so a person can see why the agent answered as it did. Task 1 had already reproduced the baseline: BM25 top-3 on AP News, compression falling back to the raw hits, and `llama3.2:3b` on CPU. The baseline terminal logged the full agent state and printed only `Answer:`.

## Key Points Explored

- The runnable tree is `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/`. Imports, `.env`, and the Lucene index resolve from there. A copy under `docs/` does not run.
- `PyseriniBM25Retriever` already stores `docid`, `score`, and `title`. `retrieve` keeps only `page_content`. Scores were considered and left out.
- On `doc155162` (Berlin Wall, 5,294 characters) the first content word is `Berlin` at character 9. The opening already says Bush was cautious and subdued as the wall came down. “Bland and bureaucratic” is at character 2,899. A density window scores highest near character 3,150 on the Kennedy “Ich bin ein Berliner” passage, because `Berlin` and `wall` repeat there.
- `STOPWORDS` is a `frozenset` of function words longer than two letters. Without it, `the` or `was` would win the earliest-hit race and anchor the snippet on a function word.
- The Berlin Wall answer text changed between Task 1 (`I don't know.`) and Task 2 (a longer refusal that the context does not discuss the fall). Retrieval was not changed. That is a new sample from the same model and the same full articles.
- Comment style follows `~/.cursor/AGENTS.md`: file-level summary, `# == Title == #` on sizable blocks, same-line notes only where the line is not obvious, no method docstrings.

## Decisions & Outcomes

- Edit and run `main.py` in the code root. `docs/Task2/main.py` is a duplicate for the submission bundle.
- Two graded items: a snippet before the answer, and color that separates them. No score or doc-id line.
- The model still receives the full articles. The cut is print-only.
- Drop the full `Agent result` log. Keep the short pipeline lines.
- Snippet rule: whole-word content terms, earliest hit, 500 characters, extend to the next whitespace, `...` if the article continues. No hit starts at the beginning of the article. One numbered snippet per hit under yellow `Retrieved`. The answer is bright green under `Answer`. Errors stay the default color.
- Comparison run is the same three Task 1 questions, in the same order. The user ran them in Ghostty from another thread. This thread checked the cutter on `doc155162` and did not launch `python main.py`.
- Usability claim, from those screenshots: the printed excerpts are short enough to read, and the color marks evidence versus the answer. On Berlin Wall, snippet 1 shows Bush cautious and subdued while the green answer denies that the context discusses the fall. Snippets 2 and 3 are Brandt and Honecker. On Iowa, only snippet 3 is the Dole / New Hampshire passage. The readable text is the window, not every sentence the model saw.

## Open Questions / Next Steps

- Task 3 has not started: long queries over 200 characters or more than one sentence, 2–4 sub-queries, fuse, then generate.
- The Task 2 explanation was given in chat. It was not saved as a draft file under `docs/Task2/`.
- The submission zip (report PDF plus modified `.py` files) has not been built.
- `docs/Context.md` still describes the pre-Task-2 tree: no `.env`, no index, and Task 2 as an unfilled print comment that includes scores.

## Artifacts

| Path | State |
|------|--------|
| `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/main.py` | Task 2 print path. This is the file to run. |
| `docs/Task2/main.py` | Identical submission copy. Does not run from that directory. |
| `docs/Task2/Question1.png` | Chernobyl. Yellow snippets, green answer. |
| `docs/Task2/Question2.png` | Berlin Wall. Snippet 1 shows the cautious Bush response; the answer still refuses. |
| `docs/Task2/Question3.png` | Iowa caucuses. Snippet 3 is the relevant hit. |
| `docs/Task1/TaskOneAnalysisDraft.md` | Baseline discussion. Unchanged this thread. |
| `agent.py`, `utils/retriever.py` | Unchanged. |
