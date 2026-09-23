# 2026-09-23 — CS410 MP1 Task 1 done, Task 2 TF-IDF script next

**Handoff Mode: Implementation**
**Receiving agent job: Resume and continue**

## 1. Thread Purpose
CS410 MP1 warmup explanation, then Graded Task 1 (BM25 `k1`/`b` sweeps on Cranfield with nDCG@10 and Precision@10 plots). Task 2 (algorithm comparison) was started only far enough to prove how TF-IDF is invoked in this Pyserini build. The user is leaving. On return they want to **investigate** a separate `.py` file that is entirely TF-IDF and mirrors the modular shape of `main.py`. Do not implement that file until they confirm the shape.

## 2. Stack & Environment
- Fedora host. User `isaacsimms`. System Java is OpenJDK 25; do not use it for this project.
- Conda env `pyserini`: `/home/isaacsimms/miniconda3/envs/pyserini`, Python 3.12, Pyserini **2.4.0**, bundled Anserini fatjar **2.3.0**.
- OpenJDK **21** is required. This session: `conda activate pyserini` sets `JAVA_HOME` to `/home/isaacsimms/miniconda3/envs/pyserini/lib/jvm`. Bare `python` (base / `/usr/bin/python`) cannot import `pyserini`.
- Matplotlib **3.11.2** is already in the env.
- Working directory for runs:
  `/home/isaacsimms/Desktop/MCS-UIUC/Text Information Systems - CS410/Programming/MP1/CS410-MP1-code/`
- Run pattern: `source ~/miniconda3/etc/profile.d/conda.sh && conda activate pyserini && python main.py`

## 3A. What Was Accomplished
1. Explained `preprocess_corpus` document ids: `"id": f"{i}"` is the 0-based corpus line number as a string so Lucene `hit.docid` matches qrels doc ids.
2. Switched `cname` to `"cranfield"` (`query_id_start` is already `1` for Cranfield).
3. Added `compute_precision_at_k` (relevance `> threshold`; missing qrels doc = 0). Task 1 uses `threshold=0`, so Cranfield grades 1–4 all count as relevant.
4. Graph A: `sweep_b` / `plot_b_sweep`. `k1` fixed at **0.9**. `b` from **0.0 to 1.0** step **0.1**. Wrote `bm25_b_sweep_cranfield.json` and `.png`.
5. Graph B: `sweep_k` / `plot_k_sweep`. `b` fixed at **0.4**. `k1` in **`[0.0, 0.3, 0.6, 0.9, 1.2, 1.5, 2.0, 2.5, 3.0]`**. Wrote `bm25_k_sweep_cranfield.json` and `.png`.
6. Built Cranfield once: `processed_corpus/cranfield` (1400 JSON files) and `indexes/cranfield`. Indexer log: **1,398 indexed, 2 empty**. Ids stay the line index inside each JSON, so the two empty lines do not renumber the rest.
7. Proved TF-IDF on that same index (one query only). No TF-IDF script was added.

### Graph A scores (`k1=0.9`)
`b` 0.0 → 1.0 nDCG@10: 0.3161, 0.3225, 0.3299, 0.3322, 0.3417, 0.3448, 0.3464, 0.3487, 0.3532, 0.3529, **0.3547**.
Precision@10: 0.1969, 0.2040, 0.2080, 0.2107, 0.2173, 0.2196, 0.2209, 0.2209, 0.2240, **0.2253**, 0.2244.
Both rise and flatten. nDCG peaks at `b=1.0`. Precision peaks at `b=0.9`. Pyserini default `b=0.4` is on the rising side, short of the plateau.

### Graph B scores (`b=0.4`)
`k1` 0.0, 0.3, 0.6, 0.9, 1.2, 1.5, 2.0, 2.5, 3.0.
nDCG@10: 0.2724, 0.3139, 0.3298, 0.3417, 0.3423, 0.3472, 0.3507, 0.3531, **0.3545**.
Precision@10: 0.1782, 0.1987, 0.2089, 0.2173, 0.2169, 0.2231, 0.2244, 0.2284, **0.2289**.
`k1=0` ignores term frequency and is the worst point. Most of the gain is in by `k1=1.5`. Best point **on this grid** is `k1=3.0`. The curve is still flat-rising at the right edge; nothing above 3.0 was run. Tiny Precision dip at `k1=1.2` (0.2169 vs 0.2173 at 0.9) while nDCG still ticks up.

### Cranfield judgment facts used in the Task 1 reading
225 queries, 1,612 judgments. Grades: 1=363, 2=734, 3=387, 4=128. No explicit 0s. Per query: min 1, median 6, mean 7.16, max 39. 173 queries have fewer than 10 judged docs. A perfect top-10 could only reach Precision@10 ≈ **0.605**. Best observed Precision@10 ≈ 0.225 is about 2.3 relevant hits in 10, not a failed run. Provided `compute_ndcg` uses **linear** gain (`rel / log2(rank+1)`). The exponential form is commented out.

## 4A. Current State
`main.py` is the Task 1 driver. `main()` always reruns **both** sweeps and overwrites the four `bm25_*_sweep_cranfield.*` files. It no longer writes a single-query `results_cranfield.json`. `results_apnews.json` is a leftover warmup file; `cname` is Cranfield.

Task 2 is not started in code. The user rejected folding TF-IDF into `main.py` as the next move. They want a **separate** script that copies `main.py`'s modular layout (load corpus/queries/qrels, search, score) but scores only with TF-IDF.

TF-IDF call that worked, on a **fresh** `LuceneSearcher`, before any search:

```python
from pyserini.pyclass import autoclass
tfidf = LuceneSearcher(index_dir)
ClassicSimilarity = autoclass("org.apache.lucene.search.similarities.ClassicSimilarity")
tfidf.object.searcher.setSimilarity(ClassicSimilarity())
```

