# CS410 Study Sheet: everything to read before the test, in one place

Exam: multiple choice, similar to the weekly quizzes. Question types seen: multiple choice, check-all-that-apply, true/false, "which is NOT true". Ideas and traps matter more than formulas.

---

## A. Top 12 things to know cold

1. **Precision = TP/(TP+FP)** (÷ retrieved). **Recall = TP/(TP+FN)** (÷ all relevant in the collection). AP divides by **total relevant**. MAP is dominated by easy queries, gMAP by hard ones.
2. **nDCG is in [0,1]** and compares across queries; DCG doesn't. Pooling = don't judge every document.
3. **Unigram LM**: multiply independent word probabilities; probabilities sum to 1; order doesn't matter; log preserves ranking.
4. **Smoothing**: JM (λ) vs Dirichlet (μ). Parameter smaller → closer to the document's MLE; larger → closer to the collection LM. Doubling all counts: JM unchanged, Dirichlet changes.
5. **BM25** TF transform (k+1)x/(x+k): k=0 → bit vector, ceiling k+1. **b** controls length normalization (b=0 → none).
6. **Inverted index**: dictionary + postings (docID-sorted), d-gaps, gamma code, accumulators allocated per matched doc.
7. **PageRank**: iterative, matrix entries in [0,1], not symmetric, sparse, random jumps fix dead ends, normalization doesn't change ranking.
8. **Feedback**: relevance (explicit) vs pseudo (no human, least reliable) vs implicit (clicks). **Push vs pull**; content-based (item similarity) vs collaborative (user similarity).
9. **Mixture model**: document-level vs word-level mixing (0.085 vs 0.0625). **EM**: E-step posterior, M-step improves parameters, likelihood never decreases, local maximum.
10. **Paradigmatic** (substitutable, similar context) vs **syntagmatic** (co-occur). **PLSA → LDA** (Dirichlet priors).
11. **Naive Bayes** (generative; Laplace smoothing) vs **k-NN / LR / SVM** (discriminative). **Micro vs macro** averaging. **Accuracy's flaws.**
12. **Context models**: ITMTF (external time series, Granger), CPLSA (context views + coverage), NetPLSA (network smoothing, neighbors similar), LARA (aspect ratings/weights).

**Calculation types that recur:** precision/recall/AP at a cutoff · unigram query likelihood with/without JM smoothing · mixture probability · multi-label P/R/F, accuracy, micro-average · NB posterior with Laplace · k-NN vote with a similarity table · single-link merges.

---

## B. Quiz traps by topic

### Retrieval & VSM (Weeks 1–2)
- Bit-vector dot product counts *distinct* matched query terms, not occurrences.
- "Ranking is computationally easier than selection" is the **false** reason for preferring ranking. The real reasons: relevance is graded, users browse sequentially, the relevant/not-relevant boundary is hard to define.
- Bag of words **loses** word order and phrases. It **keeps** counts, length, and unique-word count.
- "Relies LESS on NLP": plagiarism comparison between submissions (surface string match).
- TR is harder than DB retrieval because of unstructured data, ambiguity **and** subjective relevance (all three).
- L2 distance depends on document length; cosine doesn't.
- Accumulators are per matched document, allocated lazily. A doc matching two terms still has one.
- Higher b = more length normalization; b=0 = none. k=0 = bit vector. Upper bound of the TF transform is k+1.
- IDF is high for rare terms and about 0 for terms in every doc. Stop words get low IDF.
- Push = system initiates (Netflix, Spotify recommendations, filtering). Pull = user initiates (search, browsing).
- Gamma code: drop the leading 1; the length in unary is the number of offset bits plus a terminating 0. (Low priority.)

### Evaluation (Week 3)
- AP uses **total relevant** as the denominator, not just retrieved. With exactly one relevant doc at rank r, AP = reciprocal rank = 1/r.
- Precision and recall are easy to swap. Precision ÷ retrieved. Recall ÷ all relevant.
- "Why is pooling useful?" → don't need to judge every doc (humans are still needed). New systems that weren't in the pool are evaluated unfairly.
- "DCG is better than nDCG because it's bounded in [0,1]" is **wrong**: nDCG is the bounded one. nDCG can compare across queries; DCG can't.
- "nDCG@k discounts only top-ranked docs" is **wrong**: every position is discounted.
- Cranfield "does not involve humans for relevance judgments" is **NOT true**.
- A PR curve above another at every recall level → better. The ideal PR curve is a horizontal line at precision 1.
- Higher MAP does **not** imply higher gMAP. Higher P@10 does **not** imply higher AP.
- P@10 is **not** always higher than P@20. Recall@k never decreases as k grows.
- If A has higher precision@k than B for every k, A also has higher recall@k.
- F1 = 0.75 with precision 0.5 is impossible (max F1 is 2/3). Larger β favors recall. A recall-critical task (finding attack plans) → higher β.

### Probabilistic / LM retrieval (Week 4)
- Unigram: product for a sequence, order irrelevant, probabilities sum to 1. The missing probability = 1 − the others. P("global warming") = P("warming global").
- **Multiply, never add**: P("the technology") = p(the) × p(technology). A sequence can't be more likely than any single word in it.
- Log doesn't change the ranking (strictly increasing). It only prevents underflow. The only issue is P=0 (hence smoothing).
- Smoothing = avoid zero probabilities for unseen words (not "remove stop words").
- Without smoothing, a **query** term missing from the **document** → likelihood becomes −∞ (log form).
- λ (JM) or μ (Dirichlet) **decreased** → toward the document's MLE. **Increased** → toward the collection model.
- JM: the same λ for every document. Dirichlet: longer docs are smoothed **less**. JM is better for long queries, Dirichlet for short ones.
- Doubling every count → JM p(w|d) is the same; Dirichlet's changes. Unsmoothed query likelihood is also the same.

