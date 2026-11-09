# Qdrant, Weaviate, Milvus, and pgvector

Comparison for a CS410 Technology Review on self-hosted vector databases for text retrieval. Versions checked on 2026-11-09:

| System | Revision checked |
|---|---|
| Qdrant | v1.20.0, released 2026-10-22, commit `222b2e4`. Live docs the same day. |
| Weaviate | v1.40.4, released 2026-11-05. Live docs the same day. The README quickstart still pins image tag `1.36.0`. |
| Milvus | v3.0.5, released 2026-10-30. Docs branch `v3.0.x` at `0902cf3` (2026-11-09). `milvus.io` returned 403, so citations are the docs repository. |
| pgvector | 0.8.7, changelog date 2026-10-01. Master `bcbb135` lists 0.9.0 as unreleased. Lexical half: PostgreSQL 18, chapters 12.1, 12.3, and 12.9. |

Confidence is **partial**. pgvector’s own README and changelog are internally consistent. The other three have official pages that disagree with each other, and those disagreements are marked below. Nothing in this review was measured by running the databases. Vendor recall and speedup figures are the vendor’s.

The four individual notes are [qdrant.md](qdrant.md), [weaviate.md](weaviate.md), [milvus.md](milvus.md), and [pgvector.md](pgvector.md).

## Side-by-side

### What it is

| | Qdrant | Weaviate | Milvus | pgvector |
|---|---|---|---|---|
| Product | Vector database written in Rust. A point is a vector plus a JSON payload. | Database that stores each object with its vectors. | Cloud-native vector database, Go and C++, LF AI & Data. | PostgreSQL extension. `CREATE EXTENSION vector`. |
| Design goal | Filtering inside the index, so semantic match and faceted search share one store. | Semantic similarity and keywords on the same objects, including as a RAG store. | Similarity search on large embedding collections plus structured metadata. | “Store your vectors with the rest of your data.” |
| License | Apache 2.0 | BSD-3-Clause outside `wl/`. Enterprise license inside `wl/`. Binaries combine both. Enterprise features need a key. | Apache 2.0 | PostgreSQL License |

### How search is stored

| | Qdrant | Weaviate | Milvus | pgvector |
|---|---|---|---|---|
| Dense index | HNSW only. Defaults `m` 16, `ef_construct` 100. | HNSW by default (`maxConnections` 32, `efConstruction` 128). Also flat, dynamic, and HFresh. | Knowhere over Faiss, HNSW, DiskANN, SCANN, IVF variants, and GPU indexes. HNSW defaults `M` 30, `efConstruction` 360. The Knowhere page still mentions Annoy. The current index table does not. | HNSW and IVFFlat. Defaults `m` 16, `ef_construction` 64, `ef_search` 40. Exact scan is the default when no index exists. |
| Keyword index | Full-text payload index, and a separate exact sparse index (dot product only). | Per-property inverted index. BM25 on `indexSearchable`. | Built-in BM25 function writing a sparse vector, plus caller-supplied sparse vectors such as SPLADE. | PostgreSQL `tsvector`. Preferred index is GIN. This is Postgres, not the extension. |
| Several vectors per item | Named vectors since v0.10. Multivectors for late interaction such as ColBERT. | Named vectors since v1.24. Multi-vector MaxSim since v1.29. On HFresh, multi-vector imports require MUVERA. | Several named vector fields on one collection, up to a proxy limit of 10. This is not a ColBERT matrix type. | Another column. No named-vector or multivector type. |
| Dimension cap | Source and the vectors guide: 1 to 65,536 inclusive. The FAQ says 65,535. Source wins. Multivector flattened floats must be under 1,048,576. That cap was not re-checked in source. | Archived FAQ says 65,535. Current pages and a sample of v1.40.4 source files do not restate it. Treat it as possibly stale. | 32,768. | Indexed: `vector` 2,000, `halfvec` 4,000, `bit` 64,000, `sparsevec` 1,000 non-zero elements. Storage caps are higher for `vector` and `halfvec` (16,000). |

### Deployment

