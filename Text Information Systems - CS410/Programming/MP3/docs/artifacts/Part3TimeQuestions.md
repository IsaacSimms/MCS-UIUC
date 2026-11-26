# MP3 Part 3.1: Time Questions (paste-ready code)

## How to paste

In the 3.1 cell, keep the first two lines (`BEST_INDEX = ...` and the `print`). Replace everything below them with this block, then run the cell and the 3.1 check cell.

## Code

```python
SINGLE_TIME_MARGIN = 15
EDGE_SECONDS = 60

NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
NUMBER = r"(\d+|" + "|".join(NUMBER_WORDS) + r")\b"
CLOCK = r"(\d+(?::\d{2}){1,2})"

RANGE_PATTERN = rf"\bbetween {CLOCK} and {CLOCK}|{CLOCK}\s*(?:to|until|through|-)\s*{CLOCK}"
SPAN_PATTERN = rf"\b(first|opening|last|final) (?:{NUMBER} )?(second|minute)s?\b"
MINUTE_PATTERN = rf"\bminute {NUMBER}"

# The lookahead rejects "at the end of the encoder stage", which is not a time in the video.
NOT_OF_SOMETHING_ELSE = r"\b(?! of (?!the video|this video))"
WHOLE_QUESTION = r"\s*(?:[?.!]|$)"
START_PATTERN = (
    rf"\b(?:at|in|near) the (?:very )?(?:start|beginning){NOT_OF_SOMETHING_ELSE}"
    r"|\b(?:start|beginning) of (?:the|this) video\b"
    r"|\b(?:in|during) the (?:intro|introduction|opening)\b"
    rf"|\bhow (?:does|did) (?:it|the video|this video) (?:start|begin|open){WHOLE_QUESTION}"
)
END_PATTERN = (
    rf"\b(?:at|near|toward|towards) the (?:very )?(?:end|ending){NOT_OF_SOMETHING_ELSE}"
    r"|\b(?:end|ending) of (?:the|this) video\b"
    r"|\b(?:in|during) the (?:outro|conclusion)\b"
    rf"|\bhow (?:does|did) (?:it|the video|this video) (?:end|finish|conclude){WHOLE_QUESTION}"
)

SUMMARY_PATTERN = (
    r"\bsummar(?:y|i[sz]e)|\boverview\b|\btakeaways?\b|\b(?:main|key) (?:point|idea)s?\b"
    r"|\bwhat(?:'s| is) (?:this|the) video about\b"
)

ROUTE_SYSTEM = (
    "Classify a question about a video. Reply with exactly one word.\n"
    "time: asks about a particular moment or part of the timeline.\n"
    "summary: needs the whole video, such as its overall topic or message.\n"
    "specific: asks about one fact, person, term, or example."
)


def to_number(text):
    return NUMBER_WORDS.get(text) or int(text)


def mentioned_time(question, duration):
    """(start, end) for the time wording in the question, not yet trimmed to the video. None if there is none."""
    q = question.lower()

    if m := re.search(RANGE_PATTERN, q):
        start, end = sorted(parse_time(t) for t in m.groups() if t)
        return start, end

    if m := re.search(SPAN_PATTERN, q):
        side, count, unit = m.groups()
        length = (to_number(count) if count else 1) * (60 if unit == "minute" else 1)
        return (0, length) if side in ("first", "opening") else (duration - length, duration)

    if m := re.search(MINUTE_PATTERN, q):
        minute = to_number(m.group(1))
        return (minute - 1) * 60, minute * 60

    if m := re.search(CLOCK, q):
        t = parse_time(m.group(1))
        # An empty window past the end, so that the margin cannot pull it back into the video.
        if t > duration:
            return t, t
        return t - SINGLE_TIME_MARGIN, t + SINGLE_TIME_MARGIN

    if re.search(START_PATTERN, q):
        return 0, EDGE_SECONDS

    if re.search(END_PATTERN, q):
        return duration - EDGE_SECONDS, duration

    return None


def classify_question(question):
    """
    Return "specific", "time", or "summary".

        "time"      points to a moment: "at 3:20", "in minute 4", "at the start", "how does it end"
        "summary"   needs the whole video: "summarize", "main point", "key takeaways", "what is this video about"
        "specific"  everything else (normal retrieval)

    Use keyword rules, a regex for m:ss, an LLM call (ollama_chat), or a mix. Rules are fast and
    predictable; an LLM handles unusual wording. Explain your choice in the Part 3 answer cell.
    """
    if mentioned_time(question, DURATION) is not None:
        return "time"
    if re.search(SUMMARY_PATTERN, question.lower()):
        return "summary"
    reply = ollama_chat(f"Question: {question}", system=ROUTE_SYSTEM).lower()
    label = re.search(r"\b(specific|time|summary)\b", reply)
    return label.group(1) if label else "specific"


def time_window(question, duration=None):
    """
    Turn a time question into a (start, end) window in seconds, or None if no time is found.

    Examples for a 600 second video:
        "what happens at the start?"       → (0, 60)
        "how does the video end?"          → (540, 600)
        "what is on screen at 3:20?"       → (185, 215)    about 15 s on each side
        "what does she say in minute 4?"   → (180, 240)

    parse_time("3:20") gives 200.0. Keep the window between 0 and duration.
    """
    duration = duration or DURATION
    window = mentioned_time(question, duration)
    if window is None:
        return None
    start, end = max(0, window[0]), min(duration, window[1])
    return (start, end) if start < end else None


def answer_time_question(question):
    """
    Answer a time question from the clips in its window.

        1. window = time_window(question)
        2. If window is None, return rag_answer(question, BEST_INDEX) with "path" set to "time".
        3. Otherwise pick the clips in BEST_INDEX.docs.values() that overlap the window
           (clip start < window end, and clip end > window start).
        4. answer = answer_from_clips(question, picked_clips)

    Return a dict shaped like rag_answer's: {"question", "path": "time", "answer", "clips"}.
    """
    window = time_window(question)
    if window is None:
        return {**rag_answer(question, BEST_INDEX), "path": "time"}
    start, end = window
    clips = [c for c in BEST_INDEX.docs.values() if c["start"] < end and c["end"] > start]
    return {"question": question, "path": "time", "answer": answer_from_clips(question, clips), "clips": clips}
```

