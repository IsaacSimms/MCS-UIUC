# CS410: Week 11 — Discriminative classifiers, categorization evaluation, and sentiment classification

*CS410 Week 11 (Nov 2–8, 2026). Syllabus keywords: generative vs. discriminative classifier, training data, logistic regression, k-NN, classification accuracy, precision, recall, F measure, macro- and micro-averaging, opinion holder and target, opinion representation, sentiment classification, features, n-grams, frequent patterns, overfitting. The lectures are Zhai's 5.1–5.7 deck [Zhai 5.1–5.7].*

## Naive Bayes was already a linear classifier

The week opens with a reframing that the rest builds on. Take the two-category Naive Bayes score as a log ratio: log p(θ₁|d)/p(θ₂|d) splits into a category bias, log p(θ₁)/p(θ₂), which does not depend on d, plus a sum over the vocabulary of c(w,d) · log p(w|θ₁)/p(w|θ₂). If you call the word count the feature value xᵢ and the log ratio the weight βᵢ, you get score(d) = β₀ + Σ xᵢβᵢ. That is exactly the logistic regression form [Zhai 5.1, slide 3]. The two models share a functional form, so the real difference is how the weights are fit. NB fits them indirectly, by maximizing the joint likelihood of words and labels with per-category word distributions. Logistic regression models p(Y|X) directly and maximizes the *conditional* likelihood of the training labels, with no closed form, so it is solved iteratively (Zhai names Newton's method) [Zhai 5.1, slides 4–5]. Because LR never has to generate the words, its features do not have to be word counts at all. Anything you can compute about a document can go in.

Ng and Jordan make the tradeoff precise for this exact generative–discriminative pair. The discriminative model has lower asymptotic error. But NB can approach its own (higher) asymptotic error after about O(log n) training examples, where n is the number of features, while LR needs on the order of O(n). The result is two regimes: with little labeled data NB often wins, and with lots of data LR overtakes it [Ng & Jordan 2002, abstract and analysis]. "Discriminative is always better" is folk wisdom, not a theorem. That is the most useful sentence to carry into an exam question on this pair.

## k-NN: estimating p(Y|X) without fitting parameters

k-Nearest Neighbors finds the k training documents most similar to the test document and lets them vote. Zhai frames it as another way to estimate p(Y|X) directly. Assume the conditional probability is locally smooth, constant over a region R around d, and estimate p(θᵢ|R) = c(θᵢ, R)/|R|, the fraction of training documents in that region with label i [Zhai 5.1, slides 6–8]. Two consequences follow. k-NN is only as good as its similarity function, which is where all the vector-space machinery from Weeks 1–2 (TF-IDF weighting, cosine) comes back. And it has no training phase beyond preprocessing, which is why IIR calls it memory-based or instance-based learning [IIR §14.3].

The practical gotchas come from IIR. 1-NN is fragile because one mislabeled or atypical neighbor decides the label. An odd k makes ties less likely, k = 3 or 5 is common, and the principled choice is to tune k on held-out data. Weighting each neighbor's vote by its cosine similarity is usually more accurate than a plain vote [IIR §14.3]. The cost model is the reverse of most classifiers. Training is nearly free, but test time is linear in the size of the training set, though independent of the number of classes. Large label sets favor k-NN, and large training sets punish it [IIR §14.3.1, Table 14.3]. In code, the fix is the inverted index you built in Week 2: score the test document as a query against the training collection and take the top k.

Zhai's Part 2 adds the linear SVM, which picks the separator w·x + b = 0 that maximizes the margin. Only the support vectors determine it, and the soft-margin version trades margin against training errors through the parameter C [Zhai 5.2, slides 2–7]. His summary slide is the real takeaway: there is no clear winner among methods, and performance depends much more on feature quality than on which classifier you choose [Zhai 5.2, slide 8].

## Evaluation: why accuracy lies and which average to report

Accuracy is correct decisions over all decisions, across a k-categories × N-documents grid of yes/no calls. It has two problems. Errors have unequal costs: in spam filtering, losing a legitimate email is worse than letting a spam through. And it breaks on skewed test sets: if 98% of documents are in category 1, labeling everything as category 1 scores 98% [Zhai 5.3, slides 4–5]. So you fall back to precision, TP/(TP+FP), and recall, TP/(TP+FN), computed either per document ("does this document get all the categories it should?") or per category ("did this category reach all its documents?") [Zhai 5.3, slides 6–7].

F₁ = 2PR/(P+R) is the harmonic mean, and Zhai poses the question directly: why not 0.5P + 0.5R? A system that says "yes" to every category–document pair gets recall 1, so the arithmetic mean is at least 0.5 no matter how bad its precision is. The harmonic mean drops toward the smaller of the two numbers, so a degenerate system cannot score well [Zhai 5.3, slide 8].

With many categories you need one number, and here the quiz-style trap sits. **Macro-averaging** computes P, R, or F per category (or per document) and then averages them, so every category counts equally. **Micro-averaging** pools all decisions into one contingency table first and then computes P and R, so every decision counts equally [Zhai 5.4, slides 2–4]. IIR spells out the consequence. Under micro-averaging, large classes dominate. In its two-class example the micro-averaged precision (0.83) sits near the big class's 0.9 rather than the small class's 0.5. If you care about small classes, report macro [IIR §13.6]. On Reuters-21578, NB is only 9 points behind a linear SVM on micro-F₁ (80% vs. 89%) but 13 points behind on macro-F₁, because NB does badly on small classes with about ten training positives [IIR §13.6, Table 13.9]. One more fact worth memorizing: in one-of (single-label) classification, micro-averaged F₁ equals accuracy [IIR §13.6]. Finally, when results go to a person for editing or triage (routing email, reviewing likely spam), score-and-rank evaluation from Week 3 is often more appropriate than hard labels [Zhai 5.4, slide 5].

## Opinions as structured objects

Opinion mining treats an opinion as a record, not just a polarity. The basic fields are the *holder* (whose opinion it is), the *target* (what it is about), and the *content* (the text). The enriched fields are the *context* (time, location, discourse) and the *sentiment* (what it says about the holder's feelings) [Zhai 5.5, slide 5]. A product review is easy because the holder and target are explicit. A news sentence with an implicit holder and target needs deeper NLP. Zhai also separates the author's own opinion ("I don't like this phone"), a reported opinion ("I believe he loves that painting"), and an inferred opinion ("This phone ran out of battery in just 1 hour"), which contains no opinion word at all [Zhai 5.5, slides 6–9]. Sentiment classification is the simplest case: everything but the sentiment is known, and the sentiment is a label. That makes it ordinary text categorization, so any method above applies, and the gains come from features and from respecting the order of labels [Zhai 5.6, slides 2–3].

## Features carry sentiment classification

Zhai lists the usual feature families with their tradeoffs [Zhai 5.6, slides 4–7]:

- Character n-grams are robust to spelling errors but less discriminative.
- Word unigrams are strong for topic classification but weak for sentiment, because "it's not good" contains "good". Long n-grams are discriminative but overfit.
- POS n-grams such as "ADJECTIVE NOUN" or "great NOUN" mix words and tags.
- Word classes, frequent patterns, and parse-tree fragments are more specific still, and riskier.

The design goal is to balance exhaustivity (frequent, high-coverage features) against specificity (rare, discriminative features). Richer NLP features enlarge the space and make overfitting more likely.

Pang, Lee, and Vaithyanathan's "Thumbs up?" is the classic empirical check. On 700 positive and 700 negative movie reviews, with three-fold cross-validation, standard learners clearly beat human-written keyword lists. They still did worse than in topic classification, where 90%+ is common, because sentiment is often expressed without a single obviously negative word ("How could anyone sit through this movie?") [Pang et al. 2002, §1, §5]. Two results are good programming tips. Binary feature *presence* beat raw *frequency*: NB rose from 78.7% to 81.0% and SVM from 72.8% to 82.9%. And adding bigrams to unigrams did not help. Their negation handling is simple enough to copy: append a NOT_ tag to every token between a negation word ("not", "isn't", "didn't") and the next punctuation mark [Pang et al. 2002, §6, Figure 3].

## Ordinal logistic regression for star ratings

Ratings from 1 to k are ordered, and the features that separate 2 stars from 1 are largely the same ones that separate k from k−1. The naive approach trains k−1 independent binary LRs, each predicting "rating ≥ j", which takes (k−1)(M+1) parameters and ignores that the problems depend on each other. Ordinal LR shares one weight vector β across all thresholds and keeps only a separate intercept αⱼ per level, for M + k − 1 parameters, and all levels share the training data [Zhai 5.7, slides 2–7]. Prediction becomes a single linear score(X) = Σ βᵢxᵢ cut into bands. p(r ≥ j | X) > 0.5 exactly when score(X) > −αⱼ, so r = j when score(X) falls in [−αⱼ, −αⱼ₊₁) [Zhai 5.7, slide 8]. Implementation tip: compute the score once and binary-search the thresholds. Don't run k−1 separate classifiers.

## Sources

- [Zhai 5.1–5.7] C. Zhai, *Text Mining and Analytics* lecture slides: Discriminative Classifiers Parts 1–2, Evaluation Parts 1–2, Opinion Mining Motivation, Sentiment Classification, Ordinal Logistic Regression. Course mirror, https://github.com/rikenshah/text-mining-course/blob/master/Week5/merged5.pdf
- [IIR] C. Manning, P. Raghavan, H. Schütze, *Introduction to Information Retrieval*, Cambridge UP, 2008. Ch. 13 (§13.6) and Ch. 14 (§14.3), online-edition PDFs via the Internet Archive copy of https://nlp.stanford.edu/IR-book/pdf/13bayes.pdf and 14vcat.pdf (the Stanford server was down at write time). Zhai's slides assign IIR Ch. 13–15.
- [Ng & Jordan 2002] A. Ng, M. Jordan, "On Discriminative vs. Generative Classifiers: A comparison of logistic regression and naive Bayes," NIPS 14. https://proceedings.neurips.cc/paper_files/paper/2001/file/7b7a53e239400a13bd6be6c91c4f6c4e-Paper.pdf
- [Pang et al. 2002] B. Pang, L. Lee, S. Vaithyanathan, "Thumbs up? Sentiment Classification using Machine Learning Techniques," EMNLP 2002. https://aclanthology.org/W02-1011.pdf
- Zhai & Massung, *Text Data Management and Analysis* (ACM Books), https://dl.acm.org/doi/pdf/10.1145/2915031. Returned 403 at write time and was not used.

## For the podcast

**Audience.** UIUC MCS students already in CS410 who just finished Naive Bayes and clustering for the exam. Don't re-teach Bayes' rule, TF-IDF, or cosine similarity.

**Emphasize vs. skip.** Spend the most time on three things: the NB-to-logistic-regression rewrite (same linear form, different training objective) together with the Ng–Jordan two-regime result; macro vs. micro averaging and when each one misleads; and ordinal LR's parameter sharing. Treat SVM in one breath, since it's in the lectures but not the syllabus keywords. Skip LR's Newton-method derivation.

**Say clearly.** ChengXiang "Cheng" Zhai; Andrew Ng and Michael Jordan (the Berkeley statistician, not the athlete); Bo Pang and Lillian Lee; "Thumbs up?"; Reuters-21578; macro-averaging vs. micro-averaging; opinion holder vs. opinion target.

**Formulas out loud.**
- Logistic regression: "the log-odds of the positive class equals a bias plus a weighted sum of the features."
- F1: "twice precision times recall, over precision plus recall, the harmonic mean, which gets dragged toward the weaker of the two."
- k-NN: "the probability of a label is just the fraction of your k neighbors that carry it."
- Ordinal LR: "one shared score, sliced into bands by k minus one thresholds."

**Common misconceptions.**
- Discriminative models are not always better, because with little data NB can win.
- Micro-averaging doesn't "treat categories fairly". It weights decisions, so big categories dominate.
- k-NN is not cheap at prediction time: it is slow because it compares the test document against the whole training set.
- Sentiment classification isn't a different algorithm. It's text categorization with harder features.
- Ordinal regression isn't just k−1 independent classifiers. The point is that they share weights.
