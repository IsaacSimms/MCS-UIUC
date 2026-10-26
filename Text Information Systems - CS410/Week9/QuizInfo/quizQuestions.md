# Week 9 Practice Quiz (Set 2) Answers

## 1. What is NOT a motivation for text clustering?

**Answer:** To remove spam documents based on a small collection of human annotated spam documents

**Why:** This is a supervised classification task that relies on labeled examples. The other options are standard motivations for unsupervised clustering: linking/near-duplicate removal, creating structure over text, and obtaining a high-level overview of a large collection.

## 2. For the agglomerative clustering algorithm, which of the following is TRUE?

**Answer:** It requires the specification of a similarity measurement.

**Why:** Agglomerative clustering is bottom-up (repeatedly merges closest clusters). It is not top-down (that is divisive clustering). The depth of the resulting hierarchy is not guaranteed to be exactly \(\log_2 N\) because the tree need not be balanced.

## 3. Which variation of the hierarchical text clustering algorithm is least sensitive to outliers?

**Answer:** Complete-link

**Why:** Complete-link requires every member of one cluster to be close to every member of the other before merging, so outliers rarely force incorrect merges. Single-link is most sensitive (chaining effect). Average-link is intermediate.

## 4. Precision and recall of c1 and c2

**Answer:** \(P(c1) = 2/3\), \(R(c1) = 1\), \(P(c2) = 1/2\), \(R(c2) = 2/3\)

**Why:**
- c1: TP = 2, FP = 1, FN = 0 → P = 2/3, R = 1
- c2: TP = 2, FP = 2, FN = 1 → P = 1/2, R = 2/3

(A correct prediction is y(+) or n(-).)

## 5. Classification accuracy of the classifier

**Answer:** 6/10

**Why:** 5 documents × 2 categories = 10 decisions. Exactly 6 of them are correct (y(+) or n(-)).

## 6. Micro-averaged recall

**Answer:** 4/5

**Why:** Pooled across categories: TP = 4, FN = 1.
Micro-recall = TP / (TP + FN) = 4/5.
(Uses the same table as Question 4.)

## 7. Disadvantage of using classification accuracy (check all that apply)

**Answer:**
- Classification accuracy cannot assign different weights to different decisions
- Classification accuracy cannot deal with skewed data properly
- For imbalanced dataset, high accuracy does not imply good performance

**Why:** Accuracy treats all errors equally and is dominated by the majority class on skewed data, so high accuracy can still reflect poor minority-class performance. “Gives different results for different datasets” is not a distinctive disadvantage.

## 8. Which is NOT true about Contextual Text Mining?

**Answer:** Context does not influence both coverage and content variation of topics

**Why:** This statement is false. Context (time, location, authors, etc.) does influence both coverage and content variation of topics. The other two statements are true: context is commonly used, and it can partition text and give meaning to topics.
