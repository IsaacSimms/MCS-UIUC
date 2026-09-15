## Challenges in creating a test collection
**To create a testing suite to test TR systems, you need to build a set of queries, a set of documents, and a set of relevance judgments**
    Creating each of these things can be a difficult task.

Both the queries and the documents must be representative of reality and include a large volume of each.
    docs queries should represent actual things people care about
Judgments: of all documents and all queries while minimizing human work (very difficult due to scale and labor intensive nature of labeling a doc)
Measures:  actually capture the perceived utility by users (if you are not measuring the right thing, conclusions are mislead)

### statistical significant testing
Question it answers: How sire you can be that an observed difference does not simply result from the particular queries you chose
You can find an average by taking per-query score (Ap, nDCG@K, etc.) and then finding the average score (MAP / mean nDCG).

statistical significant testing will take that a step beyond and look at how the system preforms.
    If system B beats system A by an average .2 points reliably, you can trust B is better.
    But if B crushes some queries and fails to system A at others, still have a .2 average point gain on system A, it is much more difficult to come to the conclusion that system B is better. Statistical significance testing tests this logic.

#### Sign test
When system B is better, give that query a + sign. When System A is better score, give it a - symbol. 
if the pluses and minuses come out to similar values, they are equivalent
    Meaning, there is not a statistical significance between them
p is attributed to that value, and with a 4-3 split, p = 1

#### Wilcoxon
A sign test after you rank the wins by size. Looking at by how much System B won or lost over System A. 

### Pooling
**Instead of judging all documents in the collection, judge a subset**

Strategy:
- choose a diverse set of TR systems (ranking functions)
- use a cutoff (return top k documents)
- combine all the top-k documents into a pool.
- Have human assessors judge that pool of documents and make human-in-the-loop judgement on if the document
- "Often" to assume that un-judged docs (so docs never returned in top-k to begin with) are non-relevant (not required)
- works for evaluating systems that contributed to the initial pool. Problematic for evaluating new systems.