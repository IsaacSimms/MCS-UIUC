# Implementation Handoff: MP3 VideoRAG, Environment Set Up

> **Handoff Mode: Implementation**
> **Receiving agent job: Resume and continue. The environment is built; the notebook work has not started.**

## 1. Thread Purpose

Set up MP3 (CS410 VideoRAG: transcribe a YouTube video with Gemini, index 30 s clips with Pyserini BM25, answer with Ollama `llama3.2`, route questions with LangGraph) on a new machine. The thread converted the assignment to markdown and built a self-contained, easily deletable toolchain. No notebook cell has been run or edited yet.

## 2. Stack & Environment

- macOS, arm64 (Apple Silicon), 32 GB RAM, ~830 GB free. Shell: zsh.
- Homebrew 7.0.15 is installed (by the user). Only `python@3.12` (3.12.16) was installed through it. It is linked as `python3.12` and friends only. Bare `python3` is still `/usr/bin/python3` (3.9.6).
- **Everything else lives in `~/.cs410/` (~4.7 GB):**
  - `~/.cs410/jdk/jdk-21.0.13.1+2/Contents/Home`: Temurin JDK 21.
  - `~/.cs410/venv`: Python 3.12 venv. Installed with `--no-cache-dir`: `pyserini` 2.4.0, `pyjnius`, `langgraph` 1.2.24, `google-genai` 3.6.1, `pandas`, `requests`, `jupyter`, `torch`, `onnxruntime`, `transformers`. `faiss-cpu` is not installed (not needed for BM25).
  - `~/.cs410/ollama/`: standalone Ollama v0.40.17 binary (from the GitHub release tarball, not brew), `server.log`, and `models/` holding `llama3.2:latest` (2.0 GB).
  - `~/.cs410/gemini_key`: created by the user, perms 600, 53 bytes, no trailing whitespace. Verified: a fresh activated shell sets `GEMINI_API_KEY`, and a request to the Gemini model list returned HTTP 200.
- **Activation:** `source ~/.cs410/venv/bin/activate`. Three blocks were appended to `~/.cs410/venv/bin/activate`: `JAVA_HOME` and `PATH` for the JDK; `OLLAMA_MODELS` and `PATH` for Ollama; `GEMINI_API_KEY` loaded from `~/.cs410/gemini_key` if the file exists. Nothing was added to `~/.zshrc`.
- Outside `~/.cs410`: `~/.ollama` (12 KB, Ollama key pair and cache; not redirectable). A pre-existing `~/.local/bin/claude` symlink belongs to Claude Code. Leave it.

## 3A. What Was Accomplished

1. Converted the pasted assignment and grading criteria into `MP3/docs/Instructions.md`. The file now sits in `docs/`; it was moved there after creation.
2. Inspected the notebook for dependencies. Confirmed it needs Pyserini + Java 21, LangGraph, Ollama `llama3.2`, and a Gemini key.
3. Installed JDK 21, Python 3.12 venv, all packages, standalone Ollama, and pulled `llama3.2`.
4. Verified: `java -version` reports 21.0.13.1 inside the venv. Python starts the JVM through `pyjnius` (`autoclass('java.lang.System')` reports 21.0.13.1) and `from pyserini.search.lucene import LuceneSearcher` imports. Ollama `/api/generate` with `llama3.2` returned text.
5. Wrote `Programming/Remove-Environment.md`. It documents the full teardown: `pkill -f "ollama serve"`, `rm -rf ~/.cs410 ~/.ollama`, `brew uninstall python@3.12` + `brew autoremove`, and optional caches. The Homebrew-removal section was deleted at the user's request.

## 4A. Current State

- **Notebook:** `MP3/_646c0ca30b1c40f58aec5693f1dfef5a_mp3_videorag_final.ipynb`. 62 cells, no outputs, never run. The odd filename prefix is from the course download. It was not renamed.
- **Gemini key:** on disk and verified (see §2). The user has done nothing beyond that: no Jupyter session started, no notebook cell run, no questions written.
- **Not yet verified:** cell 4 (`setup_check()`) has never been run. A real Pyserini index build has not been tested. `ClipIndex` (cell 15) shells out to `sys.executable -m pyserini.index.lucene`, so the Jupyter kernel must be the venv Python with `JAVA_HOME` set.
- **Ollama server:** was started as a background process (`nohup ollama serve`, PID 38338) from this session. It probably is not running in a new session. Start it with `ollama serve` in a shell where the venv is active.
- **Notebook TODOs (`YOUR CODE HERE`):**
  - Cell 8: Part 0, the user's 5 questions with answers and times (`MY_QUESTIONS`).
  - Cell 10: `transcribe_video`.
  - Cell 22: `CAUSES` / judging verdicts.
  - Cell 28: `describe_screen`, `clip_text`.
  - Cell 32: rerun of the missed questions with screen text.
  - Cell 36: `classify_question`, `time_window`, `answer_time_question`.
  - Cell 39: `summarize_clip`, `make_chapters`, `summarize_video`.
  - Cell 46: final results.
  - Written answer cells throughout, and the reflection (cell 59 area, "What to Submit").
