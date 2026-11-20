# CS410 Glossary: terms to know and what they mean

Ordered by priority, not alphabetically. **Tier 1** terms show up repeatedly in your quizzes or are needed for calculations: know them cold. **Tier 2** terms appeared once in a quiz or are core lecture ideas. **Tier 3** terms are background that rarely gets tested directly. Within each tier the most exam-relevant terms come first. "Wk" is the source week.

## Tier 1 · Know cold

| Term | Meaning | Wk |
|---|---|---|
| **Precision** | Relevant retrieved ÷ **all retrieved**. TP/(TP+FP). | 3 |
| **Recall** | Relevant retrieved ÷ **all relevant in the collection**. TP/(TP+FN). | 3 |
| **Average precision (AP)** | Sum of precision at each relevant doc's rank ÷ **total number of relevant docs**. Rank-sensitive. | 3 |
| **MAP / gMAP** | Arithmetic / geometric mean of AP over queries. MAP is dominated by easy (high-AP) queries; gMAP by hard (low-AP) queries. | 3 |
| **nDCG** | DCG ÷ ideal DCG. Range [0,1], so comparable across queries. (DCG alone is unbounded.) | 3 |
| **F-measure (F_β)** | (β²+1)PR/(β²P+R). F₁ = 2PR/(P+R), the harmonic mean. Larger β favors recall. | 3 |
| **Pooling** | Judge only the union of top-k results from diverse systems, so not every doc is judged. Unjudged docs assumed non-relevant; biased against new systems. | 3 |
| **Unigram language model** | Each word drawn independently. p(sequence) = product of word probabilities. Order ignored. Probabilities sum to 1. | 4 |
| **Smoothing** | Move probability mass from seen to unseen words (using the collection model) so no word gets probability 0. | 4 |
| **Jelinek–Mercer smoothing** | p(w\|d) = (1−λ)·c(w,d)/\|d\| + λ·p(w\|C). Fixed λ for all docs. Better for long queries. | 4 |
| **Dirichlet prior smoothing** | p(w\|d) = (c(w,d)+μ·p(w\|C))/(\|d\|+μ). Longer docs get less smoothing. Better for short queries. | 4 |
| **λ / μ** | Smoothing strength. Higher = closer to the collection model; lower = closer to the document's MLE. | 4 |
| **Query likelihood** | Rank docs by p(q\|d), the chance d's language model generates q. Log gives the same ranking. | 4 |
| **Maximum likelihood estimate (MLE)** | p(w\|d) = c(w,d)/\|d\|: normalized counts. | 4 |
| **PageRank** | Query-independent link-based score from a random-surfer model. Iterative; sparse matrix; normalization doesn't change ranking. | 5 |
| **Transition matrix (M)** | Probability of moving from page i to page j. Entries in [0,1]; rows sum to 1; **not symmetric**. | 5 |
| **Random jump (damping)** | Surfer jumps to a random page with some probability; fixes dead ends and unreachable pages. | 5 |
| **Relevance feedback** | User explicitly marks results relevant/non-relevant. | 5 |
| **Pseudo (blind) feedback** | Top-k results assumed relevant. No human involved; least reliable. | 5 |
| **Implicit feedback** | Clicks treated as relevant, skips as non-relevant. | 5 |
| **MapReduce** | Map emits key-value pairs; the system groups by key; reduce runs **once per unique key**. Can build an inverted index in parallel. | 5 |
| **GFS** | Google File System: one master (metadata), many chunkservers (data), 64 MB chunks, replicated. | 5 |
| **Focused vs incremental crawling** | Focused = only a subset of pages (e.g., automobiles). Incremental = repeated crawls of frequently updated/accessed pages. | 5 |
| **Push vs pull** | Pull: user initiates (search, browse). Push: system initiates (recommendation, filtering). | 1, 6 |
| **Content-based filtering** | Recommend items similar to what the user likes (**item similarity**). | 6 |
| **Collaborative filtering** | Predict preferences from similar users' ratings (**user similarity**). Pearson and cosine are both user similarity measures. | 6 |
| **Beta-Gamma threshold learning** | Heuristically lowers the delivery threshold to explore; more training examples = less exploration. | 6 |
| **Mixture model** | Choose a component, then draw a word. p(w) = λ_B p(w\|θ_B) + (1−λ_B) p(w\|θ_d). Choosing once per doc ≠ choosing per word. | 8 |
| **EM algorithm** | Iterative MLE with hidden variables. Likelihood never decreases; ends at a local maximum. | 8 |
| **E-step / M-step** | E: compute posteriors over hidden variables. M: re-estimate parameters from fractional counts (this step improves the parameters). | 8 |
| **Paradigmatic relation** | Words that can substitute for each other (cat/dog). Found by similar contexts. | 7 |
| **Syntagmatic relation** | Words that combine/co-occur (car + drive). Found by high co-occurrence. | 7 |
| **PLSA** | k topics with per-document coverage, fit by EM. Parameters grow with the number of docs. | 8 |
| **LDA** | PLSA with Dirichlet priors on coverage and topics. | 8 |
| **Naive Bayes** | Generative classifier: argmax of log prior + Σ c(w,d)·log p(w\|θ). Needs smoothing. | 10, 11 |
| **Laplace smoothing** | Add one to every count: (c+1)/(total + \|V\|). | 11 |
| **Generative vs discriminative classifier** | Generative models P(x\|y), P(y) (Naive Bayes). Discriminative models P(y\|x) or the boundary (logistic regression, k-NN, SVM). | 10, 11 |
| **K-NN** | Classify by the labels of the k most similar training docs. No weights learned; odd k avoids ties. | 11 |
| **Accuracy** | (TP+TN)/all decisions. Fails on skewed data and can't weight errors differently. | 9, 11 |
| **Micro vs macro average** | Micro: pool all decisions (large categories dominate). Macro: average per-category scores (each category equal). | 9, 11 |
| **K-means** | Assign to nearest centroid (E-like), recompute centroids (M-like). Hard-assignment EM; local optimum; user sets K. | 10 |
| **Single / complete / average link** | Cluster similarity by closest pair / farthest pair / mean of all pairs. Single chains; average-link least outlier-sensitive. | 10 |
| **Agglomerative clustering** | Bottom-up: start with singletons, repeatedly merge the closest clusters. Needs a similarity measure. | 10 |
| **Direct vs indirect evaluation** | Direct: compare to a human gold-standard clustering. Indirect: measure an application with vs without the clusters. | 9, 10 |
| **Context (contextual text mining)** | Metadata (time, location, author, network) that partitions text and gives meaning to topics; influences both coverage and content. | 12 |
| **CPLSA** | Contextual PLSA: PLSA extended with context-dependent views (content) and coverages. | 12 |
| **NetPLSA** | PLSA + network regularizer pushing neighbors toward **similar** topic coverage. | 12 |
| **ITMTF** | Iterative topic modeling with time-series feedback: finds topics correlated with an external time series. | 12 |
| **Granger test** | Whether one series improves prediction of another (lead/lag, not proof of causation). | 12 |
| **LARA** | Latent Aspect Rating Analysis: recovers aspects, aspect ratings and aspect weights from reviews. | 12 |
| **Opinion holder / target** | Who holds the opinion / what it is about. | 11 |
| **Sentiment classification** | Text categorization: opinionated text in, sentiment label out. | 11 |
| **Bit vector + dot product** | Presence/absence vector; the dot product counts matched distinct query terms. | 1 |
| **Cosine vs L2** | Cosine ignores doc length; L2 distance is affected by it. | 1 |
| **TF transformation (BM25)** | y = (k+1)x/(x+k). k=0 → bit vector, k→∞ → linear, ceiling k+1. | 2 |
| **IDF** | log((M+1)/df). Rare terms high, terms in every doc ≈ 0. | 2 |
| **Pivoted length normalization** | Normalizer 1−b+b·\|d\|/avdl. b=0 means no normalization. | 2 |
| **BM25** | Top ranking function: TF transform + length normalization + IDF. | 2 |
| **Inverted index** | Dictionary (term, df, pointer) + postings lists (docID, tf, positions), sorted by docID. | 2 |
| **d-gap / gamma code** | Store gaps between docIDs (first value is the docID). Gamma = unary length + binary offset (drop leading 1). 9 → 1110001. | 2 |
| **Accumulator** | Running score for one doc; allocated when it first appears in a query term's postings list. | 2 |
| **Bag of words** | Unordered words with counts. Loses order and phrases; keeps counts, length, unique words. | 1 |

