# CS410 MP2 Task 3 long queries

**Date:** 2026-10-24
**Type:** implementation

## TL;DR

Task 3 is implemented. A question over 200 characters, or with more than one sentence, is split into 2–4 sub-queries, searched with BM25, and fused to the top 3 passages. The user ran both screenshots. The next thread is analysis only.

## Context & Goal

CS410 MP2 Task 3 asks the agent to accept a long information need, generate 2–4 sub-queries, fuse the hits, and answer from that merged context. Task 1 and Task 2 were already done. The runnable tree is `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/`. The corpus is AP News. The brief’s RAG-components example would not retrieve relevant documents here.

## Key Points Explored

- The course comments put decomposition and fusion inside `retrieve` in `agent.py`. `retriever.py` stays one BM25 call per query.
- Task 1 and Task 2 both logged `Compression yielded 0 docs` and then used the full articles. Searching each sub-query through that compressor would add empty model calls on CPU.
- Two to four sub-queries at `RETRIEVER_K=3` is up to 12 full articles. `llama3.2:3b` already missed a good passage inside three articles on the Berlin Wall question, so the fused list stays at 3.
- Raw BM25 scores are not on one scale across queries. Reciprocal rank fusion uses rank: `1 / (60 + rank)`.
- The graded example is one Chernobyl paragraph, not the three Task 1 questions. A fresh run of the original one-line Chernobyl question shows the short path. The old Task 1 image stays in `docs/Task1/`.
- The short screenshot and the long screenshot are different questions. The short run is not the unsplit search of the long paragraph.

## Decisions & Outcomes

- Short questions keep the Task 2 path: one search, compression then fallback, yellow snippets anchored on the question, green answer, no `Sub-queries` block.
- The long branch lives in `retrieve`. Trigger: stripped length greater than 200, or two or more non-empty pieces split on `.`, `!`, or `?`.
- One `OllamaLLM` call asks for 2–4 concise queries, one per line. Fewer than 2 lines, or a failed call, searches the original question once and leaves `subqueries` empty.
- Each sub-query calls `base_retriever` only. Duplicate doc ids are dropped. Fusion keeps the top `RETRIEVER_K` passage strings. The answer prompt still receives the original question.
- A long run prints cyan `Sub-queries`, then yellow snippets whose window uses those lines, then the green answer. The 500-character cutter is unchanged.
- `docs/Task3/` holds copies of each changed code file. The write-up was deferred. The user will ask for it in the analysis thread.
- Checked without the REPL: the Chernobyl paragraph trips the trigger, the one-line question does not, a failed split falls back to one search, and a document in more than one list ranks first. The user ran `python main.py`.

Screenshot observations, from the saved images:

- `Sub200CharQuestion1.png`: question `What was the Soviet response to the Chernobyl nuclear disaster?` Log shows compression yielding 0 docs, then 3 documents. No `Sub-queries` block. Snippets cover the death toll and cleanup, defensive officials, and a nuclear-operators association. The green answer follows that defensive-response material.
- `Above200CharQuestion1.png`: the long Chernobyl paragraph. Log has no compression line. Cyan sub-queries: `Soviet government response Chernobyl disaster`, `Chernobyl evacuation coverage`, `Release of information Chernobyl`. Snippet 1 is a Bryansk dispatch that names 12 villages to be evacuated. Snippets 2 and 3 overlap the short run’s response coverage. The green answer centers on the defensive response and the release of information.

## Open Questions / Next Steps

- The next thread is analysis only: whether the fused result was more relevant, using these two screenshots.
- The settled comparison against one BM25 search of the same long paragraph was not run. These two shots compare a short question with a long one.
- The submission zip (report PDF plus modified `.py` files) has not been built.
- `docs/Context.md` was updated after this recap was first saved, on 2026-10-24, so it now describes the long-question branch.

## Artifacts

| Path | State |
|------|--------|
| `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/agent.py` | Long branch in `retrieve`. This is the file to run. |
| `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/main.py` | Cyan sub-queries. Short path still uses the Task 2 window. |
| `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/utils/state.py` | `subqueries` on `GraphState`. |
| `docs/Task3/agent.py`, `main.py`, `state.py` | Submission copies from this implementation. |
| `docs/Task3/Sub200CharQuestion1.png` | Fresh one-line Chernobyl run. No sub-query block. |
| `docs/Task3/Above200CharQuestion1.png` | Long Chernobyl run. Three sub-queries, evacuation in snippet 1. |
| `docs/Instructions.md` | Task 3 brief. One long example is the required report piece. |
