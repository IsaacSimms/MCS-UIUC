# [MODE A] — Thread Handoff Document

> **Handoff Mode: Implementation**
> **Receiving agent job: Resume and continue**

## 1. Thread Purpose

Finish the Task 1 write-up for CS410 MP2. A separate thread, with no handoff of its own, ran the baseline RAG demo and saved the three screenshots. This thread only decided how to analyze those runs and drafted the discussion paragraph. Task 1 is not submitted. Tasks 2 and 3 have not started.

## 2. Stack & Environment

Confirmed in the prior install handoff and still true. This thread did not re-run the demo.

- Code root: `Text Information Systems - CS410/Programming/MP2/_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2`
- Conda env `pyserini` (Python 3.12.14, Pyserini 2.4.0, conda OpenJDK 21). System Java 25 breaks Pyserini.
- Ollama 0.40.7, model `llama3.2:3b`, CPU. No API key.
- `.env`: `PYSERINI_CNAME=apnews`, `OLLAMA_MODEL=llama3.2:3b`, `RETRIEVER_K=3`, `PYSERINI_K1=0.9`, `PYSERINI_B=0.4`. `OLLAMA_BASE_URL` is set and unused. `OllamaLLM` posts to `http://localhost:11434/api/generate` with `model`, `prompt`, and `stream` only.
- Index already built: `processed_corpus/apnews`, `indexes/apnews`.
- Pipeline: BM25 top-3, then `LLMChainExtractor`. On 0 compressed docs, `agent.py` falls back to the raw retriever. Prompt in `build_prompt`: use only the context; if the answer is not there, say you don't know; at most 7 sentences.

## 3A. What Was Accomplished

1. Read `docs/Instructions.md`, `docs/Context.md`, `docs/handoffs/2026-10-21-mp2-resume-after-install.md`, `docs/recaps/2026-10-21-mp2-baseline-install.md`, the README, and `agent.py` / `main.py` / `utils/llm.py`.
2. Read the three Task 1 screenshots. Did not re-run `python main.py`.
3. Settled the Task 1 discussion shape with the user (see §5).
4. Wrote `docs/Task1/TaskOneAnalysisDraft.md`: the paper paragraph plus a three-item claim checklist.
5. After that file was written, explained the generation failure. The file does not yet contain the "mixed / indirect" sentence in §4A. Do not patch it unless the user asks.

## 4A. Current State

You are here: Task 1 screenshots exist, and the discussion paragraph is drafted. The user has the screenshots in their own doc, back to back. They will write the paper paragraph themselves. The draft is the source text.

Screenshot order, which is also the paragraph order:

1. `docs/Task1/Qeustion1.png` — "What was the Soviet response to the Chernobyl nuclear disaster?" Answered well. The response followed the retrieved article. Log: `Compression yielded 0 docs; falling back to base retriever.` Then `Retrieved 3 documents`.
2. `docs/Task1/Question2.png` — "What was the American response to the fall of the Berlin Wall?" Printed answer: `I don't know.` Same compression fallback, then 3 raw documents. The logged `context` includes that President Bush's response as the wall came down was cautious, and that when the border opened his response was bland and bureaucratic, with no major policy move. `final_answer` in the same `Agent result` dict is `I don't know.`
3. `docs/Task1/Question3.png` — "How did the Iowa caucuses affect the New Hampshire primary?" Answered well. The response followed the retrieved article. Same compression fallback.

Cause of the Berlin Wall "I don't know": generation. The context contained the answer. It is not a missing article and not a hallucination. A context-window overflow is unlikely: the same three-document fallback produced real answers on the other two questions, and the code does not set a tighter limit. The Bush lines are mixed with the 1961 Kennedy crisis and other Berlin Wall material, and they state the response indirectly. The prompt invites "I don't know," and `llama3.2:3b` took that exit.

Wording offered to the user, not yet copied into the draft: the retrieved article already describes Bush's response as cautious, bland, and bureaucratic, with no major policy move, but the model answered "I don't know." Those lines are mixed in with the 1961 crisis and other Berlin Wall material, and they never state the response directly, so the model did not use them. The context contained the answer, so this is a generation failure rather than a missing article or a hallucination.

How to see it in Question 2 without a new run: one `Agent result` log line holds both `context` (search for "Bush's response was bland and bureaucratic") and `final_answer` (`I don't know.`). The compression line is an earlier step and appears on all three runs.

