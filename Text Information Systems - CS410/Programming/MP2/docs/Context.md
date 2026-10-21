# CS410 MP2 — Context & Architecture Reference

Local retrieval-augmented generation demo for CS410. A student runs a terminal loop that retrieves AP News documents with Pyserini BM25 and asks a local Ollama model to answer from those documents only. The graded work is to run that baseline, then make the evidence visible to the user, then handle long questions by splitting them into sub-queries and fusing the hits.

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
| Config | `python-dotenv` 1.1.1, `.env` not created yet |
| Numeric stack | NumPy 2.5.4, SciPy 1.18.1. Do not install the `requirements.txt` pin `numpy~=1.26.4` |

Hardware on the machine that did setup: 16 GB RAM, GeForce RTX 3050 Ti Mobile present, NVIDIA driver not installed (`nvidia-smi` missing). Ollama runs on CPU.

---

## Project Structure

```
MP2/
├── docs/
│   ├── Instructions.md                      # assignment brief and grading
│   ├── Context.md                           # this file
│   ├── handoffs/                            # session transfer notes
│   └── recaps/                              # backward-looking session records
└── _c54a3a1b26dc478f9111276a6fe991cf_MP2/
    └── MP2/                                 # code root: cwd for python and pip
        ├── main.py                          # REPL entry
        ├── agent.py                         # LangGraph pipeline
        ├── README.md                        # install, configure, run
        ├── requirements.txt                 # pip pins; NumPy pin is unsafe here
        ├── .env.example                     # template; .env does not exist yet
        ├── utils/                           # config, llm, retriever, state
        ├── data/                            # copied MP1 corpora (not indexed yet)
        ├── processed_corpus/                # created on first run, one JSON per line
        └── indexes/                         # created on first run, Lucene index
```

`processed_corpus/` and `indexes/` are absent until the first `python main.py`.

### Code root — RAG agent

- `main.py` — loads `Config`, builds one retriever, loops on stdin, invokes the graph, prints `final_answer`.
- `agent.py` — two-node graph: `retrieve` then `generate_answer`.
- `utils/config.py` — reads `.env`. Owns model name, corpus name, `RETRIEVER_K`, BM25 `k1` and `b`.
- `utils/retriever.py` — corpus preprocess, Lucene index build, `PyseriniBM25Retriever`, optional contextual compression.
- `utils/llm.py` — `OllamaLLM` HTTP client. `OllamaLLMForJson` is unused by the graph.
- `utils/state.py` — `GraphState` TypedDict passed between nodes.
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

`main.py` passes `selected_namespaces` into the initial state. `GraphState` does not declare that key. First invoke has not been run, so whether LangGraph rejects it is *(unconfirmed)*.

### Pipeline

```
stdin question
  → GraphState
  → retrieve: retriever.invoke(question)
       BM25 top-k, then LLMChainExtractor
       on 0 compressed docs, fall back to base_retriever
       page_content strings appended to state["context"]
  → generate_answer: OllamaLLM, prompt allows only that context, max 7 sentences
  → stdout "Answer: ..."
```

There is no web search. `web_search_tool` and `web_search_results` are unused state fields. `main.py` sets `web_search_tool=None`.

### Service lifetimes

- **Process-long:** one `Config`, one retriever (and therefore one Lucene searcher) created in `main()` and stored on every `GraphState`.
- **Per answer:** `generate_answer` constructs a new `OllamaLLM`. Compression's `ChatOllama` is created once inside `create_retriever()`.

### Index build

`create_index(cname)` runs at retriever construction, before the first question:

1. If `processed_corpus/{cname}/` is missing or empty, `preprocess_corpus` writes `doc{i}.json` with `id` and `contents` for each line of `data/{cname}/{cname}.dat`.
2. If `indexes/{cname}/` is missing or empty, `python -m pyserini.index.lucene` builds a `JsonCollection` index with positions, docvectors, and raw stored (`--threads 1`).
3. Non-empty directories are skipped. Delete the matching directory to force a rebuild.

---

## Key Models

| Model | Key Fields |
|-------|-----------|
| `GraphState` | `question`, `context: List[str]`, `current_step`, `final_answer`, `retriever`, `web_search_tool`, `error`, `web_search_results` |
| `Document` (LangChain) | `page_content`; metadata `docid`, `score`, `title`. Metadata is dropped when `retrieve` copies `page_content` into `context` |
| Pyserini JSON doc | `id` (line number as string), `contents` (the raw line) |
| `Config` | `OLLAMA_MODEL`, `RETRIEVER_BACKEND`, `RETRIEVER_K`, `PYSERINI_CNAME`, `PYSERINI_K1`, `PYSERINI_B` |

BM25 parameters from `.env.example`: `k=3` (`RETRIEVER_K`), `k1=0.9`, `b=0.4`. Code default for `RETRIEVER_K` is 7 when `.env` is absent.

---

## RAG Agent

Prompt rule in `build_prompt`: use only the retrieved context; if the answer is not in the context, say so; at most 7 sentences.

Task 2 is specified as presentation work in `main.py` (the comment at the print site): show passages, ids, or scores before `final_answer`. The retriever already stores `docid` and `score` on `Document.metadata`, but `retrieve` currently discards that metadata.

Task 3 is specified in comments in `agent.py`: if the question is longer than 200 characters or more than one sentence, use the LLM to make 2–4 sub-queries, retrieve top-k for each, fuse, then call `generate_answer` with the merged context. Not implemented.

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
- `main.py` logs at INFO and prints only the final answer or the error string.
- Course comments in `main.py`, `agent.py`, and `retriever.py` name the task that should edit that spot. Prefer editing those spots over adding a new framework.

---

## Testing Conventions

No test suite, no `tests/` directory, and no CI config. The assignment's check is a manual run: index builds, at least three questions return answers, and the write-up distinguishes retrieval failure from hallucination and missing context.

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
# Create local config once. Not done yet.
cp .env.example .env
```

```bash
# Build the index on first launch, then prompt for questions. Type exit to quit.
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
