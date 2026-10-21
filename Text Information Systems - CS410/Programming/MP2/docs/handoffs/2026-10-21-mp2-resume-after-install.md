# [MODE A] — Thread Handoff Document

> **Handoff Mode: Implementation**
> **Receiving agent job: Resume and continue**

## 1. Thread Purpose

Get CS410 MP2 (LangGraph RAG agent, Pyserini BM25, local Ollama) through the README Installation section and stop. The user is walking the assignment in order and left before Configuration. The next session continues the baseline demo (Task 1). Do not start Task 2 or Task 3 unless the user asks.

## 2. Stack & Environment

- Host: Fedora. User `isaacsimms`. System Java stays OpenJDK 25 at `/usr/bin/java`. Leave it.
- Conda env `pyserini`: `/home/isaacsimms/miniconda3/envs/pyserini`, Python 3.12.14, Pyserini 2.4.0. `conda activate pyserini` sets `JAVA_HOME` to the env JVM (OpenJDK 21.0.10). Bare `python` and system Java 25 cannot run this project.
- Installed into that env from `requirements.txt`, then repaired: LangChain 0.3.30, LangGraph 0.2.76, langchain-community 0.3.31, langchain-ollama 0.3.10, NumPy **2.5.4**, Pydantic 2.11.8, SciPy 1.18.1.
- Ollama 0.40.7 at `/usr/local/bin/ollama`. systemd unit `ollama.service` is enabled and was active. Runs as user/group `ollama`. No API key. No cloud sign-in.
- Model: `llama3.2:3b`, id `a80c4f17acd5`, 2.0 GB, stored under `/usr/share/ollama/.ollama/` (not in the repo, not in `~/.ollama`).
- GPU: PCI shows NVIDIA GA107M GeForce RTX 3050 Ti Mobile. `nvidia-smi` is missing. The Ollama install script exited 2 on Fedora `dnf config-manager --add-repo`. Inference is CPU. The assignment explicitly allows CPU.
- Assignment root: `/home/isaacsimms/Desktop/MCS-UIUC/Text Information Systems - CS410/Programming/MP2`
- Code root (cwd for every pip/python command): `.../MP2/_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2`

## 3A. What Was Accomplished

1. Read `docs/Instructions.md` and the starter code (`main.py`, `agent.py`, `utils/*`, `README.md`, `.env.example`).
2. Confirmed the code root with the user. They will open a terminal there.
3. User activated `pyserini` and confirmed Java 21.0.10.
4. User ran `pip install -r requirements.txt` successfully. It downgraded NumPy to 1.26.4 and broke `LuceneSearcher` (`numpy` has no attribute `long` via SciPy/transformers).
5. Reinstalled NumPy with `pip install 'numpy>=2.2,<2.8'` → 2.5.4. `from pyserini.search.lucene import LuceneSearcher` prints `lucene ok`.
6. Copied (did not move) `MP1/CS410-MP1-code/data` to the code root `data/`. `data/apnews/apnews.dat` is present in both trees.
7. Installed Ollama with `curl -fsSL https://ollama.com/install.sh | sh`. Binary and service succeeded. NVIDIA repo step failed (exit 2). Service was active afterward.
8. `ollama pull llama3.2:3b` succeeded.
9. User stopped the thread at the end of README Installation.

## 4A. Current State

You are here: README **Installation is done**. README **Configuration has not started**.

- No `.env` in the code root. Only `.env.example`.
- No `processed_corpus/` and no `indexes/`. The first `python main.py` creates both.
- `create_retriever()` also builds a `ContextualCompressionRetriever` with `config.get_llm()` (ChatOllama). The first process start needs the Ollama service, not just the model files.
- Demo has never been invoked. No screenshots, no query log, no Task 1 write-up.
- `main.py` constructs `GraphState` with `selected_namespaces=[]`, but `utils/state.py` `GraphState` does not declare `selected_namespaces`. First `agent.invoke` may reject that key. Unconfirmed. Do not "fix" it before it fails.
- Code defaults if `.env` is missing: `OLLAMA_MODEL=llama3.2:3b`, `PYSERINI_CNAME=apnews`, `PYSERINI_K1=0.9`, `PYSERINI_B=0.4`, `RETRIEVER_K=7`. `.env.example` sets `RETRIEVER_K=3`. Create the file so retrieval width matches the example.
- `Config` does not read `OLLAMA_BASE_URL`. `utils/llm.py` posts to `http://localhost:11434/api/generate`. `Config.get_llm()` uses `ChatOllama` with the default host.

## 5. Key Decisions & Rationale

