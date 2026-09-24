# 2026-09-23 — TF-IDF and RM3 scripts ready, analysis next

**Handoff Mode: Implementation**
**Receiving agent job: Resume and continue**

## 1. Thread Purpose
CS410 MP1 Graded Task 2. Task 1 BM25 sweeps on Cranfield were already done. This thread settled a separate-file design, then added `tfidf.py` and `rm3.py`. The user is leaving. On return they will run those two scripts themselves, then analyze them against `main.py` and the existing BM25 sweep artifacts. Do not rerun the scripts or start the analysis until they ask.

## 2. Stack & Environment
- Fedora host. User `isaacsimms`. System Java is OpenJDK 25; do not use it.
- Conda env `pyserini`: `/home/isaacsimms/miniconda3/envs/pyserini`, Python 3.12, Pyserini **2.4.0**, Anserini fatjar **2.3.0**.
- OpenJDK **21**. `conda activate pyserini` sets `JAVA_HOME` to `/home/isaacsimms/miniconda3/envs/pyserini/lib/jvm`. Bare `python` cannot import `pyserini`.
- Working directory for runs:
  `/home/isaacsimms/Desktop/MCS-UIUC/Text Information Systems - CS410/Programming/MP1/CS410-MP1-code/`
- Run pattern: `source ~/miniconda3/etc/profile.d/conda.sh && conda activate pyserini && python tfidf.py` (same for `rm3.py` and `main.py`).

## 3A. What Was Accomplished
1. Grilled the Task 2 shape. Decisions are in §5. Do not re-litigate them.
2. Added `tfidf.py`. Imports loaders, `search`, `compute_ndcg`, and `compute_precision_at_k` from `main.py`. Opens a fresh `LuceneSearcher` and installs Lucene `ClassicSimilarity` via `searcher.object.searcher.setSimilarity`. No `k1`/`b`. No plot. No BM25 call.
3. Added `rm3.py`. Same import and dataset skeleton. Calls `set_bm25(k1=0.9, b=0.4)` then `set_rm3(fb_terms=10, fb_docs=10, original_query_weight=0.5)` on that same fresh searcher.
4. Both scripts were run once in this thread on Cranfield (225 queries). Index build was skipped. Printed scores:
   - TF-IDF: nDCG@10 **0.3537**, Precision@10 **0.2249**
   - RM3: nDCG@10 **0.3602**, Precision@10 **0.2391**
5. Explained that the formulas are not in the Python files. Lucene scores; Anserini implements RM3; Pyserini is the Python wrapper. `ClassicSimilarity` is the TF-IDF name to use in code. In the report call it TF-IDF. Formula: `tf = sqrt(freq)`, `idf = log((N+1)/(df+1))+1`.

## 4A. Current State
`main.py` is still the Task 1 driver. `main()` always reruns both BM25 sweeps and overwrites `bm25_*_sweep_{cname}.*`. It does not score TF-IDF or RM3.

`tfidf.py` and `rm3.py` sit beside `main.py`. Default `cname` is `"cranfield"`. Each prints one line with dataset, model, nDCG@10, and Precision@10 (`threshold=0`). Neither writes JSON or a plot. Neither reads the sweep JSON.

Cranfield index and processed corpus already exist. `apnews` and `new_faculty` do not. Changing `cname` in either new script builds that dataset's index on first run and does not overwrite Cranfield.

Task 2 comparison numbers already measured on Cranfield, same queries, nDCG@10 / Precision@10, relevance `> 0`:

| Run | nDCG@10 | Precision@10 |
|---|---|---|
| BM25 `k1=0.9`, `b=0.4` (sweep JSON, not recomputed this thread) | 0.3417 | 0.2173 |
| TF-IDF | 0.3537 | 0.2249 |
| RM3 on that same BM25 pair | 0.3602 | 0.2391 |

On these settings RM3 leads, then TF-IDF, then untuned BM25. The user has not yet done this comparison themselves. No report text has been written.

## 5. Key Decisions & Rationale

