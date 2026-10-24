# CS410 MP2 — Context & Architecture Reference

Local retrieval-augmented generation demo for CS410. A student runs a terminal loop that retrieves AP News documents with Pyserini BM25 and asks a local Ollama model to answer from those documents only. The graded work is to run that baseline, then make the evidence visible to the user, then handle long questions by splitting them into sub-queries and fusing the hits.

Task 1 (baseline run and discussion), Task 2 (print-only snippets and color), and Task 3 (query decomposition and fusion) are implemented. The Task 3 relevance write-up is not saved yet.

The course brief is `docs/Instructions.md`, beside this file. The runnable tree is the nested project below, not this `docs/` directory.

---

## Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12.14 in conda env `pyserini` (`~/miniconda3/envs/pyserini`) |
| Retrieval | Pyserini 2.4.0, Lucene BM25 (`LuceneSearcher`) |
| JVM | OpenJDK 21.0.10 from the conda env. System Java 25 is unrelated and breaks Pyserini if the env is not active |
| Orchestration | LangGraph 0.2.76 (`StateGraph`) |
| LLM client | Custom `OllamaLLM` (`langchain.llms.base.LLM`) posting to `http://localhost:11434/api/generate`; compression uses `langchain_ollama.ChatOllama` |
| Local model | Ollama 0.40.7, model `llama3.2:3b` (2.0 GB). Service user `ollama`. Model files under `/usr/share/ollama/.ollama/` |
| Config | `python-dotenv` 1.1.1. `.env` exists and matches `.env.example` |
| Numeric stack | NumPy 2.5.4, SciPy 1.18.1. Do not install the `requirements.txt` pin `numpy~=1.26.4` |

Hardware on the machine that did setup: 16 GB RAM, GeForce RTX 3050 Ti Mobile present, NVIDIA driver not installed (`nvidia-smi` missing). Ollama runs on CPU.

---

## Project Structure

```
MP2/
├── docs/
│   ├── Instructions.md                      # assignment brief and grading
│   ├── Context.md                           # this file
│   ├── Task1/                               # baseline screenshots and analysis draft
│   ├── Task2/                               # Task 2 screenshots and a copy of main.py
│   ├── Task3/                               # Task 3 screenshots and copies of the changed .py files
│   ├── handoffs/                            # session transfer notes
│   └── recaps/                              # backward-looking session records
└── _c54a3a1b26dc478f9111276a6fe991cf_MP2/
    └── MP2/                                 # code root: cwd for python and pip
        ├── main.py                          # REPL entry; snippets and long-question sub-queries
        ├── agent.py                         # LangGraph pipeline; long-question split and fusion
        ├── README.md                        # install, configure, run
        ├── requirements.txt                 # pip pins; NumPy pin is unsafe here
        ├── .env.example                     # template
        ├── .env                             # present; same values as the example
        ├── utils/                           # config, llm, retriever, state
        ├── data/                            # copied MP1 corpora; apnews is indexed
        ├── processed_corpus/                # apnews JSON docs, one file per line
        └── indexes/                         # indexes/apnews Lucene index
```

`processed_corpus/apnews` and `indexes/apnews` were built on the first run. Non-empty directories are skipped on later launches.

### Code root — RAG agent

- `main.py` — loads `Config`, builds one retriever, loops on stdin, invokes the graph. `print_result` prints a yellow snippet of each context string and the green answer. A long question also prints the sub-queries in cyan. The model still receives the full articles.
- `agent.py` — two-node graph: `retrieve` then `generate_answer`. A long question is split and fused inside `retrieve`.
- `utils/config.py` — reads `.env`. Owns model name, corpus name, `RETRIEVER_K`, BM25 `k1` and `b`.
- `utils/retriever.py` — corpus preprocess, Lucene index build, `PyseriniBM25Retriever`, optional contextual compression.
- `utils/llm.py` — `OllamaLLM` HTTP client. `OllamaLLMForJson` is unused by the graph.
- `utils/state.py` — `GraphState` TypedDict passed between nodes. `subqueries` is empty unless a long question was split.
- `data/{cname}/{cname}.dat` — one document per line. Default `cname` is `apnews`. Also present: `cranfield`, `new_faculty`, plus query and qrels files the agent does not read.

### `data/` — corpora copied from MP1

Copied from `Programming/MP1/CS410-MP1-code/data`. MP1 still has its own copy. Baseline file: `data/apnews/apnews.dat` (~437 MB).

---

## Architecture Patterns

### Layering & Seams

