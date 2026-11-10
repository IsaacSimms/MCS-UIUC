# [IMPLEMENTATION] — Thread Handoff Document

> **Handoff Mode: Implementation**
> **Receiving agent job: Resume and continue.** Create the Canva deck. The user already chose `implement directly`. Do not re-grill settled decisions. Do not wait for a second implement instruction.

## 1. Thread Purpose

Build an 8-slide Canva presentation for Isaac's CS410 Technology Review, "Self-hosted vector databases for text retrieval" (pgvector, Qdrant, Weaviate, Milvus). The talk is a screen recording of about 8–12 minutes. The slide contract is the presentation runbook, tightened by a grill. Canva was never reached: this CLI session cannot open the Canva login.

## 2. Stack & Environment

- Workspace: `/home/isaacsimms/Desktop/MCS-UIUC`
- Project: `/home/isaacsimms/Desktop/MCS-UIUC/Text Information Systems - CS410/Programming/TechReview`
- Canva MCP namespace: `plugin-canva-canva`. Status when last checked: `needsAuth`. Tool exposed before auth: `mcp_auth` only.
- `CallDynamicTool` `mcp_auth` failed here: `Interactive MCP authentication is only available in the Cursor desktop IDE.`
- `canva` CLI is not installed (`canva: command not found`). Do not install it unless Isaac asks. He asked for the Canva MCP.
- No code, tests, or git commit. TDD does not apply.
- OS: Linux. Date of this handoff: 2026-11-09.

## Original Design

Audience: other CS410 students, recorded full-screen from Canva. Voice script stays in the runbook. Isaac will pace the talk live and is not locked to the runbook minute marks. Nothing on a slide encodes time.

### Deck rules

- Exactly 8 slides. 16:9. Type large enough to read in a Zoom or screen recording.
- On-slide lines are the runbook lines below. Copy them. Do not paraphrase, shorten, or add claims, systems, or numbers.
- Each content slide has a real title. Use the runbook headings below. Slide 1 is the talk title plus two lines. No separate "Title" label, no name, no "CS410" mark.
- Spoken "Say" blocks stay in the runbook. Do not put them on slides. Do not paste them into Canva speaker notes.
- Static. No entrance animation, no object animation, no animated diagram.
- Chrome: a small slide number in secondary text (1–8). No running header, no footer sentence, no timestamps.
- Order of systems, every time they appear: pgvector, Qdrant, Weaviate, Milvus. One type treatment for all four names.
- Palette: matte black in the Cursor dark-mode family, light text, one accent. Use the accent on diagram arrows and the stay/leave marks. Do not assign a hue per database. Exact hex was never sampled from Isaac's theme *(inferred: match a matte editor ground and one cool accent, not a glossy stock dark template).*
- Diagrams on slides 4, 5, and 6 only. Grammar: a few words, blocks, and one arrow. They restate mechanisms already in the bullets. They do not replace the bullets.
- Leave out of the deck: 2024–2026 changelog, tenancy, access control, quantization, vendor recall, QPS, any speed ranking, version dump (versions are verbal, if asked). The sources slide may show pgvector `v0.8.7` because that version is part of the runbook line.

### Slide 1 — title

No extra eyebrow.

- Self-hosted vector databases for text retrieval
- pgvector, Qdrant, Weaviate, Milvus
- A choice from the docs. I did not run these systems.

### Slide 2 — The problem

- Same words: keyword search can find the document
- Same meaning, different words: keyword search misses it
- A vector database stores embeddings and returns the nearest ones
- It can filter on metadata in the same query

No diagram.

### Slide 3 — Two kinds of system

- pgvector: a column in Postgres, next to the text and the metadata
- Qdrant: a Rust server; a point is a vector plus a JSON payload; filtering is inside the index
- Weaviate: each object keeps its vectors; keywords and similarity hit the same object
- Milvus: Standalone is the one-machine demo; Distributed adds node roles, etcd, and object storage

No diagram.

### Slide 4 — Filters

Diagram: filter order, same grammar for all four. pgvector is scan-then-predicate. Qdrant is edges inside the walk. Weaviate is allow-list then walk. Milvus is predicate then search. Keep these lines:

- pgvector: the `WHERE` runs after the approximate scan. At `ef_search` 40 and a predicate matching 10% of rows, about 4 rows survive.
- Qdrant: payload-index edges exist only for indexes present when the graph was built.
- Weaviate: allow-list, then the graph walk. A tight list can fall back to a flat scan.
- Milvus: filter first, then approximate search. Past about 98% filtered out, the documented heuristic switches to brute-force FLAT, and the page says the heuristic is not always right.

### Slide 5 — Fusion

This is the mechanism slide. A thin strip above the table: keyword list and vector list join into one rank. The table stays the body of the slide. Copy the formulas.

| System | What it ships |
|---|---|
| Qdrant | `1/(k + rank)`, rank starts at 0, default `k` is 2. Best hit on one list: 1/2. |
| Weaviate | Scale each list so the best score is 1 and the worst is 0, then mix with alpha. Server uses 0.75 only when the request omits alpha. |
| Milvus | `1/(k + rank)`, rank starts at 1, default `k` is 60. Best hit on one list: 1/61. |
| pgvector | The README names reciprocal rank fusion and leaves the query to you. |

### Slide 6 — The rule

Diagram: stay versus leave. Three conditions on one side, three limits on the other.

Stay on pgvector when all three are true:

- The text is already in Postgres
- The dimension fits: 2,000 on `vector`, 4,000 on `halfvec`
- You can write the fusion SQL

Leave when any one of these is the limit you actually have:

- You want fusion as a feature
- You want the filter inside the index walk
- One machine is no longer enough

Do not add the spoken Citus/PgDog clause, the cluster-migration sentences, or "hold out a labeled set." Those are talk, not slides.

### Slide 7 — Which engine, if I leave

- Qdrant: one process, filterable HNSW, a published RAM formula
- Weaviate: BM25 in the same server, and an alpha you set
- Milvus: past one machine, and you will run etcd plus object storage

No diagram. pgvector is not a fourth card on this slide.

### Slide 8 — Sources

Page name, not a paragraph. These four only. No second sources slide. A URL may sit with the page name. Do not add the filter, cluster, or capacity-planning links. Those are named out loud or saved in the TextData community.