| Decision | Rationale |
|----------|-----------|
| TF-IDF and RM3 each get their own `.py` | User rejected folding them into `main.py`. |
| Import shared functions from `main.py` | One definition of nDCG and Precision. `if __name__ == "__main__"` keeps `python tfidf.py` from launching sweeps. Run from `CS410-MP1-code`. |
| Dataset swap is `cname = "cranfield"` / `"apnews"` / `"new_faculty"` | Same pattern as `main.py`. Paths and `query_id_start` (`apnews` 0, others 1) are copied into each driver. |
| Build the index only when missing | A `cname` swap works on first run. Cranfield stays a skip. `build_index` already stores docvectors, which RM3 requires. |
| One run prints nDCG@10 and Precision@10, no plot | Task 2 needs one metric. The win/loss claim uses nDCG@10. Precision uses `threshold=0` (grades 1–4 count), matching Task 1. |
| TF-IDF has no weight sweep | `ClassicSimilarity` has no `k1`/`b`. Do not invent a parameterized TF-IDF. |
| Base BM25 is `k1=0.9`, `b=0.4` | Pyserini defaults. nDCG@10 0.3417 and P@10 0.2173 already in the `b` sweep at `b=0.4`. Tuned peaks (`k1=0.9, b=1.0` → 0.3547; `k1=3.0, b=0.4` → 0.3545) are not the baseline. |
| The new scripts do not recompute BM25 | Cranfield baseline is the sweep JSON. Another dataset's BM25 number comes from `main.py` later. Output names include `cname`, so that run does not overwrite Cranfield plots. It does run both full sweeps. |
| Second algorithm is RM3, not QLD, Rocchio, or Faiss | Assignment lists pseudo-relevance feedback. RM3 runs on the existing Lucene index. Faiss would need a new embedding index. |
| RM3 constants are the Pyserini defaults, editable, no sweep | `k1`/`b` match the baseline so the comparison is untuned BM25 vs that BM25 plus feedback. |
| Do not assign `searcher.object.similarity` | Pyjnius field writes corrupt that field and SIGSEGV'd the JVM. TF-IDF must use `searcher.object.searcher.setSimilarity(...)`. Do not call `set_bm25` on that same searcher afterward. |

## 6. Blockers & Open Questions
- **Analysis is not started.** The user will run `tfidf.py` and `rm3.py`, then compare to `main.py` and the sweep artifacts. Help with that reading. Do not regenerate Task 1 plots.
- **Task 3 dataset is not chosen** (`apnews` or `new_faculty`). Do not build either index until they pick one.
- **No PDF report** unless they ask. Peer-review due date **10/25** is carried forward from the prior handoff and was not re-checked.
- Sweep curves are still flat-rising at the right edge (`b=1.0`, `k1=3.0`). Do not call either point a global optimum.

## 7. Next Steps (Ordered)
1. Wait while the user runs `python tfidf.py` and `python rm3.py` from `CS410-MP1-code` in the `pyserini` env. Confirm their printed lines match §4A before treating the numbers as theirs.
2. When they ask, analyze those lines against `main.py` and `bm25_b_sweep_cranfield.json` / `bm25_k_sweep_cranfield.json`. Baseline row is `k1=0.9`, `b=0.4`. State what is better, by how much, and what the comparison does not show (no joint BM25 grid, RM3 is BM25 plus expansion, TF-IDF cannot be tuned).
3. Ask which second dataset they want for Task 3. Do not start it in the same step as the Cranfield reading unless they ask.

## 8. Must-Knows for the New Thread
- User paces the assignment. Explain, then edit only what they asked.
- They just learned the algorithms are not written out in the `.py` files. If they ask again: Lucene scores, `ClassicSimilarity` is TF-IDF, `set_rm3` is Anserini feedback on top of `set_bm25`, Pyserini is the wrapper.
- Document ids are the string line index `"0"`, `"1"`, ... Cranfield query ids start at 1. Breaking either makes nDCG look like 0.
- `main.py`'s `main()` spends the whole run on both sweeps. Do not point the user at `python main.py` for a single BM25 number on Cranfield. The JSON already has it.
- Instructions: `Text Information Systems - CS410/Programming/MP1/Docs/Instructions.md`. Task 2 is lines 86–92. Task 3 is lines 94–98.
- Prior handoff for Task 1 numbers and the JVM crash: `Docs/Handoffs/2026-09-23-tfidf-separate-script.md`.

## 9. Relevant Artifacts
- `CS410-MP1-code/tfidf.py` — TF-IDF driver. Done. Default Cranfield.
- `CS410-MP1-code/rm3.py` — RM3 driver. Done. Default Cranfield.
- `CS410-MP1-code/main.py` — Task 1 sweeps only.
- `CS410-MP1-code/bm25_b_sweep_cranfield.json` and `.png` — `k1=0.9`, `b` from 0.0 to 1.0. Baseline `b=0.4` is in here.
- `CS410-MP1-code/bm25_k_sweep_cranfield.json` and `.png` — `b=0.4`, `k1` grid through 3.0.
- Index: `CS410-MP1-code/indexes/cranfield`. Corpus JSON: `CS410-MP1-code/processed_corpus/cranfield`.
- Assignment: `Programming/MP1/Docs/Instructions.md`.
