# 03 · Probabilistic Retrieval & Language Models (Week 4)

[← 02 Evaluation](02-Evaluation.md) · [Overview](00-Overview.md) · Next: [04 Feedback, Web Search, Recommenders](04-Feedback-WebSearch-Recommenders.md)

## 1. Probabilistic retrieval
- Model f(d,q) = **p(R=1 | d,q)**, R∈{0,1}. Queries and docs are *observations of random variables* (in VSM they are vectors).
- **Query likelihood** approximates p(R=1|d,q) by **p(q | d, R=1)**: "if the user likes d, how likely is this query?"
- BM25 is probabilistic in origin. **PL2** is a divergence-from-randomness model.

## 2. Statistical / unigram language models
- A language model = a probability distribution over word sequences (context dependent). p("Today is Wednesday") ≫ p("Today Wednesday is") for an n-gram or grammar-aware LM.
- **Unigram LM**: words drawn **independently**.
  - p(w₁…wₙ) = Π p(wᵢ), **order doesn't matter**: p("global warming") = p("warming global").
  - Parameters: one p(w) per vocabulary word; **all sum to 1**.
  - Missing word probability = 1 − sum of the others (0.4 + 0.2 → third word must be 0.4).
  - Worked: p(text)=.4, p(mining)=.2, p(research)=.4 → p("text mining research") = .4×.2×.4 = **0.032**.
- **MLE**: p(w|d) = c(w,d) / |d|. Maximizing likelihood of one document gives **normalized counts**.
- Joint probability of A **and** B (two draws) = product. A unigram model gives equal probability to any reordering of the same words.
- LMs also show topics (word distributions) and association (ratio of topic LM to background LM removes stop words).

## 3. Query-likelihood ranking
- Rank docs by **p(q|d) = Π_{wᵢ∈q} p(wᵢ|d)**.
- **log** version: score = Σ log p(wᵢ|d). Same **ranking** as the product, because log is strictly increasing. It fixes numerical underflow, not order.
  - Quiz answer for "S₁=P(Q|D) vs S₂=log P(Q|D) give same ranked list": **True** (monotone transform). The only hiccup is P=0 (log undefined). That is exactly why you smooth.
- **Zero-probability problem**: one query word absent from d → p(q|d)=0 → the whole product (and ranking information) dies. Without smoothing, a query term not in the doc → log → **−∞**. (A doc word not in the query is harmless; a word absent from both is irrelevant.)
  - Example: Q="food safety", D1="food quality regulations" → P(Q|D1)=(1/3)(0)=**0**; D2="food safety measures" → (1/3)(1/3)=**1/9**.

## 4. Smoothing
- **Idea**: take probability mass away from seen words and give it to unseen words, in proportion to a **reference LM** (usually the **collection LM p(w|C)**).
- General form: p(w|d) = p_seen(w|d) if w∈d, else **α_d · p(w|C)**.
- Rewritten ranking = Σ_{w∈q∩d} log[p_seen(w|d) / (α_d p(w|C))] + n·log α_d + (term independent of d).
  - This reveals **TF** (p_seen), **IDF** (dividing by p(w|C)), and **document-length normalization** (α_d). Only matched words need scoring → fast.
  - Longer docs → less smoothing (α_d smaller).

| | **Jelinek–Mercer (linear interpolation)** | **Dirichlet prior** |
|---|---|---|
| p(w\|d) | **(1−λ)·c(w,d)/\|d\| + λ·p(w\|C)** | **(c(w,d) + μ·p(w\|C)) / (\|d\| + μ)** |
| Parameter | λ ∈ (0,1), fixed fraction for the collection | μ > 0, "pseudo-count" of μ collection tokens |
| α_d | λ (same for all docs) | μ/(μ+\|d\|) (**longer doc → less smoothing**) |
| Best for | **Long / verbose** queries | **Short keyword/title** queries |
| ↑ parameter | closer to **collection LM** | closer to **collection LM** |
| ↓ parameter | closer to **ML estimate of the doc** | closer to **ML estimate of the doc** |
| Score term | 1 + (1−λ)/λ · c(w,d)/(\|d\|p(w\|C)) | 1 + c(w,d)/(μ·p(w\|C)), plus n·log(μ/(μ+\|d\|)) which **can't be dropped** |

- Because α_d is constant for JM, the +n·log α_d term can be dropped; for Dirichlet it varies with |d| and **must stay**.
- **If every word count in a doc doubles** (collection LM unchanged):
  - ML estimate **unchanged**; **JM p(w|d) unchanged**.
  - **Dirichlet p(w|d) changes** (|d| doubles but μ doesn't).
  - **Unsmoothed** query likelihood is also unchanged (proportions are the same), so "query likelihood would change without smoothing" is false.
  - The correct quiz pick is "p(w|d) remains the same under Jelinek–Mercer"; "remains the same under Dirichlet" is false.
- Worked JM (λ=0.5): D1="online course catalog", D2="affordable online education"; P(w|C): online 1/3, course 1/3, education 1/9.
  - D1: p(online)=½·⅓+½·⅓=⅓, p(course)=⅓ → **1/9**.
  - D2: p(online)=⅓, p(course)=½·0+½·⅓=1/6 → **1/18**.
- Unsmoothed MLE for the same query on the same docs: P(Q|D1) = 1/9, P(Q|D2) = 0.

## Quiz traps
- Unigram: product for AND, order irrelevant; probabilities sum to 1.
- log doesn't change the ranking; it changes stability. Only issue is P=0.
- λ **decreased** (JM) or μ **decreased** (Dirichlet) → smoothed estimate moves toward the **document's MLE**. Increased → toward the **collection** model.
- Smoothing = avoid zero probabilities for unseen words (not "remove stop words").
- Without smoothing, a **query** term missing from the **document** → likelihood becomes −∞ (log form).
- Dirichlet: "longer docs get less smoothing." JM: same λ for all docs.
- Doubling every count → JM p(w|d) is the *same*; Dirichlet's changes.
