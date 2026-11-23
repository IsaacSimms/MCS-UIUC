# Implementation Handoff: MP3 VideoRAG, Parts 0 and 1 Complete

> **Handoff Mode: Implementation**
> **Receiving agent job: Resume and continue. The environment is built and Parts 0 and 1 are done. Part 2 has not been started.**

## 1. Thread Purpose

Set up MP3 (CS410 VideoRAG: transcribe a YouTube video with Gemini, index 30 s clips with Pyserini BM25, answer with Ollama `llama3.2`, route questions with LangGraph) on a new machine, then work through the notebook. The thread converted the assignment to markdown, built a self-contained, easily deletable toolchain, and carried the user through Part 0 and Part 1 of the notebook. Part 2 (screen descriptions) is next.

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

1. Converted the pasted assignment and grading criteria into `MP3/docs/Instructions.md`.
2. Installed JDK 21, a Python 3.12 venv, all packages, standalone Ollama, and `llama3.2`. Verified Java 21 under `pyjnius`, a Pyserini import, an Ollama generation, and the Gemini key (HTTP 200).
3. Wrote `Programming/Remove-Environment.md` (full teardown steps).
4. User ran the notebook setup cells. `setup_check()` printed `pass` on all seven lines and `All set.` Cells run in the venv kernel (Python 3 ipykernel), launched from the activated shell.
5. **Part 0 done.** The user wrote 5 questions with their own answers and times. `MY_FILLED` check printed `5 questions written: pass`. Copy in `MP3/docs/artifacts/InitialVideoQuestions.md`.

   | # | Question | User's answer | Time |
   |---|---|---|---|
   | 1 | How many examples are used during the machine learning? | billions | 1:52 |
   | 2 | What is a context vector? | A list of numbers which represent what the sentence means | 3:05 |
   | 3 | Is it possible to test every potential translation circumstance? | not possible | 4:18 |
   | 4 | How does OCR use transformers? | First, identifies lines of text and text direction. Then divides image into tokens. | 5:24 |
   | 5 | What are the difficulties with OCR? | deformed text | 7:25 |

6. **Part 1.1 done.** `transcribe_video()` written by the user (from a block supplied in chat): one `gemini_video(prompt, "transcription", json_output=True)` call, `parse_json`, returns the list. Result cached in `MP3/mp3_transcript.json`: 83 pieces, 1448 words, speech ends at 8:14. Spot-checked against the question times; they line up (for example "billions of examples" at 1:51, context vector at 3:04, "impossible to test everything" at 4:17, OCR with Transformers at 5:18-5:23, deformable objects at 7:22).
7. **Parts 1.2 to 1.5 run** (all provided code): 17 clips of 30 s, `BASE_INDEX` built under Pyserini (the torch `redirects.py` MacOS warning is harmless), answer functions defined, `baseline_results` produced for the 5 questions.
8. **Part 1.6 done.** Verdicts in `BASELINE_JUDGMENTS` (copy in `MP3/docs/artifacts/BaselineJudgements.md`). The scoring cell printed 1 correct, 2 partial, 2 wrong, causes 2 `other`, 2 `retrieval`:

   | # | Verdict | Cause | Basis |
   |---|---|---|---|
   | 1 | wrong | other | Right clip (1:30) retrieved; model returned only `[1:30]`. |
   | 2 | correct | none | Definition at 3:04, wording matches. |
   | 3 | wrong | other | Right clip (4:00, rank 1) retrieved; model said "I can't find this in the video." |
   | 4 | partial | retrieval | Answer split across clips: first half in 5:00 clip (retrieved), "patches of pixels... tokens" at 5:30 (not retrieved). Model only restated the question. |
   | 5 | partial | retrieval | `moment_found` = False. Video lists several difficulties (reading order 6:18, mistranslation 7:07, deformable 7:22, slang 7:40); system gave a valid, cited one (reading order) that differs from the user's reference. |

   `retrieval found` was True for 4 of 5, so that check overstates success. The cause labels have no "generation failure" option, so Q1 and Q3 use `other`. The causes for Q1, Q3, and Q4's restatement are hypotheses; none was tested (for example re-asking Q1 with only the 1:30 clip).
9. User wrote the Part 1 explanation in the "Your answer:" cell and saved a checkpoint (Cmd+S). Corrected text was supplied in chat. It still lacked an explicit answer to the third prompt question ("Did retrieval find the right moment even when the answer was wrong?"). Whether the user added it is unverified.
10. Repo `.gitignore` (at `/Users/isaacsimms/Desktop/repos/MCS-UIUC/.gitignore`) got two rules: `Text Information Systems - CS410/Programming/MP3/mp3_work/index_*/` and `.ipynb_checkpoints/`.

## 4A. Current State

