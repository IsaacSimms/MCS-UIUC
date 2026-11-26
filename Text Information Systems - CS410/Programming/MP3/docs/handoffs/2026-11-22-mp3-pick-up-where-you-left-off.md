# MP3: Pick Up Where You Left Off

Written for you, not for an agent. If you start a new agent thread, give it the other file in this folder, `2026-11-22-mp3-env-setup-handoff.md`. It holds the full technical detail.

## Where you are

**Parts 0 and 1 are done. Part 2 is next.**

- Part 0: you wrote 5 questions with your own answers and times.
- Part 1: the transcript is saved (83 pieces, ends at 8:14), the baseline ran on your questions, and you recorded verdicts and wrote your explanation.
- Baseline result: 1 correct, 2 partial, 2 wrong. The right clip was retrieved for Q1 and Q3, and the model still failed. Q4's answer was split across two clips. Q5 was a vocabulary mismatch ("difficulties" versus "challenging" and "deformable").
- Everything is set up and working: Java 21, the Python venv, Ollama with `llama3.2`, and your Gemini key.

## Start-up commands

Run these in a fresh terminal each time. Paste them one line at a time.

```sh
source ~/.cs410/venv/bin/activate
```

Activates the venv. It also sets up Java, Ollama and your Gemini key. You'll see `(venv)` in your prompt.

```sh
curl -s localhost:11434/api/version || (ollama serve > /dev/null 2>&1 &)
```

Checks whether Ollama is running. If it is, you'll see something like `{"version":"0.40.17"}`. If not, this starts it. Give it a few seconds.

```sh
cd "/Users/isaacsimms/Desktop/repos/MCS-UIUC/Text Information Systems - CS410/Programming/MP3"
jupyter notebook
```

Opens Jupyter in your browser. Click the `.ipynb` file. Keep this terminal open while you work, and press Ctrl+C in it to stop Jupyter.

## Getting the notebook back to where it was

Restarting wipes the notebook's memory, so rebuild it before you continue:

1. Open the notebook and click any cell in **Part 2** (say, the one with `describe_screen`).
2. Use the menu **Run → Run All Above Selected Cell**.

Don't use "Restart & Run All". The unfinished cells later in the notebook would error. Rerunning the cells above is safe and quick. It does not call Gemini again, because the transcript loads from `mp3_transcript.json`.

## What's next: Part 2

1. Write `describe_screen()` and `clip_text()` in the cell that has both. This is the next thing to write. The docstrings explain it. In short: ask Gemini what is shown in each 30-second window, then merge that with the transcript text for each clip.
2. Run the progress check cell below it. The first run calls Gemini once and caches the result.
3. Run the cell that builds `SCREEN_INDEX`, then the cell that reruns the questions you missed.
4. Write your Part 2 answer in the "Your answer:" cell. It asks where screen text helped or hurt, and why you chose your prompt.

Before you start, remember that none of your Part 1 failures was caused by on-screen content, and none of your questions depends on the screen. Part 2 might change little for them. That is fine and worth saying in your answer.

Each time you rerun the screen-description step, Gemini reads the whole video again. Only set `REDO_SCREEN = True` when you've actually changed the prompt, and set it back to `False` afterward.

## Small things to finish

- Check your Part 1 written answer. Make sure it answers all three questions, including "Did retrieval find the right moment even when the answer was wrong?" Press Shift+Enter on the cell so it renders.
- Nothing is committed to git yet. Commit when you're ready. The notebook, `mp3_transcript.json`, `mp3_work/cost.json` and the two files in `docs/artifacts/` are the ones worth keeping. The `.gitignore` already skips the generated indexes.
- Before you submit, search the notebook for your API key. It should not appear anywhere in the code or the outputs.

## Remaining plan

| Part       | What you do                                                                                       |
| ---------- | ------------------------------------------------------------------------------------------------- |
| 2          | Screen descriptions merged into clip text, new index, rerun missed questions, written answer      |
| 3          | Route time and summary questions, chapters and summary, written answer                            |
| 4          | Verdicts on the full system, course question cells, answer the four questions                     |
| Reflection | Half a page inside the notebook                                                                   |
| Submit     | PDF export of the finished notebook, then one `.zip` with the notebook and the PDF. No API key. |

Only export the PDF once the whole notebook has run.

## Where things live

| What                                              | Where                                                              |
| ------------------------------------------------- | ------------------------------------------------------------------ |
| Notebook                                          | `MP3/_646c0ca30b1c40f58aec5693f1dfef5a_mp3_videorag_final.ipynb` |
| Your transcript                                   | `MP3/mp3_transcript.json`                                        |
| Your questions and verdicts                       | `MP3/docs/artifacts/`                                            |
| Assignment text and grading                       | `MP3/docs/Instructions.md`                                       |
| The whole environment (Java, Python, Ollama, key) | `~/.cs410/`                                                      |
| How to delete all of it later                     | `Programming/Remove-Environment.md`                              |

## If something breaks

- **The notebook says Ollama isn't running:** run the `curl ... || (ollama serve ...)` line again.
- **An indexing or Java error:** Jupyter wasn't started from the activated terminal. Stop it with Ctrl+C and redo the three commands above in order.
- **`GEMINI_API_KEY set` fails:** you launched Jupyter without activating the venv first. Same fix.
- **A `NameError` for something like `CLIPS` or `TRANSCRIPT`:** the notebook's memory was lost. Use Run All Above Selected Cell.
- **The red torch "Redirects are currently not supported in MacOS" warning:** harmless. Ignore it.
