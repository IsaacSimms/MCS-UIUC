# CS410 Exam Prep · Overview

**Exam**: 1 hour, questions "similar to the weekly quizzes." This set is built quiz-first: each file ends with a **Quiz traps** list drawn from your quizzes and practice quizzes (screenshots + notes).

## Files
| # | File | Weeks | Quiz weight |
|---|---|---|---|
| 01 | [Retrieval & VSM](01-Retrieval-and-VSM.md) | 1–2 | Medium (bit vector, dot product, TF/IDF, BM25, inverted index, gamma code) |
| 02 | [Evaluation](02-Evaluation.md) | 3 | **High** (20 quiz Qs: P/R/AP/MAP/gMAP/F/nDCG, pooling, Cranfield) |
| 03 | [Probabilistic / LM Retrieval](03-Probabilistic-LM-Retrieval.md) | 4 | **High** (unigram math, smoothing JM vs Dirichlet) |
| 04 | [Feedback, Web Search, Recommenders](04-Feedback-WebSearch-Recommenders.md) | 5–6 | **High** (PageRank, crawling, GFS/MapReduce, feedback types, CF vs content) |
| 05 | [Text Mining & Topic Models](05-Text-Mining-Topic-Models.md) | 7–8 | Medium-High (paradigmatic/syntagmatic, mixture calc, EM) |
| 06 | [Categorization, Clustering, Opinions, Context](06-Categorization-Clustering-Context.md) | 9–12 | **High** (NB/k-NN math, micro/macro, linkage, CPLSA/NetPLSA/ITMTF) |
| — | [Quiz Bank](QuizBank.md) | all | Q&A material for the quizzing agent |

## Top 12 things to know cold
1. **Precision = TP/(TP+FP)**, **recall = TP/(TP+FN)**. AP divides by **total relevant**. MAP is dominated by easy queries, gMAP by hard ones.
2. **nDCG ∈ [0,1]** and compares across queries; DCG doesn't. Pooling = don't judge every document.
3. **Unigram LM**: multiply independent word probabilities; probabilities sum to 1; order doesn't matter; log preserves ranking.
4. **Smoothing**: JM (λ) vs Dirichlet (μ). Parameter ↓ → closer to doc MLE; ↑ → closer to collection LM. Doubling counts: JM unchanged, Dirichlet changes.
5. **BM25** TF transform (k+1)x/(x+k): k=0 → bit vector, ceiling k+1. **b** controls length normalization (b=0 none).
6. **Inverted index**: dictionary + postings (docID-sorted), d-gaps, **gamma code** encode/decode, accumulators allocated per matched doc.
7. **PageRank**: iterative, matrix entries in [0,1], not symmetric, sparse, random jumps fix dead ends, normalization doesn't change ranking.
8. **Feedback**: relevance (explicit) vs pseudo (no human, least reliable) vs implicit (clicks). **Push vs pull**; content-based (item similarity) vs collaborative (user similarity).
9. **Mixture model**: document-level vs word-level mixing calc (0.085 vs 0.0625); **EM** E-step posterior, M-step improves parameters, monotone, local max.
10. **Paradigmatic** (substitutable, similar context) vs **syntagmatic** (co-occur). **PLSA→LDA** (Dirichlet priors).
11. **Naive Bayes** (generative; Laplace smoothing; compute posterior by hand) vs **k-NN / LR / SVM** (discriminative). **Micro vs macro** averaging. **Accuracy's flaws.**
12. **Context models**: ITMTF (external time series, Granger), CPLSA (context views+coverage), NetPLSA (network smoothing, neighbors similar), LARA (aspect ratings/weights).

## Calculation types to practice (they recur)
Precision/recall/AP at a cutoff · unigram query likelihood with/without JM smoothing · mixture probability · gamma encode/decode and d-gaps · multi-label P/R/F, accuracy, micro-average · NB posterior with Laplace · k-NN vote with a similarity table · single-link merges.

## Inconsistencies found in your notes (resolved in these docs)
- **Week 3 `QuizNotes.md`** has precision and recall **swapped**. Correct: precision divides by *retrieved*, recall by *relevant*.
- **Week 2 `Terminology.md`** writes IDF as log(N/df); the lecture uses **log((M+1)/df)**. Both fine for ranking.
- **Week 9 `quizQuestions.md`** says complete-link is least outlier-sensitive; lecture and Week 10 notes say **average-link**.
- **Week 3 Lec 2 notes** say recall divides by "the total number of docs in the collection." Correct: all **relevant** docs in the collection.
- Week 4 practice Q4 (S₁ vs log S₂ same ranking): the quiz's answer is **True**; your note about P=0 is the caveat that motivates smoothing.
- Screenshot caveat: for ungraded screenshots (W1, W3, W4 quiz, W6 quiz, W8) I treated your selected answers as correct, and re-derived every computation. Non-computed items from those are marked in the Quiz Bank only where I could not verify independently.
