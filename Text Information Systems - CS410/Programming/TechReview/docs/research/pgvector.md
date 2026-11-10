# pgvector

Self-hosted notes for text retrieval. Checked against **pgvector 0.8.7** (tag `v0.8.7`, changelog date 2026-10-01) and master commit `bcbb135` (2026-11-09), where 0.9.0 is still unreleased. Lexical search was checked against PostgreSQL 18 documentation, chapters 12.1, 12.3, and 12.9. Confidence is **confident** for what the README, changelog, and those Postgres chapters say. Confidence does not extend to a row count where a dedicated vector database becomes the better system. Those sources do not give one. pgvector was not started, and no recall table was measured.

## A. What it is and the design goal

pgvector is an open-source PostgreSQL extension for exact and approximate nearest-neighbor search. The README’s design line is “Store your vectors with the rest of your data.” You enable it with `CREATE EXTENSION vector`. It is not a separate database server. The same database gives you ACID, point-in-time recovery, JOINs, and the rest of Postgres. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

The `LICENSE` file at tag v0.8.7 is the PostgreSQL License. It grants use, copy, modification, and distribution for any purpose, without fee, provided the copyright notice and the warranty disclaimer stay in all copies. The copyright lines are “Portions Copyright (c) 1996-2026, PostgreSQL Global Development Group” and “Portions Copyright (c) 1994, The Regents of the University of California.” The file has no SPDX identifier line. ([LICENSE at v0.8.7](https://github.com/pgvector/pgvector/blob/v0.8.7/LICENSE))

A student should read the README first. It is the project’s SQL reference for types, indexes, filtering, tenancy, hybrid search, and scaling. Read the changelog second. Read PostgreSQL 18 chapters 12.1, 12.3, and 12.9 for the lexical half, because that half is Postgres. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md), [PostgreSQL 18 full-text search](https://www.postgresql.org/docs/18/textsearch-intro.html))

## B. How it stores and searches

Storage is a column on a normal table: `vector(n)`, `halfvec(n)`, PostgreSQL `bit(n)`, or `sparsevec(n)`. Inserts, updates, deletes, upserts, and binary `COPY` are ordinary SQL. With no index, search is exact nearest neighbor by ordering on a distance operator and limiting. Adding an approximate index trades some recall for speed, and the README warns that results can change after that index exists. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

On-disk value sizes in the README are the type payloads, not a full Postgres tuple and not an index-size formula:

| Type | Size | Cap that matters |
|---|---|---|
| `vector` | `4 * dimensions + 8` bytes | Up to 16,000 dimensions stored. HNSW and IVFFlat index up to 2,000. |
| `halfvec` | `2 * dimensions + 8` bytes | Same 16,000 stored. Indexed up to 4,000. |
| `bit` | `dimensions / 8 + 8` bytes | Indexed up to 64,000. |
| `sparsevec` | `8 * non-zero elements + 16` bytes | Up to 16,000 non-zero elements stored. HNSW indexes up to 1,000 non-zero elements. |

The sparse literal form is `{index:value,...}/dimensions` with indexes starting at 1. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

Distance operators: `<->` L2, `<#>` negative inner product, `<=>` cosine distance, `<+>` L1, `<~>` Hamming on `bit`, `<%>` Jaccard on `bit`. `<#>` is negative because Postgres index scans on operators are ascending only. Inner product for display is that value times -1. Cosine similarity is `1 - cosine distance`. An approximate index is used for `ORDER BY` of the distance operator itself, ascending, with `LIMIT`. An expression such as `ORDER BY 1 - (embedding <=> query) DESC` does not use the index. For vectors already normalized to length 1, the README says inner product is the faster exact-search choice. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

**The only index types named are HNSW and IVFFlat.** None is added in the 0.6.0 through 0.8.7 changelog or in the unreleased 0.9.0 notes. Half-precision indexing, binary quantization, and subvector indexing are expression indexes, not new index access methods.

HNSW is a multilayer graph. The README says it has a better speed-recall tradeoff than IVFFlat, slower builds, and more memory, and that it can be built on an empty table because there is no training step. Defaults: `m = 16`, `ef_construction = 64`, query `hnsw.ef_search = 40`. Higher `ef_construction` and `ef_search` buy recall with build time, insert speed, or query speed. One index is per distance opclass (`vector_l2_ops`, `vector_ip_ops`, `vector_cosine_ops`, `vector_l1_ops`, and the `halfvec` and `sparsevec` equivalents, plus Hamming and Jaccard on `bit`).

IVFFlat divides vectors into lists and searches the lists closest to the query. It builds faster and uses less memory than HNSW, with a worse speed-recall tradeoff. The README’s starting points are heuristics, not a measured corpus result: create the index after the table has data; `lists` around `rows / 1000` up to 1 million rows and `sqrt(rows)` above that; `ivfflat.probes` starts at 1 and a suggested query setting is `sqrt(lists)`. Probes equal to the number of lists is exact search, and at that point the planner will not use the index. The IVFFlat supported-type list is `vector`, `halfvec`, and `bit`, not `sparsevec`.

Binary quantization stores `binary_quantize(embedding)::bit(n)`. The README’s recall pattern is to take a larger Hamming candidate set and re-rank with the original vectors. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md), [CHANGELOG at master](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/CHANGELOG.md))