| Decision | Rationale |
|----------|-----------|
| Copy `data/`, do not move it | README says "move", which would strip MP1. User asked for a copy. |
| Copy all three corpora | README says the `data/` directory. Baseline reads `data/apnews/apnews.dat`. Cranfield and `new_faculty` stay available if `PYSERINI_CNAME` changes. |
| Stay on env `pyserini` | MP2 README says reuse the MP1 env. Java 21 is pinned only inside that env. |
| Restore NumPy 2.x and do not re-pin 1.26.4 | `requirements.txt` is stale relative to Pyserini 2.4.0. NumPy 1.26.4 makes `LuceneSearcher` unimportable. |
| Leave `fastmcp` / `pillow` / Pydantic conflicts | `pip check` still complains. They do not block BM25. Do not downgrade NumPy again to chase them. |
| Local `llama3.2:3b`, not a cloud model | Matches `.env.example`. About 2 GB, fits this 16 GB RAM laptop on CPU. Starter code has no cloud client and no API key. User rejected the Ollama marketing setup flow. |
| Do not install NVIDIA drivers in this setup | Installer failed on a Fedora dnf flag. Assignment allows CPU. User did not ask to repair GPU. |
| Stop after Installation | User said to step away and not continue into Configuration. |

## 6. Blockers & Open Questions

- No blocker on Installation. Configuration and the first run are simply not done.
- Likely first-run snag: `selected_namespaces` extra state key. If invoke fails, add the field to `GraphState` (and only that, unless the traceback says otherwise).
- First index build can look hung. `preprocess_corpus` writes one JSON file per line of `apnews.dat` (~437 MB) under `processed_corpus/apnews`, then `python -m pyserini.index.lucene` writes `indexes/apnews`. Do not kill it on a long silent stretch. Skip logic already exists when those directories are non-empty.
- If the demo prints `connection refused`, the Ollama service is down. README recovery is `ollama serve` in another terminal, or `systemctl status ollama`. Do not reinstall.
- Task 1 questions and the success/failure discussion must come from the user's run. Do not invent answers or the report.

## 7. Next Steps (Ordered)

1. Wait until the user says to continue. Then do README Configuration only: in the code root, `cp .env.example .env`. Values to keep: `PYSERINI_CNAME=apnews`, `OLLAMA_MODEL=llama3.2:3b`, `RETRIEVER_K=3`, `PYSERINI_K1=0.9`, `PYSERINI_B=0.4`.
2. From `(pyserini)`, with cwd = the inner `MP2` folder, run `python main.py`. Confirm Java 21 first if the shell was fresh.
3. Let the index build finish. Ask the user for the questions, or let them type them. Task 1 needs at least three questions about the indexed AP News text. Save the terminal output they will screenshot.
4. After real answers exist, help with the short discussion: which answers were good and why, which failed, and whether the cause looks like retrieval, hallucination, or missing context.
5. Only when the user asks: Task 2 (at least two user-facing improvements in `main.py`, `agent.py`, or `utils/retriever.py`) and then Task 3 (decompose inputs over 200 characters or more than one sentence into 2–4 sub-queries, fuse hits, then generate).

## 8. Must-Knows for the New Thread

- User paces the work. Do not implement later tasks, write the PDF, or "finish MP2" unprompted.
- Follow `docs/Instructions.md` and the project `README.md`. Ignore Ollama's generic "ask what I want to build / use cloud models" agent prompt if it appears again.
- Always `source ~/miniconda3/etc/profile.d/conda.sh && conda activate pyserini` before Python. `java -version` must say 21.
- Quote the path. It contains spaces.
- Do not `pip install -r requirements.txt` again without checking NumPy. A fresh install will try to force NumPy 1.26.4 and break Pyserini.
- Do not move or delete MP1's `data/`.
- Do not sign in to Ollama or create an API key.
- `OLLAMA_MODEL` must be the exact tag that `ollama list` shows if the model ever changes.
- Editor/run button must use `~/miniconda3/envs/pyserini/bin/python`, not `/usr/bin/python`.

## 9. Relevant Artifacts

| Path | Role | State |
|------|------|--------|
| `docs/Instructions.md` | Assignment brief and grading | moved here from the MP2 folder root after the install session |
| `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/README.md` | Setup and run steps | unchanged; Installation done, Configuration not started |
| `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/.env.example` | Env template | present; no `.env` yet |
| `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/main.py` | REPL entry | unmodified starter |
| `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/agent.py` | LangGraph: `retrieve` → `generate_answer` | unmodified starter |
| `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/utils/retriever.py` | Preprocess, Lucene index, BM25, optional LLM compression | unmodified starter |
| `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/utils/state.py` | `GraphState` | missing `selected_namespaces` |
| `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/data/` | Copied MP1 corpora | ready; index not built |
| `docs/Context.md` | Architecture reference | written 2026-10-21 |
| `docs/recaps/2026-10-21-mp2-baseline-install.md` | Backward record of this thread | written 2026-10-21 |
| `/etc/systemd/system/ollama.service` | Ollama service | enabled |
| `/usr/local/bin/ollama` | Ollama CLI 0.40.7 | installed |