| | Qdrant | Weaviate | Milvus | pgvector |
|---|---|---|---|---|
| Single node | Docker, binary, or Kubernetes. The quick start has no authentication and listens on all interfaces. | Docker. No native Windows build. Embedded mode is experimental. | Standalone: one Docker image, embedded Woodpecker. Also Milvus Lite, a Python library. | Postgres plus the extension. Docker tags for Postgres 13–18. Compile needs Postgres 13+ on the 0.8.7 README. |
| Cluster | Raft. You place shards and replicas. At least three nodes. Shard count is fixed at creation. No open-source resharding. | Kubernetes. Raft for schema and tenant state since v1.25. Object replicas are leaderless. Adding a node does not move old shards until replica movement (v1.32). | Kubernetes. Proxy, coordinator, streaming, query, and data nodes, plus etcd and object storage. No online upgrade from Standalone. | Postgres WAL replicas. Citus or PgDog are named by the README. They are not pgvector features. |
| Managed | Managed Cloud, Hybrid Cloud, Private Cloud. Qdrant Edge is an in-process library, not the server. | Weaviate Cloud. DigitalOcean is a separate managed preview. | Zilliz Cloud: Serverless, Dedicated, BYOC. Internals were not documented on the pages read. | Whatever hosted Postgres packages the extension. The provider list is GitHub issue 54, which was not opened. |

### Resources

| | Qdrant | Weaviate | Milvus | pgvector |
|---|---|---|---|---|
| What must be in RAM | Dense vectors and HNSW default to `cached`. Payloads default to `cold`. Sparse vectors are disk-only. | The HNSW graph. The docs say object text is not the limiting factor. | Full-load mode: segment data and indexes on the QueryNode, under 90% of query-node memory. | The index is faster in RAM. It does not have to fit. HNSW builds are much faster when the graph fits in `maintenance_work_mem`. |
| Sizing | Published formulas. A worked example: 1M points, replication 2, 768-d float32, cached, is about 5.72 GB of vectors. The same example with pinned 4-bit TurboQuant and cold originals is about 0.72 GB. | Two official notes disagree. Resource planning uses about 2× the float32 bytes. Best practices says about 6 GB for 1M × 1024-d, which is not 2× (that would be 8 GB). | No general byte formula. An IVF arithmetic example is published for 1M × 128-d. DiskANN, mmap, and tiered storage are the documented off-ramps. | No HNSW byte formula. `halfvec` and `binary_quantize` plus a re-rank are the documented shrink path. `shared_buffers` at 25% of RAM is quoted PgTune advice, not a pgvector benchmark. |
| CPU | Matters most while ingesting and indexing. Default indexing uses up to 16 threads. Optional GPU indexing. | Each search and each insert is single-threaded. More shards use more cores. The database process does not use GPUs. | Builds and queries raise CPU. A segment under 1,024 rows can be searched brute-force. | Distance math, builds, and scans. Linux x86-64 dispatch since 0.7.0. Default builds may use `-march=native`. |
| Disk | Everything is also on disk. On-disk vectors want local SSDs of at least 50,000 IOPS, per the capacity page. Avoid a cold HNSW graph. | LSM, default `mmap`. Prefer SSD, ext4 or XFS. Do not put the data path on NFS. | Object storage is the copy of record (MinIO, S3, and others). etcd holds metadata. Local cache and mmap sit on QueryNodes. | Ordinary Postgres. A non-partitioned table is 32 TB by default. HNSW vacuum can take a long time. |

### Hybrid search

| | Qdrant | Weaviate | Milvus | pgvector |
|---|---|---|---|---|
| Lexical leg | BM25 on a full-text payload index since v1.20, or BM25 as a sparse vector. The two paths do not share stemming, stopwords, or `k`/`b` defaults. No BM25F. | BM25 over the inverted index. The how-to page says BM25F. The concept page says BM25. No user-supplied sparse embedding was found on the pages read. | Built-in BM25 (`k1` 1.2, `b` 0.75) or a caller-supplied sparse vector. | `ts_rank` or `ts_rank_cd` on a `tsvector`. PostgreSQL 18 does not document BM25. `sparsevec` is not a lexical weight vector. |
| Fusion | `rrf` or `dbsf`. | `relativeScoreFusion` (default since v1.24) or `rankedFusion`. | `RRFRanker` or `WeightedRanker`. | The README names reciprocal rank fusion or a cross-encoder and does not define either. You write the SQL. |
| Default mix | RRF, `k` default 2, zero-based rank, weights default to 1. | Alpha 0.75 when the request omits it. Client libraries often send their own alpha. | RRF `k` default 60. The worked table uses rank 1. A code sample passes `k` 100. | None. |

