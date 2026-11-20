# 05 · Text Mining, Word Association & Topic Models (Weeks 7–8)

[← 04 Feedback / Web / Recsys](04-Feedback-WebSearch-Recommenders.md) · [Overview](00-Overview.md) · Next: [06 Categorization, Clustering, Context](06-Categorization-Clustering-Context.md)

## 1. Text mining basics
- **Text mining ≈ text analytics**. Mining stresses the process; analytics stresses the result. Goal: turn text into actionable knowledge. **Text retrieval is a preprocessor** for mining.
- **Humans as sensors**: real world → observed by humans → expressed as text. **Mining reverses this**; how far back you go:
  1. the language itself · 2. the **content** · 3. the **observer** (opinions, sentiment) · 4. the **real world** (predictive analytics).
- Non-text data adds context: align text with external events, compare by time/location, build joint predictors. Small text can be high value.
- **Text representation spectrum** (shallow/robust → deep/fragile):
  character string → **sequence of words (BOW)** → + POS tags → + syntactic structure → + entities & relations → + logical predicates → + speech acts.
  - **The course focuses on the word-sequence level** (general, robust, easy, effective). Deeper = more analysis power but more error and more NLP.
- NLP steps (quiz item): **POS tagging → syntactic analysis (parsing) → semantic analysis → inference**.

## 2. Word association
| | **Paradigmatic** | **Syntagmatic** |
|---|---|---|
| Meaning | Words can **substitute** for each other (same class) | Words **combine / co-occur** in a context |
| Examples | cat ↔ dog, Monday ↔ Tuesday | cat + sit, car + drive |
| Detect by | **Similar context** (same words appear around both) | **High co-occurrence** (sequential relation) |

- **Paradigmatic method**: build a **pseudo document** for each word (its context: Left1, Right1, Window8 (±8 words)…), turn each into a bag-of-words **vector**, compare with a similarity function. Sim(cat,dog) = Σ over context views. Left1/Right1 → tight syntactic similarity; Window8 → broader topical similarity.
- **EOWC** (Expected Overlap of Words in Context): xᵢ = c(wᵢ,d₁)/|d₁|, yᵢ = c(wᵢ,d₂)/|d₂|, Sim = Σ xᵢyᵢ = P(a random word from each context is identical).
  - Flaw 1: **frequency dominance** → fix with **sublinear TF (BM25 transform)**.
  - Flaw 2: **stop words weighted equally** → fix with **IDF weighting**.
- Same weighted context vector, dual use: **compare two vectors → paradigmatic**; **look at high-weight terms inside one vector → syntagmatic**.
- Uses: query expansion/suggestions, topic maps, summarizing opinions, grammar learning (paradigmatic gives word classes; syntagmatic gives how classes combine).

## 3. Topic mining
- **Task**: input C={d₁…d_N} and **k**; output topics θ₁…θ_k and **coverage π_ij** = probability that document dᵢ covers topic θⱼ.
- **Topic = term** (pick top-k by TF-IDF): too coarse/ambiguous, brittle coverage, can't group related words.
- **Topic = word distribution** (a unigram LM) fixes it: multiple words, weights, and the same word (e.g., *star*) can sit in different topics with different probability.
- **Generative model**: each word is produced by (1) choose a topic by the document's mixture π_i, (2) draw the word from that topic's distribution. Parameters Λ = all θ and π. Likelihood p(data | Λ).

## 4. Single topic and the mixture model
- **One document, one topic**: maximize Π p(wᵢ|θ)^c(wᵢ,d) subject to Σp=1 → **MLE = normalized counts**. Problem: top words are *the, a, of*.
- **Two-component mixture (topic + background)**: for every word first choose component (λ_B for background, 1−λ_B for topic), then draw the word.
  **p(w) = λ_B·p(w|θ_B) + (1−λ_B)·p(w|θ_d)** (θ_B is **fixed**, estimated from a big collection).
  - Example: P("the") = 0.5·0.000001 + 0.5·0.03 = 0.0150005.
  - **Two ways to compute a document's probability**: (a) choose the model once per document, then *all* words from it → **0.5·(0.4·0.4) + 0.5·(0.1·0.1) = 0.085** for "data software"; (b) choose per word → **(0.5·0.4+0.5·0.1)² = 0.0625**. (θ₁: concert .1, music .1, data .4, software .4; θ₂: .4, .4, .1, .1.)
- **Why background words get factored out**: components **collaborate** (both explain the data) and **compete** (probabilities sum to 1).
  - The topic LM puts mass on words the background explains poorly (content words).
  - Three behaviors: (1) every component wants high probability on **frequent words**; (2) different components **specialize** on different words; (3) the **mixing weight** controls how strongly each responds.
  - **Larger λ_B → the topic distribution contains even fewer common words**; with λ_B=0 the topic would give high probability to "the". (Redundant components that give high mass to the same words are wasteful.)
  - If λ=0 and W is the most frequent word, the sum of its probabilities from the two distributions is **not** always 1 (both are separate distributions).
- Word order is irrelevant: reversing or shuffling words leaves the maximum likelihood unchanged.

## 5. EM algorithm
- Iterative **maximum-likelihood** estimation with **hidden (latent) variables** (here z = which component generated a word).
- **E-step**: with current parameters compute the posterior over hidden variables (soft assignment).
  p(z=topic | w) = (1−λ_B)p(w|θ_d) / [(1−λ_B)p(w|θ_d) + λ_B p(w|θ_B)]
- **M-step**: treat posteriors as **fractional counts**, re-normalize: p(w|θ_d) ∝ c(w,d)·p(z=topic|w). **The M-step is what improves the parameters** (increases the likelihood).
- Properties: likelihood **increases monotonically** (never decreases); **hill climbing → local maximum only**; depends on initialization (use random restarts); converges (**it does converge** even when both distributions are unknown). Each iteration processes all words.

## 6. PLSA and LDA
- **PLSA**: k topics, per-document coverage: p_d(w) = Σ_j π_{d,j} p(w|θ_j) (optionally + background). Hidden variable = which topic produced each word. EM again.
  - Parameters: **k|V| word probs + N·k coverages** → grows with the number of documents → **overfitting**, no principled way to give a new document a probability.
  - **MAP/prior version (user-controlled PLSA)**: add pseudo-counts μ·p(w|θ′) in the M-step.
- **LDA** = **PLSA with Dirichlet priors** on π_d (α) and topics θ_j (β). A true generative model; parameters don't grow with N; new documents get probabilities; inference is approximate (variational EM, Gibbs sampling). Topics for mining are comparable to PLSA.
- Both **require the user to set the number of topics**, both are iterative, results depend on initialization. (Same as K-means; see [06](06-Categorization-Clustering-Context.md).)

## Quiz traps
- Paradigmatic = substitutable (similar **context**); syntagmatic = co-occur.
- Mixture: **document-level** pick (0.085) vs **word-level** pick (0.0625).
- EM: M-step improves the parameters; likelihood **never decreases**; local maximum; converges.
- Missing unigram probability = 1 − others. P("global warming") = P("warming global").
- Larger λ_B → common words get *smaller* probability in the topic model.
- Adding many occurrences of W to the collection raises W's probability in the distributions; if one distribution gives the most frequent word a small probability, the other tends to give a higher one.
- NLP order: POS → syntactic → semantic → inference.