## 5. Key Decisions & Rationale

| Decision | Rationale |
|----------|-----------|
| These three screenshots are the whole Task 1 case set | The deliverable is at least three questions plus a short discussion. No fourth run. |
| Screenshots back to back, then one paragraph the user writes | Matches the deliverable. No setup section. |
| Opening of the paragraph | All three used the README pipeline and dataset. Every run logged compression yielded 0 docs, fell back to the base retriever, and retrieved 3 documents. Compression is shared, so it is not the Berlin Wall cause. |
| Paragraph order is screenshot order | Chernobyl, Berlin Wall, Iowa. The failure sits in the middle on purpose. |
| Chernobyl and Iowa: short success sentences | Each answer followed the retrieved article. Do not retell the articles. |
| Berlin Wall: generation failure, with the Bush clause | The logged article states the response. The model still said "I don't know." |
| "Difficult to parse" is the right idea; do not use "parse" | The model failed to pick out an indirect answer, not to read the text. |
| Three blocks are a checklist only | The paper stays one paragraph. Checklist is in the draft under the paragraph. |
| Do not re-run the demo to prove Task 1 | User already knows it works. |

## 6. Blockers & Open Questions

- No code blocker.
- The draft's Berlin Wall sentences do not yet include the mixed-1961 / indirect wording from §4A. The user has that wording in chat and did not ask for the file to be updated.
- Whether the user has pasted the paragraph into the report doc is unknown. The screenshots in `docs/Task1/` are the copies in the repo. The user also has them in their own doc.
- Tasks 2 and 3 are untouched.

## 7. Next Steps (Ordered)

1. Wait until the user says to continue. Do not re-open the Task 1 decisions in §5.
2. If they want the draft brought in line with the later wording, edit only the Berlin Wall sentences in `docs/Task1/TaskOneAnalysisDraft.md`. Add that the Bush lines are mixed with the 1961 crisis and other Berlin Wall material and state the response indirectly.
3. Leave the paragraph in their report doc for them to place after the three screenshots, unless they ask for the paste.
4. Only when they ask: Task 2 (at least two user-facing improvements in `main.py`, `agent.py`, or `utils/retriever.py`), then Task 3 (long queries over 200 characters or more than one sentence; 2–4 sub-queries; fuse; then generate).

## 8. Must-Knows for the New Thread

- User paces the work. Do not write the PDF, start Task 2, or "finish MP2" unprompted.
- Do not re-run the index or the three questions to confirm Task 1.
- The other thread produced the screenshots. This thread produced the analysis. There is no handoff from the screenshot thread.
- Screenshot filename typo is real: `Qeustion1.png`.
- `main.py` logs the full agent state at INFO, including `context` and `final_answer`. The terminal UI prints only `Answer:`.
- If a later shell is needed: `source ~/miniconda3/etc/profile.d/conda.sh && conda activate pyserini`, Java 21, quote paths with spaces. Do not `pip install -r requirements.txt` without fixing NumPy; 1.26.4 breaks this Pyserini. Keep NumPy 2.5.4.
- Do not move or delete MP1's `data/`. The MP2 copy stays.

## 9. Relevant Artifacts

| Path | Role | State |
|------|------|--------|
| `docs/Task1/TaskOneAnalysisDraft.md` | Paper paragraph and claim checklist | Written this thread. Berlin Wall "why" is missing the later mixed/indirect sentence |
| `docs/Task1/Qeustion1.png` | Chernobyl screenshot | From the other thread |
| `docs/Task1/Question2.png` | Berlin Wall screenshot | From the other thread. Evidence for the generation failure |
| `docs/Task1/Question3.png` | Iowa / New Hampshire screenshot | From the other thread |
| `docs/Instructions.md` | Assignment brief and grading | Unchanged |
| `docs/Context.md` | Architecture reference | Written 2026-10-21. Says `.env` and the index were not created; both now exist |
| `docs/handoffs/2026-10-21-mp2-resume-after-install.md` | Install handoff | Superseded for "where we are." Still the source for env pitfalls |
| `docs/recaps/2026-10-21-mp2-baseline-install.md` | Install recap | Backward record only |
| `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/` | Code root | Starter code. Task 2 and 3 comments are unfilled |