## Tier 2 · Should know

| Term | Meaning | Wk |
|---|---|---|
| **Cranfield methodology** | Frozen, reusable collection + queries + human relevance judgments. | 3 |
| **PR curve** | Precision (y) vs recall (x). Ideal = flat line at 1; curve above another at all recall = better. | 3 |
| **Precision@k** | Precision within the top k results. | 3 |
| **Gain / cumulative gain / DCG** | Gain = graded relevance value. CG sums gains; DCG discounts by rank position. | 3 |
| **MRR** | Mean of 1/rank of the single relevant doc (known-item search). | 3 |
| **Sign test / Wilcoxon** | Significance tests across queries: win/loss counts; Wilcoxon also ranks the size of the differences. | 3 |
| **Rocchio** | VSM feedback: move the query toward the centroid of relevant docs and away from non-relevant ones. | 5 |
| **Crawler / seed URLs** | Fetches pages by following links from seed URLs. Can't find pages with no incoming links. | 5 |
| **Authority / hub** | Authority: many pages link to it. Hub: links to many pages. | 5 |
| **Anchor text** | Text of a link; describes the target page. | 5 |
| **Hadoop** | Open-source MapReduce. | 5 |
| **Filtering** | Immediate yes/no delivery decision for each arriving item, using a scorer plus a threshold. | 6 |
| **User profile / utility function** | Long-lived interest description used as a classifier. Utility e.g. 3·#good − 2·#bad. | 6 |
| **Exploration vs exploitation** | Deliver near-threshold items to learn vs only deliver sure matches. | 6 |
| **Censored data** | Only delivered docs get judged, so the threshold can't be validated for the rest. | 6 |
| **Cold start / data sparseness** | Little info about a new user/item / few observed ratings. | 6 |
| **Memory-based CF** | Keeps the rating matrix; predicts via a weighted average of similar users' ratings. | 6 |
| **DUS triangle** | Data, Users, Services. | 6 |
| **Background model θ_B** | Fixed word distribution for common words. Larger λ_B pushes common words out of the topic. | 8 |
| **Hidden (latent) variable** | Unobserved variable, e.g., which component generated a word. | 8 |
| **Coverage (π)** | Probability that a document covers a topic. | 7 |
| **Topic** | A word distribution (unigram LM) representing a theme. | 8 |
| **EOWC** | Expected overlap of words in context: Σ xᵢyᵢ, xᵢ = c(wᵢ,d)/\|d\|. Fixed by BM25-style TF and IDF. | 7 |
| **Context (pseudo document)** | Words around a candidate word, treated as a document (Left1, Right1, Window8). | 7 |
| **Text categorization** | Supervised: assign docs to predefined categories from labeled examples. | 9 |
| **Text clustering** | Unsupervised: group similar text objects. | 9 |
| **Clustering bias** | The perspective that defines "similar". | 9 |
| **Model-based clustering** | Clusters as mixture components fit by EM; hard to change the similarity measure. | 10 |
| **Logistic regression** | Discriminative classifier with d+1 weights. | 11 |
| **SVM** | Linear classifier maximizing the margin. | 11 |
| **Contingency table** | TP, FP, FN, TN counts for a category. | 9 |
| **Text-based prediction** | Use text (plus non-text) to estimate a real-world variable. | 12 |
| **Data mining loop** | Sensors → joint mining → predictors → predictions → decisions → world. | 12 |
| **Coverage / content variation** | How much a topic appears across contexts / how its words differ across contexts. | 12 |
| **Causal topic** | Coherent topic whose coverage correlates (with lag) with an external time series. | 12 |
| **Ordinal logistic regression** | Rating prediction with a shared weight vector and a separate intercept per threshold. | 11 |
| **Overfitting** | Fitting training data too closely (e.g., very specific features). | 11 |
| **Document ranking vs selection** | Ranking scores and sorts (relative); selection is a binary yes/no per doc. Ranking preferred. | 1 |
| **Probability Ranking Principle** | Ranking by P(relevant) is optimal if doc utilities are independent and users browse sequentially. | 1 |
| **Term frequency / document frequency / collection frequency** | Count in a doc / number of docs containing the term / total count in the collection. | 2 |
| **Stop words / Zipf's law** | Very frequent structural words; rank × frequency ≈ constant. | 2 |
| **Dictionary / postings list** | The two parts of an inverted index (dictionary in memory, postings compressed on disk). | 2 |
| **Unary / binary / delta codes** | Unary: x−1 ones then 0. Binary: fixed width. Delta: gamma-code the length instead of unary. | 2 |
| **Stemming / tokenizer** | Mapping word forms to a root / splitting text into terms. | 2 |
| **Collection language model p(w\|C)** | Word probabilities from the whole collection; the smoothing reference. | 4 |
| **Probabilistic model** | Scores by p(R=1\|d,q). | 4 |
| **NLP steps (POS, syntactic, semantic, inference)** | Tag words → find structure → assign meaning → draw conclusions. | 1, 7 |
| **Anaphora / presupposition** | Finding what a referring word points to / background assumed but not stated. | 1 |
| **Text mining / analytics** | Turning text into actionable knowledge. | 7 |
| **Component model / generative model** | One distribution in a mixture / a probabilistic story of how the data was produced. | 8 |

