# Presentation runbook: Self-Hosted Vector Databases for Text Retrieval

About **10 minutes**. Slides only. First person. Every number below is from the official docs, checked 2026-11-09. Say once, early, that you did not run the databases. Each slide has a TLDR. That is the point of the slide. The Say block is what you speak.

**The line the talk defends.** Stay on pgvector when the text is already in Postgres, the dimension fits an index (2,000 float32 or 4,000 halfvec), and you can write the fusion SQL. Leave for built-in fusion, in-index filters, or more than one machine.

Versions if someone asks: Qdrant v1.20.0 (2026-10-22), Weaviate v1.40.4 (2026-11-05), Milvus v3.0.5 with docs branch `v3.0.x`, pgvector 0.8.7 (changelog 2026-10-01).

## Clock

| Time | Slide | Job |
|---|---|---|
| 0:00–1:00 | 1–2 | Why a vector database, and the question |
| 1:00–2:15 | 3 | Two kinds of system, one sentence each |
| 2:15–3:45 | 4 | How each filter helps or hurts retrieval |
| 3:45–5:05 | 5 | The four fusion formulas |
| 5:05–7:15 | 6–7 | The stay rule, the cluster sentence, the three picks |
| 7:15–8:00 | 7 | Your assessment |
| 8:00–10:00 | 8 | Ten sources, one sentence on why each one helps |

If you are past 10:30 when you reach the sources slide, say the pgvector README, the three fusion pages, and Qdrant capacity planning, then point at the other five. Drop the Citus/PgDog clause and the "hold out a labeled set" sentence before that. Keep the dimension cap and the four formulas.

## Slide 1 — Title (leave it up while you say this)

**TLDR**

This slide names the talk. Text retrieval by shared words misses a document that says the same thing in different words. I am looking at four systems I can run myself, and I did not run them. The stay-or-leave question waits until pgvector has been defined.

**On the slide**

- Self-hosted vector databases for text retrieval
- pgvector, Qdrant, Weaviate, Milvus
- A choice from the docs. I did not run these systems.

**Say**

Keyword search finds a document that shares words with the query and misses one that says the same thing in different words. That gap is the text-retrieval problem this talk is about. I look at four systems you can run yourself, pgvector, Qdrant, Weaviate, and Milvus. They store a numeric stand-in for the text and return the nearest ones. I did not run them. The comparison is from the docs.

## Slide 2 — The problem (0:00–1:00)

**TLDR**

This slide is why a vector database exists for text. Keyword search matches shared words. An embedding is a list of numbers that stands in for meaning. A vector database stores those embeddings, returns the nearest ones, and can filter on metadata in the same query. Define pgvector before the question: it is a column in Postgres, next to the text. The other three are a second system.

**On the slide**

- Same words: keyword search can find the document
- Same meaning, different words: keyword search misses it
- A vector database stores embeddings and returns the nearest ones
- It can filter on metadata in the same query

**Say**

Keyword search finds documents that share words with the query. It misses the document that says the same thing in different words.

Vector search turns text into an embedding, a list of numbers that stands in for meaning, and looks for embeddings near the query. A vector database stores those embeddings and returns the neighbors. It can also filter on ordinary metadata in the same query: date, author, source, category.

I looked at four systems you can run yourself: pgvector, Qdrant, Weaviate, and Milvus. pgvector is not a new server. The embedding is a column in Postgres, next to the text and the metadata. The other three are a second system. The question I wanted answered is when I would stay, and when I would add one of those three.

## Slide 3 — Two kinds of system (1:00–2:15)

**TLDR**

This slide splits the four into two kinds. pgvector keeps the vector in the database I already operate, on the same row as the text. Qdrant, Weaviate, and Milvus are a second system. They are in the talk because they ship a fusion rule and a filter that takes part in the index walk.

**On the slide**

- pgvector: a column in Postgres, next to the text and the metadata
- Qdrant: a Rust server; a point is a vector plus a JSON payload; filtering is inside the index
- Weaviate: each object keeps its vectors; keywords and similarity hit the same object
- Milvus: Standalone is the one-machine demo; Distributed adds node roles, etcd, and object storage

**Say**

These four are two kinds of system.

pgvector is a PostgreSQL extension. The embedding is a column on the same table as the document and the metadata. The README's design line is to store the vectors with the rest of your data.