`NULL` vectors are not indexed. Zero vectors are not indexed for cosine distance. A column declared as `vector` without a dimension can store mixed lengths, but an index is only valid for rows with one fixed dimension, via an expression index plus a partial index. Dimensions above the index caps are handled in the FAQ by half-precision indexing (4,000), binary quantization (64,000), subvector indexing, or dimensionality reduction. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

There is no named-vector or multivector type. A second embedding is another column. ([README](https://github.com/pgvector/pgvector/blob/master/README.md))

## C. Deployment models

Single-node deployment is Postgres with the extension installed. The README’s paths are: compile from tag `v0.8.7` (`make` / `make install`, Postgres 13+ in the README), the Docker image `pgvector/pgvector` with 0.8.7 tags for Postgres 13 through 18, or apt, yum, PGXN, Homebrew, pkgsrc-style packages, conda-forge, or Postgres.app. Upgrade inside each database with `ALTER EXTENSION vector UPDATE`. Check `SELECT extversion FROM pg_extension WHERE extname = 'vector'`. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

Replication is PostgreSQL’s, via the write-ahead log. The FAQ says pgvector uses WAL, which allows replication and point-in-time recovery. The scaling section’s horizontal options are Postgres replicas (it links the hot-standby chapter), or Citus, PgDog, or another sharding approach. Those sharders are named by the README. They are not pgvector features. pgvector does not ship its own cluster product. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

Managed deployment is managed Postgres that includes the extension. The README says it comes preinstalled with Postgres.app and many hosted providers, and points the provider list at [GitHub issue 54](https://github.com/pgvector/pgvector/issues/54). That issue was not opened, so this note does not name vendors or the version each host packages. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

On master, and not shipped: 0.9.0 is labeled unreleased and lists asynchronous I/O for indexes, vacuum progress for indexes, and dropping Postgres 13 and 14. The README at the same commit still says the build supports Postgres 13+. Treat 13+ as the 0.8.7 documented support window. GitHub’s Releases page for the repo lists no releases. The tag and the changelog are the version record. ([CHANGELOG at master](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/CHANGELOG.md), [Releases page](https://github.com/pgvector/pgvector/releases))

ParadeDB, pgvectorscale, and any DiskANN-style index are not in the README or the changelogs that were read. They are not part of upstream pgvector 0.8.7.

## D. Resource characteristics

HNSW build memory is dominated by whether the graph fits in `maintenance_work_mem`. The README says builds are significantly faster when it fits, shows `SET maintenance_work_mem = '8GB'` as an example, prints a notice when the graph no longer fits, and says not to set it so high that it exhausts server memory. Parallel build workers default to 2 plus a leader. `max_parallel_workers` defaults to 8. For Docker, `--shm-size` must be at least `maintenance_work_mem` or parallel HNSW builds can fail. Create indexes after the initial load. In production use `CREATE INDEX CONCURRENTLY`. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

Query memory for iterative HNSW scans is `hnsw.scan_mem_multiplier` times `work_mem` (default multiplier 1). `hnsw.max_scan_tuples` defaults to 20,000, is approximate, and does not affect the initial scan. The README says to raise the multiplier if raising `max_scan_tuples` does not improve recall. IVFFlat’s iterative cap is `ivfflat.max_probes`. If that is lower than `ivfflat.probes`, `probes` is used. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

The README’s own scale path for a smaller working set is `halfvec` in the table and binary quantization on the index, with re-ranking at query time. It then says to scale vertically by adding memory, CPU, and storage on one instance. Indexes do not have to fit in memory. The FAQ says that, like other index types, performance is better when they do. Index size is `pg_relation_size`. No HNSW-graph byte formula and no query-latency number is stated. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

CPU work is distance calculation plus index build and scan. Since 0.7.0 the changelog records CPU dispatch for distance functions on Linux x86-64. The README says default builds use `-march=native` on some platforms, which can raise `Illegal instruction` if that binary is copied to another machine. `make OPTFLAGS=""` is the documented portable build. Exact search without an index can use more workers via `max_parallel_workers_per_gather`. The planner ignores out-of-line storage in cost estimates, so a parallel sequential scan may look too expensive. The documented session workaround is lowering `min_parallel_table_scan_size` and `parallel_setup_cost`, or `SET STORAGE PLAIN` on the column. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md), [CHANGELOG at v0.8.7](https://github.com/pgvector/pgvector/blob/v0.8.7/CHANGELOG.md))

For server memory, the README points at a tuner such as PgTune and says, as an instance of that advice, that `shared_buffers` should typically be 25% of the server’s memory. That is Postgres startup guidance quoted by the project, not a pgvector benchmark. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

Disk and durability follow Postgres. 0.6.0 changed `vector` storage from `extended` to `external`, reduced WAL from HNSW builds, and fixed a logical-replication error. A non-partitioned table is limited to 32 TB by default. A partitioned table can have thousands of partitions of that size. HNSW vacuum can take a long time. The documented speedup is `REINDEX INDEX CONCURRENTLY` and then `VACUUM`. Build progress is visible in `pg_stat_progress_create_index`. There is no separate process cold-start section. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md), [CHANGELOG at v0.8.7](https://github.com/pgvector/pgvector/blob/v0.8.7/CHANGELOG.md))

## E. Hybrid search

Hybrid search, in the pgvector README, means using the extension together with Postgres full-text search. The only SQL in that section is the lexical leg: `plainto_tsquery`, a `textsearch` column, the `@@` match operator, and `ORDER BY ts_rank_cd(...) DESC`. The next sentence says you can use reciprocal rank fusion or a cross-encoder to combine results, and it links example files in the pgvector-python repository. The extension README does not define an RRF function, a fusion operator, a `k`, or a weight. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

Lexical match and rank are PostgreSQL, not pgvector. PostgreSQL 18 parses documents to `tsvector` and queries to `tsquery`. `@@` is the match. The two built-in ranking functions are `ts_rank` (frequency of matching lexemes) and `ts_rank_cd` (cover density, citing Clarke, Cormack, and Tudhope 1999). That ranking page does not document BM25. Ranking uses only per-document information, can be I/O heavy because every match’s `tsvector` is consulted, and the docs say the built-in rankers are examples you can replace or combine with other factors. ([PostgreSQL 18, 12.1](https://www.postgresql.org/docs/18/textsearch-intro.html), [12.3](https://www.postgresql.org/docs/18/textsearch-controls.html))

The preferred Postgres index for a `tsvector` column is GIN. GiST is the other documented text-search index and is lossy. GIN build time can be improved by raising `maintenance_work_mem`. That is PostgreSQL full-text indexing, separate from HNSW and IVFFlat. The pgvector hybrid snippet assumes a `textsearch` column and does not create this index. ([PostgreSQL 18, 12.9](https://www.postgresql.org/docs/18/textsearch-indexes.html))

`sparsevec` is a sparse floating-point vector with L2, inner product, cosine, and L1, added in 0.7.0. The hybrid-search section does not use it. Neither the README nor the changelogs checked here describe it as a BM25 or lexical weight vector. A dense `vector` column and a `sparsevec` column can sit on the same table and be ordered separately in SQL. The README does not define a fused sparse-plus-dense score. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md), [CHANGELOG at v0.8.7](https://github.com/pgvector/pgvector/blob/v0.8.7/CHANGELOG.md))

Maintainer Andrew Kane, on a request to order by two vector distances at once, wrote that `ORDER BY (embedding <-> a) + (other_embedding <-> b)` will not use an index and will run exact nearest-neighbor search. That is a sum of distances. The README does not present it as hybrid fusion. ([Issue 623](https://github.com/pgvector/pgvector/issues/623))

The fusion SQL the README links, `examples/hybrid_search/rrf.py` and the cross-encoder example beside it in pgvector-python, are application queries in another repository. They were not read. Constants in those files are not pgvector parameters.

A minimal official example from the README:

```sql
CREATE EXTENSION vector;
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;
CREATE INDEX ON items USING hnsw (embedding vector_l2_ops);
```

The hybrid example on the same page is the lexical `ts_rank_cd` query, not a fused vector query. ([README](https://github.com/pgvector/pgvector/blob/master/README.md))

## F. Metadata filtering and multi-tenancy

Metadata filtering is a SQL `WHERE` clause. The README’s first tool is an index on the filter column. Postgres index types it names for that are B-tree (the default), hash, GiST, SP-GiST, GIN, and BRIN, plus multicolumn indexes. Those exact indexes fit when the condition matches a low percentage of rows.

With an approximate vector index, filtering happens after the index scan. The README’s illustration, not a benchmark: if the condition matches 10% of rows and `hnsw.ef_search` is 40, about 4 rows match on average. Few distinct filter values can use a partial HNSW index. Many values can use list partitioning. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

Iterative index scans, added in 0.8.0, keep scanning until enough filtered rows are found or a cap is hit (`hnsw.max_scan_tuples` or `ivfflat.max_probes`). `hnsw.iterative_scan = strict_order` keeps exact distance order. `relaxed_order` is documented for both HNSW and IVFFlat and can return rows slightly out of distance order, with better recall. Strict order after a relaxed scan is a materialized CTE plus `ORDER BY distance`, and the README says `distance + 0` is required on Postgres 17+. 0.8.0 also improved cost estimates so the planner picks indexes better when filtering. The README shows `strict_order` for HNSW. It was not confirmed whether IVFFlat iterative scans accept `strict_order`. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md), [CHANGELOG at v0.8.7](https://github.com/pgvector/pgvector/blob/v0.8.7/CHANGELOG.md))

Multi-tenancy in the README is about approximate-index coupling. One shared approximate index means one tenant’s vectors can change recall and speed for other tenants. The documented isolation is list partitioning on the tenant id, or separate tables. The README does not document row-level security or schema-per-tenant as the vector-search pattern. Postgres can still do those. They are not the pattern the pgvector README writes down for this problem. ([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md))

## G. Notable changes, 2024–2026

From the changelog at tag v0.8.7.

**2024**

- **0.6.0** (2024-01-29): parallel HNSW builds, the `vector` storage change from `extended` to `external`, faster HNSW, less HNSW build memory and WAL, a logical-replication fix, and per-Postgres Docker tags. Dropped Postgres 11.
- **0.6.1–0.6.2:** `ANALYZE` with mixed dimensions, a crash with `shared_preload_libraries`, and lock contention on parallel HNSW builds.
- **0.7.0** (2024-04-29): `halfvec`, `sparsevec`, `bit` indexing, HNSW L1, `binary_quantize`, Hamming and Jaccard, `l2_normalize`, `subvector`, concatenate, Linux x86-64 CPU dispatch, and comparisons between different dimensions.
- **0.7.1–0.7.4:** on-disk HNSW build speed, the init fork for unlogged tables, `failed to add index item` on `sparsevec`, and locking for parallel HNSW builds.
- **0.8.0** (2024-10-30): iterative index scans, array-to-`sparsevec` casts, better filter cost estimates, and faster HNSW scan, insert, and on-disk build. Dropped Postgres 12.

**2025–2026**

- **0.8.1** (2025-09-04): Postgres 18 rc1 support and faster `binary_quantize`.
- **0.8.2** (2026-02-25): a buffer overflow in parallel HNSW builds, and `Index Searches` in Postgres 18 `EXPLAIN`.
- **0.8.3** (2026-06-17): possible HNSW index corruption during vacuum, and a Postgres 18 Hamming/Jaccard regression.
- **0.8.4** (2026-06-30): further HNSW vacuum errors, and IVFFlat builds whose memory exceeded `maintenance_work_mem`.
- **0.8.5** (2026-07-08): less IVFFlat build memory on small tables.
- **0.8.6** (2026-07-29): a 32-bit IVFFlat build overflow, a non-zero-element limit on the array-to-`sparsevec` cast, and IVFFlat scan memory with nested-loop joins.
- **0.8.7** (2026-10-01): an IVFFlat index-build buffer overflow, and `avg` when no rows match.

The vacuum fixes in 0.8.3 and 0.8.4 are the operational ones. Chunk deletes and updates want a current patch and a reindex plan. ([CHANGELOG at v0.8.7](https://github.com/pgvector/pgvector/blob/v0.8.7/CHANGELOG.md))

## H. Strengths and limitations for text retrieval

**Strengths**

- Embeddings, document text, and metadata share one transactional Postgres database.
- Exact search is the default. Approximate search is something you turn on.
- Selective metadata filters are ordinary SQL indexes. Iterative scans are the documented fix when an approximate index filters too early.
- Lexical search is already in Postgres: `tsvector`, a GIN index, and `ts_rank_cd`.
- Half-precision and binary quantization plus a re-rank are the documented way to shrink RAM.
- WAL gives replicas and point-in-time recovery. Any language with a Postgres client can query it.

**Limitations**

- No documented BM25, and no fusion operator inside the extension. `sparsevec` is not the hybrid lexical type, and its HNSW index allows 1,000 non-zero elements.
- Approximate filters run after the scan. The 10% / `ef_search=40` / about-4-rows illustration is the failure mode to remember.
- HNSW costs memory and build time. IVFFlat needs a populated table and has lower recall at the same speed.
- Index dimension caps are 2,000 for `vector`, 4,000 for `halfvec`, 64,000 for `bit`, and 1,000 non-zero elements for `sparsevec`.
- A shared approximate index couples tenants. Isolation wants partitions or separate tables.
- HNSW vacuum is slow, and 0.8.3–0.8.4 fixed vacuum corruption. Stay on a current patch.
- Indexes are faster in RAM. The docs give no resident-set or row-count formula for when they stop being fast enough.
- The point at which a dedicated vector database is the alternative is not stated. The documented next step after one node is still Postgres: quantize, add memory, CPU, and disk, add replicas, or shard with Citus or PgDog.

([README](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md), [PostgreSQL 18, 12.3](https://www.postgresql.org/docs/18/textsearch-controls.html), [CHANGELOG at v0.8.7](https://github.com/pgvector/pgvector/blob/v0.8.7/CHANGELOG.md))

Present upstream pgvector 0.8.7 when the documents, metadata, and embeddings already belong in one Postgres and you would rather run an extension than a second database. Describe the search path as exact distance ordering, HNSW once an exact scan is the wrong cost, Postgres full text as the lexical leg, and reciprocal rank fusion or a cross-encoder in application SQL as the combiner the README names. Size `maintenance_work_mem` so the HNSW graph builds in memory. Use `halfvec` or binary quantization with a re-rank when float32 will not fit. A dedicated vector database is the comparison once quantize, a larger node, replicas, or Citus/PgDog is the system you do not want to run. These sources do not tell you the row count where that happens.

## I. Sources

1. [pgvector README at `bcbb135`](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/README.md) Types, operators, both indexes, filtering, iterative scans, the hybrid paragraph, and the scaling section. This is the page to keep open.
2. [CHANGELOG at v0.8.7](https://github.com/pgvector/pgvector/blob/v0.8.7/CHANGELOG.md) What actually shipped from 0.6.0 through 0.8.7, including the vacuum fixes.
3. [CHANGELOG on master](https://github.com/pgvector/pgvector/blob/bcbb135db5f6f7539965e18565ddd5990efcf165/CHANGELOG.md) Shows 0.9.0 as unreleased, so a talk pinned to 0.8.7 does not claim async I/O.
4. [LICENSE at v0.8.7](https://github.com/pgvector/pgvector/blob/v0.8.7/LICENSE) The PostgreSQL License text.
5. [PostgreSQL 18, full-text introduction](https://www.postgresql.org/docs/18/textsearch-intro.html) Why the lexical half is `tsvector` and `tsquery`.
6. [PostgreSQL 18, controlling text search](https://www.postgresql.org/docs/18/textsearch-controls.html) `ts_rank` and `ts_rank_cd`, and the absence of BM25 on that page.
7. [PostgreSQL 18, text-search indexes](https://www.postgresql.org/docs/18/textsearch-indexes.html) GIN for the keyword column, separate from HNSW.
8. [pgvector issue 623](https://github.com/pgvector/pgvector/issues/623) The maintainer’s statement that summing two distance operators skips the index.
9. [pgvector issue 54](https://github.com/pgvector/pgvector/issues/54) The pointer to hosted providers. Not read. Open it when you need to know which host packages which version, and expect the list to go stale independently of tag 0.8.7.

Learning pointers, not evidence, and not read: the RRF and cross-encoder examples at `pgvector-python/examples/hybrid_search/`, and the Citus example linked from the scaling section. The papers in the README “Thanks” section (HNSW, Faiss, PASE, and the k-means papers) were not read. High-level index behavior above is the README’s.

Figures such as the 10% filter illustration and `lists = rows / 1000` are the README’s starting guidance, not benchmark winners.
