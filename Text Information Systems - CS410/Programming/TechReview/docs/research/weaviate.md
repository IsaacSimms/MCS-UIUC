# Weaviate

Self-hosted notes for text retrieval. Checked against Weaviate **v1.40.4** (published 2026-11-05) and the documentation pages fetched on 2026-11-09. Those pages do not print a git revision. The README quickstart still pins Docker image tag `1.36.0`, which is behind v1.40.4. Confidence is **partial**: the two official RAM formulas disagree, a numeric dimension cap was found only in an archived FAQ, and Weaviate was not started. No latency or RSS number below was measured for this review.

## A. What it is and the design goal

Weaviate is an open-source database that stores each data object together with its vectors, so one query can combine dense similarity, keyword search, and metadata filters. The docs also position that store as a backend for retrieval-augmented generation. The repository describes the same goal as a cloud-native database for semantic search at scale, with reranking available in the query interface. ([What is Weaviate?](https://docs.weaviate.io/), [README](https://github.com/weaviate/weaviate/blob/main/README.md))

The license is split. Source outside the `wl/` directory is BSD-3-Clause. Source inside `wl/` is Copyright Weaviate B.V. 2026–present and is available only under a separate enterprise license. Published binaries combine both, and enterprise features require a license key. GitHub reports SPDX `NOASSERTION` because the repo is dual-licensed. ([LICENSE](https://github.com/weaviate/weaviate/blob/main/LICENSE), [README](https://github.com/weaviate/weaviate/blob/main/README.md))

The newest line checked is v1.40.4, with no breaking changes in that patch. The releases page still ships patches for older lines, including v1.39.15, v1.38.24, v1.37.18, and v1.36.24 around the same week. ([Releases](https://github.com/weaviate/weaviate/releases))

## B. How it stores and searches

A collection is stored as one or more shards. Each shard has its own vector index, inverted indexes, and object store. For a single-tenant collection the shard count is fixed at creation. The shard key is the object UUID, hashed with 64-bit MurmurHash3. On-disk access is an LSM store. `PERSISTENCE_LSM_ACCESS_STRATEGY` defaults to `mmap` (`pread` is the other named option). ([Horizontal scaling](https://docs.weaviate.io/weaviate/concepts/cluster), [Environment variables](https://docs.weaviate.io/deploy/configuration/env-vars))

**Vector indexes.** There are four.

| Index | What it is | When the docs point at it |
|---|---|---|
| HNSW | In-memory multi-layer graph. The default. | The general case. |
| Flat | Disk-backed brute force. | Small sets. |
| Dynamic | Starts as flat and converts one way to HNSW. Default threshold is 10,000 objects. | Uneven tenant sizes. On self-hosted servers this index type requires `ASYNC_INDEXING=true`, which defaults to false. |
| HFresh | Cluster index based on SPFresh, added in v1.36. An HNSW centroid index stays compressed in memory. Posting lists stay on disk. | A working set that should not sit fully in RAM. Documented tradeoff: lower peak query throughput than HNSW. Distance is only cosine or squared L2. |

Documented HNSW defaults include distance `cosine`, `ef` of `-1` (dynamic ef), `efConstruction` 128, and `maxConnections` 32. The docs say `ef` above 512 has diminishing recall returns. The HNSW write-ahead log defaults to 500 MiB. ([Indexing](https://docs.weaviate.io/weaviate/starter-guides/managing-resources/indexing), [Vector index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index))

**Keyword side.** Per-property inverted indexes. `indexSearchable` (default on for text) is the BM25 map. `indexFilterable` (default on) is a roaring-bitmap index. `indexRangeFilters` (default off, since v1.26) is a range index for `int`, `number`, and `date`. Turning searchable or filterable indexes off reduces import work and disk use. The default tokenizer is `word` (split on non-alphanumeric characters, lowercased). The default stopword preset is English. Stopwords are stored in the index and removed from the query, and since v1.18 they still affect the BM25 score. ([Inverted indexes](https://docs.weaviate.io/weaviate/concepts/indexing/inverted-index), [Collection definition](https://docs.weaviate.io/weaviate/config-refs/collections))

**Named vectors and multi-vectors.** Named vectors (`vectorConfig`) let one object carry several vector spaces, each with its own vectorizer, index, and compression. The archived collection reference says this arrived in v1.24.0. The current reference still recommends named vectors for new collections, and a named vector can be dropped from v1.40. Multi-vector embeddings (ColBERT, ColPali, ColQwen, and user-supplied matrices) arrived in v1.29. Each object holds many token vectors and is scored with late interaction (MaxSim). The tutorial’s size example is 6 kB for one 1536-dimensional float32 vector versus about 25 kB for 64 vectors of 96 dimensions. On HFresh, from v1.40, multi-vector imports require MUVERA encoding. `multivector.enabled` alone does not accept them. ([Collection definition](https://docs.weaviate.io/weaviate/config-refs/collections), [Archived collection definition](https://archive.docs.weaviate.io/weaviate/config-refs/collections), [Multi-vector embeddings](https://docs.weaviate.io/weaviate/tutorials/multi-vector-embeddings), [Vector index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index))

**Dimension cap, unresolved.** An archived FAQ says the maximum embedding length is 65,535 because the embedding is stored with `uint16`. The current vector-index, hybrid, and quantization pages that were read do not restate a number. A handful of v1.40.4 Go validation files did not contain 65535 or 65536. A full-text search of the tree was not finished. Treat 65,535 as an archived figure that may be stale. ([Archived FAQ](https://archive.docs.weaviate.io/weaviate/more-resources/faq))

## C. Deployment models

| Shape | What it is |
|---|---|
| Single node | Docker, documented for local evaluation and development, with optional local inference containers. There is no native Windows build. Windows is Docker or WSL. |
| Embedded | Launched from the Python or JavaScript client. Documented as experimental, for basic evaluation. |
| Kubernetes cluster | Helm chart, StatefulSet, headless Service. Nodes discover each other with Hashicorp memberlist. |
| Weaviate Cloud | Shared infrastructure operated by Weaviate, from a free evaluation tier through production. Optional replication and optional zero-downtime updates. The deploy guide says Cloud generally gets versions first, and that self-managed instances run the same database. |
| Marketplace and DigitalOcean | AWS and GCP marketplace listings can bill a shared Cloud or a Kubernetes install. DigitalOcean is a separate fully managed preview with daily backups and TLS. |

([Deploy](https://docs.weaviate.io/deploy), [Documentation home](https://docs.weaviate.io/))

**Two different replication mechanisms.** From v1.25, collection definitions and tenant activity use Raft, so a minority of nodes can fail without blocking metadata writes. Before v1.25, metadata used a two-phase commit that stalled if any node was down. Kubernetes upgrades into 1.25 require a manual Raft migration, including deleting the existing StatefulSet. Object data is separate and leaderless. The replication factor is per collection (the archived collection reference lists default `1`). Read and write acknowledgements are `ONE`, `QUORUM` (n/2+1), or `ALL`. The docs say Weaviate generally prefers availability over consistency because it is used for approximate search, and that consistency is tunable. ([Horizontal scaling](https://docs.weaviate.io/weaviate/concepts/cluster), [Replication architecture](https://docs.weaviate.io/weaviate/concepts/replication-architecture), [Migration](https://docs.weaviate.io/deploy/migration))

Adding a node does not move existing shards. Replica movement, added in v1.32, is how shards are rebalanced or how a shard’s replication factor changes. More shards increase dataset size and import speed, including multiple shards on one node so imports use more CPUs. They do not raise query throughput. More replicas raise availability and read throughput (near-linear when reads use consistency `ONE`) and do not raise import speed. From v1.38, async replication runs for every collection whose factor is greater than 1 unless `ASYNC_REPLICATION_DISABLED` is true. ([Horizontal scaling](https://docs.weaviate.io/weaviate/concepts/cluster), [Resource planning](https://docs.weaviate.io/weaviate/concepts/resources))

`LIMIT_RESOURCES=true` caps the process at 80% of memory and all but one core. The database process itself does not use GPUs. Model containers such as `text2vec-transformers` can. ([Resource planning](https://docs.weaviate.io/weaviate/concepts/resources), [Environment variables](https://docs.weaviate.io/deploy/configuration/env-vars))

## D. Resource characteristics

CPU affects query and import speed, not how many vectors fit. Each insert and each search is single-threaded. Parallel batches and multiple shards use more cores. Vector search, and imports that search while building HNSW, are the CPU-heavy work. ([Resource planning](https://docs.weaviate.io/weaviate/concepts/resources))

For HNSW, RAM determines the maximum dataset. The docs say the HNSW index must sit in memory, that the original object text is not the limiting factor, and that query load does not change the index footprint. Each object has at most `maxConnections` links per layer, 8–10 bytes each, and the base layer allows `2 * maxConnections`. ([Resource planning](https://docs.weaviate.io/weaviate/concepts/resources))

**The two official sizing notes disagree.** Neither is a measurement from this review.

- Resource planning says `memory ≈ 2 × (float32 vector bytes)` to cover garbage collection. One million 384-dimensional float32 vectors are 1.5 GB of vectors and about 3 GB with that multiplier. The same page’s `maxConnections=64` example is about 2.2 GB and explicitly omits garbage collection.
- Best practices says about 6 GB for one million 1024-dimensional vectors (4 GB of floats plus overhead), 1.5 GB for one million 256-dimensional vectors, and 2 GB for one million 1024-dimensional vectors “with quantization enabled,” without naming the quantizer. A 2× multiplier on 1024-dimensional float32 data would be 8 GB, not 6 GB.

([Resource planning](https://docs.weaviate.io/weaviate/concepts/resources), [Best practices](https://docs.weaviate.io/weaviate/best-practices))

`vectorCacheMaxObjects` defaults to `1e12` on a new collection, which is large enough to hold a normal dataset. The docs say a disk fetch is orders of magnitude slower than a cache hit, and that import speed collapses if the cache cannot hold every vector, because each import does several searches. If the cache fills, Weaviate drops the entire cache and refills it from disk. Shrinking it is documented as a last resort, useful when most queries touch a hot subset. A page titled for vector-cache sizing is referenced from the index docs and was not read, so no separate cache formula is stated here. ([Resource planning](https://docs.weaviate.io/weaviate/concepts/resources), [Vector index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index))

**Compression**, on HNSW: rotational quantization (RQ), product quantization (PQ), binary quantization (BQ), and scalar quantization (SQ). The indexing guide recommends RQ first. It rotates the vector, then stores each dimension in 8, 4, or 1 bits instead of 32, with no training step. The guide says internal testing saw 8-bit RQ recall up to 98–99%. That figure is the vendor’s internal test. PQ and SQ train on the data. PQ on HNSW wants roughly 10,000 to 100,000 vectors loaded per shard before it is enabled. Once quantization is set on a collection, it cannot be disabled. `DEFAULT_QUANTIZATION` (v1.33) is unset by default, so new collections are uncompressed unless the variable or the schema says otherwise. `rq-4` was added as a value of that variable in v1.40. PQ and SQ are not applied to flat indexes. ([Indexing](https://docs.weaviate.io/weaviate/starter-guides/managing-resources/indexing), [Vector index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index), [Best practices](https://docs.weaviate.io/weaviate/best-practices))

HFresh keeps only the compressed centroid index in memory. The indexing guide says 8-bit RQ for centroids and mandatory 1-bit RQ for postings. The vector-index reference says HFresh `rq.bits` is fixed at 1 and a wider width is rejected, with default `rescoreLimit` 350. Default `searchProbe` is 256 on v1.36.20, v1.37.10, v1.38.2, and later, and 64 on earlier builds of those lines. ([Indexing](https://docs.weaviate.io/weaviate/starter-guides/managing-resources/indexing), [Vector index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index))

**Disk.** Prefer SSDs. Spinning disks work with a performance penalty. Do not put `PERSISTENCE_DATA_PATH` on NFS. Prefer ext4 or XFS on SAN-style volumes such as EBS. Very fast imports on large machines can allocate faster than the Go garbage collector frees memory and can be OOM-killed. The documented mitigation is `LIMIT_RESOURCES` or `GOMEMLIMIT`. Container RSS overstates the heap because the runtime uses `MADV_FREE`. `MEMORY_WARNING_PERCENTAGE` defaults to 80. From v1.36.0, shards that entered read-only because of pressure return to ready when usage falls. From v1.36.6, shard loading is eager until a collection passes either 1,000 shards or 100 GB, then it becomes lazy. ([Resource planning](https://docs.weaviate.io/weaviate/concepts/resources), [Best practices](https://docs.weaviate.io/weaviate/best-practices), [Environment variables](https://docs.weaviate.io/deploy/configuration/env-vars))

HNSW “algorithms are costly when you add data during the index building process.” `ASYNC_INDEXING=true` decouples the queue from the insert. `vectorQueueLength` on the nodes endpoint is the documented backlog. Tombstone cleanup on very large shards is documented as a performance problem. The 300-million-object example on that page is a suggested starting point, not a measurement. No page in the set that was read uses the words “cold start.” ([Vector index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index))

## E. Hybrid search

Hybrid search runs a dense vector search and a BM25 keyword search in parallel, then fuses the scores. The how-to page calls the keyword leg BM25F. The concept page calls it BM25. They describe the same fused query. The inverted-index reference’s example labels `invertedIndexConfig` as the “sparse index.” That index is the token inverted index. The pages that were read do not describe a separate user-supplied sparse embedding such as SPLADE. ([Hybrid concepts](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search), [Hybrid how-to](https://docs.weaviate.io/weaviate/search/hybrid), [Inverted index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/inverted-index))

Collection-level BM25 defaults are `k1` 1.2 and `b` 0.75. A `bm25` object on a property is discarded. Both parameters are mutable. Query operators, added in v1.31, are `or` (default), `and`, and `and_cross` (from v1.38.8, every token must match somewhere across the searched properties). Properties can be selected and boosted (`question^2`). ([Inverted index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/inverted-index), [Hybrid how-to](https://docs.weaviate.io/weaviate/search/hybrid))

**Fusion.** The default since v1.24 is `relativeScoreFusion`: each leg is scaled so its best score is 1 and its worst is 0, then the two normalized scores are combined with alpha. `rankedFusion`, the default through v1.23, ignores the raw scores and uses `1 / (rank + 60)` on each list, then adds those rank scores. The concept page prefers relative score fusion because it keeps score gaps that rank fusion throws away. That preference is a design statement, not a measured win on a public dataset. ([Hybrid concepts](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search), [Search operators](https://docs.weaviate.io/weaviate/api/graphql/search-operators))

Alpha is the vector weight. 0 is keyword only. 1 is vector only. The server default is 0.75 when the request omits alpha. That omission works for GraphQL, and for gRPC from v1.36.7. Client libraries often send their own alpha, and the docs warn that the effective mix can differ from 0.75 and can even be keyword-only. `max vector distance` drops vector-leg hits beyond a distance. It does not apply to BM25 or to the fused score, because BM25 is unbounded. ([Hybrid concepts](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search), [Hybrid how-to](https://docs.weaviate.io/weaviate/search/hybrid))

BlockMax WAND, added in v1.30 and on by default, skips irrelevant inverted-index blocks during BM25 and hybrid search. Collections created before v1.30 need the v1.30 migration to use the on-disk format. Scores can differ slightly from the older WAND. Single-property versus multi-property scores can differ because IDF and length normalization differ. The docs call that expected. An October 2024 BM25F fix, in v1.24.26, v1.25.20, v1.26.6, and v1.27.0, sped segment merges and fixed a multi-property segment bug. ([Inverted indexes](https://docs.weaviate.io/weaviate/concepts/indexing/inverted-index), [Migration](https://docs.weaviate.io/deploy/migration))

A minimal official example is the Python client call `collections.use("JeopardyQuestion").query.hybrid(query="food", fusion_type=HybridFusion.RELATIVE_SCORE, limit=3)`. The same guide’s GraphQL form sets `fusionType: relativeScoreFusion`. GraphQL on Weaviate Cloud is being turned off. Self-hosted Weaviate keeps GraphQL at least until 2027-05-01. The vector-index page also shows a Docker Compose snippet pinned to `weaviate:1.40.4` with `ASYNC_INDEXING: "true"`. ([Hybrid how-to](https://docs.weaviate.io/weaviate/search/hybrid), [Vector index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index))

## F. Metadata filtering and multi-tenancy

Filtered vector search is pre-filtering. The inverted index builds an allow-list of ids, and HNSW walks its edges as usual but only admits ids on that list. The docs say a post-filter can return fewer than `k` hits when the filter is tight, and that filtered recall is typically no worse than unfiltered recall because the graph is still fully walked. If the filter is very restrictive, traversal becomes close to exhaustive, so Weaviate can switch to a brute-force search on the allow-list. `flatSearchCutoff` defaults to 40000, and 0 forces a vector-index search. The reference page does not say whether 40000 is an object count. The concept page’s figure uses an illustrative cutoff near 15% of the dataset. Those two numbers were not reconciled. ([Filtering](https://docs.weaviate.io/weaviate/concepts/filtering), [Vector index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index))

HNSW filter strategies are `sweeping`, `acorn` (default as of v1.34), and `pathseer` (v1.40). The strategy can be changed without a reindex. Downgrade from v1.40 requires leaving `pathseer` first. The docs say Weaviate’s `acorn` is a custom implementation inspired by the ACORN paper, and that it helps when the filter is weakly correlated with the query. `pathseer` is attributed to the SIGMOD 2026 paper “PathSeer,” and the docs say Weaviate’s own benchmarks found it fastest or within a few percent, with ACORN still faster for sparse filters negatively correlated with the query. Those papers were not opened. ([Filtering](https://docs.weaviate.io/weaviate/concepts/filtering))

The performance page says a filter alone uses the inverted index, a vector search alone uses HNSW, and the combination costs more when the filter returns fewer candidates because the vector search skips more of the graph. It also says “Sub-50ms 20NN-vector queries on datasets of over 1–100M objects are possible.” That sentence has no hardware or recall attached. It is a vendor claim. ([Index types and performance](https://docs.weaviate.io/weaviate/more-resources/performance))

**Multi-tenancy** is off by default, must be set at collection creation, and cannot be turned on later. Each tenant is one shard, so tenant data is not visible across tenants. Tenants are not a substitute for a query that must span subsets. The best-practices page recommends multi-tenancy only when subsets share a schema and settings and are never queried together. Tenant states are `ACTIVE` (served), `INACTIVE` (on disk, not served), and `OFFLOADED` (cloud storage, not on local disk). v1.26 renamed `HOT` to `ACTIVE` and `COLD` to `INACTIVE`. Names are 4–64 characters. `autoTenantCreation` exists from v1.25.0 for batches. Offload is documented as open-source only, not Weaviate Cloud. Backups omit offloaded tenant data. Backup of inactive tenants arrived in v1.37.0. Tenant activity is Raft metadata. ([Multi-tenancy](https://docs.weaviate.io/weaviate/manage-collections/multi-tenancy), [Best practices](https://docs.weaviate.io/weaviate/best-practices), [Replication architecture](https://docs.weaviate.io/weaviate/concepts/replication-architecture))

## G. Notable changes, 2024–2026

Dates below come from “added in” notes on the current docs, the archived named-vector note, and the newest GitHub release page. Every minor release note was not read line by line.

- **v1.24:** `relativeScoreFusion` becomes the default. Named vectors are documented from v1.24.0 in the archived collection reference.
- **v1.25:** Raft for schema and tenant activity. Auto-tenants. Dynamic index marked experimental. Upgrading a Kubernetes cluster into 1.25 is a manual migration.
- **v1.26:** Range filters. Tenant states renamed to `ACTIVE` and `INACTIVE`.
- **v1.29:** Multi-vector embeddings and MaxSim.
- **v1.30:** BlockMax WAND on by default. Collections created earlier need a migration, and BM25 scores can shift.
- **v1.31:** BM25 `and` / `or` operators. Scalar quantization can be enabled on an existing collection. HNSW snapshots.
- **v1.32:** Replica movement, so existing shards can finally move. 8-bit RQ on HNSW.
- **v1.33:** 1-bit RQ on HNSW. `DEFAULT_QUANTIZATION`.
- **v1.34:** ACORN becomes the default filter strategy.
- **v1.35:** RQ on the flat index.
- **v1.36:** HFresh. Lazy shard loading. Snapshots enabled by default. From v1.36.0, shards recover from memory-pressure read-only.
- **v1.37:** Accent folding and custom stopword presets (preview). Inactive-tenant backups.
- **v1.38:** Async replication on by default when the factor is greater than 1. `and_cross` at v1.38.8.
- **v1.39:** HNSW snapshot environment variables deprecated and ignored.
- **v1.40:** PathSeer. Dropping a named vector. MUVERA multi-vector on HFresh. `rq-4` as a `DEFAULT_QUANTIZATION` value. v1.40.4 is the patch checked here (2026-11-05).

([Vector index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index), [Indexing](https://docs.weaviate.io/weaviate/starter-guides/managing-resources/indexing), [Migration](https://docs.weaviate.io/deploy/migration), [Filtering](https://docs.weaviate.io/weaviate/concepts/filtering), [Releases](https://github.com/weaviate/weaviate/releases))

Generative and reranker modules are configurable separately from the vector index. Module settings for those two became mutable in v1.26.8 and v1.27.1. The v1.40.3 notes fix rerank and generate so they run once on a nearText sub-search, which shows they are attached stages, not the BM25 or HNSW ranker. The rerank scoring formula was not read. ([Collection definition](https://docs.weaviate.io/weaviate/config-refs/collections), [v1.40.3](https://github.com/weaviate/weaviate/releases/tag/v1.40.3))

## H. Strengths and limitations for text retrieval

**Strengths**

- One process holds the objects, BM25, dense search, filters, and optional multi-vector late interaction.
- The fusion method is named, and alpha is an explicit knob. Relative score fusion puts the two legs on a 0–1 scale before mixing them.
- Pre-filtering stays on the HNSW graph, with ACORN and PathSeer as swappable strategies.
- Tenants have active, inactive, and offloaded states, so a quiet tenant does not have to stay in the serving set.
- The path from one Docker node to a Raft cluster, or to Weaviate Cloud, stays on the same database.

**Limitations**

- The HNSW working set is an in-memory structure, and the two official RAM write-ups do not match.
- The vector cache dumps itself entirely when it fills, which collapses import speed.
- Dynamic-index conversion is one way. HFresh trades peak throughput and drops dot-product distance. Quantization cannot be turned off once set.
- The keyword leg is BM25 over Weaviate’s inverted index. A user-supplied sparse embedding such as SPLADE was not found on the pages that were read.
- Client libraries can send their own alpha and silently ignore the 0.75 server default.
- BlockMax WAND can change scores after the v1.30 migration.
- Tenants cannot be queried together. Offload is absent from Cloud and from backups.
- New nodes do not receive old shards until replica movement.
- A single query does not span cores. Data consistency is tunable and availability-leaning. Only metadata is Raft.

([Documentation home](https://docs.weaviate.io/), [Hybrid concepts](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search), [Filtering](https://docs.weaviate.io/weaviate/concepts/filtering), [Resource planning](https://docs.weaviate.io/weaviate/concepts/resources), [Horizontal scaling](https://docs.weaviate.io/weaviate/concepts/cluster))

For a short demo, use one Docker node on the 1.40 line, HNSW, `relativeScoreFusion`, and an explicit alpha of 0.5 or 0.75. Budget RAM with the resource-planning formula (about twice the float32 vector bytes, plus link overhead) and say in the talk that the best-practices 6 GB / 1.5 GB / 2 GB figures do not match that formula. Turn on 8-bit RQ, or move to HFresh, only when the vector set will not fit. Mention a Kubernetes cluster for availability or read scale, and say that extra nodes sit idle for existing data until replica movement.

## I. Sources

1. [What is Weaviate?](https://docs.weaviate.io/) The project’s own one-page description of objects, vectors, and hybrid retrieval.
2. [README and LICENSE](https://github.com/weaviate/weaviate/blob/main/README.md) The dual license, and the quickstart tag that is still behind the release.
3. [Hybrid search concepts](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search) The fusion formulas and the alpha warning. This is the keyword-plus-dense story.
4. [Hybrid search how-to](https://docs.weaviate.io/weaviate/search/hybrid) The shortest official query example, and the BM25F wording.
5. [Resource planning](https://docs.weaviate.io/weaviate/concepts/resources) What RAM, CPU, and disk actually bound, including the 2× formula.
6. [Best practices](https://docs.weaviate.io/weaviate/best-practices) The other RAM figures, lazy loading, and when multi-tenancy is recommended. Read it next to resource planning because the numbers disagree.
7. [Filtering](https://docs.weaviate.io/weaviate/concepts/filtering) Allow-list pre-filtering, ACORN, and PathSeer.
8. [Vector index reference](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index) HNSW, flat, dynamic, HFresh, and the compression knobs.
9. [Replication architecture](https://docs.weaviate.io/weaviate/concepts/replication-architecture) Raft for metadata, leaderless replicas for objects.
10. [Migration](https://docs.weaviate.io/deploy/migration) The v1.25 Raft upgrade and the v1.30 BM25 format change.
11. [Multi-tenancy](https://docs.weaviate.io/weaviate/manage-collections/multi-tenancy) One shard per tenant, and the three activity states.
12. [Releases](https://github.com/weaviate/weaviate/releases) v1.40.4 is the patch this note is pinned to.

Not used as evidence: Weaviate Academy, the fusion blog linked from the hybrid concept page, and the ACORN, PathSeer, and SPFresh papers. The papers are the right next read for the filtered-ANN and disk-index ideas. They were not opened, so nothing above is taken from them. Weaviate was not started.