Checked on the first Cranfield query (`query_id_start` still applies when scoring, not to this raw search). Top-10 doc ids, BM25 `k1=0.9, b=0.4`: `50, 485, 183, 572, 11, ...`. TF-IDF: `50, 11, 485, 877, 183, ...`. Order changed. Full 225-query nDCG was **not** run.

`LuceneSearcher` in this install exposes `set_bm25` and `set_qld` only. There is no `set_tfidf` and no `set_similarity` on `io.anserini.search.SimpleSearcher`.

## 5. Key Decisions & Rationale

| Decision | Rationale |
|----------|-----------|
| Task 1 dataset is Cranfield only | Assignment text. `cname = "cranfield"`. |
| Precision@10 threshold is 0 | User did not pick the stricter `> 2` cutoff. Grades 1–4 count. State this in the report. |
| Graph A holds `k1=0.9`; Graph B holds `b=0.4` | One-factor sweeps. These are Pyserini defaults for the held parameter. They are not a joint optimum. |
| `k1` grid ends at 3.0 | Agreed sweep. Do not claim 3.0 is a global peak. |
| TF-IDF lives in its own `.py`, modeled on `main.py` | User's return intent. Do not drop `ClassicSimilarity` into `main()` as the design. |
| Reuse `indexes/cranfield` | Lucene ClassicSimilarity is a search-time similarity. Do not rebuild the index for TF-IDF. |
| Compare with nDCG@10 unless the user picks another metric | Task 2 allows any metric. nDCG@10 was the metric in the setup discussion. Not explicitly locked. |

## 6. Blockers & Open Questions
- **Separate-file shape is the open investigation.** Which pieces move vs stay imported from `main.py` (preprocess/index/load/search/`compute_ndcg`) is not decided. User asked to investigate, not to write the file yet.
- **BM25 baseline pair for Task 2 is not chosen.** Legal choices already measured: `k1=0.9, b=1.0` (best nDCG on the `b` sweep) or `k1=3.0, b=0.4` (best on the `k1` sweep). Say which pair is the baseline. No joint grid was run.
- **Second extra algorithm is not chosen.** Task 2 requires **two** algorithms besides BM25. Only TF-IDF was requested. `set_rm3` was mentioned as the supported pseudo-relevance-feedback option (`searcher.set_bm25(...)` then `searcher.set_rm3(...)`). User has not picked it.
- **Do not assign `searcher.object.similarity`.** Pyjnius field writes corrupt that field. Calling `get_similarity()` afterward SIGSEGV'd the JVM (OpenJDK 21). Use only `searcher.object.searcher.setSimilarity(...)`. Do not call `set_bm25` on that same searcher afterward; it replaces the similarity.
- Crash logs `hs_err_pid114216.log` and `hs_err_pid114504.log` were created in `CS410-MP1-code` during that bad field write and then deleted.

## 7. Next Steps (Ordered)
1. Read this handoff. Propose how a separate TF-IDF script mirrors `main.py` (what it imports, what it copies, what it refuses to own). Wait for the user before creating the file.
2. After they accept the shape, add that script: fresh `LuceneSearcher` on `indexes/cranfield`, `ClassicSimilarity` via `object.searcher.setSimilarity`, same `search` + `compute_ndcg` path, print nDCG@10. No plot.
3. Score BM25 once at the baseline pair they choose, on the same queries, and report both numbers.
4. Ask which second algorithm they want. Do not start Task 3 or a PDF report unless they ask.

## 8. Must-Knows for the New Thread
- User paces the assignment. Explain the change, then edit only what they asked. They left specifically to resume on the separate TF-IDF file.
- `ClassicSimilarity` is the name to use in code. In the report call it TF-IDF. It has no `k1`/`b`. Lucene's formula: `tf = sqrt(freq)`, `idf = log((N+1)/(df+1))+1`.
- Document id contract: string line index `"0"`, `"1"`, ... Query ids for Cranfield start at 1. Breaking either makes nDCG look like 0.
- `main.py` currently spends its whole `main()` on the two sweeps. A TF-IDF script should not rerun those sweeps.
- Task 1 plots already exist. Do not regenerate them unless asked.
- Instructions: `Text Information Systems - CS410/Programming/MP1/Docs/Instructions.md`. Task 2 is lines 86–92. Deliverable later is a PDF plus the `.py` files in one zip. Peer-review context from the prior handoff: due **10/25** *(carried forward, not re-checked this thread)*.

## 9. Relevant Artifacts
- Script: `.../CS410-MP1-code/main.py` — Task 1 sweeps. Functions added: `compute_precision_at_k`, `sweep_b`, `plot_b_sweep`, `sweep_k`, `plot_k_sweep`.
- Plots/scores: `bm25_b_sweep_cranfield.png`, `bm25_b_sweep_cranfield.json`, `bm25_k_sweep_cranfield.png`, `bm25_k_sweep_cranfield.json` in `CS410-MP1-code/`.
- Index: `CS410-MP1-code/indexes/cranfield`. Corpus JSON: `CS410-MP1-code/processed_corpus/cranfield`.
- Data: `CS410-MP1-code/data/cranfield/{cranfield.dat,cranfield-queries.txt,cranfield-qrels.txt}`.
- Assignment: `.../Programming/MP1/Docs/Instructions.md`.
- Prior env handoff: `.../Programming/MP1/Docs/Handoffs/09-22-2026CS410MP1Handoff01.md`.
- Searcher source of truth for this install: `.../site-packages/pyserini/search/lucene/_searcher.py` (`set_bm25`, `set_qld` only) and `pyserini/resources/jars/anserini-2.3.0-fatjar.jar` class `io.anserini.search.SimpleSearcher`.