## Tier 3 · Background

| Term | Meaning | Wk |
|---|---|---|
| **Retrieval model** | Computational definition of relevance used to build a ranking function. | 1 |
| **R(q) / R′(q)** | True relevant set / the set the system returns. | 1 |
| **Vector space model (VSM)** | Framework: docs and queries are term vectors; relevance = similarity. | 1 |
| **Lexical analysis / lexicon** | POS tagging of tokens / lookup table mapping strings to integer IDs. | 1, 2 |
| **Scorer / indexer** | Applies the ranking function online / builds the index offline. | 2 |
| **Sort-based inversion** | Index larger than memory: collect tuples, sort runs on disk, merge. | 2 |
| **BM25F / BM25+** | BM25 for structured docs (combine fields first) / adds a small TF constant so long docs aren't over-penalized. | 2 |
| **PL2** | A divergence-from-randomness retrieval model. | 4 |
| **Chunk / chunkserver** | GFS stores 64 MB chunks on chunkservers. | 5 |
| **Vertical search engine** | Search specialized to a domain or user group. | 6 |
| **Hierarchical clustering variants** | Divisive = top-down splitting (the opposite of agglomerative). | 10 |
| **Purity / NMI** | Direct clustering measures vs a gold standard. Purity is trivially 1 with singleton clusters. | 10 |
| **Aspect (LARA)** | A facet of an entity (e.g., room, service) with its own rating and weight. | 12 |
| **Variants of categorization** | Binary, multi-class, hierarchical, multi-label (joint). | 9 |
| **Generative model of text mining** | Hidden process producing observed text. | 8 |
