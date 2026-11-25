# MP3 Part 2: Screen Descriptions Implemented and Run

**Date:** 2026-11-25
**Type:** implementation
**Environment / Systems:** `~/.cs410` venv, Jupyter, Ollama 0.40.17, Gemini (`gemini-3.6-flash`), notebook `MP3/_646c0ca30b1c40f58aec5693f1dfef5a_mp3_videorag_final.ipynb`

## TL;DR
`describe_screen()` and `clip_text()` for Part 2 are written, debugged, and run. Gemini described all 17 clips and the result is cached. `SCREEN_INDEX` was built. The Part 2 written answer is not started, and Part 2 outputs were not saved in the notebook at the last disk check.

## Context & Goal
Resume MP3 after Parts 0 and 1 (handoff `2026-11-22-mp3-env-setup-handoff.md`). The user was unsure what Part 2 required and asked for the code, a breakdown of why it works, and a model prompt, written to a markdown file. A `/grill-me` pass settled the shape first.

## Key Points Explored
- **Design grill.** Settled: file holds paste-ready code, a why-it-works breakdown, and the prompt modeled sentence by sentence. The prompt was drafted and annotated by the agent for the user to adapt. `high_res=True` on the first run. Spec-only handling of Gemini's JSON. Describe what is visible in every window, with `""` only when nothing is. `clip_text` uses `Said: ...\nShown: ...`, dropping an empty part. "Describe only changes" was proposed and dropped because each clip is indexed alone and the check needs at least `len(CLIPS) // 2` = 8 described clips.
- **Pasting errors, in order found:**
  1. The first paste into the notebook (and into the markdown file) had a truncated `return sho`, a mangled window sentence (`{{CLIP_SECOND}}}`), and two bullets merged into one. Fixed in the file and the cell.
  2. `clip_text` had its body pasted twice, leaving `return "\n".join(parts)    parts = []` on one line. Two statements on one line is a `SyntaxError`. Fixed by deleting the duplicate.
  3. `NameError: name 'os' is not defined`. The kernel had only run the function cell and the check cell, so the helper cell was never run. Fixed with Run All Above Selected Cell.
  4. `NameError: name 'DURATION' is not defined` (and `CLIPS`). Run All Above stops at the first failing cell. That cell was `In[8]`, where the Part 0 `MY_QUESTIONS` cell and the `transcribe_video` cell had merged into `]def transcribe_video():`. A newline after the `]` fixed it. This was the same cell that blocked `TRANSCRIPT`, `DURATION`, and `CLIPS`.
- **One misread by the agent.** A low-resolution screenshot looked like `[{{{"start"` (three braces) in the JSON example line. The user's zoomed screenshot showed two, which is correct for an f-string. The line was fine.
- **Result on disk:** `mp3_work/screen_descriptions.json` has 17 keys and all 17 are non-empty, so the `covered >= 8` check clears. `mp3_work/index_screen/` exists. The user reported the two cells after the check ran without issue; the printed output of the check and rerun cells was not seen by the agent.
- **Cost anomaly.** `mp3_work/cost.json` records `screen descriptions (Gemini)`: 73.1 s, 45,732 tokens, against `transcription`: 46.8 s, 45,603 tokens. The `high_res=True` call did not raise the token count about 3x as the `gemini_video` docstring and the earlier advice predicted. Cause not investigated.

## Decisions & Outcomes
- Part 2 code is implemented in the notebook as specified in `docs/artifacts/Part2-ScreenDescriptions.md`.
- `high_res=True` was kept for the single Gemini call. It is cached, so no `REDO_SCREEN` run is needed unless the prompt changes.
- Part 2 written answer left to the user. The agent did not write it.

## Open Questions / Next Steps
- Write the Part 2 "Your answer:" cell: which questions changed with screen text, one case it helped, one it hurt if any, and the prompt with its reasons. Read the printed rerun results first.
- Save the notebook (Cmd+S). At the last disk check (07:42) the Part 2 check, index, and rerun cells had no saved execution counts or outputs.
- Part 4 Q3 uses the 4.4 cost table. The screen-descriptions token row is about equal to transcription, not 3x. Explain what the table shows.
- `docs/artifacts/Part2-ScreenDescriptions.md` section 6 still says `high_res` raises the token figure about 3x. That is contradicted by `cost.json`. The file was not changed in this recap.
- Remaining: Part 3 (`classify_question`, `time_window`, `answer_time_question`, `summarize_clip`, `make_chapters`, `summarize_video`), `final_results`, Part 3 and Part 4 written answers, reflection, PDF export and zip. No Gemini key may appear in the notebook or its outputs.
- Still unverified from Part 1: whether the written answer covers "Did retrieval find the right moment even when the answer was wrong?"

## Artifacts
- `MP3/docs/artifacts/Part2-ScreenDescriptions.md`: paste-ready code, annotated prompt, breakdown. Untracked.
- `MP3/mp3_work/screen_descriptions.json`: cached Gemini output, 17 clips. Untracked.
- `MP3/mp3_work/cost.json`: now includes the screen-description and screen-index rows. Modified.
- `MP3/_646c0ca30b1c40f58aec5693f1dfef5a_mp3_videorag_final.ipynb`: Part 2 code in. Modified, uncommitted.
- `MP3/docs/handoffs/2026-11-22-mp3-env-setup-handoff.md`: updated with this thread's state.
