# Quiz notes

## 1. Sentiment classification can be treated as a text categorization problem.

**Context.** This tests the standard framing of text classification / categorization in IR and NLP. Sentiment classification assigns each text to one of a fixed set of labels.

**Correct answer.** True

**Why.** Sentiment classification assigns each text to one of a fixed set of labels (e.g., positive / negative / neutral). That is exactly the definition of a text categorization problem: documents are mapped into predefined classes.

---

## 2. Which of the following is not true?

**Context.** Per-category evaluation of a multi-label text classifier (documents may belong to multiple categories). Each category is treated as an independent binary problem. Precision P(ci) = TP / (TP + FP), recall R(ci) = TP / (TP + FN), and F1 = 2 · P · R / (P + R).

**Correct answer.** P(c3) = 2/3  R(c3) = 1

**Why.** From the table for c3: TP = 2, FP = 0, FN = 1, so P(c3) = 1 and R(c3) = 2/3. The stated values are swapped. The other two claims match the table: P(c1) = R(c1) = 1 and F(c2) = F(c3) = 4/5.

---

## 3. Given the same data as in Question 2, what are the precision and recall values of the classifier using micro-averaging (i.e., by pooling all decisions together)?

**Context.** Micro-averaged precision and recall for multi-label text classification: pool every TP, FP, and FN across all categories, then compute a single P and R on the pooled counts.

**Correct answer.** P = 7/8  R = 7/8

**Why.** Across the three categories the pooled counts are TP = 7, FP = 1, FN = 1. P = 7 / (7 + 1) = 7/8 and R = 7 / (7 + 1) = 7/8.

---

## 4. Which of the following is not true?

**Context.** Generative classifiers model how the data is created (Naïve Bayes models P(x|y) and P(y)). Discriminative classifiers model the boundary or posterior directly. Logistic regression learns a weight vector of length d+1. K-NN is non-parametric and instance-based; it does not estimate a weight vector.

**Correct answer.** K-NN tries to estimate d+1 weights associated with d features.

**Why.** K-NN does not estimate a weight vector of any kind. Naïve Bayes is generative while K-NN is discriminative, and logistic regression does estimate d+1 weights.

---

## 5. Using maximum likelihood estimation without smoothing, what is P(Spam)?

**Context.** Class prior under maximum-likelihood estimation (no smoothing) for Naïve Bayes. The MLE prior is the relative frequency of the class in the training documents.

**Correct answer.** 1/3

**Why.** Three training documents, exactly one labeled Spam. The MLE prior is the relative frequency: P(Spam) = 1/3.

---

## 6. Which of the following documents has the highest probability of being classified as spam by the Naive Bayes classifier?

**Context.** Naïve Bayes classification score (with additive smoothing) on the training set from the prior question. The posterior favors spam when the document’s words are more characteristic of the spam class than the ham class.

**Correct answer.** “No fees”

**Why.** “No” and “fees” appear only in the single spam document and nowhere in ham. The other three documents each contain at least one word that appears only in the ham documents. Under the smoothed likelihoods those pure-spam words raise the spam score more than any mixture of spam + ham words.

---

## 7. Given a new document d3=(w3,w4), what will P(d3|θ1) be?

**Context.** Multinomial Naïve Bayes likelihood under maximum-likelihood estimation (no smoothing). The probability of a document given a category is the product of the per-word probabilities estimated from that category.

**Correct answer.** 0

**Why.** Document d3 contains the word w4. Under MLE for category T1, c(w4, T1) = 0, so P(w4|θ1) = 0. The product for the whole document is therefore zero: P(d3|θ1) = P(w3|θ1) · P(w4|θ1) = (2/5) · 0 = 0.

---

## 8. Suppose that we now use Laplace smoothing, what is P(θ1|d3)?

**Context.** Posterior probability P(θ1|d3) under multinomial Naïve Bayes with Laplace (add-one) smoothing. When the two class priors are equal, P(θi|d) is simply the relative magnitude of the smoothed likelihoods P(d|θi).

**Correct answer.** 3/7

**Why.** The smoothed probabilities yield P(d3|θ1) ∝ (3/10) · (1/10) and P(d3|θ2) ∝ (2/10) · (2/10). Normalizing gives P(θ1|d3) = (3/100) / (3/100 + 4/100) = 3/7.

---

## 9. Which category would Naive Bayes predict for d3 if we use Laplace smoothing?

**Context.** Naïve Bayes prediction under Laplace smoothing for the same d3 / θ1 / θ2 setup. The classifier assigns the category with the higher posterior.

**Correct answer.** Category 2

**Why.** From the previous calculation P(θ1|d3) = 3/7 < 0.5, so P(θ2|d3) > 1/2. Category 2 therefore has the higher posterior and is the prediction.

---

## 10. If k=1, then the prediction of the classifier for D6 is:

**Context.** 1-nearest-neighbor classification using a pre-computed similarity matrix. The predicted label is simply the label of the single training document with the highest similarity to the test document.

**Correct answer.** 1

**Why.** Similarities of D6 to the training set {D1–D5} are D1: 0.85, D2: 0.7, D3: 0.6, D4: 0.1, D5: 0.3. The maximum is 0.85 (D1). D1’s label is 1, so the 1-NN prediction is 1.

---

## 11. If k = 2, then the prediction would be:

**Context.** 2-nearest-neighbor classification on the same similarity matrix. With an even k, a split vote produces a tie.

**Correct answer.** There is a tie and thus 0 or 1.

**Why.** The two highest similarities to D6 are D1 (0.85, label 1) and D2 (0.7, label 0). One neighbor votes 1 and one votes 0, so the vote is tied.