- **Notebook:** `MP3/_646c0ca30b1c40f58aec5693f1dfef5a_mp3_videorag_final.ipynb` (62 cells). Parts 0 and 1 executed with outputs and saved. Parts 2 to 4 and the reflection are untouched. The odd filename prefix is from the course download. It was not renamed.
- **Part 2 is next and not started.** Cells (indexes from the original notebook): 28 `describe_screen` and `clip_text` (both `YOUR CODE HERE`); 29 progress check, which calls `load_screen_descriptions()` and caches to `mp3_work/screen_descriptions.json`; 31 builds `SCREEN_INDEX = ClipIndex("screen", CLIPS, clip_text)`; 32 reruns the baseline's non-correct questions on `SCREEN_INDEX`; 33 and 34 are the Part 2 written prompt and "Your answer:" cell.
- **Remaining TODOs after Part 2:** cell 36 `classify_question`, `time_window`, `answer_time_question`; cell 39 `summarize_clip`, `make_chapters`, `summarize_video`; cell 46 `final_results`; the Part 3 and Part 4 written answers; the reflection; PDF export and zip.
- **Heads-up for Part 2:** none of the five Part 1 failures was about on-screen content, and none of the user's questions depends on the screen. Part 2 may change little for them. Q5 (a different retrieved passage) and Q4 (split clips) are the likeliest to move. The user knows this.
- **Gemini calls so far:** one (transcription), cached in `mp3_transcript.json`. Part 2 will make one more call, cached in `mp3_work/screen_descriptions.json`. Each `REDO_*` flag re-reads the whole video and spends free-tier quota (8 h of video per day).
- **Ollama server:** was running during the session (answered `{"version":"0.40.17"}` when Jupyter was launched). Its state in a new session is unknown. Start it with `ollama serve` in the activated shell if `curl -s localhost:11434/api/version` fails.
- **Git:** uncommitted. Untracked or modified: the notebook (M), `MP3/docs/artifacts/BaselineJudgements.md`, `MP3/docs/artifacts/InitialVideoQuestions.md`, `MP3/mp3_transcript.json`, `MP3/mp3_work/cost.json`. Generated Lucene indexes and `.ipynb_checkpoints/` are now ignored. Nothing has been committed. Recommend committing the transcript and `cost.json` and the docs, as agreed in chat. The user has not asked for a commit.
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
- No blockers. Open items: whether the Part 1 written answer now covers the third prompt question; whether the notebook output contains any key text (check before the final export).

## 7. Next Steps (Ordered)

1. In a shell: `source ~/.cs410/venv/bin/activate`, then `ollama serve &` if `curl -s localhost:11434/api/version` fails, then `jupyter notebook` from `MP3/`.
2. In the notebook, restore kernel state by running the cells above the work position (Run menu, "Run All Above Selected Cell", with a Part 2 cell selected). Do not use Restart & Run All, because the unfinished later cells raise `NotImplementedError`. The cached transcript loads from disk, so Gemini is not called again.
3. Part 2 (cell 28): write `describe_screen()` and `clip_text()`, run the cell 29 check, build `SCREEN_INDEX` (cell 31), rerun the missed questions (cell 32), and write the Part 2 answer. The cell docstring specifies a per-window JSON prompt and the key mapping into `CLIPS`.
4. Part 3 (cells 36 to 41), then Part 4, then the reflection.
5. Submission: one `.zip` with the notebook and its PDF export. No API key anywhere in the notebook or its outputs.

## 8. Must-Knows for the New Thread

- **Grading is on effort and understanding.** Part 0 questions, verdicts, written explanations, and the reflection are the student's own work. In Parts 0 and 1 the user wrote them; the agent supplied code blocks for `transcribe_video`, corrected text for the Part 1 answer on request, and an analysis of results. Offer help, but do not write the explanations unprompted.
- Do not edit the notebook file on disk while it is open in the user's browser. Give code blocks to paste instead; an on-disk edit would clash with the next save.
- **User's global rules** (`~/.claude/CLAUDE.md`): concise; no affirmations ("you're right", etc.); push back when something is wrong; do not volunteer work beyond the request. A direct request to change something is the approval. Discussion or ideation is not. Prefer inline edits over rewriting files. Title comments for sizable code blocks: `# == Title == #` in Python.
- Never ask for, print, or echo the Gemini key. It is already on disk; do not recreate it. To check it, test file size and permissions or the env var's length, never the value.
- Start Jupyter or VS Code from the activated shell, or the kernel will not see `JAVA_HOME`, Ollama on `PATH`, or the key.
- The permission classifier blocks `curl | sh`. Do not work around it.
- Keep `Remove-Environment.md` in sync with anything new added under `~/.cs410` or outside it.

## 9. Relevant Artifacts

| Path (under `/Users/isaacsimms/Desktop/repos/MCS-UIUC/Text Information Systems - CS410/Programming/`) | Role | State |
|---|---|---|
| `MP3/_646c0ca30b1c40f58aec5693f1dfef5a_mp3_videorag_final.ipynb` | The assignment notebook | Parts 0 and 1 done and saved; Part 2 onward untouched |
| `MP3/mp3_transcript.json` | Gemini transcript with times (83 pieces) | Final; cached, do not regenerate |
| `MP3/mp3_work/` | `cost.json`, `index_transcript/` (generated, git-ignored) | Regenerated by running cells |
| `MP3/docs/Instructions.md` | Assignment text plus grading criteria | Complete |
| `MP3/docs/artifacts/InitialVideoQuestions.md` | User's 5 questions, answers, times | Final (Part 0 is locked) |
| `MP3/docs/artifacts/BaselineJudgements.md` | `BASELINE_JUDGMENTS` block | Final |
| `MP3/docs/handoffs/2026-11-22-mp3-pick-up-where-you-left-off.md` | Companion handoff written for the user, not an agent | Current |
| `Remove-Environment.md` | Teardown steps for the whole environment | Current |
| `/Users/isaacsimms/Desktop/repos/MCS-UIUC/.gitignore` | Repo ignore rules, MP3 rules appended | Current |
| `~/.cs410/venv/bin/activate` | Venv activate script with the Java, Ollama, and key blocks | Edited; do not overwrite |
