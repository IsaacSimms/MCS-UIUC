# 01 · Text Retrieval & the Vector Space Model (Weeks 1–2)

[← Overview](00-Overview.md) · Next: [02 Evaluation](02-Evaluation.md)

## 1. Big picture
- Course = **text retrieval** (reduce a big collection to a relevant subset) → **text mining** (turn text into knowledge) → LLM layer.
- NLP pipeline, shallow → deep: **lexical** (POS tagging, ~97% accurate) → **syntactic** (parsing, partial ~90%) → **semantic** (entities, word senses) → **inference** / pragmatics.
- Ambiguity is the core difficulty: word level ("root"), syntactic ("A man saw a boy with a telescope" = **2** structures), anaphora ("himself"), presupposition.
- Retrieval uses **shallow NLP = bag of words (BOW)**: general, robust, efficient. Deep NLP does not scale.
- BOW **loses** word order and multi-word phrases. It **keeps** counts, length, and unique-word count.

## 2. Access modes and the retrieval problem
| | **Pull** | **Push** |
|---|---|---|
| Initiative | User | System |
| Need | Ad hoc, temporary | Stable, long-lived (a *profile*) |
| Example | Search engine (query / browse) | Recommender, Netflix, Spotify app |

- Query = know what you want. Browse = don't know the keywords.
- **TR vs database retrieval**: unstructured and ambiguous vs structured and exact (SQL). TR is **empirical**; relevance is subjective and judged by humans.
- Goal: compute **R′(q)**, an approximation of the true relevant set R(q).
- **Selection** (binary classifier, absolute relevance) vs **ranking** (score each doc, relative relevance). **Ranking is preferred** because:
  - the selection boundary is hard to define (over- or under-constrained queries)
  - relevance is a matter of degree
  - users browse sequentially
  - *Not* a reason: "ranking is computationally easier."
- **Probability Ranking Principle**: rank by P(relevant) is optimal if (1) each doc's utility is independent and (2) the user browses sequentially.

## 3. Retrieval models
- **Similarity-based** f(q,d)=sim(q,d) (VSM) · **Probabilistic** f=p(R=1|d,q) (query likelihood, classic, PL2/divergence-from-randomness) · **Probabilistic inference** · **Axiomatic** (constraints).
- Universal heuristics: **TF** (more occurrences → more relevant), **IDF/DF** (rare matches matter more), **doc length** (long docs get penalized).
- State of the art (all perform similarly once tuned): **pivoted length norm, BM25 (most popular), query likelihood, PL2**.

## 4. Vector Space Model (VSM) builds up in steps
| Version | Vector entries | Score | Fixes / flaw |
|---|---|---|---|
| **Bit vector + dot product** | 1 if term present else 0 | # distinct matched query terms | Ignores TF, IDF, length |
| **TF vector** | raw count c(w,d) | Σ c(w,q)·c(w,d) | Spam: 50 hits = 10× weight of 5 hits; stop words count |
| **TF-IDF** | count × IDF | Σ c(w,q)·c(w,d)·IDF(w) | Still linear in TF |
| **+ TF transformation** | sublinear TF | see below | Caps influence of repeats |
| **+ length normalization** | divide by pivot normalizer | pivoted / BM25 | Stops long docs winning |

- **IDF(w) = log((M+1)/df(w))**. M = #docs, df = #docs containing w. Rare → high; in every doc → ≈0. Log base doesn't change ranking.
- **TF transformation**: first occurrence matters most. Options: y = log(1+x) (or log(1+log(1+x))) and the **BM25 transform y = (k+1)x / (x+k)**.
  - **k=0** → bit vector. **k→∞** → linear (raw TF). Upper bound **k+1** as x→∞.
- **Pivoted length normalization**: normalizer = 1 − b + b·|d|/avdl. Pivot = avg doc length (no penalty, no bonus). Longer → penalty; shorter → bonus. **b=0 → no normalization**; larger b → more normalization.
  - Distinguish *long because verbose* (penalize more) vs *long because multi-topic* (penalize less).
