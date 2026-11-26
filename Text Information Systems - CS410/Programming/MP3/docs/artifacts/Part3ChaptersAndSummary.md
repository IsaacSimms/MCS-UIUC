# MP3 Part 3.2: Chapters and Summary (paste-ready code)

## How to paste

In the 3.2 cell, replace everything with this block. Run that cell, then the 3.2 check cell.

If you change `summarize_clip` or its prompt later, set `REDO_SUMMARIES = True`, run the check cell once, and set it back to `False`. Clip summaries are cached; chapters and the video summary are rebuilt on every run.

## Code

```python
CHAPTER_MIN_GAP = 60
SECONDS_PER_CHAPTER = 120

CLIP_SYSTEM = (
    "You summarize one clip of a video in one or two sentences. "
    "'Said' is the speech and 'Shown' is what is on screen. "
    "Take the topic from what is said, and use what is shown only to support it. "
    "Reply with the summary only, with no introduction."
)
CHAPTER_SYSTEM = (
    "You divide a video into chapters, where each chapter is a run of neighboring clips on one topic. "
    "Reply only with one line per chapter in the form m:ss | Title. "
    "Use start times from the list, begin at 0:00, and keep each title under eight words."
)
VIDEO_SYSTEM = (
    "You summarize a whole video in one paragraph of 4 to 6 sentences. "
    "Cover the beginning, middle, and end, using only the information given. "
    "Reply with the paragraph only, with no introduction."
)

CHAPTER_LINE = re.compile(
    r"^\W*(\d+(?::\d{2}){1,2})"          # start time, after any bullet, bracket or bold marks
    r"(?:\s*[-–|]\s*\d+(?::\d{2}){1,2})*"  # an end time, or the start time the model sometimes repeats
    r"[\]\)*]*\s*[|:\-–—]?\s*(.+)$"
)


def clean_reply(text):
    """One line of text without an opening such as 'Here is a summary:'."""
    text = re.sub(r"^(?:sure\b[^\n]*?[.!:]\s*)?(?:here(?:'s| is| are)\b[^\n:]*:|summary:)", "",
                  text.strip(), flags=re.IGNORECASE)
    return " ".join(text.split())


def parse_chapters(reply, clip_starts):
    """Usable chapters from the model's reply, in time order and at least CHAPTER_MIN_GAP apart."""
    found = {}
    for line in reply.splitlines():
        m = CHAPTER_LINE.match(line.strip())
        if not m:
            continue
        t, title = parse_time(m.group(1)), m.group(2).strip(' *"|')
        if t < DURATION and title:
            found.setdefault(max(s for s in clip_starts if s <= t), title)

    chapters = []
    for start, title in sorted(found.items()):
        if not chapters:
            start = 0.0
        elif start - chapters[-1]["start"] < CHAPTER_MIN_GAP:
            continue
        chapters.append({"start": start, "title": title})
    return chapters


def interval_chapters(clip_summaries):
    """One chapter every SECONDS_PER_CHAPTER, titled from the opening words of that clip's summary."""
    return [{"start": s["start"], "title": " ".join(s["summary"].split()[:8]) or fmt_time(s["start"])}
            for s in clip_summaries if s["start"] % SECONDS_PER_CHAPTER == 0]


def summarize_clip(clip):
    """
    Map step: one or two sentences on what this clip covers.

    clip["text"] is the clip's indexed text (what is said plus what is shown). Use ollama_chat.
    Return "" if the clip has no text.
    """
    if not clip["text"].strip():
        return ""
    return clean_reply(ollama_chat(f"Video clip:\n\n{clip['text']}", system=CLIP_SYSTEM))


def make_chapters(clip_summaries):
    """
    Group neighboring clips into chapters, like the chapter list under a video.

    clip_summaries: list of {"start": seconds, "summary": str}, in time order.
    Return a list of {"start": seconds, "title": str} in time order, with the first chapter at 0.

    One way: send the timed summaries to the LLM, ask for lines like "1:30 | Title",
    and parse each line with parse_time. Another way: start a new chapter when the topic
    changes between neighboring clips. Aim for about one chapter per 1 to 3 minutes.
    For long videos, pass num_ctx=8192 (or more) to ollama_chat so nothing gets cut off.
    """
    listing = "\n".join(f"{fmt_time(s['start'])} | {s['summary']}" for s in clip_summaries if s["summary"])
    count = max(2, round(DURATION / SECONDS_PER_CHAPTER))
    prompt = (f"The video is {fmt_time(DURATION)} long. Group these clips into about {count} chapters, "
              f"each lasting 1 to 3 minutes.\n\nClips (start time | summary):\n{listing}")
    reply = ollama_chat(prompt, system=CHAPTER_SYSTEM, num_ctx=8192)
    chapters = parse_chapters(reply, [s["start"] for s in clip_summaries])
    if len(chapters) >= 2:
        return chapters
    print("make_chapters: unusable model reply, using fixed intervals")
    return interval_chapters(clip_summaries)


def summarize_video(chapters, clip_summaries):
    """
    Reduce step: one paragraph (4 to 6 sentences) on the whole video,
    written from the chapter titles and the clip summaries. Return the text.
    """
    titles = "\n".join(f"{fmt_time(ch['start'])} | {ch['title']}" for ch in chapters)
    clips = "\n".join(s["summary"] for s in clip_summaries if s["summary"])
    prompt = (f"Chapters:\n{titles}\n\nClip summaries, in order:\n{clips}\n\n"
              "Summarize the whole video in one paragraph of 4 to 6 sentences.")
    return clean_reply(ollama_chat(prompt, system=VIDEO_SYSTEM, num_ctx=8192))
```

