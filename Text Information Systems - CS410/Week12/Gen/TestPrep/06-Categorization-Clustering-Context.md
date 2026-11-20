# 06 · Categorization, Clustering, Opinions & Contextual Text Mining (Weeks 9–12)

[← 05 Text Mining](05-Text-Mining-Topic-Models.md) · [Overview](00-Overview.md) · [Quiz Bank](QuizBank.md)

## 1. Text categorization (supervised)
- Given **predefined categories** + **labeled training examples**, assign new objects to categories. Clustering asks "what groups exist?"; categorization asks "which known group?".
- **Internal** categories come from content (topic, sentiment); **external** from metadata (author).
- Variants: **binary**, **multi-class** (k mutually exclusive), **hierarchical**, **multi-label / joint**.
- **Manual rules**: fine with clear surface cues and domain knowledge; expensive, don't scale, can't handle uncertainty. **ML**: needs training data (quality = system quality) + features; learns **soft rules**.
- **Sentiment classification = text categorization.** Input = an opinionated text object, **output = a sentiment label** (not an opinionated text object). Any categorization method works; features matter most.
- **Features** that help: domain knowledge, error analysis, ML-based selection (all of the above). Word unigrams are weak for sentiment ("not good"); n-grams/POS patterns help but risk **overfitting**; balance exhaustivity vs specificity.

### Generative vs discriminative
| | **Generative** | **Discriminative** |
|---|---|---|
| Models | P(x\|y) and P(y), then Bayes rule | P(y\|x) or the boundary directly |
| Examples | **Naive Bayes** | **Logistic regression, k-NN, SVM** |
| Objective | Likelihood (indirect) | Separation / conditional likelihood |

- **Naive Bayes** (multinomial = unigram LM per category): category = argmax_i [ log p(θᵢ) + Σ_w c(w,d)·log p(w|θᵢ) ]. Training = **counting**: p(θᵢ) = Nᵢ/N (MLE prior, e.g., 1 spam of 3 docs → **1/3**), p(w|θᵢ) = share of tokens in category i.
  - **Needs smoothing**: an unseen word gives p(w|θᵢ)=0 → P(d|θᵢ)=0. **Laplace (add-one)**: (c+1)/(total + |V|).
  - Worked (equal priors): P(d3|θ₁) ∝ (3/10)(1/10)=3/100, P(d3|θ₂) ∝ (2/10)(2/10)=4/100 → **P(θ₁|d3) = 3/7 < ½ → Category 2**. Without smoothing the unseen word gives P(d3|θ₁) = 0.
  - A doc whose words occur **only** in the spam docs scores highest as spam ("No fees").
  - Naive Bayes is a **linear** scorer in the word counts (same form as logistic regression); "naive" = conditional independence of words.
- **Logistic regression** learns **d+1 weights** (d features + bias). **k-NN** is instance-based: **no weights estimated**, no training phase, only as good as its similarity function.
  - **Worked k-NN**: D6's similarities to D1–D5 = .85 (label 1), .7 (0), .6, .1, .3 → **k=1 → label of D1 = 1**; **k=2** → neighbors D1 (1) and D2 (0) → **tie**, so odd k is preferred.
- **SVM**: linear separator maximizing the margin (support vectors); soft margin parameter C. No clear winner among classifiers; **feature quality matters more** than classifier choice. NB is better with little data, LR with lots.