### Filtering and tenancy

| | Qdrant | Weaviate | Milvus | pgvector |
|---|---|---|---|---|
| Filter and ANN | Filterable HNSW walks the graph with extra edges from payload indexes that existed at build time. Very small candidate sets can full-scan. ACORN since v1.16 looks past filtered-out neighbors. | Allow-list pre-filter, then the HNSW walk. `flatSearchCutoff` default 40000 can fall back to brute force. The unit of 40000 is not stated. Strategies: sweeping, ACORN (default since v1.34), PathSeer (v1.40). | Standard mode filters first, then ANN. Iterative mode walks vector hits until top-K survives. Heuristic: over about 98% filtered out, use FLAT. The page says the heuristic is not always right. | `WHERE` runs after the approximate scan. At `ef_search` 40 and a predicate matching 10% of rows, about 4 rows survive. Iterative scans since 0.8.0 keep walking. |
| Tenancy | A tenant payload field, optional dedicated shards since v1.16. `is_tenant` co-locates points. It is not authorization. | Off by default. One shard per tenant. Cannot be queried across. States: active, inactive, offloaded. Must be chosen at creation. | Database, collection, partition (1,024), or partition key (“millions,” many tenants per physical partition). RBAC stops at database and collection. | List partitioning or separate tables, because one shared HNSW couples tenants’ recall. Row-level security is Postgres, and the README does not present it as the vector pattern. |

### What changed, 2024–2026

| Year | Qdrant | Weaviate | Milvus | pgvector |
|---|---|---|---|---|
| 2024 | Query API and hybrid fusion (v1.10). DBSF (v1.11). Vectors move to mmap (v1.12). v1.13 and v1.14 notes were not read. | Relative score fusion becomes the default (v1.24). Raft metadata (v1.25). Multi-vector embeddings (v1.29). | Sparse vectors and multi-vector RRF (2.4). In-server BM25 on raw text (2.5, December 2024). | `halfvec`, `sparsevec`, binary quantization (0.7, April). Iterative scans (0.8, October). |
| 2025 | Phrase match, stemmer, asymmetric quantization, off RocksDB (v1.15). ACORN, tenant promotion, configurable RRF `k` (v1.16). | BlockMax WAND (v1.30), which can change BM25 scores. Replica movement (v1.32). ACORN default (v1.34). HFresh (v1.36). | Streaming node GA, Woodpecker replaces Kafka/Pulsar, phrase match (2.6, August 2025). Storage-v2 speedups in the release notes are the project’s figures. | Mostly fixes. 0.8.1 adds Postgres 18 rc1 support (September 2025). |
| 2026 | Weighted RRF (v1.17). TurboQuant and the memory tiers (v1.18, v1.19). BM25 on the payload text index (v1.20, October). | Async replication on by default when replicated (v1.38). PathSeer, drop a named vector, MUVERA on HFresh (v1.40). | TEXT fields and new sparse indexes, both opt-in (3.0, July). Storage V3 off by default on 3.0.5, and turning it on blocks rollback to 2.6. | 0.8.2 through 0.8.7 are fixes, including HNSW vacuum corruption in 0.8.3–0.8.4. 0.9.0 is unreleased. |

## Trade-offs

Pick **pgvector** when the documents, the metadata, and the embeddings already belong in one Postgres, and the operator would rather add an extension than a second database. Exact search stays available. Filters are SQL. The lexical ranker is `ts_rank_cd`, and the fusion step is SQL the application writes. The project’s own scale path never leaves Postgres: quantize, a bigger machine, replicas, or Citus/PgDog. The cost is that BM25, a fusion operator, and an in-index filter strategy are not in the extension.

Pick **Qdrant** when one self-hosted process should do filterable HNSW, BM25, and a named fusion, and you want a published RAM formula before you buy the machine. The open-source cluster does not reshard itself, and the tenant flag is not access control. RRF with the default `k` of 2 is the fusion to show first, because cosine and BM25 are not on the same scale.

Pick **Weaviate** when the keyword leg should be BM25 inside the same server as the objects, with an explicit alpha, and when tenants should be able to go inactive or offloaded. Budget RAM from the resource-planning page (about twice the float32 vector bytes) and say out loud that the best-practices page’s gigabyte figures do not match that formula. A new node does not receive old shards until replica movement. Client libraries can override alpha without you noticing.

