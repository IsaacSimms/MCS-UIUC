# Quiz Notes Style Guide

Using only the conversation above, write personal quiz notes. The conversation has already worked the questions. Record the conclusion it settled. Do not solve a question again. Do not add a concept, stem, option, course, week, or quiz name that the conversation never stated.

## Reply format

Reply with exactly one fenced `markdown` block and no other text.

- Do not create or edit a file.
- Do not write anything before or after the fence.
- Inside the block, keep code and formulas inline, as the conversation wrote them. Do not put a second fence inside the block.
- Do not copy the format samples below into the reply.
- The notes are study notes. State the subject directly. Do not narrate the chat ("we said", "the thread decided") except inside **Unresolved.**, which must say what is still open.

## Which questions

- Include every item the conversation treated as a quiz question.
- Leave out side discussion that was not a quiz question.
- If a question was revisited, write one section and use the last conclusion.
- If the conversation settled no quiz questions, and none were left open, the fenced block is only this:

```markdown
# Quiz notes

No quiz questions were settled in this thread.
```

Do not append that sentence to notes that contain questions.

## Title and groups

- The first line inside the fence is one H1.
- If the conversation gave a name for the notes as a whole, use that name as the H1.
- If it gave no name, the H1 is exactly `# Quiz notes`.
- Do not invent a course, week, or quiz type.
- One quiz: no group heading. Each question is a `##` heading.
- More than one quiz: add a group only when the conversation itself treated the work as separate quizzes. Each group is a `##` heading using the conversation's name for that quiz, in the order the conversation took them up. Questions inside a group are `###` headings.
- Do not split one quiz by topic.

## Numbering and stems

- Keep the question numbers the conversation used. Numbering restarts inside each group.
- If a quiz was never numbered, number its questions `1..n` in the order they first appeared.
- List questions in number order. If a number was never opened, leave the gap. Do not add a stub for it.
- The heading text is the stem the conversation stated, still phrased as a question, including words such as NOT or "check all that apply."
- If the conversation only paraphrased the stem, use that paraphrase.

Heading form: `## 1. Stem here?` or, inside a group, `### 1. Stem here?`

## Settled questions

After the heading, use these fields in this order. Put a blank line after the heading and between fields.

**Context.** One to three sentences on the concept required to understand the question. Use only concepts the conversation already stated. If that explanation was thin, keep this thin.

Then exactly one of these:

- One settled option: `**Correct answer.**` followed by the option.
- Every option settled, and more than one is correct: `**Correct answers.**` followed by a bullet for each option.

Write the option as the conversation stated it. When both a letter and the option text appear, write the letter and the full text (`B. Blue`). When there is no letter, write the text only. Never write a bare letter.

**Why.** Why the settled answer is right. Add one short clause for each rejected option the conversation actually discussed, and skip any option it did not discuss. For a calculation, put the short derivation in this field, using only steps the conversation already showed.

Between questions, put a line that contains only `---`. Do not put that line after the last question of the note or of a group.

## Unsettled questions

If the conversation never settled the question, or if a check-all still has any option open, do not guess. Write the heading and **Context.** as above, then:

**Unresolved.** What is still open. For a half-settled check-all, name the options that were agreed and the options that were still open, using the letter and full text when the conversation has them.

Do not include **Correct answer.**, **Correct answers.**, or **Why.**

## Format samples

These samples show the labels for a single quiz. They are not part of the conversation. Do not include them in the reply. A grouped quiz uses the same fields under `###` headings.

### Single answer

```markdown
## 1. Which of the following is a primary color?

**Context.** Primary colors are the base colors this quiz mixes to make other colors. In that set, the primaries are red, blue, and yellow.

**Correct answer.** B. Blue

**Why.** Blue is one of those three primaries. Green was treated as a mixture of blue and yellow, so it is not a primary.
```

### Check all

```markdown
## 2. Which of the following are primary colors? (Check all that apply)

**Context.** The primary set is red, blue, and yellow. A color mixed from those is not itself primary.

**Correct answers.**
- A. Red
- C. Yellow

**Why.** Red and yellow are in the primary set. Green was treated as a mixture, so it is not selected.
```