| Seam | Interface | Implementations |
|------|-----------|-----------------|
| Retriever | `langchain_core.retrievers.BaseRetriever` | `PyseriniBM25Retriever`; wrapped by `ContextualCompressionRetriever` + `LLMChainExtractor` |
| Generation LLM | `langchain.llms.base.LLM` | `OllamaLLM` (hardcoded `http://localhost:11434/api/generate`) |
| Compression LLM | `ChatOllama` via `Config.get_llm()` | `ChatOllama(model=OLLAMA_MODEL)` piped to `StrOutputParser` |
| Graph state | `GraphState` TypedDict | single dict mutated by `retrieve` and `generate_answer` |
| Settings | `Config` | env vars with defaults; no other config source |

`RETRIEVER_BACKEND` is read in `Config` and never consulted. Retrieval is always Pyserini.

`main.py` passes `selected_namespaces` into the initial state. `GraphState` does not declare that key. Task 1 and Task 2 invokes both finished, so this LangGraph version accepted the extra key.

### Pipeline

```
stdin question
  → GraphState
  → retrieve:
       short (200 characters or fewer, and one sentence):
         retriever.invoke(question)
         BM25 top-k, then LLMChainExtractor
         on 0 compressed docs, fall back to base_retriever
       long (more than 200 characters, or more than one sentence):
         one OllamaLLM call writes 2–4 lines
         fewer than 2 lines, or a failed call: the short search above
         else each line calls base_retriever only
         drop duplicate doc ids, rank with 1/(60+rank), keep top RETRIEVER_K
       page_content strings appended to state["context"]
       state["subqueries"] set only when the split is used
  → generate_answer: OllamaLLM, original question, only that context, max 7 sentences
  → print_result:
       long split: cyan Sub-queries, yellow snippets anchored on those lines
       otherwise: yellow snippets anchored on the question
       then the green answer
```

`print_result` does not log the agent-state dict. The short INFO lines from retrieval and generation still print.

There is no web search. `web_search_tool` and `web_search_results` are unused state fields. `main.py` sets `web_search_tool=None`.

### Service lifetimes

- **Process-long:** one `Config`, one retriever (and therefore one Lucene searcher) created in `main()` and stored on every `GraphState`.
- **Per answer:** `generate_answer` constructs a new `OllamaLLM`. Compression's `ChatOllama` is created once inside `create_retriever()`.
- **Per long question:** `decompose_query` constructs another `OllamaLLM` before that. A short question does not. The long search does not call the compressor.

### Index build

`create_index(cname)` runs at retriever construction, before the first question:

1. If `processed_corpus/{cname}/` is missing or empty, `preprocess_corpus` writes `doc{i}.json` with `id` and `contents` for each line of `data/{cname}/{cname}.dat`.
2. If `indexes/{cname}/` is missing or empty, `python -m pyserini.index.lucene` builds a `JsonCollection` index with positions, docvectors, and raw stored (`--threads 1`).
3. Non-empty directories are skipped. Delete the matching directory to force a rebuild.

---

## Key Models

| Model | Key Fields |
|-------|-----------|
| `GraphState` | `question`, `context: List[str]`, `subqueries: List[str]`, `current_step`, `final_answer`, `retriever`, `web_search_tool`, `error`, `web_search_results` |
| `Document` (LangChain) | `page_content`; metadata `docid`, `score`, `title`. Fusion reads `docid`, then `retrieve` stores only `page_content` in `context` |
| Pyserini JSON doc | `id` (line number as string), `contents` (the raw line) |
| `Config` | `OLLAMA_MODEL`, `RETRIEVER_BACKEND`, `RETRIEVER_K`, `PYSERINI_CNAME`, `PYSERINI_K1`, `PYSERINI_B` |

`.env` sets `RETRIEVER_K=3`, `PYSERINI_K1=0.9`, `PYSERINI_B=0.4`. The code default for `RETRIEVER_K` is 7 when `.env` is absent.

---

## RAG Agent

Prompt rule in `build_prompt`: use only the retrieved context; if the answer is not in the context, say so; at most 7 sentences.

Task 2 is implemented in `main.py` only. `print_result` shows one numbered snippet per retrieved passage, then the answer. Snippets are bright yellow (`\033[93m`) under `Retrieved`. The answer is bright green (`\033[92m`) under `Answer`. Each snippet starts at the earliest whole-word content hit, takes 500 characters, and extends to the next whitespace. `STOPWORDS` is a `frozenset` of function words, so those words do not set the start. If no content word hits, the snippet starts at the beginning of the article. `...` marks a cut. Scores and doc ids are not shown. `retrieve` stores passage text in `context`. `utils/retriever.py` is unchanged.

