# MP2 baseline install through the README Installation section

**Date:** 2026-10-21
**Type:** setup
**Environment / Systems:** Fedora desktop; Miniconda env `pyserini` (Python 3.12.14, Pyserini 2.4.0, conda OpenJDK 21.0.10); system OpenJDK 25 left in place; Ollama 0.40.7 as a systemd service

## TL;DR

CS410 MP2 Task 1 setup stopped at the end of the README Installation section. The MP1 `pyserini` env has the MP2 Python packages, NumPy was put back on 2.5.4 so Pyserini imports, the MP1 `data/` tree was copied into the inner MP2 project, and `llama3.2:3b` (2.0 GB) is installed for the system Ollama service. Configuration (`.env`) and `python main.py` were not started.

## Context & Goal

Start Programming Assignment 2 (a LangGraph RAG agent over the MP1 corpora, using Pyserini BM25 and a local Ollama model). The user wanted a high-level read of `Instructions.md`, then to walk the README Installation section one step at a time and stop there.

## Key Points Explored

- The assignment is three tasks: reproduce the baseline (30%), improve how retrieved evidence is shown (40%), and decompose long queries then fuse retrieval results (30%). Submission is one zip with a PDF report and the Python files.
- Task 1 is run-and-analyze, not a feature. Graded pieces are a running index, at least three queries with screenshots or logs, and a diagnosis of good vs failed answers.
- The runnable project is the inner folder `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/`, next to `main.py`. The hash-prefixed parent is only a wrapper.
- `pip install -r requirements.txt` finished and then printed dependency conflicts. It downgraded NumPy to 1.26.4. Pyserini 2.4.0 and SciPy 1.18.1 need NumPy 2.x. `from pyserini.search.lucene import LuceneSearcher` failed until NumPy was restored.
- The user's first NumPy command omitted the comma (`numpy>=2.2<2.8`). The working specifier is `numpy>=2.2,<2.8`, which installed NumPy 2.5.4. A follow-up import printed `lucene ok`.
- `pip check` still reports non-blocking conflicts: `fastmcp` 2.12.5 (Pyserini wants `>=2.14`), `pillow` 10.4.0 (Pyserini wants `>=12`), and Pydantic 2.11.8 vs `mcp-types` / `fastmcp-slim`. BM25 search does not use those.
- Ollama was not installed. The official `curl | sh` installer placed `/usr/local/bin/ollama` 0.40.7, created the `ollama` user, and enabled `ollama.service`. The script then exited 2 on `dnf config-manager --add-repo` (Fedora does not accept that flag). `nvidia-smi` is absent. A GeForce RTX 3050 Ti Mobile is on the PCI bus, but generation will use the CPU.
- `ollama pull llama3.2:3b` completed. `ollama list` shows id `a80c4f17acd5`, size 2.0 GB.
- The model is not in the project and not in `~/.ollama` (that directory does not exist). The service runs as user `ollama`, and the model store is `/usr/share/ollama/.ollama/` (directory exists; listing it is denied without that user's permissions).
- The user does not need the course default model specifically. They chose `llama3.2:3b` because it matches `.env.example` and fits this laptop. A local model is required because `main.py` calls Ollama at `http://localhost:11434`; the chat assistant is not that process.
- An Ollama marketing setup prompt was shared as context only. The user rejected following it and said to stay on the assignment README. No Ollama sign-in and no API key.

## Decisions & Outcomes

- Copy `data/` from `MP1/CS410-MP1-code/data` into the inner MP2 folder. Do not move it. The copy is about 445 MB and includes `apnews`, `cranfield`, and `new_faculty`. MP1's original is intact. `data/apnews/apnews.dat` is about 437 MB.
- Keep working in conda env `pyserini`. A shell that is not activated still sees system Java 25, which breaks Pyserini.
- Keep NumPy on the 2.x line (`2.5.4`). Do not reinstall the `requirements.txt` pin `numpy~=1.26.4`.
- Use local `llama3.2:3b`. Do not switch the agent to a cloud model.
- Stop after the README Installation section. Do not create `.env` or run the demo in this thread.

Verified: `java -version` inside `(pyserini)` is 21.0.10; Lucene import succeeds; `systemctl` reports `ollama` active and enabled; `ollama list` shows `llama3.2:3b`.

## Open Questions / Next Steps

- README Configuration is next: create `.env` from `.env.example` in the inner MP2 folder, then run `python main.py` from `(pyserini)`.
- First launch builds `processed_corpus/apnews` (one JSON file per line of `apnews.dat`) and `indexes/apnews`. That run is long. The retriever then builds an LLM compression layer, so Ollama must be up before the first question.
- `main.py` passes `selected_namespaces` into `GraphState`, and `utils/state.py` does not declare that key. Whether LangGraph rejects it is unconfirmed; the demo has not been run.
- Task 1 still needs at least three questions about the indexed news text, screenshots or logs, and a short success-vs-failure discussion. Tasks 2 and 3 are untouched.
- GPU acceleration is unset. Fixing the Fedora NVIDIA repo step was left alone on purpose.

## Artifacts

- Assignment brief: `docs/Instructions.md`. It was read from the MP2 folder root during this session and moved under `docs/` afterward.
- Starter code and README: `_c54a3a1b26dc478f9111276a6fe991cf_MP2/MP2/`.
- Copied corpus: that folder's `data/` (`apnews`, `cranfield`, `new_faculty`).
- `.env` does not exist yet. `.env.example` does.
- Ollama unit: `/etc/systemd/system/ollama.service`. Binary: `/usr/local/bin/ollama`.
- Forward handoff: `docs/handoffs/2026-10-21-mp2-resume-after-install.md`.
- Architecture reference: `docs/Context.md`.