## How it fits together

```
summarize_clip   (map)     17 clips -> 17 short summaries (cached by the check cell)
make_chapters              timed summaries -> one llama3.2 call
                           -> parse_chapters: repair the reply
                           -> interval_chapters if fewer than 2 are usable
summarize_video  (reduce)  chapter titles + clip summaries -> one paragraph
```

## Why each choice

| Choice                               | Reason                                                                           |
| ------------------------------------ | -------------------------------------------------------------------------------- |
| One call lists the chapters          | Gives boundaries and titles together                                             |
| Speech first in clip summaries       | Keeps visual details from taking over the topic                                  |
| `parse_chapters` repairs the reply | A small model does not reliably follow the format                                |
| Times moved to a clip start          | The model only has information per 30 second clip                                |
| At least 60 s between starts         | Prevents a chapter for nearly every clip                                         |
| First chapter forced to 0:00         | Required, and the model may skip it                                              |
| Fixed 2 minute fallback              | The pipeline always finishes. It prints a message when used                      |
| `clean_reply`                      | Removes openings such as "Here is a summary:" and joins lines into one paragraph |
| Length only requested in the prompt  | Cutting sentences could drop the end of the video                                |
| `num_ctx=8192`                     | Stops Ollama from silently cutting the long input                                |

## Test results

Run outside the notebook, using your saved screen index, transcript and local `llama3.2`. Your `mp3_work` folder was not written to.

The progress check conditions pass. The model produced these chapters, and the fallback was not used:

| Start | Title                         |
| ----- | ----------------------------- |
| 0:00  | Google Translate Basics       |
| 1:30  | Transformer Model Explained   |
| 4:30  | Optical Character Recognition |
| 7:30  | Google Lens Challenges        |

The video summary was 5 sentences in one paragraph.

**One fix after the first run:** the model wrote each time twice (`0:00 | 0:00 | Title`), which left a time inside every title. The pattern now accepts the repeated time. The prompts were not changed.

**Weaknesses in the output:**

- The 3:30 clip summary says the decoder is "decoding human language back into individual words". The decoder turns numbers back into language. The video summary repeats this error.
- The 4:00 clip summary says the limitation leads to "increased testing time for non-English languages". The video says translating between two non-English languages takes more steps.
- "Google Lens Challenges" (7:30) is a poor title: that part is about slang, tone, dialects and adding languages.
- The video summary mostly strings clip summaries together, and leaves out text layout and replacing text in images.

## Notes for the Part 3 written answer

- **Chapter boundaries:** `llama3.2` read all 17 timed clip summaries and chose them. Code moved each to a clip start, required at least 60 s between starts, and forced the first to 0:00.
- **Limit:** boundaries can only fall every 30 s, so a topic that changes mid clip is placed early or late.
- **Limit:** errors in a clip summary carry into the chapters and the video summary.

Confirm the chapters and errors against your notebook output before writing about them.