- Notebook settings (cell 2): `VIDEO_URL = https://www.youtube.com/watch?v=OPTKlycwIkM`, `CLIP_SECONDS = 30`, `TOP_K = 3`, `TIME_TOLERANCE = 10`, `TEXT_MODEL = "llama3.2"`, `GEMINI_MODEL = "gemini-3.6-flash"`, `OLLAMA_URL = http://localhost:11434`.

## 5. Key Decisions & Rationale

| Decision | Rationale |
|----------|-----------|
| Python 3.12, not 3.15.2 | Pyserini 2.4.0 needs >=3.12, but the current `pyjnius`, `faiss-cpu`, and `onnxruntime` have no cp315 wheels (3.15 would compile from source). The user's MP1 cache shows 3.12. |
| Everything in `~/.cs410/` | The user wants a self-contained, easily deletable environment and no bloat near the root. |
| `JAVA_HOME`, Ollama vars, key set in the venv `activate` script, not `~/.zshrc` | Nothing leaks outside the venv; deactivate or delete undoes it. |
| Ollama from the release tarball, not `brew install ollama` or the desktop app | Keeps the binary and models under `~/.cs410`. No launchd or brew service. |
| `OLLAMA_MODELS=~/.cs410/ollama/models` | Moves the 2 GB model out of `~/.ollama`. |
| `--no-cache-dir` for pip | Avoids `~/Library/Caches/pip` growth. |
| Gemini key in `~/.cs410/gemini_key` (perms 600), written by the user | The key stays out of chat, the notebook, and the repo. The submission must not contain it. |
| Homebrew was not touched beyond `python@3.12` | The user never intends to remove Homebrew. Do not add Homebrew-removal steps anywhere. |

## 6. Blockers & Open Questions

- The first `uv` install attempt (`curl ... | sh`) was denied by the permission classifier. It was not retried. `uv` is not installed and not needed.
- Open until verified: whether Pyserini builds an index under the venv kernel, and whether cell 4 passes end to end inside Jupyter.

## 7. Next Steps (Ordered)

1. In a shell: `source ~/.cs410/venv/bin/activate`, then `ollama serve &` if `curl -s localhost:11434/api/version` fails, then `jupyter notebook` from `MP3/`.
2. Run notebook cells 2-4 (settings, helpers, `setup_check()`). Fix any `FIX` lines. Expected: all `pass`.
3. Part 0: the user watches the video and writes 5 questions with their own answers and times in cell 8.
4. Part 1: implement `transcribe_video` (Gemini, timestamped transcript saved to `mp3_transcript.json`), then run clips, index, answer, and judge cells (12-22).
5. Part 2, Part 3, Part 4, then the reflection and the written answer cells.
6. Submission: one `.zip` with the notebook and its PDF export. No API key anywhere in the notebook or its outputs.

## 8. Must-Knows for the New Thread

- **Grading is on effort and understanding.** Part 0 questions and the reflection are the student's own work *(inferred)*. Offer help, but do not write them unprompted.
- **User's global rules** (`~/.claude/CLAUDE.md`): concise; no affirmations ("you're right", etc.); push back when something is wrong; do not volunteer work beyond the request. A direct request to change something is the approval. Discussion or ideation is not. Prefer inline edits over rewriting files. Title comments for sizable code blocks: `# == Title == #` in Python.
- Never ask for, print, or echo the Gemini key. It is already on disk; do not recreate it. To check it, test file size and permissions or the env var's length, never the value.
- Start Jupyter or VS Code from the activated shell, or the kernel will not see `JAVA_HOME`, Ollama on `PATH`, or the key.
- The permission classifier blocks `curl | sh`. Do not work around it.
- Keep `Remove-Environment.md` in sync with anything new added under `~/.cs410` or outside it.

## 9. Relevant Artifacts

| Path (under `/Users/isaacsimms/Desktop/repos/MCS-UIUC/Text Information Systems - CS410/Programming/`) | Role | State |
|---|---|---|
| `MP3/_646c0ca30b1c40f58aec5693f1dfef5a_mp3_videorag_final.ipynb` | The assignment notebook | Untouched, no outputs |
| `MP3/docs/Instructions.md` | Assignment text plus grading criteria | Complete |
| `Remove-Environment.md` | Teardown steps for the whole environment | Current; lists the key file, Ollama, and `~/.ollama` |
| `MP3/docs/handoffs/2026-11-22-mp3-env-setup-handoff.md` | This file | Current |
| `~/.cs410/venv/bin/activate` | Venv activate script with the Java, Ollama, and key blocks | Edited; do not overwrite |
