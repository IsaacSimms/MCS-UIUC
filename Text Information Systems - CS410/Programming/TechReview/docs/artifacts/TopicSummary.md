# Technology Review Topic: Self-Hosted Vector Databases for Text Retrieval

## What this topic is

This Technology Review examines **self-hosted vector databases** used for text retrieval. It compares four systems:

- Qdrant
- Weaviate
- Milvus
- pgvector

The goal is to explain what these systems do, how they differ in practice, and when one is a better fit than another for retrieving text by meaning rather than exact keywords.

## The problem it addresses

Traditional keyword search (BM25) finds documents that contain the same words as the query. It fails when the wording differs even if the meaning is the same.

Vector search solves this by turning text into numerical embeddings that represent meaning. A **vector database** stores those embeddings and can quickly find the nearest ones to a query embedding. It also usually supports filtering on ordinary metadata (date, author, category, source, etc.) at the same time.

For a sysadmin or infrastructure-focused person, the interesting questions are operational:

- How do you deploy and run each system?
- What are the resource costs (memory, CPU, disk)?
- How well does it support hybrid search (keywords + meaning)?
- How does metadata filtering behave?
- What are the practical trade-offs?

## Why these four systems

| System   | Type                  | Notes                                      |
|----------|-----------------------|--------------------------------------------|
| Qdrant   | Dedicated vector DB   | Rust-based, relatively light, strong filtering |
| Weaviate | Dedicated vector DB   | Strong native hybrid search                |
| Milvus   | Dedicated vector DB   | Built for larger scale, heavier to operate |
| pgvector | Postgres extension    | Runs inside existing PostgreSQL            |

They represent the main practical choices someone faces when adding vector search to a text retrieval stack without relying solely on a fully managed SaaS.

## What the review covers

For each system:

- What it is and its design goal
- High-level architecture
- Deployment models (single-node, cluster, managed)
- Resource characteristics
- Hybrid search support
- Metadata filtering and multi-tenancy
- Notable changes from 2024–2026
- Strengths and limitations for text retrieval
- Key resources

The comparison looks at the same dimensions side-by-side and includes cross-cutting notes on hybrid fusion methods, embedding considerations, evaluation basics, common pitfalls, and when a dedicated vector database is unnecessary.

## Why this fits CS410

The topic sits in the core area of text data retrieval and analysis. It is infrastructure-focused, has abundant recent practical resources and benchmarks, and can be explained at a level that does not require deep expertise in embedding math or ranking theory. It produces clear strengths, limitations, and trade-offs suitable for an 8–12 minute Technology Review presentation.