Qdrant is a vector database written in Rust. A record is a vector plus a JSON payload. The design goal is filtering inside the index, so the meaning match and the metadata filter share one store.

Weaviate stores each object with its vectors. Keyword match and similarity search run on those same objects.

Milvus is the one built for a collection that may outgrow one machine. Standalone is a single process, and that is the demo. Distributed adds several node roles, plus etcd and object storage.

The first kind keeps the vectors in the database you already operate. The other three are a second system. They are also the ones that ship a combiner for hybrid search, and a filter that takes part in the index walk. Those two differences are the rest of the talk. I have not run any of the four.

## Slide 4 — Filters (2:15–3:45)

**TLDR**

This slide is how a metadata filter helps or hurts approximate search. It helps when the constraint stays in the same query. It hurts when the result comes back short, or when the engine drops the approximate index. HNSW is the graph index. On pgvector, `ef_search` is how many candidates the scan keeps before the `WHERE` runs.

**On the slide.** Four lines, no extra strategies.

- pgvector: the `WHERE` runs after the approximate scan. At `ef_search` 40 and a predicate matching 10% of rows, about 4 rows survive.
- Qdrant: payload-index edges exist only for indexes present when the graph was built.
- Weaviate: allow-list, then the graph walk. A tight list can fall back to a flat scan.
- Milvus: filter first, then approximate search. Past about 98% filtered out, the documented heuristic switches to brute-force FLAT, and the page says the heuristic is not always right.

**Say**

Approximate search and a metadata predicate fight, and each project documents a different fight. A filter supports retrieval when the metadata constraint stays in the same query. It hurts retrieval when the result comes back short, or when the engine gives up the approximate index.

On pgvector, after you add an HNSW index, the `WHERE` runs after that scan. The README's illustration: if the predicate matches about 10 percent of the rows, and `hnsw.ef_search` stays at its default of 40, about 4 rows survive. Ask for 10 and the filter has starved the list. Exact search, with no approximate index, does not do this. That illustration is in the pgvector README.

On Qdrant, filterable HNSW walks the graph on extra edges built from payload indexes. Those edges are for indexes that already existed when the graph was built. Create the payload index afterward and the edges are missing until a rebuild. A very small candidate set can fall back to a full scan. The page is Qdrant's indexing guide.

On Weaviate, search builds an allow-list of ids that pass the filter, then walks HNSW and keeps ids on that list. When the list is restrictive enough, Weaviate can drop to a brute-force scan of the allow-list. The page is Weaviate's filtering concepts.

On Milvus, standard filtering applies the predicate first and then runs approximate search on what remains. The index guide's heuristic says that when the filter removes more than about 98 percent of the rows, use a brute-force FLAT index. The same page says that rule is not always right. The pages are Milvus filtered search and the index guide.

## Slide 5 — Fusion (3:45–5:05)

**TLDR**

This slide is hybrid search, two lists made into one ranking. A keyword score and a vector score are different units, so they cannot be added raw. Fusion is the rule that combines them. Alpha is Weaviate's mix: 0 is keywords only, 1 is vectors only. pgvector names the rule and leaves the SQL to me.

**On the slide.** This is the one mechanism slide. Copy the formulas.

| System | What it ships |
|---|---|
| Qdrant | `1/(k + rank)`, rank starts at 0, default `k` is 2. Best hit on one list: 1/2. |
| Weaviate | Scale each list so the best score is 1 and the worst is 0, then mix with alpha. Server uses 0.75 only when the request omits alpha. |
| Milvus | `1/(k + rank)`, rank starts at 1, default `k` is 60. Best hit on one list: 1/61. |
| pgvector | The README names reciprocal rank fusion and leaves the query to you. |

**Say**

Hybrid search is two lists: a keyword list and a nearest-embedding list. A keyword score and a vector score are different units. Fusion is the rule that makes one ranking. Three of these systems ship a rule. The rules differ.

Qdrant's default is reciprocal rank fusion, 1 over `k` plus rank. Rank starts at 0, and `k` defaults to 2, so the best hit on one list scores one half.

Weaviate's default since 1.24 scales each list so the best raw score is 1 and the worst is 0, then mixes them with alpha. Alpha 0 is keywords only. Alpha 1 is vectors only. The server uses 0.75 only when the request leaves alpha out. Client libraries often send their own value, so I would set alpha in the call.

