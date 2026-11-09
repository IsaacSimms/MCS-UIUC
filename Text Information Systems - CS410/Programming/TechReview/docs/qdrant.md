# Qdrant

Self-hosted notes for text retrieval. Checked against Qdrant **v1.20.0** (release published 2026-10-22, commit `222b2e4`) and the live documentation fetched on 2026-11-09. The docs pages do not publish a git revision. Confidence is **partial**: the v1.13 and v1.14 release notes were not read, and the old distributed-deployment guide returned 404. Cluster behavior below comes from the overview and the production guide.

Nothing here was measured by running Qdrant. Figures are the ones Qdrant publishes.

## A. What it is and the design goal

Qdrant (pronounced “quadrant”) is a vector similarity engine and database written in Rust. It stores **points**: a vector plus an arbitrary JSON payload. Clients talk to it over HTTP or gRPC. Official clients exist for Python, JavaScript/TypeScript, Rust, Go, .NET, and Java. The license is Apache 2.0. ([README](https://github.com/qdrant/qdrant/blob/master/README.md), [LICENSE](https://github.com/qdrant/qdrant/blob/master/LICENSE), [Overview](https://qdrant.tech/documentation/overview/))

The design goal is **filtering inside the index**, not vector search bolted onto a general-purpose database. The project’s own framing is that general-purpose databases degrade once data leaves one machine, filters get selective, or memory gets tight. Qdrant is built so the same store can do semantic match and faceted search. ([README](https://github.com/qdrant/qdrant/blob/master/README.md), [docs index](https://qdrant.tech/llms.txt))

For text, that means three retrievers you can combine: dense vectors on an HNSW graph, sparse vectors on an exact inverted-style index, and, since v1.20.0, BM25 scored directly from a full-text payload index. ([Indexing](https://qdrant.tech/documentation/manage-data/indexing/))

## B. How it stores and searches

A **collection** is split into **shards**. Each shard stores points in **segments**. Fewer, larger segments search faster and index slower. Not every segment has an index: the optimizer builds one from the number of stored points. Index settings live on the collection; the indexes themselves live in the segments. ([Overview](https://qdrant.tech/documentation/overview/), [Indexing](https://qdrant.tech/documentation/manage-data/indexing/))

**Dense search.** The only dense index is HNSW. Documented defaults are `m: 16` and `ef_construct: 100`. Search `ef` defaults to `ef_construct`. The query planner can skip the graph and full-scan when the estimated matching set is smaller than `full_scan_threshold` (the documented example is 10000, described as a size threshold in kilobytes, with 1 KB equal to one 256-dimensional vector). ([Indexing](https://qdrant.tech/documentation/manage-data/indexing/))

**Filtered dense search** is filterable HNSW. The graph gets extra edges from indexed payload values, and the filter is applied while walking the graph. Weak filters can use plain HNSW. Very strict filters can use the payload index and rescore. The extra edges exist for the middle case. They are built per payload field, not per combination of fields, and only for payload indexes that already exist when the graph is built. Two or more strict filters, or many soft-deleted points, can still disconnect the walk. ACORN, added in v1.16.0, then looks at neighbors of filtered-out neighbors. The docs say this improves accuracy and costs performance. ([Indexing](https://qdrant.tech/documentation/manage-data/indexing/))

**Sparse search**, since v1.7.0, is a separate exact index, similar to an inverted index. It supports dot product only and does not need a fixed dimension. New sparse vectors land immediately in a mutable index; an immutable index is built by the same optimizer as the dense index. ([Indexing](https://qdrant.tech/documentation/manage-data/indexing/))

## C. Deployment models

| Shape | What you operate | What you do not get |
|---|---|---|
| Single node | Docker, a binary, or Kubernetes. The README quick start is `docker run -p 6333:6333 qdrant/qdrant`. | No authentication in that quick start, and it listens on all interfaces. No redundancy. The default config is a proof of concept. |
| Self-hosted cluster | You place shards and replicas yourself. Consensus is Raft. At least three nodes so a pair can keep quorum, and replication factor at least 2. | Shard count is fixed at creation. Resharding means recreating the collection. No automatic failover, rebalance, zero-downtime upgrades, or automated backups. |
| Managed Cloud | Qdrant runs it on AWS, GCP, or Azure. | You are on their control plane. |
| Hybrid Cloud | Database in your Kubernetes cluster, managed through Qdrant Cloud. Data stays on your network. | You still run Kubernetes. |
| Private Cloud | Air-gapped Kubernetes, no Qdrant Cloud connectivity. | You operate the cluster. Resharding after adding nodes is available here, unlike open-source self-host. |
| Qdrant Edge | In-process library, same storage format, can read server shard snapshots. | Not a server and not a cluster. For offline or embedded retrieval. |

Sources: [README](https://github.com/qdrant/qdrant/blob/master/README.md), [Deploy](https://qdrant.tech/documentation/deploy-intro/), [Overview](https://qdrant.tech/documentation/overview/), [Vector search in production](https://qdrant.tech/documentation/deploy-and-scale/vector-search-in-production/).

Shard count should start equal to the node count for throughput, or at 12 if you want to grow through 1, 2, 3, 6, or 12 nodes without resharding. The overview’s matrix marks automatic failover, zero-downtime upgrades, monitoring and alerting, a management UI, automatic rebalancing, and automated backups as absent from open source and present on Managed Cloud. ([Overview](https://qdrant.tech/documentation/overview/))

Strict mode can reject filters on fields that have no payload index. Qdrant Cloud does that by default. The open-source build enforces nothing until strict mode is turned on. ([Indexing](https://qdrant.tech/documentation/manage-data/indexing/), [Overview](https://qdrant.tech/documentation/overview/))

## D. Resource characteristics

Since v1.19.0 every structure has a memory tier: `pinned` (heap, not evicted), `cached` (memory-mapped and pre-warmed), or `cold` (memory-mapped, loaded on first read). `cold` and `cached` are both mmap; the OS may evict either. Everything is also stored on disk. The memory tier only adds a RAM copy or cache. ([Capacity planning](https://qdrant.tech/documentation/capacity-planning/))

Documented defaults:

- Dense vectors and the HNSW graph are `cached` and count toward RAM.
- Payloads are `cold`.
- Payload indexes and the ID tracker are `pinned`.
- Sparse vectors cannot be cached in RAM. They need disk only.
- Sparse indexes default to `pinned`.

The capacity page gives formulas, not a benchmark from this review. Dense size is points × replication factor × dimensions × bytes per dimension (`float32` 4, `float16` and `turbo16` 2, `uint8` and `turbo8` 1, `turbo4` 0.5). HNSW size is `base * m * 2 * 4 * 1.2` bytes. The ID tracker formula is 52 bytes per point. Payload on disk is about 1.5× average JSON size; a cached payload is budgeted at about 3× that. A payload index is coarsely about twice the indexed field. Add about 20% headroom for page cache, runtime, the optimizer, the WAL, snapshots, and temporary segments. ([Capacity planning](https://qdrant.tech/documentation/capacity-planning/))

Worked example on that page, not remeasured here: 1,000,000 points, replication factor 2, 768-dimensional `float32`, default `cached` tier, is about 5.72 GB for the vectors, about 0.29 GB for HNSW at `m` 16, and about 0.10 GB for the ID tracker. With 4-bit TurboQuant (0.5 bytes per dimension), originals `cold`, quantized vectors `pinned`, the dense RAM figure in the example drops to about 0.72 GB. The page says to confirm recall before relying on quantization. ([Capacity planning](https://qdrant.tech/documentation/capacity-planning/))

Quantization, from the quantization page:

| Method | Since | Compression vs float32 | Operational note |
|---|---|---|---|
| Scalar (`float32` to `uint8`) | v1.1.0 | 4× | SIMD makes the comparison faster. Qdrant’s own experiments usually saw under 1% accuracy error. That is their experiment, not a guarantee. |
| Product | v1.2.0 | up to 64× | 256 centroids. Not SIMD-friendly. Slower than scalar. |
| Binary (1 bit) | v1.5.0 | 32× | Docs say up to 40× faster than original vectors, only when vectors are high-dimensional and centered. |
| 2-bit and 1.5-bit binary | v1.15.0 | 16× and about 21× | Asymmetric mode scores binary stored vectors against a scalar-quantized query. |
| TurboQuant | v1.18.0 | 4× to 32× | Stored vectors are compressed. Queries stay full precision. Default encoding is `bits4`. `bits8` arrived in v1.20.0. Manhattan reconstructs the vector and is much slower. |

The README says built-in quantization cuts RAM by up to 97%. The method page’s largest stated factors are product quantization at up to 64× and binary at 32×. Those statements were not reconciled in one formula. Treat 97% as a README claim and 4× / 32× / 64× as the method page’s claims. ([README](https://github.com/qdrant/qdrant/blob/master/README.md), [Quantization](https://qdrant.tech/documentation/manage-data/quantization/))

Rescoring with the original vectors is how accuracy comes back, and it reads those vectors. That is slow if they are on disk. If vectors are on disk, the capacity page’s rule of thumb is that keeping half as many vectors in RAM roughly doubles search latency. It says to use local SSDs with at least 50,000 IOPS for on-disk vectors. Its own disk comparison, stated there and not remeasured here: a network disk at about 6,400 IOPS and 25 MiB/s was too slow; a local disk at about 63,000 IOPS and 247 MiB/s was much faster; a local SSD at about 183,000 IOPS and 716 MiB/s was faster still. AWS gp3’s starting 3,000 IOPS and 125 MiB/s is called a baseline, not a target. Avoid a `cold` HNSW graph when you can: traversal does many small random reads. A single node typically tops out around 100 million vectors, as a rough ceiling that moves with dimension, datatype, and quantization. ([Quantization](https://qdrant.tech/documentation/manage-data/quantization/), [Capacity planning](https://qdrant.tech/documentation/capacity-planning/))

CPU matters most while a node ingests and indexes at once. Default indexing uses up to 16 threads; more cores need an explicit increase. The capacity page attributes one hardware sketch to the Large-Scale Search tutorial: 8 CPU cores, 64 GB RAM, and 1 TB disk as a minimal single-node setup for indexing and exploring 400 million vectors, with production possibly needing more. That number is second-hand inside the official page. ([Capacity planning](https://qdrant.tech/documentation/capacity-planning/))

The README also lists SIMD on x86-64 and Neon, optional GPU indexing for NVIDIA and AMD, `io_uring` for disk reads, and a write-ahead log so an acknowledged update survives power loss. ([README](https://github.com/qdrant/qdrant/blob/master/README.md))

Before v1.19, placement was `on_disk` and `memmap_threshold`. v1.15.0 deprecated `mmap_threshold` because, from v1.12, vector storage is memory-mapped and `on_disk` is the cache switch. v1.19 replaced that pair with the memory tiers. ([v1.15.0 notes](https://github.com/qdrant/qdrant/releases/tag/v1.15.0), [Capacity planning](https://qdrant.tech/documentation/capacity-planning/))

## E. Hybrid search

Hybrid search is the Query API: one or more `prefetch` queries, then a main query over those candidates. A document that neither prefetch returns cannot appear. `offset` applies only to the main query, so each prefetch `limit` must be at least the main `limit` plus `offset`. ([Hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/))

Two fusion methods are named.

**RRF (reciprocal rank fusion)** uses rank, not the raw score. With default weight 1, the score is the sum of `1/(k + r)` over rankings, with zero-based rank and default `k` of 2. Weights default to 1. The docs say a fixed alpha mix of raw cosine and raw BM25 is unreliable because the scales differ and shift per query. `k` has been configurable since v1.16.0. Weights arrived in v1.17.0. ([Hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/), [v1.16.0](https://github.com/qdrant/qdrant/releases/tag/v1.16.0), [v1.17.0 through v1.20.0](https://github.com/qdrant/qdrant/releases))

**DBSF (distribution-based score fusion)**, since v1.11.0, normalizes each prefetch’s scores with that result list’s mean and sample standard deviation, using the 3-sigma ends as the remap, then sums the normalized scores. Statistics come only from that query’s prefetch hits. Identical scores, or a single hit, become 0.5. The docs’ choice table: weighted RRF when you have an eval set, DBSF when you trust raw-score magnitude and have no eval set, and plain RRF otherwise. ([Hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/))

In a multi-shard collection, fusion merges across shards only when it is the top-level `query`. A fusion nested inside a prefetch is computed per shard. ([Hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/))

**Two BM25 paths, and they do not share defaults.**

1. Full-text payload index (`type: text`), with scoring enabled, since v1.20.0. Phrase matching and BM25 scoring are independent switches. The index stores document length and term frequency and computes statistics such as average document length from the data, so it uses more memory and disk than a filter-only text index. `k` and `b` are per query, not index settings. This is the path the sparse-vector docs recommend, because the text is already in the payload and you do not need a sparse embedding. The text index does not apply the English stemming and stopword removal that the sparse BM25 model uses by default.
2. Sparse-vector BM25, via the `qdrant/bm25` inference model or client-side FastEmbed, with an IDF modifier. Ingest-time defaults are `k` 1.2, `b` 0.75, and `avg_len` 256. The sparse model defaults to English stemming and English stopword removal.

Qdrant does not implement BM25F. The documented workaround for multi-field text is separate sparse vectors per field, fused through the Query API. Learned sparse vectors are also supported. The docs name SPLADE++ and miniCOIL, and say SPLADE can miss terms outside its vocabulary, such as product IDs, and costs more CPU than BM25. ([Indexing](https://qdrant.tech/documentation/manage-data/indexing/), [Sparse vectors](https://qdrant.tech/documentation/search/text-search/sparse-vector-search/))

## F. Metadata filtering and multi-tenancy

Payload indexes are optional and per field. Documented types include keyword, integer, float, bool, geo, datetime (v1.8.0), text, and uuid (v1.11.0). They cost memory and disk. Index the fields you filter on, and prefer the field that cuts the result set the most. Filters combine keyword, full-text, numeric range, and geo conditions with `should`, `must`, and `must_not`. Unindexed filters still return results, but the engine reads payloads to evaluate them, which raises latency and can hurt other queries. ([README](https://github.com/qdrant/qdrant/blob/master/README.md), [Indexing](https://qdrant.tech/documentation/manage-data/indexing/))

Multitenancy is a layout choice, not an authorization feature. The current guide:

- Many similar small tenants share one collection and a tenant payload field.
- Mixed sizes use tiered multitenancy (a shared fallback shard plus dedicated shards) since v1.16.
- A few tenants that need different schemas or collection-level permissions get separate collections.
- Data that must sit on specific nodes uses custom shard keys. Custom sharding has to be chosen at collection creation and cannot be switched later. The shared fallback shard must fit on one node.

`is_tenant: true` on a keyword index, since v1.11, tells Qdrant to co-locate that tenant’s points, which means fewer disk reads. The flag does not authorize anything. A client that can omit the filter can read other tenants. The application has to add the tenant filter on every query, update, and delete. If every search is tenant-filtered and indexing is the bottleneck, `m: 0` disables the global HNSW graph and a positive `payload_m` keeps payload-aware links. Queries without the tenant filter then get slower. ([Multitenancy](https://qdrant.tech/documentation/deploy-and-scale/multitenant-search/), [Indexing](https://qdrant.tech/documentation/manage-data/indexing/))

**Unresolved conflict.** The v1.16.0 release notes remove payload filters from RBAC/JWT (deprecated in v1.15) and reject API keys that still use them. The stated alternative is collection-based access control. The production guide still says a Cloud API key or an open-source JWT can enforce a payload filter. The release note is the newer engine claim. The security reference page was not re-read, so live JWT behavior is not confirmed. ([v1.16.0 notes](https://github.com/qdrant/qdrant/releases/tag/v1.16.0), [Production guide](https://qdrant.tech/documentation/deploy-and-scale/vector-search-in-production/))

## G. Notable changes, 2024–2026

From the release notes that were actually opened. v1.13 and v1.14 were not.

**2024**

- **v1.8.0** (2024-03-06): datetime payload index, a minimum number of `should` conditions, sparse search called 16× faster, and a smaller, compressed text index.
- **v1.9.0** (2024-04-22): another stated 7% sparse-search improvement, and faster shard recovery via shard diff transfer.
- **v1.10.0** (2024-07-01): the universal Query API, including hybrid fusion; multivectors; `float16` dense vectors at half the memory; `float16` and `uint8` sparse indexes; an IDF modifier so BM25-style sparse updates can stream; sparse delta and bitpacking compression up to 75% less memory.
- **v1.11.0** (2024-08-12): DBSF, UUID payload index, several on-disk payload index types, and data-locality work for multitenant collections.
- **v1.12.0** (2024-10-08): vector storage moved to memory-mapped files so RSS falls and the OS cache holds the vectors. Text and geo indexes can sit on disk.

**2025**

- **v1.15.0** (2025-07-18): full-text phrase matching, stopwords, a multilingual tokenizer as the default, a Snowball stemmer, asymmetric binary quantization, 1.5-bit and 2-bit binary quantization, maximum marginal relevance, and the migration off RocksDB.
- **v1.16.0** (2025-11-17): optional inline vectors inside the HNSW file, tenant promotion, ACORN, ASCII folding on full text, `text_any`, a configurable RRF `k`, and new mutable payload storage on Gridstore instead of RocksDB.

**2026**

- **v1.17.0** (2026-02-20): weighted RRF, a control to avoid serving unoptimized segments under write load, and a read fan-out delay for replicated tail latency. RocksDB support would be removed in the v1.17 line. A direct upgrade from v1.15.x to v1.17.x would not work.
- **v1.18.0** (2026-05-11): RocksDB support fully removed. TurboQuant, a low-memory startup mode, and a strict-mode resident-memory limit.
- **v1.19.0** (2026-08-05): 4-bit TurboQuant as a primary vector datatype so original vectors need not be stored, the `cold` / `cached` / `pinned` memory setting, keyword prefix match, and a per-query IDF corpus for sparse search.
- **v1.20.0** (2026-10-22): BM25 scoring on the full-text payload index, `turbo8` and `turbo16` datatypes, a `code` tokenizer, and `hnsw_config.inline_storage` so vectors can live only in the HNSW file. This was the newest tag on 2026-11-09.

Sources: [releases covering v1.8.0–v1.12.5](https://github.com/qdrant/qdrant/releases), [v1.15.0](https://github.com/qdrant/qdrant/releases/tag/v1.15.0), [v1.16.0](https://github.com/qdrant/qdrant/releases/tag/v1.16.0), [v1.17.0–v1.20.0](https://github.com/qdrant/qdrant/releases).

Speedup percentages in those notes are Qdrant’s claims. They were not rerun.

## H. Strengths and limitations for text retrieval

**Strengths**

- Filterable HNSW, an exact sparse index, and first-party BM25, fused with RRF or DBSF. You do not have to invent a score mix.
- Quantization and memory tiers come with published sizing formulas, so a sysadmin can budget RAM before buying a node.
- A tenant field changes storage layout without a collection per user.
- One binary. Single-node Docker is a short path to a real index.

**Limitations**

- HNSW is approximate, and it is the only dense index.
- Multi-filter queries can still miss the extra edges. Payload indexes added after the graph is built do not help that graph until a rebuild.
- Sparse search is dot product only. The two BM25 paths do not share stemming, stopwords, or `k` / `b` defaults.
- Self-hosted shard count and sharding method are fixed at creation. Automatic rebalance and resharding are not in the open-source deploy.
- The tenant index is not access control.
- Quantization recall is data-dependent. Rescoring pulls original vectors from disk.
- There is no BM25F. Multi-field lexical rank means separate sparse vectors fused in the query.

([Indexing](https://qdrant.tech/documentation/manage-data/indexing/), [Hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/), [Capacity planning](https://qdrant.tech/documentation/capacity-planning/), [Overview](https://qdrant.tech/documentation/overview/), [Quantization](https://qdrant.tech/documentation/manage-data/quantization/))

For a short demo, the practical shape is one Docker node, one collection, dense vectors plus a v1.20 full-text index with BM25 scoring, fused with default RRF. Create the payload indexes, including `is_tenant` if there are tenants, before loading data. Leave quantization off until a recall check. Do not demo a collection per tenant, a raw-score alpha mix, or a self-hosted cluster as if it resharded itself. RRF ignores how far ahead a hit was, which is what makes cosine and BM25 comparable. DBSF keeps that gap but normalizes only the small prefetch sample.

## I. Sources

Official pages worth reading, each for one reason:

1. [README](https://github.com/qdrant/qdrant/blob/master/README.md). Identity, license, and the feature list in the project’s own words.
2. [Overview](https://qdrant.tech/documentation/overview/). Shards, segments, and which availability features are open-source versus managed.
3. [Indexing](https://qdrant.tech/documentation/manage-data/indexing/). HNSW, payload indexes, and BM25 on the text index.
4. [Hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/). RRF and DBSF, including the formulas and the shard-fusion rule.
5. [Sparse vector search](https://qdrant.tech/documentation/search/text-search/sparse-vector-search/). Why the text index is the recommended BM25 path, and what the sparse path still does.
6. [Quantization](https://qdrant.tech/documentation/manage-data/quantization/). What compression costs in recall and CPU.
7. [Capacity planning](https://qdrant.tech/documentation/capacity-planning/). How to budget RAM and disk, including the memory tiers.
8. [Multitenancy](https://qdrant.tech/documentation/deploy-and-scale/multitenant-search/). Shared collection versus dedicated shards, and the fact that the tenant index is not authorization.
9. [Deploy](https://qdrant.tech/documentation/deploy-intro/) and [production guide](https://qdrant.tech/documentation/deploy-and-scale/vector-search-in-production/). Single node, cluster, and the three cloud shapes.
10. [Release notes](https://github.com/qdrant/qdrant/releases), especially v1.10.0, v1.15.0, v1.16.0, v1.19.0, and v1.20.0. The text-retrieval changes from the Query API through BM25-on-payload.

Not read, so not used as evidence: the filterable-HNSW design article linked from the indexing page, the HNSW paper (Malkov and Yashunin), the 2009 reciprocal-rank-fusion paper (Cormack, Clarke, and Buettcher), and the Large-Scale Search tutorial behind the 8-core / 64 GB / 1 TB sketch. Customer timings in the production guide were also left out. The dedicated cluster page `distributed_deployment.md` 404’d.
