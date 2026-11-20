# 02 · Evaluating Retrieval Systems (Week 3)

[← 01 Retrieval & VSM](01-Retrieval-and-VSM.md) · [Overview](00-Overview.md) · Next: [03 Probabilistic / LM Retrieval](03-Probabilistic-LM-Retrieval.md)

## 1. Why and how
- Measure **effectiveness** (relevant docs ranked on top), **efficiency** (time/space), and real-user **utility** (user studies).
- **Cranfield methodology** (1960s lab standard): **freeze** (1) a document collection, (2) a set of queries, (3) relevance judgments. Judgments are made **by humans once**, and the collection is **reusable** to compare systems. It simulates queries and collections but does involve humans for judgments.
- Test collections are hard to build: representative queries and docs, judging at scale, and measures that match user utility.

## 2. Set-based measures (CORRECT definitions)
|  | Retrieved | Not retrieved |
|---|---|---|
| **Relevant** | a (TP) | b (FN) |
| **Not relevant** | c (FP) | d (TN) |

- **Precision = a/(a+c)** = relevant retrieved ÷ **all retrieved**.
- **Recall = a/(a+b)** = relevant retrieved ÷ **all relevant in the collection**.
- **F_β = (β²+1)·P·R / (β²·P + R)**. **F₁ = 2PR/(P+R)** (harmonic mean). **Larger β → favors recall.** A recall-critical task (filtering for possible terrorist plans) → **higher** β.
- F₁ ≤ 2P·1/(P+1). With P=0.5, F₁ can be at most **2/3**, so **F₁=0.75 with P=0.5 is impossible**.
- ⚠ Your Week 3 quiz note has precision and recall **swapped**. The lecture and quiz answers above are right.
- Recall@k can only increase with k. **Precision@10 is NOT always higher than precision@20.**
- If A has higher precision@k than B **for every k**, A also has higher recall@k for every k (recall@k = P@k·k / #relevant).

## 3. Ranked lists
- Evaluate at a **cutoff** k (e.g., precision@10, what the user actually reads). Docs beyond the cutoff count as 0.
- **PR curve**: precision (y) vs recall (x), plot at each relevant doc. **Curve A above B at all recall levels → A is better.** Not monotonic. The **ideal** system is a flat line at precision = 1.
- **Average Precision (AP)** = Σ over each relevant doc found of precision at its rank ÷ **total # relevant in the collection** (not just retrieved). Sensitive to **ranks** of relevant docs; it effectively combines precision and recall.
  - Example (5 relevant total): hits at ranks 1,2 → (1/1+2/2)/5 = **2/5**. Hits at ranks 2,5,10 → (1/2+2/5+3/10)/5 = **6/25**.
  - Example (4 relevant): one hit at rank 2 → (1/2)/4 = **1/8**. Hits at 1,2 → (1+1)/4 = **1/2**.
  - Also: P@10 = 1/10 and R = 1/4 for the first; P@10 = 2/10 and R = 2/4 for the second.
- **MAP** = arithmetic mean of AP over queries; **dominated by high (easy) queries**. **gMAP** = geometric mean (Q-th root of product); **dominated by low (hard) queries**, so use it to improve poor queries.
  - Higher MAP does **not** imply higher gMAP.
  - Higher P@10 does **not** imply higher AP.
- **Reciprocal rank** = 1/r when exactly one relevant doc (known-item search) → **MRR**.

## 4. Multi-level relevance → gain
- Use **gain** (e.g., 3 = highly relevant, 2, 1, 0). Precision/recall need binary judgments.
- **CG** = sum of gains down the list (ignores position).
- **DCG@k** = G₁ + G₂/log 2 + G₃/log 3 + … (lecture form: rank 1 undiscounted, rank i divided by log i). Some texts use log₂(i+1); the idea is the same. **The discount applies at every position, not just the top ones.**
- **nDCG@k = DCG@k / ideal DCG@k**. Range **[0,1]**; 1 = ideal ordering. **DCG isn't bounded to [0,1], nDCG is.**
  - nDCG is what lets you **compare across queries**: raw DCG scales with how many good docs exist for that query.
- nDCG, DCG, and MAP all suit comparing ranking algorithms; precision@10 is easy for users to interpret.

## 5. Significance and pooling
- **Statistical significance testing** asks whether an observed mean difference could be due to which queries you happened to pick.
- **Sign test**: + if B beats A on a query, − if A beats B; a balanced split means no significance. **Wilcoxon** also ranks the *size* of the differences.
- **Pooling**: judge only a **subset**: take top-k results from a **diverse set of systems**, union them into a pool, have humans judge the pool.
  - Purpose: **we don't need to judge every document** (human judging is still needed).
  - Unjudged docs are assumed non-relevant. Works for systems that contributed to the pool; **biased against new systems**.

## Quiz traps
- Practice: AP uses *total relevant* (not retrieved) as denominator, so retrieving 2 of 5 relevant at ranks 1–2 gives 2/5, not 1.
- "Why is pooling useful?" → don't need to judge every doc (not "no humans").
- "DCG is better than nDCG because bounded in [0,1]" is **wrong** (nDCG is bounded).
- "nDCG@k discounts only top-ranked docs" is **wrong**.
- Cranfield "does not involve humans for relevance judgments" is **NOT true**.
- A PR curve above another at all recall values → better. The ideal PR curve is a *horizontal line*, not monotone increasing/decreasing.
- Average precision **does** show rank differences.