Milvus's default is also 1 over `k` plus rank. Rank starts at 1, and `k` defaults to 60, so the best hit on one list scores 1 over 61.

pgvector's README names reciprocal rank fusion and does not define it. The hybrid example on that page is a `ts_rank_cd` query. PostgreSQL's full-text ranking page documents `ts_rank` and `ts_rank_cd`. The combiner is SQL you write.

I would tune whichever rule I ship on a labeled set I hold out. Scoring the same queries I used to pick the weights makes the result look better than it is.

## Slide 6 — The rule (5:05–6:20)

**TLDR**

This slide is the decision, not a new mechanism. Stay only when all three are true: the text is already in Postgres, the dimension fits (2,000 on `vector`, 4,000 on `halfvec`), and I can write the fusion SQL. Leave when the limit I actually have is fusion as a feature, the filter inside the index walk, or more than one machine.

**On the slide**

Stay on pgvector when all three are true:

- The text is already in Postgres
- The dimension fits: 2,000 on `vector`, 4,000 on `halfvec`
- You can write the fusion SQL

Leave when any one of these is the limit you actually have:

- You want fusion as a feature
- You want the filter inside the index walk
- One machine is no longer enough

**Say**

Here is the rule I would use.

I would stay on pgvector when the text is already in Postgres, the dimension fits the index, and I can write that fusion SQL. The index cap is 2,000 dimensions for a float32 `vector`, and 4,000 for `halfvec`. A 3,072-dimension float32 model does not fit an HNSW index on `vector`.

I would leave in three cases. I want fusion as a product feature. I want the filter inside the index walk, because the pgvector illustration is a selective `WHERE` coming back short. Or one machine is no longer enough, and a bigger Postgres, replicas, or a sharder such as Citus or PgDog is a system I will not operate.

A cluster is a later step, for a corpus that already fails one node. Qdrant's open-source shard count is fixed at creation. Weaviate moves existing shards onto a new node with replica movement. Milvus Standalone upgrades into Distributed by a migration. There is no online upgrade from Standalone.

## Slide 7 — Which engine, if I leave (6:20–8:00)

**TLDR**

This slide is the pick after I leave. It is not a four-way scoreboard, and pgvector is not on it. Qdrant is one process, filterable HNSW, and a published RAM formula. Weaviate is BM25 in the same server and an alpha I set. Milvus is the system past one machine, which means I also run etcd and object storage.

**On the slide**

- Qdrant: one process, filterable HNSW, a published RAM formula
- Weaviate: BM25 in the same server, and an alpha you set
- Milvus: past one machine, and you will run etcd plus object storage

**Say**

If I leave, the next pick depends on which limit I hit.

I would pick Qdrant when I want one process that does filterable HNSW and I want a published RAM formula before I buy the machine. That formula is on Qdrant's capacity-planning page. It is a formula plus a worked example. It is not a measurement of my corpus.

I would pick Weaviate when I want BM25 in the same server as the objects, and an alpha I set explicitly.

I would pick Milvus when the collection is heading past one machine and I will run etcd and object storage. Standalone is the demo. Distributed is the shape past one machine.

What I take from the four docs is that these are two product choices and one operations choice. Who writes the fusion. Whether the filter participates in the index. How many processes I am willing to run. I would start in Postgres when the text is already there and the dimension fits. I would add a dedicated engine when one of those three limits is the limit I have. I did not run these databases, and I would not rank them from a vendor recall or QPS table. Those figures do not share a dataset, and I did not rerun them.

## Slide 8 — Sources (8:00–10:00)

**TLDR**

This slide is the ten pages a listener would open to check the choice. Each sentence says why that page settles a claim from the talk. The URLs are on the slide. I say the page name and the reason. I do not read the URLs out.

**On the slide.** Ten pages. Name, then URL. No paragraph on the slide. The reason each one helps is spoken, one sentence at a time, in this order.

