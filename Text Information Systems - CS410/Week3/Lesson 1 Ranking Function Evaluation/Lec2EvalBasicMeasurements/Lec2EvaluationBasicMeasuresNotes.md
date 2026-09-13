# Designing basic measurements to quantitatively compare two ranking functions

Example Used:
Let's say a collection has 48 docs. 10 of them are relevant to query 1.
System A returns 3 docs, 2 of those docs are relevant to the query
System B returns 5 docs, 3 of those docs are relevant to the query

## Precision
the fraction of total docs that are returned by a system that are considered relevant to a query
If a system has a precision of 100%, all docs returned are relevant

System A Precision = 2/3

System B Precision = 3/5


## Recall
The fraction of the relevant docs that are returned, regardless of how many nonrelevant docs are returned. "Completeness of coverage
System A recall = 2/10

System B recall = 3/10

**Precision and Recall are the core measurements**

## Precision and Recall for evaluating a set of retrieval docs
|              | Retrived | Not Retrived |
|--------------|----------|--------------|
| Relevant     |    a     |      b       |
| Not Relevant |    c     |      d       |
|

**Precision = a / (a + c)** (simply put, retrived docs that are relevant divided by total number of retrived docs)

**Recall    = a / (a + b)** (simply put, retrived docs that are relevant divided by the total number of docs in the collection)

Ideal results numerically look like Precision = Recall = 1.0
    In practice, recall that is to high is associated with low precision
        The ranking function may be returning a large portion of the relevant docs, but they can only do that by returning a large portion of the collection, regardless of relevance

**Note:** Any set/measurement can be defined by a cutoff. (example: precision at first ten docs in the ranked list is what is common to care about when ranking web results)

## F-Measure
see "Text Information Systems - CS410/Week3/Lesson 1 Ranking Function Evaluation/Lec2EvaluationBasicMeasuresNotes.md"
F-measure is an equation to combine precision and recall into a single value
Technically, a "harmonic mean" Of precision and recall

F_beta = ((beta^2 + 1) P * R) / ((beta^2 * P) + R)
P    = precision
R    = Recall
Beta = parameter (often set to 1)

When beta is set to one, that is a special F-measure called F_1:
F_1 = (2PR) / (P + R)