# Week 9 Practice Quiz Answers

## 1. Which of the following is NOT a use of text clustering?

**Answer:** Grouping similar pictures together

**Why:** Text clustering operates on textual units (documents, sentences, websites treated as text collections). Grouping similar pictures is image clustering, not text clustering. The other three options are standard uses of text clustering.

## 2. What is the difference between direct and indirect evaluation for a clustering algorithm? (Check all that apply)

**Answer:**
- Indirect evaluation requires a user specified application to test with.
- Direct evaluation requires a human annotated gold standard cluster.

**Why:**
- Direct evaluation measures cluster quality by comparing results to a human-annotated gold standard (external evaluation).
- Indirect evaluation measures the utility of the clusters by their effect on a downstream application/task.
- The other two statements are false: EM results *do* depend on initialization, and neither evaluation method is inherently better than the other.

## 3. Agglomerative hierarchical clustering with single-link similarity → two clusters

**Answer:** Cluster 1 = {D1, D4, D5, D6}; Cluster 2 = {D2, D3}

**Why:**
1. Highest similarity is D4–D5 (0.9) → merge into {D4, D5}.
2. Next highest are the 0.85 pairs (D1–D6 and D2–D3). Merging either first yields the same final partition.
3. After those merges the clusters are {D1, D6}, {D2, D3}, {D4, D5}.
4. Strongest remaining single-link is 0.82 between {D1, D6} and {D4, D5} → merge them.

Final result is the two clusters above. (Single-link uses the maximum pairwise similarity between members of two clusters.)

## 4. Multi-label classification (documents can belong to multiple categories). Which statement is **not** true?

**Answer:** P(c3) = 2/3, R(c3) = 1

**Why:**
Per-category counts from the table:

| Category | TP | FP | FN | Precision | Recall | F1 |
|----------|----|----|----|-----------|--------|----|
| c1       | 3  | 0  | 0  | 1         | 1      | 1  |
| c2       | 2  | 1  | 0  | 2/3       | 1      | 4/5|
| c3       | 2  | 0  | 1  | 1         | 2/3    | 4/5|

- F(c2) = F(c3) = 4/5 is true.
- P(c1) = 1, R(c1) = 1 is true.
- P(c3) = 1 and R(c3) = 2/3, so the statement “P(c3) = 2/3, R(c3) = 1” is false.

(A correct prediction is y(+) or n(-).)

## 5. Micro-averaged precision and recall (pool all decisions)

**Answer:** P = 7/8, R = 7/8

**Why:**
Pool across the three categories:
- Total TP = 3 + 2 + 2 = 7
- Total FP = 0 + 1 + 0 = 1
- Total FN = 0 + 0 + 1 = 1

Micro-precision = TP / (TP + FP) = 7/8
Micro-recall = TP / (TP + FN) = 7/8
