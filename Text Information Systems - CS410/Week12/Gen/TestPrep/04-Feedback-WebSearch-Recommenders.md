# 04 · Feedback, Web Search & Recommender Systems (Weeks 5–6)

[← 03 LM Retrieval](03-Probabilistic-LM-Retrieval.md) · [Overview](00-Overview.md) · Next: [05 Text Mining & Topic Models](05-Text-Mining-Topic-Models.md)

## 1. Feedback in retrieval
Feedback = use evidence from the first ranking to rewrite the query, then search again.

| Type | Who judges | Assumption | Reliability |
|---|---|---|---|
| **Relevance feedback** | **User, explicit** | User marks relevant / non-relevant | Best, but costs user effort |
| **Pseudo / blind / automatic** | **No human** | Top-k results *assumed* relevant | **Least reliable**; zero effort; adds related terms |
| **Implicit** | Human, indirectly | Clicked = relevant, skipped = non-relevant | Middle; no extra effort |

- **Rocchio** (VSM feedback): move the query vector toward the **centroid of relevant docs** and away from non-relevant ones.
  q_new = α·q + β·mean(relevant docs) − γ·mean(non-relevant docs).
  - Truncate to the top-weighted terms. **Keep a fairly high weight on the original query** to avoid over-fitting / **topic drift**.
  - Works with all three feedback types.
- Query modification = add new weighted terms (**expansion**) and reweight old ones.

## 2. Web search
- **Challenges**: scalability, low-quality information, dynamics of the web (all three, "all of the above").
- **Opportunities**: links and metadata, parallel indexing (MapReduce), spam detection.
- Components: **crawler** → cached pages → **indexer** → inverted index → **retriever**.
- **Crawler**: seed URLs in a priority queue → fetch → parse links → enqueue → repeat.
  - **A link-following crawler cannot find pages with no incoming links.**
  - Issues: robustness / crawler traps, politeness (robots exclusion), many file types, duplicate URLs, finding new pages.
  - **Breadth-first** (balanced load) · **parallel** · **focused** (only a subset of pages, e.g., all pages about "automobiles", chosen by a query) · **incremental** (re-crawl; target **frequently updated / frequently accessed** pages; learns from past experience).
  - "Target a subset of pages (e.g., automobiles)" is focused crawling, **not** incremental.
- **GFS**: one **master** (metadata, namespace, chunk locations, logs), many **chunkservers** (hold the bytes), client. Files split into **64 MB chunks**, replicated for fault tolerance. Flow: client → master (file name, chunk index) → master returns chunk handle + locations → client → chunkserver (handle, byte range) → data.
- **MapReduce**: hides parallelism, fault tolerance, load balancing. Programmer writes **map** and **reduce**.
  - Input splits → map emits **key-value pairs** → system **groups by key** → **reduce is called once per unique key** (not once overall) → output.
  - Word count: map emits (word,1); reduce sums.
  - **Inverted index**: map(docID, text) → (word, (docID, count)); reduce concatenates postings per word. **MapReduce does allow parallel index construction.**
  - **Hadoop** = open-source MapReduce.
