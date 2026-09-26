# Feedback in a Vector Space Model
A methodology for TR systems learning from examples to improve retrieval accuracy.
Term definition:
- positive examples: docs that are known to be relevant (viewed by users)
- negative examples: ocs that are known to be non-relevant (skipped by users)

## The general method: query modification (changing query vector)
- adding new *weighted* terms (i.e. query expansion)
- also adjusting the weights of old terms

### Rocchio Feedback
Rocchio feedback is the vector space wya to do relevance feedback. The query is a point in the vector space just like all the docs (both positive and negative examples).
Move that query point within the vector space so that it is tightly coupled with as many positive examples as possible. (using labeled hits).
The most optimal place for the query point to be under this context is known as the **centroid of relevant documents**.

Above is the geometic theory/concept behind Rocchio feedback. To look at it algebraically, look at: "Text Information Systems - CS410/Week5/Lec2FeedbackInVectorSpaceModel/Formula-RocchioFeedback.png"

### Rocchio gen notes
- The vector is often truncated (small number of words hold the highest value)
- Avoid "over-fitting" by keeping a relatively high weight on the original query weights
This is bc over-fitting can lead to topic drifting
- this can be used in all three feedback methods discussed in lec 1 of this lesson
- usually a robust and effective method in vector space models