### Evaluation of classifiers
- Per category/decision: **TP, FP, FN, TN**. **Accuracy = (TP+TN)/all decisions.** **Precision = TP/(TP+FP)**, **Recall = TP/(TP+FN)**, **F₁ = 2PR/(P+R)** (harmonic mean: can't be gamed by "say yes to everything").
- **Accuracy's disadvantages** (pick all three): can't weight decisions differently; can't handle **skewed data**; with **imbalance, high accuracy ≠ good performance**. ("Different datasets give different results" is *not* a special disadvantage.)
- **Macro-average**: compute metric per category, then average → each **category** counts equally; small classes matter. **Micro-average**: pool all decisions, compute once → each **decision** counts equally; large classes dominate. In single-label classification micro-F₁ = accuracy.
- **Worked table (c1, c2; 5 docs; correct = y(+) or n(−))**: c1: TP=2, FP=1, FN=0 → P=2/3, R=1; c2: TP=2, FP=2, FN=1 → P=1/2, R=2/3; accuracy = **6/10**; micro-recall = pooled 4/(4+1) = **4/5**.
- **Worked table (c1,c2,c3)**: c1 TP3 FP0 FN0; c2 TP2 FP1 FN0 (P=2/3, R=1, F=4/5); c3 TP2 FP0 FN1 (P=1, R=2/3, F=4/5). Micro: TP=7, FP=1, FN=1 → **P=R=7/8**.

## 2. Text clustering (unsupervised)
- Group similar objects (docs, terms, passages, sites). **Not** for images. **Not** removing spam from human-labeled examples (that's categorization).
- **Clustering bias**: "similar" is only defined once the user picks a perspective. Motivations: overview of a collection, near-duplicate linking, structure/browsing.
- **Model-based** (mixture of unigram LMs, PLSA-style, EM): disadvantage = **hard to swap in a different similarity measure**.
  - **One topic per document**: p(d) = Σ_i p(θᵢ) Π_w p(w|θᵢ)^c(w,d). **Sum outside the product**, p(θᵢ) is **global** (not per-doc). In PLSA each *word* picks a topic (product outside, per-doc coverage π_{d,j}).
  - Naive Bayes = the same model with the label observed (count) vs hidden (EM).
- **Similarity-based**:
  - **Agglomerative (bottom-up)** hierarchical: start with singletons, merge the closest pair; **needs a similarity measure**; hierarchy not guaranteed to be log₂N deep. **Divisive** = top-down.
  - **Single-link** = closest pair (max similarity) → chaining, **most sensitive to outliers**. **Complete-link** = farthest pair → tight clusters. **Average-link** = mean of all pairs → compromise and **least sensitive to outliers** (lecture + Week 10 quiz).
  - ⚠ Your Week 9 `quizQuestions.md` answers "Complete-link"; the lecture/Week 10 notes say **Average-link**. Trust average-link.
  - **Single-link worked** (D4–D5 .9; D1–D6 .85; D2–D3 .85; then .82 between {D1,D6},{D4,D5}) → **{D1,D4,D5,D6}, {D2,D3}**.
  - **K-means**: choose K, seed centroids, repeat (assign each doc to nearest centroid = E-step; recompute centroids = M-step). Hard-assignment EM → **local optimum**, depends on initialization, **K specified by the user**. K-means and PLSA are alike: both iterative, both need user-set K/Z, both initialization-dependent. Of NB, K-means, agglomerative → **K-means is closest to EM**.
- **Evaluation**: **Direct** = compare to a human-annotated **gold-standard clustering** (purity, NMI). **Indirect** = plug the clusters into an application and measure with vs without clustering (needs a user-specified application); **better for large collections** (annotating everything is impractical). Neither is inherently better.

## 3. Opinion mining
- Opinion = **holder** (who) + **target** (about what) + **content** + **context** (time/location) + **sentiment**. "Tom thinks programming is difficult" → holder **Tom**, target programming.
- Types: author's own, reported, inferred ("ran out of battery in 1 hour" has no opinion word).
- **Ordinal logistic regression** for star ratings: one shared weight vector, separate intercept per threshold.
- **LARA (Latent Aspect Rating Analysis)**: from review text + overall rating, recover **latent aspects, aspect-level ratings, and aspect weights** (an overall rating is decomposed into aspect scores). Applications (all): opinion-based **entity ranking**, **aspect-level opinion summarization**, **reviewer-preference** analysis.

## 4. Text-based prediction & contextual text mining (Week 12)
- **Text-based prediction**: use text (plus non-text) to infer a real-world variable. Text = data from **human sensors**; the **data mining loop**: sensors → joint text/non-text mining → predictors → predictions → decisions → world.
- **Two-way**: **non-text helps text mining** (context) **and text helps interpret non-text patterns** (pattern annotation). Both true: "non-text data can help text mining" ✔.
- **Context** (time, location, author, source, network, series) **partitions** the collection for comparison and **gives meaning to topics**. Context influences **both coverage and content** of topics.
- **CPLSA** (contextual PLSA) = **extension of PLSA** with context: **view** = context-specific word distributions of themes (**content variation**); **coverage** = context-specific theme distribution (**coverage variation**). Applications: temporal themes (life cycles), spatiotemporal analysis (Katrina), event impact (before/after splits), **comparing groups via metadata** (US vs non-US researchers on deep learning; trending topics by country).
- **NetPLSA** = PLSA + **network regularizer** (graph harmonic / squared difference of topic coverage across edges). Uses **both text and network**; forces **neighbors to have similar** (smooth) topic coverage, **not different**. λ=0 → plain PLSA; λ=1 → graph-only. Any graph (coauthor, geography).
- **Causal topic mining (ITMTF – iterative topic modeling with time-series feedback)**: input = **text + an external time series** (extra input is **time**); find topics whose coverage correlates (with lag) with the series. Loop: fit topics → test correlation / **Granger** causality → find impacting words (sign) → build prior (split positive vs negative) → refit → repeat. **Granger** = lead/lag predictiveness, not proof of causation.
- **Which technique?** External numeric series (exchange rates, airline prices vs Twitter, stock) → **ITMTF**. Compare topics across location/author groups, trending topics by country → **CPLSA**. Network among authors/nodes → **NetPLSA**. Aspect ratings from reviews → **LARA**.

## Quiz traps
- Naive Bayes = generative; k-NN, SVM, LR = discriminative. k-NN does **not** estimate d+1 weights; LR does.
- "Output of sentiment classification is an opinionated text object" is **false**.
- NetPLSA forces neighbors to have **different** coverage → **False**.
- "Context does **not** influence both coverage and content" is the false statement.
- Direct eval needs a gold-standard clustering; indirect eval needs an application.
- Agglomerative needs a similarity measure and is bottom-up. Not for pictures. Spam from labeled examples = categorization, not clustering motivation.
- Maximum likelihood is unchanged when a document's words are **reversed** (counts same), changed when tokens are doubled or word identities swapped.
- P and R are easy to swap in tables: P = TP/(TP+FP), R = TP/(TP+FN).
