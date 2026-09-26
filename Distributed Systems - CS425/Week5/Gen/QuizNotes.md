# Notes from completeing CS425 week 5 quiz

How virtual rings work in cassandra. How nodes are placed on that ring, along with how replicas are placed within those nodes based on the ring. 

How nitches work in cassandra

Granular of what CAP, what consistency models are, and what the tradeoffs are weak vs strong consistency


"A Cassandra-like key-value store system uses write consistency level of size W and read level of size R. There are N replicas of each key, and N is an even integer that is large enough. You are told that to maintain the strong consistency needed by your application, all conflicting writes must be detected by at least one replica (i.e., any two sets of written replicas must overlap) and a read must return the value of the latest acknowledged write (i.e., a read replica set must overlap with every written replica set). Which of the following combinations DOES maintain strong consistency?" 
^^ Still don't totally understand how to answer this one, more review required.

Lamport timestamps: Lamport events = internal + send + receive. Init (0) is not an event.
these timestamps are a single int

You need to be able to look at a lamprot timestamp graph and diagnose what the timestamp is at any given point.
Same for Vector timestamps.
This "look at timestamp graphs and be able to produce a number" concept is 



Understand how bloom filters work at a granular level. How bits are set to 0/1

# CS425 — Bloom filters (quiz mechanics)

Created by: Isaac Simms
Category: CS425

A Bloom filter is an `m`-bit array, start all 0s, plus `k` hash functions `h1..hk` each mapping a key → `{0,…,m-1}`.

- **Insert(x):** set `B[hi(x)] = 1` for every i.
- **Query(x):** if any `B[hi(x)]` is 0 → **definitely not present**. If all are 1 → **maybe present**.
- False negatives: impossible (no deletes).
- False positives: possible. Bits that x would need were set by *other* keys. Query says yes, x was never inserted.

That is the whole contract. “In the filter” on the quiz means the query returned yes.

## Hand arithmetic for this quiz

Given `hi(x) = ((x² + x³) · i) mod m` with `m = 32`, `i ∈ {1,2,3}`.

Never compute `2010³`. Reduce first:

`r = x mod 32`, then `(x² + x³) ≡ r² + r³ (mod 32)`, then `× i`, then mod 32.

`32 × 62 = 1984`, so the years on the quiz:

| x | r |
|---|---|
| 2013 | 29 |
| 2010 | 26 |
| 2007 | 23 |
| 2004 | 20 |
| 2001 | 17 |
| 1998 | 14 |
| 0 | 0 |

Square `r` (≤961), leftover after multiples of 32, multiply by `r` once more, add, scale by i.

Worked leftover pattern: `26²=676`, `32×21=672` → 4; `26×4=104`, `32×3=96` → 8; sum 12 → hashes **12, 24, 4**.

## Bits this quiz actually sets

| x | h1, h2, h3 |
|---|---|
| 2010 | 12, 24, 4 |
| 2013 | 14, 28, 10 |
| 2007 | 24, 16, 8 |
| 2004 | 16, 0, 16 |
| 2001 | 18, 4, 22 |
| 1998 | 28, 24, 20 |
| 0 | 0, 0, 0 |

- After 2010+2013: `{4,10,12,14,24,28}` → **16 is not set**.
- After the listed inserts: **28 is set**; 30, 6, 26 never are.
- Query 0 looks only at bit 0. 2004 already set it. 0 was not inserted → **false positive**.

## Keep

Query is a bit check, not a stored-key check. One 0 ⇒ no. All 1s ⇒ maybe. All 1s + key never inserted = false positive. Mod-before-you-cube is how you survive the arithmetic questions.