- **Link analysis**: anchor text describes the target page; links ≈ citations. **Authority** = many pages link to it; **hub** = links to many pages.
- **PageRank** = query-independent score of how much the link graph endorses a page; used as one feature next to content scores.
  - Random surfer: with prob. (1−α) follow an outlink; with prob. **α jump to a random page** (your notes call the follow-probability *d*, so d = 1−α).
  - Transition matrix **M**: M_ij = P(go from dᵢ to dⱼ). Entries are in **[0,1]**; each row sums to 1 (sum of probabilities of leaving a page = 1); **not symmetric** (P(A→B) ≠ P(B→A)).
  - **Iterative** algorithm (power iteration). Efficient because M is **sparse**, each iteration is a matrix multiply (a large dimension is *not* a reason it's efficient).
  - **Random jumping** fixes: disconnected pages with zero probability, **dead ends (zero out-links)** swallowing all probability, and favoring nodes with *fewer* in-links is **NOT** a benefit.
  - A page with many in-links and no out-links scores higher than a page that only links out. Pages with many (and highly ranked) in-links get more probability.
  - **Normalization doesn't change the ranking**, only absolute values.
  - PageRank uses only link structure, but modern engines **combine many features** (content, links, clicks) via machine learning. PageRank can be used for things other than link analysis.
- **Future of search**: vertical/personalized engines, learning over time, integrated search + browse + recommendation. **DUS triangle** = **Data, Users, Services** (not "Internet providers").
- Learning-based ranking became popular because there are **more information needs** (spam, diversity), **more features**, **and more combining methods** (all three).

## 3. Recommenders and filtering
- **Push (recommendation, filtering) vs pull (search)**. Filtering = reusing a retrieval scorer with a threshold against a **stable profile** over a dynamic stream; decision is **immediate and binary**.
- Basic question: *Will user U like item X?*
  - **Content-based**: compare X to what U already likes → **item similarity**, uses content, not other users.
  - **Collaborative**: find users like U who liked X → **user similarity**, ignores content.
  - Hybrid combines both. Recommendation + search = push + pull.
- **Content-based filtering system**: user interest profile = a **binary classifier / utility function**, with an initializer (profile text), a learning module and feedback.
  - Can be solved as **classification**: spam filtering, recommendation (and ranking, per your quiz).
  - **Linear utility** example: U = 3·(#good) − 2·(#bad). Search metrics (MAP etc.) aren't suitable.
- **Threshold learning** (deliver if score > θ). Difficulties: **censored data** (only delivered docs get judged), little labeled data, **exploration vs exploitation**.
  - **Empirical utility optimization** picks θ maximizing utility on labeled data (biased).
  - **Beta-Gamma threshold learning**: heuristically **lower** θ from the optimal toward the **zero-utility threshold** to explore. θ = α·θ_zero + (1−α)·θ_optimal, with α shrinking as the number of training examples N grows (α = β + (1−β)·e^(−N·γ), recalled from the slides). **More training examples → less exploration.**
- **Collaborative filtering**: fill the empty cells of a user × item rating matrix. Assumptions: shared interests imply similar preferences; enough observed ratings.
  - **Memory-based**: keep the ratings; predicted rating = (baseline) + weighted average of similar users' ratings. Weights = **user similarity**: **Pearson correlation** (over co-rated items) or **cosine**; *both* are user similarity measures.
  - **Cosine does not solve missing values** (unrated entries remain missing), but it is not biased by how active/inactive a user is (less/more ratings).
  - Two intuitions: user-user, item-item.
- Why recommendation is hard: **data sparseness**, **cold start**. ("High user expectations" is *not* a reason, since expectations are actually low.)
- **New user** help: ask for a few liked items, ask for a short self-description. **Random recommendations won't help.**
- Valid heuristics: same user likes similar items; similar users like the same items. **Invalid**: "if a user likes one item, they dislike other items not similar to it."
- **Search engine properties**: ad hoc need, user takes initiative. It does **not** start with good prior knowledge of the user's need (that's push).

## Quiz traps
- Pseudo feedback = no humans, least reliable. Relevance feedback = explicit judgments. Implicit = clicks.
- GFS chunk = **64 MB**. Reduce is called **per unique key**.
- Crawler that only follows links can't find orphan pages. Focused ≠ incremental.
- PageRank matrix entries ∈ [0,1], **not symmetric**, iterative, sparse; normalization doesn't affect ranking.
- A site with only in-links ranks high; random jumping *doesn't* favor pages with fewer in-links.
- Content-based = item similarity; collaborative = user similarity; Pearson **and** cosine = user similarity.
- Beta-Gamma: more training data → less exploration; central idea = heuristic lowering of the threshold.
- Search = pull; recommendation = push; profile = long-lived, query = one-shot.
