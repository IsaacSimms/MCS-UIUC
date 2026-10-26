---
title: HW3 research brief
status: ready
updated: 2026-10-26
project: Distributed Systems - CS425/Week8/Homework 3
---

# HW3 research brief

## TL;DR

Hand a new session this plan and one file under `docs/research/`. It reads that file only and answers in the thread with three short parts: what the question asks, the points worth remembering, and an example answer that already contains the note’s result. The research note stays the source. The brief is only there so the note does not have to be read in full. Do not build the homework from this plan.

## Problem Statement

`docs/research/` has nine notes for CS425 Fall 2026 Homework 3: questions 1–4 and 6–10. Each note is about 1,900–4,200 words and already has the question, a full answer, findings, a recommendation, ruled-out approaches, and open questions. That is more than is needed to write the solution. Question 5 has no note.

## Requirements

1. Given this plan and a path to one research markdown file, return a brief in the thread.
2. The brief has three parts, in this order: **Question shape**, **Keep**, **Example answer**.
3. **Question shape** states the parts the question asks for and what each part must contain. A few bullets. Use the file’s `question:` field and the Answer’s part headings.
4. **Keep** is the smallest set of bullets that hold the mechanism and the result. One fact per bullet.
5. **Example answer** is a compressed solution split into the question’s parts. It includes the note’s actual result: the decisions, numbers, timestamps, sequence, or algorithm steps.
6. The thread reply is shorter than the source file.

## Constraints

- Read only the named research file. Leave the PDF, lecture slides, images, sibling notes, and the web closed.
- Do not edit the research file, and do not write the Gradescope PDF.
- Do not resolve anything the note leaves open. If frontmatter `confidence` is other than `confident`, or an item under `## Open questions` would change a line of the example, add one sentence naming that limit and leave the line unresolved.
- If the path is missing, say so and stop. Question 5 has no note.
- The thread contains the whole brief. A spare copy under this homework’s `docs/artifacts/` is optional. If you write one, the thread still has the brief and names the path.
- Skip question 10 part iii. The note marks it out of scope.
- One brief per file. If several files are named, emit a separate brief for each. Do not merge them.
- This is a repeated procedure. Do not set this plan’s `status` to `done` after a question, and do not check off Progress.
- This file is permission to write the brief the user just asked for, and nothing else.

## Key Decisions

> **Decision:** The brief is question shape, memory bullets, and an example answer that carries the note’s result.
> **Rationale:** The notes already did the work. The session only has to surface the root so the question can be written from the bullets and the example.
> **Alternatives considered:** A scaffold that hides the result. A long submission-ready essay. A rule that every table must be copied in full.

> **Decision:** The named research file is the only source.
> **Rationale:** The Findings section already cites the slides and the PDF. Opening them again repeats the note.
> **Alternatives considered:** Re-read `hw3.fa26.pdf`. Re-read the cited lecture slides.

> **Decision:** Deliver the brief in the thread. A saved copy is optional.
> **Rationale:** The assignment is short-lived, and the thread is what gets read. A file is a spare, not a substitute.
> **Alternatives considered:** Thread only, with no file allowed. File only, with the thread pointing at it.

> **Decision:** This plan lives at `docs/plans/hw3-research-brief.md` inside Homework 3.
> **Rationale:** That is the folder for handing the contract to a new agent.
> **Alternatives considered:** The homework’s `docs/artifacts/`. The repo-root `docs/artifacts/`.

> **Decision:** Cut for speed. Keep the result, drop the essay around it.
> **Rationale:** The notes are already complete. The pass should be faster than reading them. A strict full reprint of every table was not required.
> **Alternatives considered:** Reprint the artifact and the Recommendation section. Summarize the artifact and leave it in the note.

## Deferred

Question 5. The typed Gradescope PDF. Any check of a note against the slides or the textbook.

## Implementation Phases

### Phase 1 — Write the brief

Objective: Turn the named research file into the thread brief.

Tasks:

1. Read the named file from frontmatter through Open questions. Read nothing else.
2. Write **Question shape** from `question:` and the Answer’s part headings. Leave out the story framing.
3. Write **Keep**. Include a trap only when Ruled out shows a plausible wrong answer. Skip Findings, the version list, and open items that only record an unread source.
4. Write **Example answer** in the question’s parts. Include the result. Use a table or a short step list when the result is one. Do not retell the Keep bullets in paragraphs.
5. Add the one-sentence limit from Constraints when confidence or an open question would change the example.
6. Post the brief in the thread. Optionally write the same text under `docs/artifacts/` and name that path.

Acceptance criteria:

- The thread contains Question shape, Keep, and Example answer.
- The example answer states the note’s result for every required part.
- The reply is shorter than the source file.
- No source other than the named file was used.

## Progress

- [ ] Per run: brief for the research file named in the user message. Leave this unchecked. Leave `status: ready`.

## Cold-start

Read `Distributed Systems - CS425/Week8/Homework 3/docs/plans/hw3-research-brief.md` and write the brief for the research file named in the user message. Honor Constraints and Key Decisions. Do not re-open them. Follow Phase 1. The plan alone is not permission to do anything except that brief.

## Reference Files

- `Distributed Systems - CS425/Week8/Homework 3/docs/research/` — one note per question. q5 is absent.
- `Distributed Systems - CS425/Week8/Homework 3/hw3.fa26.pdf` — the assignment. Leave it closed while writing a brief. The note’s `question:` field is the prompt.
