# Task 1 analysis draft

Place the three screenshots first, in this order: Chernobyl, the Berlin Wall, the Iowa caucuses. The discussion below is the paragraph for the paper.

## Discussion

All three questions were asked using the same pipeline and dataset described in the README. On every run the log recorded "Compression yielded 0 docs; falling back to base retriever," and the retriever then returned 3 documents. Asked what the Soviet response to the Chernobyl nuclear disaster was, the system answered well, and its response followed the retrieved article. Asked what the American response to the fall of the Berlin Wall was, the system failed. The retrieved article describes President Bush's response as cautious, bland, and bureaucratic, with no major policy move, but the model answered, "I don't know." The context already contained that answer, so the failure is in generation. It is not a hallucination, and the context was not missing. Asked how the Iowa caucuses affected the New Hampshire primary, the system answered well, and its response followed the retrieved article.

## Claim checklist

### Chernobyl

- Question: What was the Soviet response to the Chernobyl nuclear disaster?
- Verdict: Answered well.
- Why: The response followed the retrieved article.

### Berlin Wall

- Question: What was the American response to the fall of the Berlin Wall?
- Answer: "I don't know."
- Verdict: Failed in generation.
- Why: The retrieved article describes President Bush's response as cautious, bland, and bureaucratic, with no major policy move. The context contained that answer, and the model did not use it. This is not a hallucination, and the context was not missing.

### Iowa caucuses

- Question: How did the Iowa caucuses affect the New Hampshire primary?
- Verdict: Answered well.
- Why: The response followed the retrieved article.