- Full formulas
  - **Pivoted:** Σ c(w,q) · ln(1+ln(1+c(w,d))) / (1−b+b|d|/avdl) · log((M+1)/df)
  - **BM25:** Σ c(w,q) · (k+1)c(w,d) / [c(w,d) + k(1−b+b|d|/avdl)] · log((M+1)/df)
  - Same IDF and c(w,q) in both; only the TF-transform and normalizer differ.
- Variants: **BM25F** (structured docs, combine fields first), **BM25+** (small constant added to TF so long docs aren't over-penalized).
- Dimensions can be refined (stop words, stemming, phrases, n-grams) but BOW is usually enough. **Dot product** stays the best default similarity.

**Distance measures**
- **L2** ‖v₁−v₂‖ is **affected by document length**. A longer doc with the same word proportions is far from the origin.
- **Cosine** = v₁·v₂ / (‖v₁‖‖v₂‖) is **not** affected by length (scaling cancels). Default in VSM.

## 5. System implementation
- Pipeline: **tokenizer** (split, lowercase, **stemming** computer/computing → compute) → **indexer** (offline) → **inverted index**; query → tokenizer → **scorer** (online) → ranked results → judgments/feedback.
- **Inverted index** = **dictionary** (term, **df**, total freq, pointer; in memory: hash/B-tree) + **postings lists** (docID, tf, optionally **positions** for phrases; **sorted by docID**; on disk, compressed). Postings are bigger than the dictionary.
- Why an inverted index: no scan of every document; only docs containing query terms are touched. Boolean AND = intersect postings; OR = union.
- **Accumulators**: one running score per document, **allocated only when that doc first appears in a query term's postings list**, not one per doc in the collection. A doc matching two terms still has one accumulator.
  - Efficiency tricks: caching, keep only promising accumulators, parallelism.
- I/O, not CPU, is the bottleneck, so compression is nearly free.
- **Zipf's law**: rank × frequency ≈ constant (cf ∝ 1/rank). A few words are very frequent (structural, low IDF); most are rare. Basis for stop words and for coding small integers with fewer bits.
- Index construction when data doesn't fit memory: **sort-based inversion** (collect <termID, docID, freq> tuples → sort runs on disk → pairwise merge). Lexicons map term/doc strings → integers.

## 6. Integer compression (a frequent quiz item)
- **d-gap**: store differences between consecutive docIDs; the **first value is the docID itself**. Decode by running sum. Postings are accessed sequentially, so this works.
- **Binary** = fixed width (wasteful for small numbers). **Unary(x)** = (x−1) ones then a 0 (3→110, 5→11110) cheap for small, awful for large. **Gamma** = unary length + binary offset. **Delta** = gamma-code the length instead.
- **Encode γ(x)**: (1) binary of x, (2) drop the leading 1 → offset (N bits), (3) write N ones then a 0, (4) prepend that to the offset.
  - 9 = 1001 → offset 001 → 1110 | 001 = **1110001**
  - 5 → 11001 · 13 → 1110101 · 1 → 0 · 2 → 100 · 3 → 101 · 4 → 11000
- **Decode γ**: count ones up to the first 0 (= N), read N more bits, put a leading 1 back, convert. **1110|010 → 1010 = 10**. Value = 2^N + offset.
- Compress **skewed** values with **variable-length** codes.

## Quiz traps
- Bit-vector dot product counts *distinct* matched query terms, not occurrences.
- "Ranking is computationally easier than selection" is the **false** reason.
- "Relies LESS on NLP": plagiarism comparison between submissions (surface string match).
- TR is harder than DB retrieval because of unstructured data, ambiguity **and** subjective relevance (all three, per your annotated screenshot).
- L2 depends on length; cosine doesn't.
- Accumulators are per matched document, allocated lazily.
- Higher b = more length normalization; b=0 = none. k=0 = bit vector.
- Gamma: *drop the leading 1*, length in unary = number of offset bits **plus a terminating 0**.