- [pgvector README](https://github.com/pgvector/pgvector/blob/v0.8.7/README.md) (v0.8.7)
- [Qdrant hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/)
- [Weaviate hybrid concepts](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search)
- [Milvus RRF ranker](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/userGuide/embeddings-reranking/reranking/rrf-ranker.md)

## 3A. What Was Accomplished

- Read `docs/misc/presentation-runbook.md`, `docs/artifacts/instructions.md`, and `docs/artifacts/TopicSummary.md`.
- Grill closed. Isaac chose `implement directly`.
- Canva MCP inspected. Namespace `plugin-canva-canva` was `needsAuth`.
- `mcp_auth` attempted via `CallDynamicTool`. Failed: interactive MCP auth only works in the Cursor desktop IDE.
- `canva --version` failed: command not found.
- No Canva design, candidate, or local slide file was created.

## 4A. Current State

You are here: spec locked, zero slides in Canva. The runbook is still the spoken script. This handoff is the build contract. Desktop Cursor is the first environment that can complete Canva login.

## 5. Key Decisions & Rationale

| Decision | Rationale |
|----------|-----------|
| Eight slides, runbook lines copied onto the slides | The runbook is already the talk. Paraphrase and extra slides were rejected. |
| Say script stays in the runbook | One script. Full-screen Canva while recording. Notes in Canva would be a second copy. |
| 16:9, large type | The assignment is a recorded screen share. |
| Matte black, Cursor-dark, one accent, one type treatment for the four names | Isaac asked for dark mode like Cursor. Four brand hues and stock decorative templates were rejected. |
| Diagrams only on filters, fusion, and stay/leave | Those mechanisms are hard to see in bullets. Fusion keeps the formula table plus a thin "two lists → one rank" strip. |
| Slide 1 is the three runbook lines only | Includes the line that he did not run the systems. No name, no course mark. |
| Slide 8 is the four source pages | Assignment needs citations on screen. A ninth sources slide was rejected. |
| Static slides, slide number only | He will not be locked to the minute marks. The clock is not printed. |
| Canva MCP, not the CLI | He asked for the MCP. The CLI is absent and was not approved. |

## 6. Blockers & Open Questions

- **Canva auth.** This session cannot complete it. In the desktop app, authenticate `plugin-canva-canva`, then `GetDynamicTools` on that namespace and confirm real tools (not only `mcp_auth`).
- **Brand kits were never listed.** The Canva presentation skill (`inactive-skills/generate-deck/SKILL.md`, name `canva-branded-presentation`) requires `list_brand_kits` and an explicit user choice before `generate-design`. Do not auto-select a kit. A kit can override the settled matte-black palette. If kits exist, ask, and say that. If none exist, say so and generate without a kit. If the scope error says `brandkit:read` is missing, ask Isaac to disconnect and reconnect Canva.
- **No open design questions.** Palette hex is unspecified on purpose. Do not stop to ask for a hex.

## 7. Next Steps

1. Authenticate Canva in the desktop app. Confirm the namespace is usable.
2. Read this file and `docs/misc/presentation-runbook.md`. Build only the on-slide lines in Original Design. Use the runbook for spoken wording if Isaac asks. Do not import research notes onto slides.
3. `list_brand_kits`. Ask only if at least one kit exists (see §6). Otherwise continue without a kit.
4. Call `generate-design` (`_generate_design` if that is the callable name) with `design_type: "presentation"`. Do **not** call `prepare-design-generation` or `_prepare_design_generation`. The skill says to stop rather than fall through to prepare.
5. Put the Original Design deck rules and the eight slides in the generation query: exact 8, 16:9, matte black, one accent, static, slide numbers, exact lines, diagrams only on 4–6, formula table on 5. Working title: `Self-hosted vector databases for text retrieval`.
6. If Canva returns candidates, show them and ask which one to turn into an editable design. Reject a light theme, a wrong slide count, or paraphrased formulas. Regenerate rather than rebuilding structure.
7. After a design exists, text-only fixes go through `start-editing-transaction` → `perform-editing-operations` → show thumbnails → ask Isaac before `commit-editing-transaction`. The editing API cannot add text boxes, add or remove slides, change the background, change the font family, or edit animations. If the dark ground or the page count is wrong, regenerate. Do not pretend an edit fixed it.
8. Return the Canva edit link. Do not commit git. Do not write a plan, recap, or second handoff unless Isaac asks.

## 8. Must-Knows for the New Thread

- Isaac's name stays off the slides. He asked for that by picking the three-line title.
- "I did not run these systems" stays on slide 1. He did not benchmark the four databases.
- Formulas are load-bearing. Qdrant rank starts at 0 and `k` is 2 (best hit 1/2). Milvus rank starts at 1 and `k` is 60 (best hit 1/61). Weaviate's server alpha 0.75 applies only when the request omits alpha. pgvector names reciprocal rank fusion and does not ship the query.
- The four numbers already allowed on slides are the runbook's: `ef_search` 40, 10% of rows, about 4 rows, about 98% filtered out, dimension caps 2,000 and 4,000. Do not add corpus sizes, QPS, or recall.
- Slide 7 is the leave pick. It is Qdrant, Weaviate, Milvus. Not a four-way scoreboard.
- Canva AI will try to rewrite sparse academic bullets into marketing copy. The presentation skill defaults to sales decks. This deck is a class explanation. The query must forbid a CTA, a product pitch, stock photography, and extra slides.
- Show generation thumbnails and the edit-commit preview. Do not tell Isaac the design is saved before commit succeeds.
- First person lives in the spoken script ("I would stay"). Slides use the runbook's own wording, including "You can write the fusion SQL" and "you will run etcd."

## 9. Relevant Artifacts

| Path | Role | State |
|------|------|-------|
| `docs/misc/presentation-runbook.md` | Spoken script, clock, Q&A, pages to name aloud, leave-out list | Current. Source of on-slide lines. |
| `docs/artifacts/instructions.md` | CS410 assignment: 8–12 min recording, voice, citations, original analysis | Reference only. |
| `docs/artifacts/TopicSummary.md` | Topic framing. Broader than the 10-minute deck. | Do not mine it for extra slides. |
| `docs/research/comparison.md` | Longer source list for the TextData community | Not slide content. The runbook says this list stays off the recording's closing slide. |
| `docs/research/{pgvector,qdrant,weaviate,milvus}.md` | Research notes | Out of the deck. |
| `inactive-skills/generate-deck/SKILL.md` under the Canva plugin cache | How to call `generate-design` and brand kits | Follow its tool rules. Ignore its sales-narrative defaults. |
| `skills/edit-design/SKILL.md` under the Canva plugin cache | Transaction protocol and the CANNOT list | Use only after a design exists. |