Pick **Milvus** when one collection must hold dense vectors and BM25, the corpus is heading past one machine, and you accept etcd plus object storage as the bill of materials. Standalone is the demo. Distributed is the production shape when one server’s RAM or availability is the limit, and it cannot be reached by an online upgrade from Standalone. The 90% query-node load ceiling is the capacity rule the docs actually give. Storage V3 and the 3.0 sparse-index changes are opt-in.

Do not rank these four from a vendor recall table. Qdrant’s quantization page, Weaviate’s “98–99%” rotational-quantization sentence and “sub-50ms” sentence, and Milvus’s storage and QPS multiples are each project’s own numbers. They were not rerun, and they do not share a dataset.

## Cross-cutting

### Hybrid fusion in practice

“They all use RRF” is the wrong sentence. The formulas differ.

**Qdrant RRF** sums `1/(k + rank)` with zero-based rank and default `k` of 2. Weighted RRF, since v1.17.0, uses `1/(k + (rank+1)/weight − 1)`. The docs say a fixed alpha on raw cosine and raw BM25 is unreliable because the scales differ and shift per query. **DBSF**, since v1.11.0, keeps the raw scores, computes mean and standard deviation on that query’s prefetch hits only, and remaps with a 3-sigma window. Identical scores, or a single hit, become 0.5. One outlier in a short prefetch can skew a query. The project’s choice table: weighted RRF when you have an eval set, DBSF when you trust score magnitude and have no eval set, plain RRF otherwise. Qdrant’s tuning page says the 2009 RRF paper’s `k` of 60 corresponds to `k` of 61 in Qdrant’s zero-based formula. The paper was not fetched. ([Hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/), [Tuning](https://qdrant.tech/documentation/search-tuning/how-to-tune-hybrid-search/))

**Weaviate relative score fusion**, the default since v1.24, min-max scales each list so the best raw score is 1 and the worst is 0, then mixes them with alpha. **Ranked fusion**, the default through v1.23, scores a hit as `1/(rank + 60)`. Alpha 0 is keyword only and alpha 1 is vector only. The server uses 0.75 only when the request omits alpha. Set it explicitly in the client. ([Hybrid concepts](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search))

**Milvus RRF** uses `1/(k + rank)` with default `k` of 60 and rank starting at 1, so the best hit on one list scores 1/61. The recommended band is [10, 100]. **Weighted Ranker** can arctan-normalize scores into `[0, 1]` before applying weights, because inner product and L2 are not comparable. The numeric example on that page does not show the arctan step. Weights are each in `[0, 1]` and do not have to sum to 1. The limits table says hybrid search on `SPARSE_INVERTED_INDEX` supports only `RRFRanker`. The weighted-ranker guide does not repeat that restriction. Unresolved. ([RRF](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/userGuide/embeddings-reranking/reranking/rrf-ranker.md), [Weighted ranker](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/userGuide/embeddings-reranking/reranking/weighted-ranker.md), [Limits](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/about/limitations.md))

**pgvector** names reciprocal rank fusion and does not ship it. The README’s hybrid SQL is `plainto_tsquery` and `ts_rank_cd`. Fusion lives in application SQL. Summing two distance operators, per the maintainer on issue 623, skips the index and runs an exact scan. ([README](https://github.com/pgvector/pgvector/blob/master/README.md), [Issue 623](https://github.com/pgvector/pgvector/issues/623))

For a talk, put the four formulas on one slide. Then say they have to be tuned on a labeled set you hold out. Qdrant’s own tuning page already picks nDCG@10 for that, and it warns that scoring the queries you used to pick the weights inflates the number.

### Embedding models, and what they force

The model’s dimension has to fit the index, not just the column.

- Qdrant’s validator accepts 1 through 65,536 dense dimensions. A ColBERT-style multivector is capped by the FAQ at fewer than 1,048,576 flattened floats. Quantization is scalar (4×), product (up to 64×), binary (up to 32×), and TurboQuant (4× to 32×, queries stay full precision). The FAQ says the original vectors are still required to rescore and to rebuild quantization. The v1.19 notes say 4-bit TurboQuant can be the stored datatype so the originals need not be stored. Those two texts were not reconciled.
- Weaviate compresses per named vector: PQ, BQ (about 32×), SQ (4×), and RQ at 8, 4, or 1 bit. The indexing guide recommends 8-bit RQ first because it needs no training step. Once quantization is set, it cannot be disabled. PQ wants on the order of 10,000 to 100,000 vectors per shard before training. Multi-vector models (ColBERT, ColPali, ColQwen) are supported. On HFresh they require MUVERA, which is 1-bit RQ. The “98–99% recall” sentence for 8-bit RQ is an internal test.
- Milvus lists a 32,768 dimension maximum. SQ8 is described as one byte per dimension. IVF-PQ’s example compression is 4–32×, with lower recall. Multi-vector means extra fields, such as one dense field and one sparse field, not a token matrix. A model that emits both a dense vector and a SPLADE vector fits this shape. A ColBERT matrix does not, on the pages that were read.
- pgvector indexes 2,000 float32 dimensions, 4,000 half-precision, or 64,000 bits. A 3072-dimensional float32 model does not fit an HNSW index on `vector`. It can use `halfvec` up to 4,000, or binary quantization at 64,000 bits with a re-rank against the original column. There is no multivector type.

Quantization recall is data-dependent on every system that states it. Rescoring reads the original vectors. If those vectors are on disk, the rescore is a random read.

### How to read a benchmark

Three numbers show up, and they answer different questions.

**Recall@k** is the fraction of the true nearest k that the approximate search returned. pgvector is the most direct of the four: exact search with no approximate index “provides perfect recall,” and the monitoring section says to measure recall by comparing approximate results with exact search (`SET LOCAL enable_indexscan = off`). Speed debugging is `EXPLAIN (ANALYZE, BUFFERS)`. It does not name recall@k, p99, or QPS. Weaviate’s own ANN benchmark page measures Recall@10 and Recall@100, multi-threaded QPS, mean latency, p99, and import time, over 10,000 requests, including network and full object retrieval, on unfiltered search only. The result cells did not survive extraction, so no Weaviate QPS figure is repeated here. The page says this differs from ann-benchmarks, which returns ids from an embedded library. Qdrant’s hybrid tuning page uses **nDCG@10**, which cares about graded relevance and rank position, not only whether the true neighbor appeared. Milvus’s index guide tells the operator to balance build time, QPS, and recall, then says to tune recall on their own data.

A benchmark that returns ids from a library, a benchmark that returns full objects over the network, and a benchmark of hybrid fusion are three different tests. An unfiltered recall number does not predict a filtered workload. Weaviate’s ANN page is unfiltered. Qdrant’s quantization sweeps are the vendor’s, and the page itself says 100 queries are not a confidence interval.

**Latency** without hardware, recall, and whether the filter was on is not comparable. Weaviate’s “sub-50ms” sentence has no hardware or recall attached. Qdrant’s capacity page says that, for on-disk vectors, keeping half as many vectors in RAM roughly doubles search latency. That is a rule of thumb on one page, not a cross-system result.

**Filters change the index.** Each project documents a different failure:

- pgvector post-filters, so a selective `WHERE` can starve `LIMIT`.
- Qdrant full-scans when the estimated match set is under `full_scan_threshold`, and a payload index created after the graph does not add edges until a rebuild.
- Weaviate can drop to a flat scan past `flatSearchCutoff`, and ACORN matters most when the filter is weakly correlated with the query.
- Milvus’s own heuristic switches to brute-force FLAT when the filter removes almost everything, and iterative filtering can itself get slow when many hits fail the predicate.

### Production pitfalls

**Index build.** pgvector emits `NOTICE: hnsw graph no longer fits into maintenance_work_mem` and the build gets much slower. Build after the initial `COPY`, and use `CREATE INDEX CONCURRENTLY` in production. Docker needs `--shm-size` at least as large as `maintenance_work_mem`. IVFFlat must be built after the table has data. Qdrant builds HNSW in the background. Segments under the indexing threshold stay on a full scan, so “indexed vector count” can be lower than the point count while status is still green. A restart during optimization can leave the collection grey, and search falls back to a full scan. Weaviate says HNSW is costly when data arrives during the build. `ASYNC_INDEXING=true` is required for the dynamic index on self-hosted servers, and it defaults to false. Tombstone cleanup on very large shards is a documented performance problem. Milvus will not search a collection that is not loaded.

**Cold start.** Milvus’s load step pulls index files and raw field data into query-node memory and is the documented cold-start analogue. Tiered storage, from the 2.6.4 docs onward, loads only segment metadata first, and the guide says cold queries can be slower. Qdrant v1.18 adds a low-memory startup mode that opens storage on disk “to minimize out of memory crash on startup,” and a strict-mode resident-memory limit. Weaviate’s pages that were read do not use the words “cold start.” What they do document is a vector cache that drops entirely and refills from disk when it fills, and lazy shard loading after a collection passes 1,000 shards or 100 GB. pgvector has no separate process cold-start section. The practical equivalent is the first queries after a restart, which are faster when the index is in RAM, plus a long HNSW vacuum. The 0.8.3 and 0.8.4 fixes for HNSW vacuum corruption are a reason to be on 0.8.7 rather than an earlier 0.8 patch.

**Memory estimation.** Use Qdrant’s capacity-planning formulas when the system is Qdrant, and say they are formulas plus a worked example, not a measurement of your corpus. For Weaviate, use the resource-planning 2× rule and treat the best-practices gigabyte figures as a conflicting official note. For Milvus, plan to the 90% query-node ceiling and then benchmark. The IVF arithmetic example does not generalize to HNSW. For pgvector, size `maintenance_work_mem` so the build fits, check index size with `pg_relation_size`, and expect search to be better when that index is cached. None of the four publishes a row count at which it stops being the right tool.

**Other traps that are written down.** Qdrant’s quick-start container has no authentication. Weaviate client alpha can silently disagree with the 0.75 server default, and BlockMax WAND can shift BM25 scores after the v1.30 migration. Milvus Standalone cannot be upgraded online into a cluster, and enabling Storage V3 blocks rollback to 2.6. pgvector binaries built with `-march=native` can raise `Illegal instruction` on another machine. A Qdrant or Weaviate tenant filter is a query convention unless something else enforces it. A Milvus partition key is not RBAC.

### When a dedicated vector database is the wrong tool

pgvector’s opening line is the scoping statement: store the vectors with the rest of the data, and keep ACID, point-in-time recovery, and JOINs. Exact nearest neighbor is the default, so an approximate index is optional. The scaling section tells the operator to grow one Postgres machine, then replicas or Citus or PgDog. It never states a row count at which Postgres stops being enough.

Qdrant, Weaviate, and Milvus pages that were read do not hand the workload back to PostgreSQL. Each documents its own BM25. Absence is the finding. It is not a claim that they recommend a dedicated database for every corpus.

A comment on a pgvector issue that “pgvector is pretty good up to 10kk” cites a Supabase blog. That comment is not a maintainer statement, and the blog is not evidence. No row-count ceiling from these sources belongs on a slide.

The operational reading, for a sysadmin choosing a system:

- Stay in Postgres when the text, the metadata, and the embeddings are already one database, the dimension fits `vector` or `halfvec`, and you can write the fusion query yourself.
- Stay on an exact scan while the planner’s cost is acceptable. pgvector treats the approximate index as the thing that gives up recall.
- Add a dedicated engine when you want the fusion and the in-index filter as product features, or when the working set and the availability target are past one Postgres machine and you do not want to operate Citus or PgDog.
- Do not add Milvus Distributed, or a Qdrant or Weaviate cluster, as the first sketch of a corpus that fits on one node. The cluster features that look automatic (resharding, rebalancing) are the ones the open-source docs mark as manual or absent.

### Minimal examples from the official docs

Qdrant. The hybrid-queries page shows `POST /collections/{collection_name}/points/query` with two prefetches and `"query": { "rrf": {} }`. One prefetch is a BM25 `query.text` on a payload field. The other is a dense vector `using` a named vector. Each prefetch `limit` in that example is 20, and the outer `limit` is 10. Defaults only: no custom `k` and no weights. Copy the body from the page rather than from memory. The field names for text versus the named vector are easy to swap. ([Hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/))

Weaviate. The hybrid how-to uses `collections.use("JeopardyQuestion").query.hybrid(query="food", fusion_type=HybridFusion.RELATIVE_SCORE, limit=3)`. The same guide’s GraphQL form sets `fusionType: relativeScoreFusion`. Set alpha in that call. A client that sends its own alpha will not use the server default of 0.75. GraphQL on Weaviate Cloud is being turned off. Self-hosted Weaviate keeps GraphQL at least until 2027-05-01. The vector-index page also shows a Docker Compose snippet pinned to `weaviate:1.40.4` with `ASYNC_INDEXING: "true"`. ([Hybrid how-to](https://docs.weaviate.io/weaviate/search/hybrid), [Vector index](https://docs.weaviate.io/weaviate/config-refs/indexing/vector-index))

Milvus. The RRF page shows `MilvusClient.hybrid_search` on two `AnnSearchRequest`s. One is `text_vector` with the string `"modern dining table"`. The other is `image_vector` with a prepared embedding. Each request `limit` is 10. The ranker is `RRFRanker(k=100)`, and the outer `limit` is 10. The collection is assumed to already exist. `k=100` is the sample. The documented default is 60. ([RRF ranker](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/userGuide/embeddings-reranking/reranking/rrf-ranker.md))

pgvector, exact distance, then an HNSW index. ([README](https://github.com/pgvector/pgvector/blob/master/README.md))

```sql
CREATE EXTENSION vector;
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;
CREATE INDEX ON items USING hnsw (embedding vector_l2_ops);
```

The hybrid example in that README is a `ts_rank_cd` query. It is not a fused vector query.

### Ranked resources

These are the pages worth saving for the CS410 library. The first twelve are sources this review actually used. The last two are papers the projects cite and this review did not open. A short paragraph says why each one is worth a student’s time.

1. [pgvector README](https://github.com/pgvector/pgvector/blob/v0.8.7/README.md). This is the whole extension in one page: types, distance operators, HNSW and IVFFlat, the post-filter failure mode, iterative scans, and the one paragraph that says hybrid search is Postgres full text plus something you write. Read it before any blog post about pgvector, because the blogs tend to invent a BM25 operator the README does not have.

2. [PostgreSQL 18, full-text search](https://www.postgresql.org/docs/18/textsearch.html). Chapters 12.1, 12.3, and 12.9 are the lexical half of a pgvector hybrid system. They define `tsvector`, `ts_rank_cd`, and the GIN index, and they do not define BM25. That absence is the point. If a write-up claims pgvector does BM25, this is the page that settles it.

3. [Qdrant hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/). The RRF and DBSF formulas, including default `k` of 2 and the warning against mixing raw cosine with raw BM25. This is the page that makes “we use RRF” precise enough to implement and to compare with Milvus and Weaviate.

4. [Qdrant indexing](https://qdrant.tech/documentation/manage-data/indexing/). Filterable HNSW, the full-scan threshold, payload indexes, and BM25 scoring on the text index as of v1.20. It is the right page for the question “what happens when the filter is selective?”

5. [Qdrant capacity planning](https://qdrant.tech/documentation/capacity-planning/). The memory tiers and the sizing formulas, plus the worked 768-dimensional example. It is the most concrete official RAM write-up of the four systems. The disk IOPS numbers on the same page are Qdrant’s comparison, not a number to copy onto a purchase order without a test.

6. [Qdrant multitenancy](https://qdrant.tech/documentation/deploy-and-scale/multitenant-search/). Shared collection versus dedicated shards, and the explicit statement that `is_tenant` does not authorize anything. Useful because tenant features are easy to mistake for access control.

7. [Weaviate hybrid search concepts](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search). Relative score fusion, ranked fusion, and the alpha warning, including the fact that a client can send a different alpha than the server default. Read the [how-to](https://docs.weaviate.io/weaviate/search/hybrid) next to it for the shortest official query.

8. [Weaviate resource planning](https://docs.weaviate.io/weaviate/concepts/resources) and [best practices](https://docs.weaviate.io/weaviate/best-practices). Read them as a pair. One gives the 2× float32 formula. The other gives gigabyte figures that do not match it. The disagreement is itself the lesson: do not quote a single RAM number from a vendor’s secondary page.

9. [Weaviate filtering](https://docs.weaviate.io/weaviate/concepts/filtering) and [replication architecture](https://docs.weaviate.io/weaviate/concepts/replication-architecture). The first explains allow-list pre-filtering, ACORN, and PathSeer. The second separates Raft metadata from leaderless object replicas, which is the part a sysadmin has to operate.

10. [Milvus architecture overview](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/reference/architecture/architecture_overview.md) and [install overview](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/getstarted/install-overview.md). How a write becomes a sealed segment, and what Lite, Standalone, and Distributed each include. Use these two before the Knowhere page, which still mentions components the 2.6 merger removed.

11. [Milvus full-text search](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/userGuide/search-query-get/full-text-search.md), the [BM25 function](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/userGuide/embeddings-reranking/embedding-function/bm25-function.md), and the [RRF ranker](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/userGuide/embeddings-reranking/reranking/rrf-ranker.md). The lexical path and the fusion path, including `k1`, `b`, and the two different `k` values in the RRF examples. The [limits page](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/about/limitations.md) belongs in the same sitting, because it disagrees with the hybrid guide on weighted ranking.

12. [Milvus multi-tenancy](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/reference/multi_tenancy.md) and [tiered storage](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/userGuide/storage-optimization/tiered-storage-overview.md). The tenancy page is the one that maps tenant count to database, collection, partition, or partition key. The storage page is the one that says full-load is the latency choice and cold reads are the price of not fitting in RAM.

13. [Qdrant](https://github.com/qdrant/qdrant/releases), [Weaviate](https://github.com/weaviate/weaviate/releases), [Milvus](https://github.com/milvus-io/milvus/releases), and [pgvector changelog](https://github.com/pgvector/pgvector/blob/v0.8.7/CHANGELOG.md) release notes for 2024–2026. These are how you check whether a blog’s feature list is current. The pgvector changelog is also where the HNSW vacuum fixes live. Qdrant v1.10, v1.15, v1.16, v1.19, and v1.20, Weaviate v1.25 and v1.30, and Milvus 2.4, 2.5, 2.6, and 3.0 are the text-retrieval markers.

14. Wang et al., “Milvus: A Purpose-Built Vector Data Management System,” SIGMOD 2021, [doi:10.1145/3448016.3457550](https://doi.org/10.1145/3448016.3457550), and the ACORN and PathSeer papers named on Weaviate’s filtering page. The Milvus README asks readers to cite the SIGMOD paper and the 2022 Manu paper. Weaviate attributes its filter strategies to ACORN and to PathSeer (SIGMOD 2026). None of those papers was opened for this review. They are the right next read for the design argument, and they are older or narrower than the 2026 server behavior, so check them against the current architecture page before you repeat a diagram from 2021.

Learning pointers that were not used as evidence: Qdrant’s hybrid page points at Cormack, Clarke, and Buettcher, “Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods” (SIGIR 2009), for the original `k` of 60. Weaviate’s ANN benchmark page names ann-benchmarks as a different harness. The fusion blog linked from Weaviate’s concept page repeats formulas the concept page already states.

## Presentation-ready takeaways

- These four are two kinds of system. pgvector keeps vectors, SQL filters, and lexical search inside PostgreSQL, and it leaves fusion to a query you write. Qdrant, Weaviate, and Milvus ship the fusion and an in-index filter, and they ship a second process to operate.
- “RRF” is three different scores. Qdrant’s default `k` is 2 with rank 0 on top. Weaviate’s older rank fusion uses `1/(rank+60)`. Milvus’s default `k` is 60 with rank 1 on top. Weaviate’s current default is min-max normalization plus alpha, and a client can override that alpha. Tune on a held-out labeled set. Qdrant’s page names nDCG@10.
- Filters and approximate search fight, in a way each project documents. pgvector can return about 4 rows when you asked for more. Qdrant needs the payload index before the graph is built. Weaviate can fall back to a flat scan. Milvus’s own heuristic switches to brute force when the filter removes almost everything.
- Memory is the capacity plan, and only Qdrant publishes a formula you can repeat. Weaviate’s two official estimates disagree. Milvus caps loaded data at 90% of query-node RAM and tells you to benchmark. pgvector builds much faster when the HNSW graph fits in `maintenance_work_mem`, and search is better when the index is in RAM. Quantization numbers from the vendors are not a ranking.
- For a first text corpus that already lives in Postgres and fits one machine, the sources support staying there. Add a dedicated engine when you want built-in fusion and in-index filtering, or when one node’s RAM and availability are the limit you will not solve with a bigger Postgres, replicas, or a sharder. No official page gives the row count where that happens. A cluster is not the first demo: Qdrant open source does not reshard itself, Weaviate does not move old shards until replica movement, and Milvus Standalone does not upgrade online into Distributed.
