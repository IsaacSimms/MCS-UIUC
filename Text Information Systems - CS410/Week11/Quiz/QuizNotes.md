# Quiz notes

## 1. The precision and recall of c1 and c2 are:

**Context.** Multi-label classification evaluates each category independently with the usual TP/FP/FN counts.

**Correct answer.** P(c1)=2/3 R(c1)=1 P(c2)=1/2 R(c2)=2/3

**Why.** For c1, TP=2, FP=1, FN=0 gives P=2/3 and R=1. For c2, TP=2, FP=2, FN=1 gives P=1/2 and R=2/3.

---

## 2. Given the same data as in Question 1, the classification accuracy of the classifier is:

**Context.** Accuracy counts every (document, category) decision. A prediction is correct only when it is y(+) or n(−).

**Correct answer.** 6/10

**Why.** Four correct cells in the c1 column plus two correct cells in the c2 column, out of ten total decisions.

---

## 3. Given the same data as in Question 1, what is the recall of the classifier using micro-averaging (i.e., by pooling all decisions together)?

**Context.** Micro-averaging pools TP and FN counts across all categories before computing the single ratio of true yeses over actual yeses.

**Correct answer.** 4/5

**Why.** Total TP across both categories is 4 and total FN is 1, so micro-recall = 4/(4+1) = 4/5.

---

## 4. Which of the following is not a Discriminatave classifier?

**Context.** Discriminative classifiers model P(y|x) or the decision boundary directly. Generative classifiers model P(x|y) and P(y).

**Correct answer.** Naive-Bayes

**Why.** Naive-Bayes is generative. K-Nearest Neighbors, Support Vector Machine, and Logistic Regression are all discriminative.

---

## 5. When Designing features for text categorization, which of these are useful?

**Context.** Feature design for text categorization mixes domain knowledge, error analysis, and machine-learning methods.

**Correct answer.** All of the above

**Why.** Domain knowledge supplies relevant terms and patterns. Error analysis reveals missing or weak features. Machine-learning techniques can select or construct features from data.

---

## 6. Which of the following is false?

**Context.** Sentiment classification is text categorization whose input is an opinionated text object and whose output is a sentiment label.

**Correct answer.** The output for sentiment classification is an opinionated text object

**Why.** The output is a sentiment class or polarity, not another opinionated text object. The input is an opinionated text object, and any text categorization method can be used for the task.

---

## 7. What is a disadvantage of using classification accuracy as an assessment of classifiers? Check all that apply:

**Context.** Accuracy is the fraction of correct decisions. It treats every decision equally and can be high on skewed data while missing the minority class.

**Correct answers.**
- For imbalanced dataset, high accuracy does not imply good performance.
- Classification accuracy cannot assign different weights to different decisions
- Classification accuracy cannot deal with skewed data properly

**Why.** These three capture the distinctive problems with accuracy on imbalanced data and equal error weighting. The statement that accuracy gives different results for different datasets is true of essentially every metric and is not a special disadvantage.

---

## 8. What is the opinion holder in the following sentence? "Tom thinks programming is difficult."

**Context.** In opinion mining the opinion holder is the entity that expresses the opinion.

**Correct answer.** Tom

**Why.** The sentence attributes the view to Tom. Difficulty is a property of the target and programming is the target itself.