## How it fits together

```
classify_question
 ├─ mentioned_time found time wording?   → "time"
 ├─ SUMMARY_PATTERN matches?             → "summary"
 └─ otherwise ask llama3.2               → "time" | "summary" | "specific"

time_window          = mentioned_time, trimmed to 0..DURATION
answer_time_question = time_window → overlapping clips → answer_from_clips
```

## Why each choice

| Choice                                                        | Reason                                                                                                              |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Rules before the model                                        | Same result every run for the common wordings, with no model call                                                   |
| Model fallback                                                | Catches summary or time wording the rules do not list                                                               |
| `mentioned_time` separate from `time_window`              | "at 12:00" is still a time question although the video has no such window                                           |
| Patterns checked from range down to start/end                 | A range also contains a single time, so the more specific pattern must win                                          |
| Time checked before summary                                   | "Summarize the first two minutes" should use only those clips                                                       |
| "start" and "end" only inside phrases                         | "How does the model start learning?" is not about the timeline                                                      |
| Past the end returns `None`                                 | Falls back to normal retrieval instead of answering about a different moment. Spans partly past the end are trimmed |
| First `specific`, `time` or `summary` word in the reply | `llama3.2` may add words around its label; anything else counts as `specific`                                   |

## Wordings understood

| Wording                                                   | Window                      |
| --------------------------------------------------------- | --------------------------- |
| "from 2:00 to 3:00", "between 2:00 and 3:00", "2:00-3:00" | that range                  |
| "first two minutes", "last 30 seconds"                    | from that edge of the video |
| "in minute 4"                                             | 3:00 to 4:00                |
| "at 3:20"                                                 | 15 s on each side           |
| "at the very start", "in the intro"                       | first 60 s                  |
| "how does the video end", "in the conclusion"             | last 60 s                   |

Numbers can be digits or one to ten.

## Test results

Run outside the notebook, using your saved screen index, transcript and local `llama3.2`.

- The four docstring examples give the expected windows.
- The five sample questions from the check cell route as expected.
- "What is shown at 12:00?" routes to `time` and falls back to retrieval (retrieval itself was stubbed in this test).
- The right clips are selected, but the answers are weak: "What happens at the very start?" returned only `[0:00]`, and "What is on the screen at 4:07?" returned "I can't find this in the video." Answer generation is the provided `answer_from_clips`.

## Notes for the Part 3 written answer

- **Classifier:** time rules, then summary rules, then `llama3.2` for everything else. Most ordinary questions reach the model, because `specific` has no rules.
- **A misrouted question:** "What happens halfway through?" was routed to `specific`. It should be `time`. No rule lists "halfway", and the model fallback did not catch it.
- **Fallback working:** "Give me the gist." matches no rule and was routed to `summary`.
- **Another limit:** "from minute 2 to minute 3" is read as minute 2 only.

Confirm these in your notebook before writing about them.