### Feedback, web search, recommenders (Weeks 5–6)
- Relevance feedback = explicit judgments (most reliable). Implicit = clicks. Pseudo = no humans, top-k assumed relevant, **least reliable**.
- Rocchio: move the query toward the centroid of relevant docs, keep weight on the original query to avoid topic drift.
- GFS chunk = **64 MB**; master holds metadata, chunkservers hold the data.
- MapReduce: map emits key-value pairs; the system groups by key; **Reduce is called once per unique key**; it does allow parallel index construction.
- A crawler that only follows links can't find pages with no incoming links. Focused crawling ≠ incremental crawling (incremental targets frequently updated or accessed pages).
- PageRank: matrix entries ∈ [0,1], each row sums to 1, **not symmetric**, iterative, sparse, query-independent. Normalization doesn't affect ranking. A page with only in-links ranks high. A large matrix dimension is **not** a reason it's efficient. Random jumping doesn't favor pages with fewer in-links. PageRank is not only for link analysis; modern engines combine many features.
- Content-based = item similarity. Collaborative = user similarity. Pearson **and** cosine are user similarity measures.
- Recommenders are hard because of data sparseness and cold start ("high user expectations" is not a reason). Random recommendations don't help a new user.
- Beta-Gamma threshold learning: more training data → less exploration; the central idea is heuristically lowering the threshold.
- Search = pull, ad hoc, user takes initiative. DUS triangle = Data, Users, Services.

### Text mining & topic models (Weeks 7–8)
- **Paradigmatic** = substitutable, found by similar **context** (Monday/Tuesday, cat/dog). **Syntagmatic** = combine, found by high **co-occurrence** (car + drive).
- Mixture: choose the model once per document (0.085) vs per word (0.0625).
- EM: the M-step improves the parameters; E-step computes posteriors over the hidden variable. Likelihood **never decreases**; it reaches a **local** maximum; it converges.
- Larger background weight λ_B → common words get a smaller probability in the topic model.
- If one distribution gives the most frequent word a small probability, the other tends to give it a higher one.
- Reversing or shuffling word order leaves the likelihood unchanged.
- NLP order: POS tagging → syntactic → semantic → inference.
- PLSA parameters grow with the number of documents (overfitting). LDA = PLSA with Dirichlet priors.

### Categorization, clustering, opinions, context (Weeks 9–12)
- Naive Bayes = **generative**. k-NN, SVM, logistic regression = **discriminative**. k-NN does **not** estimate d+1 weights; LR does.
- Sentiment classification = text categorization. The input is an opinionated text; the **output is a label**, not an opinionated text object. Any categorization method works.
- Accuracy's disadvantages (all three): can't weight decisions differently, can't handle skewed data, and high accuracy ≠ good performance on imbalanced data. "Different results for different datasets" is not a special disadvantage.
- **Micro-average**: pool all decisions; large categories dominate. **Macro-average**: average per-category scores; every category counts equally, so a small bad category pulls it down.
- P = TP/(TP+FP), R = TP/(TP+FN). These are easy to swap in tables.
- K-means: user sets K, hard assignment, local optimum depends on initialization; assignment ≈ E-step, centroid update ≈ M-step. K-means is the closest to EM among NB / K-means / agglomerative.
- Agglomerative = bottom-up, needs a similarity measure; depth isn't guaranteed to be log₂N.
- Single-link: closest pair, chains, **most** outlier-sensitive. Complete-link: farthest pair. **Average-link: least outlier-sensitive.** (Your Week 9 `quizQuestions.md` says complete-link; that is wrong.)
- Clustering is unsupervised. Not for pictures. Removing spam using human-labeled examples = categorization, not clustering.
- Direct evaluation needs a gold-standard clustering. Indirect evaluation needs an application and is better for large collections.
- Opinion = holder + target + content + context + sentiment. "Tom thinks programming is difficult" → holder Tom.
- LARA recovers aspects, aspect ratings, and aspect weights. Applications: entity ranking, aspect-level summarization, reviewer-preference analysis.
- "Context does not influence both coverage and content" is the **false** statement. Non-text data can help text mining, and text can help interpret non-text patterns.
- **NetPLSA forces neighbors to have *similar* coverage** (not different). It uses both text and the network.
- Pick the method by the extra input:
  - External numeric time series (exchange rates, airline prices, stock) → **ITMTF** (with Granger test; Granger = lead/lag, not proof of causation).
  - Compare groups by location / author / time (US vs non-US, trending topics by country, event before/after) → **CPLSA**.
  - Network among authors or nodes → **NetPLSA**.
  - Reviews + ratings → aspect ratings and weights → **LARA**.
  - Text only → PLSA / LDA.

---

## C. Short definitions you asked for during the session

- **d-gap:** store differences between consecutive docIDs in a postings list (the first value is the docID itself). Decode with a running sum.
- **Gamma code:** a variable-length code for small integers: unary length part + binary offset part. Offset = binary of x with the leading 1 removed.
- **Reciprocal rank:** 1 ÷ the rank of the first relevant document.
- **AP:** at each rank where a relevant doc appears, take precision of the top-k up to that rank; sum; divide by total number of relevant docs.
- **Smoothing:** takes a little probability away from seen words and gives it to unseen words, using the collection model, so no word has probability 0.
- **Hidden variable:** something that affected how the data was produced but isn't recorded in it (e.g., which component generated each word).
- **Transition matrix (PageRank):** M_ij = probability the surfer goes from page i to page j.
- **Pooling:** judge only the union of the top-k results from a diverse set of systems; unjudged docs are assumed non-relevant.

---

## D. Skipped by choice

- Binary conversion and gamma encode/decode (one question at most).
- Formula memorization.