- [pgvector README](https://github.com/pgvector/pgvector/blob/v0.8.7/README.md) (v0.8.7)
- [PostgreSQL 18 full-text search](https://www.postgresql.org/docs/18/textsearch.html)
- [Qdrant hybrid queries](https://qdrant.tech/documentation/search/hybrid-queries/)
- [Qdrant indexing](https://qdrant.tech/documentation/manage-data/indexing/)
- [Qdrant capacity planning](https://qdrant.tech/documentation/capacity-planning/)
- [Weaviate hybrid concepts](https://docs.weaviate.io/weaviate/concepts/search/hybrid-search)
- [Weaviate filtering](https://docs.weaviate.io/weaviate/concepts/filtering)
- [Milvus RRF ranker](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/userGuide/embeddings-reranking/reranking/rrf-ranker.md)
- [Milvus filtered search](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/userGuide/search-query-get/filtered-search.md)
- [Milvus index explained](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/userGuide/indexes/index-explained.md)

**Say**

These ten are the pages I would hand someone who has to check this choice. One sentence on why each one helps.

The pgvector README is the extension on one page: the dimension caps, the post-filter illustration, and the hybrid section that leaves the combiner to you.

PostgreSQL's full-text search page is the lexical half. It documents `ts_rank` and `ts_rank_cd`. It does not document BM25, which is how you check a claim that pgvector ships BM25.

Qdrant's hybrid queries page is the RRF formula, including the default `k` of 2, and the warning against adding a raw cosine score to a raw BM25 score.

Qdrant's indexing page is where filterable HNSW is specified. The payload-index edges exist only for indexes that were present when the graph was built.

Qdrant's capacity-planning page is the published RAM formula and a worked example. It is a formula, not a measurement of my corpus. That is the page I would use before I buy the machine.

Weaviate's hybrid concepts page is relative score fusion and the alpha warning. The server uses 0.75 only when the request omits alpha. Read it before trusting a client library's default.

Weaviate's filtering page is the allow-list. Search builds that list, then walks the graph, and a tight list can fall back to a flat scan.

The Milvus RRF ranker page uses `k` of 60 and rank starting at 1. The code sample on that page passes `k` of 100. The default and the sample are different numbers.

Milvus filtered search is the order on the filter slide: the predicate runs first, then approximate search runs on what remains.

The Milvus index guide is the 98 percent heuristic. Past about 98 percent filtered out, the documented rule switches to brute-force FLAT, and the same page says that rule is not always right.

## Pages to name, and when

Say the page name out loud. Leave the URL on the slide or in the community.

| When you say it | Page |
|---|---|
| Filter beat, pgvector | [pgvector README, v0.8.7](https://github.com/pgvector/pgvector/blob/v0.8.7/README.md) |
| Filter beat, Qdrant | [Indexing](https://qdrant.tech/documentation/manage-data/indexing/) |
| Filter beat, Weaviate | [Filtering](https://docs.weaviate.io/weaviate/concepts/filtering) |
| Filter beat, Milvus | [Filtered search](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/userGuide/search-query-get/filtered-search.md) and [Index explained](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/userGuide/indexes/index-explained.md) |
| Fusion slide | The fusion pages on the closing slide: the pgvector README, [PostgreSQL 18 full-text search](https://www.postgresql.org/docs/18/textsearch.html), Qdrant hybrid queries, Weaviate hybrid concepts, and the Milvus RRF ranker |
| Qdrant pick | [Capacity planning](https://qdrant.tech/documentation/capacity-planning/) |
| Cluster sentence | [Qdrant overview](https://qdrant.tech/documentation/overview/), [Weaviate horizontal scaling](https://docs.weaviate.io/weaviate/concepts/cluster), [Milvus install overview](https://github.com/milvus-io/milvus-docs/blob/v3.0.x/site/en/getstarted/install-overview.md) |

The closing slide is these ten, and the spoken walkthrough is the short explanation of why each one is useful. The ranked list in `docs/research/comparison.md` is the rest of the TextData set, including the cluster pages named during the talk.

## If someone asks

- **Qdrant has more than one fusion.** Yes. DBSF and weighted RRF exist. The slide is the default, plain RRF with `k` of 2. Say that and stop.
- **Weaviate used to fuse by rank.** Through v1.23 the default was `1/(rank + 60)`. Relative score fusion is the default since v1.24.
- **Milvus has a weighted ranker.** Yes. Leave the disagreement between the limits page and the weighted-ranker guide alone. It is unresolved in the notes.
- **Where is the row count where Postgres is too small?** No official page in this set gives one. The stay rule is the conditions above, not a magic corpus size.
- **Did you benchmark them?** No.

## Leave out of the recording

The 2024–2026 changelog, tenancy and access control, quantization ratios, vendor recall and QPS, and any ranking of the four by speed. Those are in the research notes. They are not in this 10 minutes.
