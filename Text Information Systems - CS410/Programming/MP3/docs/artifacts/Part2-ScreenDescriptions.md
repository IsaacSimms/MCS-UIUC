# MP3 Part 2: Screen Descriptions (paste-ready code)

Target: the first Part 2 cell, `describe_screen()` and `clip_text(clip)`. In each function, replace both `# YOUR CODE HERE` and `raise NotImplementedError` with the body below. Keep the docstrings.

Settled design (from the grill):

| Decision                 | Choice                                                                           |
| ------------------------ | -------------------------------------------------------------------------------- |
| Prompt ownership         | Drafted and annotated here; adapt it in your own words before the written answer |
| `high_res`             | `True` on the first run                                                        |
| Robustness               | Spec only: skip out-of-range items, join duplicates in one clip                  |
| Windows with nothing new | Describe what is visible anyway; `""` only when nothing is visible             |
| `clip_text` format     | `Said: ...\nShown: ...`, empty part dropped                                    |

## 1. `describe_screen()` body

```python
    prompt = f"""Watch this video and describe what is shown on screen. Do not transcribe the speech.

Split the video into consecutive {CLIP_SECONDS} second windows starting at 0:00 (0:00, 0:30, 1:00, ...) until the end of the video, which is {fmt_time(DURATION)} long. Return a JSON list with exactly one entry per window, in this form:
[{{"start": "0:00", "shown": "..."}}, {{"start": "0:30", "shown": "..."}}]

In "shown", write 2 to 4 short sentences about what is visible during that window:
- Copy any text on screen exactly as written: slide titles, bullet points, diagram labels, numbers, captions, name tags.
- Say what kind of visual it is (slide, diagram, animation, screen recording, person at a desk) and what it depicts.
- Describe the screen even when it looks the same as the previous window.
- Do not repeat what is only said aloud, and do not describe anything that is not visible.
- If nothing meaningful is visible (a black frame, or a speaker with no text), use an empty string."""
    reply = gemini_video(prompt, "screen descriptions (Gemini)", json_output=True, high_res=True)
    items = parse_json(reply)
    shown = {}
    for item in items:
        index = int(parse_time(item["start"]) // CLIP_SECONDS)
        if not 0 <= index < len(CLIPS):
            continue
        clip_id = CLIPS[index]["id"]
        shown[clip_id] = (shown.get(clip_id, "") + " " + item["shown"]).strip()
    return shown
```

## 2. `clip_text(clip)` body

```python
    parts = []
    if clip["transcript"]:
        parts.append(f"Said: {clip['transcript']}")
    if clip.get("shown"):
        parts.append(f"Shown: {clip['shown']}")
    return "\n".join(parts)
```

## 3. The prompt, sentence by sentence

| Prompt text                                                                       | Why it is there                                                                                                                                                                              |
| --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Do not transcribe the speech."                                                   | Gemini hears the audio. Without this it fills `shown` with speech, which duplicates the transcript and adds nothing new for BM25.                                                          |
| "consecutive 30 second windows starting at 0:00 ... until the end ... 8:14 long"  | Fixes the grid to `CLIP_SECONDS`, so `int(start // CLIP_SECONDS)` lands on the right clip. Giving the video length tells it where to stop, which prevents invented windows past the end. |
| The JSON example with `start` and `shown`                                     | Matches the keys the code reads. `json_output=True` forces valid JSON; the example fixes the shape. The `{{ }}` are f-string escapes for literal braces.                                 |
| "exactly one entry per window"                                                    | One entry per window keeps the mapping to clips one to one, so coverage is high.                                                                                                             |
| "2 to 4 short sentences"                                                          | Matches the docstring. Short text keeps the BM25 document balanced against the transcript, so screen text does not drown out speech.                                                         |
| "Copy any text on screen exactly"                                                 | The main retrieval payoff. A query like "what does the slide titled X say" only matches if the index holds the exact words.                                                                  |
| "Say what kind of visual it is"                                                   | Lets queries such as "the diagram of the encoder" match even when no text is on screen.                                                                                                      |
| "Describe the screen even when it looks the same"                                 | Each clip is indexed alone. A slide that stays up for three windows needs its text in all three, or the later clips lose it.                                                                 |
| "Do not repeat what is only said aloud, and do not describe anything not visible" | Keeps `shown` complementary to `said` and limits invented detail.                                                                                                                        |
| "use an empty string" for nothing visible                                         | An empty `shown` makes `clip_text` drop the `Shown:` line, so BM25 gets no filler such as "a person speaks".                                                                           |