`docs/Task2/main.py` is a duplicate for the submission bundle. It does not run from that directory. Screenshots of the three Task 1 questions, in order, are `docs/Task2/Question1.png` (Chernobyl), `Question2.png` (Berlin Wall), and `Question3.png` (Iowa caucuses). The Berlin Wall answer text differed from the Task 1 run. Retrieval was the same. That is a new sample from the same model and the same full articles. The yellow window is not the full text the model saw. On `doc155162`, “bland and bureaucratic” is past the 500-character cut. Snippet 1 still shows Bush as cautious and subdued as the wall came down.

Task 3 is implemented in `agent.py` and `main.py`. A sentence boundary is a split on `.`, `!`, or `?` after empty pieces are dropped. `decompose_query` asks `OllamaLLM` for 2–4 concise lines and strips blank lines, leading numbers, and bullets, keeping at most 4. `fuse_subqueries` calls `base_retriever` once per line. The same doc id adds `1 / (60 + rank)` for each list it appears in. Ties break by best rank, then doc id. The top `RETRIEVER_K` passages, 3 in `.env`, are the context. `docs/Task3/main.py`, `agent.py`, and `state.py` are submission copies and do not run from that directory. `Sub200CharQuestion1.png` is a fresh run of the one-line Chernobyl question: compression falls back, three snippets, no `Sub-queries` block. `Above200CharQuestion1.png` is the long Chernobyl paragraph. Its sub-queries were `Soviet government response Chernobyl disaster`, `Chernobyl evacuation coverage`, and `Release of information Chernobyl`. Snippet 1 names 12 villages to be evacuated. Those two screenshots are different questions. The unsplit search of the long paragraph was not run. `generate_answer` still has a comment about storing structured sub-query dicts in `context`. The code does not do that.

`OllamaLLM._call` sends `{"model", "prompt", "stream": false}` and returns JSON field `response`. It does not send `OLLAMA_BASE_URL`.

---

## Naming Conventions

### Backend

| Thing | Convention | Example |
|-------|-----------|---------|
| Corpus id | short lowercase name, directory and `.dat` share it | `apnews` → `data/apnews/apnews.dat` |
| Env vars | `SCREAMING_SNAKE` prefix by subsystem | `PYSERINI_K1`, `OLLAMA_MODEL` |
| Graph nodes | verb phrases matching `current_step` | `retrieve`, `generate_answer` |
| Index paths | `processed_corpus/{cname}`, `indexes/{cname}` | `indexes/apnews` |

---

## Code Style

- Starter modules use a banner docstring, then imports, then `logger = logging.getLogger(__name__)`.
- `agent.py` and `retriever.py` mark sections with `# -----` banners.
- Nodes mutate the `GraphState` dict and return it. Failures set `state["error"]` and do not raise out of the node.
- `main.py` uses a one-line module docstring and `# == Title == #` on the snippet window, the printed result, and the REPL. Same-line comments mark the non-obvious cuts. It logs the question at INFO and does not log the full agent state.
- `retriever.py` still says to call the BM25 method once per sub-query from the node above. That is what `fuse_subqueries` does. `generate_answer` still comments on a structured `context` shape the long branch does not use.

---

## Testing Conventions

No test suite, no `tests/` directory, and no CI config. The assignment's check is a manual run. Task 1 and Task 2 each have three-question screenshots under `docs/Task1/` and `docs/Task2/`. The Task 1 Chernobyl filename is `Qeustion1.png`. The Task 1 discussion draft is `docs/Task1/TaskOneAnalysisDraft.md`. The Task 2 usability write-up was given in chat on 2026-10-24 and was not saved as its own draft file. Task 3 screenshots are `docs/Task3/Sub200CharQuestion1.png` and `docs/Task3/Above200CharQuestion1.png`. The Task 3 relevance write-up has not been saved. A direct check on 2026-10-24 confirmed the trigger, the line parser, fusion rank, the short path, and the failed-split fallback, without launching the REPL.

---

## Dev Commands

Run these from the code root with the conda env active:

```bash
cd "/home/isaacsimms/Desktop/MCS-UIUC/Text Information Systems - CS410/Programming/MP2/_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2"
source ~/miniconda3/etc/profile.d/conda.sh
conda activate pyserini
java -version   # must be 21
```

```bash
# .env already exists. Copy the example again only to reset it.
cp .env.example .env
```

```bash
# indexes/apnews already exists, so launch skips the rebuild. Type exit to quit.
python main.py
```

```bash
# If the agent reports connection refused
systemctl status ollama
ollama serve
```

```bash
# Confirm the model the .env name must match
ollama list
```

Do not re-run `pip install -r requirements.txt` unless NumPy is restored afterward. The file pins `numpy~=1.26.4`, and that version makes `LuceneSearcher` fail to import on this Pyserini 2.4.0 install. The repair that worked is:

```bash
pip install 'numpy>=2.2,<2.8'
python -c "from pyserini.search.lucene import LuceneSearcher; print('lucene ok')"
```