## 4. Why the code works

### `describe_screen`

1. **One Gemini call.** `gemini_video(...)` sends the video link plus the prompt and returns the reply text. It uses `temperature` 0, so reruns give nearly the same result. It also records seconds and token count under the step name `screen descriptions (Gemini)`, which appears in the Part 4.4 cost table. `high_res=True` raises the token count to about 3x for that row.
2. **`parse_json(reply)`** strips code fences and returns a Python list of dicts, so `items` is `[{"start": "0:00", "shown": "..."}, ...]`.
3. **Window to clip.** `parse_time("0:30")` returns `30.0`. `30.0 // 30` is `1.0`, and `int(...)` gives `1`, so the item belongs to `CLIPS[1]`. Gemini may write `"00:30"` or `"0:30"`; `parse_time` handles both.
4. **Range guard.** `0 <= index < len(CLIPS)` skips any item past the end or before 0:00, as the docstring requires.
5. **Joining duplicates.** If two items land in one clip, `shown.get(clip_id, "")` returns the earlier text, and the new text is appended with a space. `.strip()` removes the leading space when the clip is new.
6. **Return type.** The function returns a plain `dict` of string keys to string values. `load_screen_descriptions()` checks `isinstance(shown, dict)`, saves it as JSON (string keys only, which clip ids are), then sets `c["shown"] = str(shown.get(c["id"], "")).strip()` on every clip. Clips Gemini left out get `""`.

### `clip_text`

1. `clip["transcript"]` is always present (may be `""`), so it is read directly. `clip.get("shown")` is used because `shown` is added to the clips only after `load_screen_descriptions()` runs.
2. An empty part is skipped, so a clip with no speech indexes only `Shown: ...`, and a clip with no screen text indexes only `Said: ...`.
3. The labels let the LLM tell speech from screen text when it reads the retrieved clip.

### What the check cell tests

| Check in the progress cell                                                      | How this code satisfies it                                                                                                               |
| ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `describe_screen` returns a `dict`                                          | `shown = {}` is returned.                                                                                                              |
| No `unknown` keys                                                             | Keys come from `CLIPS[index]["id"]`, so every key is a real clip id.                                                                   |
| `covered >= len(CLIPS) // 2`                                                  | `17 // 2 = 8`, so at least 8 of 17 clips need a non-empty description. The "describe even when the same" rule is what keeps this high. |
| `clip_text` with both parts contains `"SHOWN TEXT"` and `transcript[:30]` | Both `if` branches fire and both strings are joined.                                                                                   |
| `clip_text` with an empty transcript still contains `"SHOWN TEXT"`          | The transcript branch is skipped and the shown branch still returns it.                                                                  |

## 5. Running it

1. Paste both bodies and run the first Part 2 cell. This only defines the functions.
2. Run the progress cell. The first run makes one Gemini call and writes `mp3_work/screen_descriptions.json`. Expect `describe_screen: pass` and `clip_text: pass`.
3. Run the next cell to build `SCREEN_INDEX`, then the cell that reruns your non-correct questions.
4. Read the printed descriptions against the video for a clip with a slide. If text is wrong or missing, change the prompt, set `REDO_SCREEN = True`, run the check cell once, then set it back to `False`.

## 6. Known risks

- If Gemini wraps the list in an object (for example `{"windows": [...]}`), `item["start"]` raises. Spec-only handling does not catch this. Rerun with `REDO_SCREEN = True`, or state "a JSON list, not an object" in the prompt.
- A `start` with an unusual format (for example `"0:30-1:00"`) makes `parse_time` return `None`, and `None // 30` raises a `TypeError`. The prompt's example format makes this unlikely.
- `high_res=True` raises the `screen descriptions (Gemini)` token figure in the Part 4.4 table by about 3x. Keep that in mind for the Part 4 Q3 answer.
