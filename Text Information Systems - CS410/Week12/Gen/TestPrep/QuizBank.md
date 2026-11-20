# CS410 Quiz Bank (for a quizzing agent)

This file is long on purpose. It holds the questions from your weekly quizzes and practice quizzes (tagged **ORIGINAL**) plus similar but not identical questions (tagged **VARIANT**). Every item has the answer and a full explanation, and links to the cheat-sheet file to review.

## Instructions for the quizzing agent (read first)
You are quizzing a student who has a 1-hour CS410 (Text Information Systems, UIUC MCS) exam made of questions like the weekly quizzes.

1. **Ask one question at a time.** Show the question and options only. **Never show the answer, the explanation, or the item tags before the student answers.**
2. After the student answers: say **correct / incorrect**, give the correct answer, and give the explanation in your own words. If the student was wrong or guessed, ask one short follow-up that tests the underlying idea, then link them to the **Review** file.
3. **Order**: start with ORIGINAL items, then VARIANT items of the same topic. Let the student pick a section (1–6) or run "mixed". Prioritize sections 2, 3, 4 and 6 (highest quiz weight).
4. **Track misses.** Re-ask missed items (reworded) later in the session. At the end, list weak topics and the matching review files.
5. Calculation items: ask the student to show the work; accept equivalent forms (0.5 = 1/2). Do not give hints unless asked, and then give the smallest hint first.
6. Question types seen on the real quizzes: multiple choice, **check-all-that-apply**, **true/false**, and **"which is NOT true"**. Mix them.
7. Items tagged **TOPIC** come from the student's quiz-topic notes (no screenshot was available); items marked ⚠ rest on the student's own screenshot selection and were not independently verifiable.
8. Be concise. No praise filler.

**Item key:** `<section>.<n>` = original, `<section>.<n>a/b` = variants of that original. Sources: W# = week, "Practice" = practice quiz, "Quiz" = graded quiz.

**Sections:** 1 Retrieval & VSM (W1–2) · 2 Evaluation (W3) · 3 LM Retrieval (W4) · 4 Feedback / Web / Recommenders (W5–6) · 5 Text Mining & Topic Models (W7–8) · 6 Categorization, Clustering, Opinions, Context (W9–12)

---

# Section 1 · Retrieval & VSM (Weeks 1–2)
Review: [01-Retrieval-and-VSM.md](01-Retrieval-and-VSM.md)

### 1.1 · W1 Practice Q1 · ORIGINAL
Bit-vector VSM. Q = "future of online education"; D1 = "Coursera is shaping the future of online education; online education is affordable."; D2 = "In the future, online education will dominate." V(X) = [future, of, online, education]. Which is true?
- A) V(Q)=[1 1 1 1], V(D1)=[1 1 1 1], V(D2)=[1 0 1 1]
- B) V(Q)=[1 1 1 1], V(D1)=[1 1 0 1], V(D2)=[1 0 1 1]
- C) V(Q)=[1 1 1 1], V(D1)=[1 1 2 2], V(D2)=[1 1 1 1]

**Answer:** A. **Why:** Bit vectors record presence only. D1 contains all four terms (including "of"); D2 lacks "of". C uses counts, which is a TF vector, not a bit vector.

### 1.2 · W1 Practice Q2 · ORIGINAL
Same scenario, dot product as the similarity. Which is true?
- A) Sim(Q,D1)=6, Sim(Q,D2)=4  B) Sim(Q,D1)=6, Sim(Q,D2)=3  C) Sim(Q,D1)=4, Sim(Q,D2)=3

**Answer:** C. **Why:** Dot product of bit vectors = number of shared terms: [1111]·[1111]=4, [1111]·[1011]=3. 6 would require counts.

### 1.2a · VARIANT
Same Q, D1, D2, but now each vector holds **raw term counts** (TF vectors) and similarity is the dot product. What are Sim(Q,D1) and Sim(Q,D2)?

**Answer:** Sim(Q,D1)=6, Sim(Q,D2)=3. **Why:** D1 counts = [1,1,2,2] (future 1, of 1, online 2, education 2) → 1+1+2+2 = 6. D2 = [1,0,1,1] → 3. Q = [1,1,1,1]. Repeating "online education" in D1 raises its score only under TF weighting.

### 1.2b · VARIANT
With bit vectors, Q = "learning from online data", terms [learning, online, data, future]; D1 = "Online data is the future"; D2 = "Learning online is fun". What are the dot products?

**Answer:** Sim(Q,D1)=2, Sim(Q,D2)=2. **Why:** Q=[1,1,1,0]. D1=[0,1,1,1] → shares online+data = 2. D2=[1,1,0,0] → shares learning+online = 2. A tie, which shows a weakness of the bit-vector model (no TF/IDF).

### 1.3 · W1 Practice Q3 · ORIGINAL
Which is **NOT** a reason ranking is preferred over document selection?
- A) Not all relevant documents are equally relevant. B) Users prefer to browse results sequentially. C) The boundary between relevant and not relevant is hard to define. D) Ranking is computationally easier than selection.

**Answer:** D. **Why:** Ranking is preferred because relevance is graded, users browse in order, and a binary cutoff is hard to set. Computational ease is not a stated reason.

### 1.3a · VARIANT
Under the Probability Ranking Principle, ranking by P(relevant) is optimal when (check all that apply):
- A) The utility of a document is independent of other documents.  B) The user browses results sequentially.  C) All relevant documents are equally relevant.  D) Documents are short.

**Answer:** A and B. **Why:** These are the two assumptions of the PRP. C and D are not.

### 1.4 · W1 Practice Q4 · ORIGINAL
Which text-retrieval scenario relies **LESS** on NLP?
- A) Use an English query to retrieve French documents  B) Compare homework submissions to check for plagiarism

**Answer:** B. **Why:** Plagiarism detection compares surface strings between same-language texts. Cross-language retrieval needs translation/language understanding.

### 1.4a · VARIANT
Which scenario relies **MOST** on deeper NLP (parsing/semantics) rather than bag-of-words?
- A) Keyword search over a news archive  B) Machine translation  C) Ranking pages by term frequency

**Answer:** B. **Why:** Translation needs structure and meaning; BOW discards word order. Search engines get by with BOW.

### 1.5 · W1 Practice Q5 · ORIGINAL (check all that apply)
What information is **lost** with a "bag of words" representation?
- A) Word occurrence counts  B) Number of unique words  C) Document length  D) Phrases formed by multiple words  E) Word ordering

**Answer:** D and E. **Why:** BOW keeps counts (so also length and unique words) but throws away order and therefore phrases.

### 1.5a · VARIANT
"Java applet" vs "Java coffee": a bag-of-words retrieval model can partly resolve the ambiguity of "Java" because…
- A) It parses the sentence  B) Other query words (e.g., "applet") co-occur in matching documents  C) It tags parts of speech

**Answer:** B. **Why:** Context terms in the query (and in matching docs) disambiguate without deep NLP; relevance feedback helps too.

### 1.6 · W1 Practice Q6 · ORIGINAL (check all that apply)
Which applications provide **push** information access? Bing · Netflix · Spotify mobile app · Google Maps (search)

**Answer:** Netflix, Spotify. **Why:** Push = the system recommends/delivers without a query. Bing and map search are pull (user-initiated).

### 1.6a · VARIANT
Match each to push or pull: (i) typing a query into a search box, (ii) a "recommended for you" home feed, (iii) browsing a topic hierarchy, (iv) an email spam filter delivering your mail.

**Answer:** (i) pull, (ii) push, (iii) pull (browsing), (iv) push (filtering with a stable profile). **Why:** Pull = user takes initiative (query or browse). Push = system takes initiative given a stable need.

### 1.7 · W1 Practice Q7 · ORIGINAL (check all that apply)
What makes text retrieval harder than database retrieval? Unstructured/free-text query and data · Subjective judgement of relevance and empirical evaluation involving humans · Ambiguity in text

**Answer:** All three. (Your screenshot annotation: the "subjective judgement" option "is also correct".) **Why:** DB retrieval has structured data, exact semantics (SQL) and exact matches; TR is empirical and ambiguous.

### 1.7a · VARIANT (True/False)
"A database query completely specifies the records to return, whereas a text query is often ambiguous and incomplete."

**Answer:** True.

### 1.8 · W1 Practice Q8 · ORIGINAL
How many syntactic structures can you identify in "A man saw a boy with a telescope"? 1 / 2 / 3

**Answer:** 2. **Why:** "with a telescope" attaches either to *saw* (the man used it) or to *boy* (the boy has it).

### 1.8a · VARIANT
"John persuaded Bill to buy a TV for himself." Resolving who "himself" refers to is called… and it is an example of ambiguity at which level?
- A) POS tagging, lexical  B) Anaphora resolution, discourse/semantic  C) Stemming, lexical

**Answer:** B.

### 1.9 · W1 Practice Q9 · ORIGINAL
In the VSM, which similarity/distance measure is **affected by document length**? L2 distance ‖v₁−v₂‖ or cosine similarity?

**Answer:** L2 distance. **Why:** Longer docs have larger count vectors that lie farther from the origin. Cosine divides by the vector lengths, so scaling cancels.

### 1.9a · VARIANT
d₂ is d₁ repeated twice (every count doubled). What is cos(d₁,d₂), and is ‖d₁−d₂‖₂ zero?

**Answer:** cos = 1; L2 distance is not zero (it equals ‖d₁‖). **Why:** Same direction → angle 0 → cosine 1. Different magnitude → positive L2 distance.

---
### Week 2 topics (TOPIC items from your Week 2 quiz notes; no screenshot)

### 1.10 · TOPIC · gamma encode
Encode the d-gap **9** in gamma code.

**Answer:** 1110001. **Why:** 9=1001 → drop the leading 1 → offset 001 (3 bits) → 3 ones + 0 = 1110 → 1110|001.

### 1.10a · VARIANT
Gamma-encode the term frequency **6**, and the d-gap sequence for docIDs 3, 7, 8, 15 (gaps first, then each gap's gamma code).

**Answer:** γ(6)=11010 (110 → offset 10). Gaps = 3, 4, 1, 7 (first value is the docID itself). Codes: γ(3)=101, γ(4)=11000, γ(1)=0, γ(7)=11011. **Why:** 4=100→offset 00→110|00; 7=111→offset 11→110|11.

### 1.11 · TOPIC · gamma decode
Decode **1110010**.

**Answer:** 10. **Why:** 1110|010 — three ones before the first 0 ⇒ 3 offset bits (010); put the 1 back → 1010 = 10.

### 1.11a · VARIANT
Decode the gamma codes 110101 and 11001, and recover the docIDs if the d-gaps decode to 2, 3, 5.

**Answer:** 110101 → 6; 11001 → 5. docIDs: 2, 5, 10 (running sum). **Why:** 110101: two ones then 0 ⇒ N=2, offset = next 2 bits "10", put the leading 1 back → 110 = 6. 11001: N=2, offset "01" → 101 = 5.

### 1.12 · TOPIC · accumulators
A query has two terms. How many accumulators are allocated for a document containing both, and when?

**Answer:** One, allocated the first time the document appears in a query term's postings list. **Why:** Accumulators are per matched document, created lazily; docs with no matching term never get one.

### 1.12a · VARIANT
Query "information security"; the postings list for "information" has 800 docs and for "security" has 500 docs, 200 of which are in both. At most how many accumulators exist, in a collection of 1,000,000 docs?

**Answer:** 1,100 (800 + 500 − 200). **Why:** Union of the matching docs, not the collection size.

### 1.13 · TOPIC · Zipf and stop words
State Zipf's law, and say what it implies for IDF weighting and compression.

**Answer:** rank × frequency ≈ constant (frequency ∝ 1/rank). A few words are very common (structural words → low IDF, often removed); most are rare (high IDF). Small integers are far more common than large ones, so variable-length codes with fewer bits for small values save space.

### 1.13a · VARIANT
The most frequent word occurs 6000 times. By Zipf's law approximately how often does the 3rd most frequent word occur?

**Answer:** ≈ 2000. **Why:** rank × freq = 6000×1 → freq(3) = 6000/3.

### 1.14 · TOPIC · BM25 TF transformation
In y = (k+1)x/(x+k): what happens at k=0, as k→∞, and what is the upper bound?

**Answer:** k=0 → bit vector (y=1 for x≥1); k→∞ → linear in x (raw TF); upper bound k+1 as x grows. **Why:** Sublinear TF caps the influence of repeated terms.

### 1.14a · VARIANT
With k=1, compute y for x = 1, 3, and the limit as x → ∞.

**Answer:** y(1)=1, y(3)=(2·3)/(3+1)=1.5, limit 2. **Why:** (k+1)=2.

### 1.15 · TOPIC · length normalization
In pivoted normalization 1−b+b·|d|/avdl, what does b=0 do, and what is the penalty for a document twice the average length when b=0.5?

**Answer:** b=0 → no length normalization. Twice the average, b=0.5 → 1−0.5+0.5·2 = **1.5** (>1, penalty; a doc of average length has normalizer 1).

### 1.15a · VARIANT
For which document does the normalizer fall below 1 (a bonus): longer or shorter than the average length? (b>0)

**Answer:** Shorter. **Why:** |d|<avdl ⇒ 1−b+b|d|/avdl < 1 ⇒ the score is divided by something smaller than 1 (boosted).

### 1.16 · TOPIC · IDF
Which has a higher IDF in log((M+1)/df): a term in 1 doc or a term in every doc? Does the log base change the ranking?

**Answer:** The term in 1 doc (maximal). A term in every doc → IDF ≈ 0. The base does not change the ranking.

### 1.16a · VARIANT (True/False)
"IDF gives a larger weight to a stop word like 'the' because it appears in so many documents."

**Answer:** False. High df → low IDF.

### 1.17 · TOPIC · inverted index structure
Which parts of an inverted index are kept in memory vs on disk, and what does a postings entry contain?

**Answer:** The **dictionary** (term, df, total frequency, pointer) is kept in memory (hash/B-tree); the **postings lists** (docID, tf, optionally positions, sorted by docID) can stay compressed on disk since they are read sequentially. Indexing is offline; scoring is online.

### 1.17a · VARIANT (check all that apply)
Which are true? A) Postings are sorted by docID. B) Positions are stored so phrase queries can be checked. C) The dictionary stores the full document text. D) CPU decompression is usually the bottleneck.

**Answer:** A and B. **Why:** I/O (not CPU) is the bottleneck, which is why compression is cheap.

---
# Section 2 · Evaluation (Week 3)
Review: [02-Evaluation.md](02-Evaluation.md)

*Scenario S (practice):* 5 relevant docs exist in a 100-doc collection. System A returns 10 docs with relevance pattern [+ + − − − − − − − −] and System B [− + − − + − − − − +] (leftmost = top rank).

### 2.1 · W3 Practice Q1 · ORIGINAL
Precision at 10 documents for A and B?
- A) 2/10, 3/10  B) 2/100, 3/100  C) 2/5, 3/5  D) 8/100, 7/100

**Answer:** A. **Why:** Precision@10 = relevant in the top 10 ÷ 10: A has 2, B has 3.

### 2.2 · W3 Practice Q2 · ORIGINAL
Recall for A and B in Scenario S? A) 2/5, 3/5  B) 2/100, 3/100  C) 2/10, 3/10

**Answer:** A. **Why:** Recall = relevant retrieved ÷ total relevant (5). 

### 2.3 · W3 Practice Q3 · ORIGINAL
Average precision of A and B in Scenario S? A) 2/5, 6/25  B) 2/10, 3/25  C) 3/10, 9/20

**Answer:** A. **Why:** A: (1/1 + 2/2)/5 = 2/5. B: relevant at ranks 2, 5, 10 → (1/2 + 2/5 + 3/10)/5 = 1.2/5 = 6/25. The denominator is the total number of relevant docs (5).

### 2.3a · VARIANT (compute)
Query has **6** relevant docs. System C = [+ − + − − + − − − −], System D = [− − + + − − − − − −]. Give P@10, recall, and AP for each.

**Answer:** C: P@10=3/10, R=3/6=1/2, AP=(1/1+2/3+3/6)/6 = (13/6)/6 = **13/36 ≈ 0.361**. D: P@10=2/10, R=2/6=1/3, AP=(1/3+2/4)/6 = (5/6)/6 = **5/36 ≈ 0.139**.

### 2.3b · VARIANT
Only one relevant document exists and a system ranks it 4th. What are AP and the reciprocal rank?

**Answer:** Both 1/4. **Why:** With one relevant doc, AP = RR = 1/r; the mean over queries is MRR.

### 2.4 · W3 Practice Q4 · ORIGINAL
X has a higher **MAP** than Y. Can Y have a higher **gMAP**? Yes/No

**Answer:** Yes. **Why:** MAP is dominated by high-AP queries, gMAP by low ones. A system can win MAP on easy queries and lose gMAP on hard ones.

### 2.4a · VARIANT (compute)
Two queries. System X has AP = 0.9 and 0.1. System Y has AP = 0.5 and 0.5. Compare MAP and gMAP.

**Answer:** MAP: both 0.5. gMAP: X = √(0.9·0.1) = 0.3, Y = 0.5. So Y is better on gMAP and tied on MAP. **Why:** The geometric mean punishes the poor query.

### 2.5 · W3 Practice Q5 · ORIGINAL
If A has higher precision@k than B for **every** k, does A also have higher recall@k than B at every position? Yes/No

**Answer:** Yes. **Why:** recall@k = (#relevant in top k)/R = precision@k·k/R with the same k and R.

### 2.5a · VARIANT
If A has higher **recall@k** than B for every k, does A have higher **precision@k** for every k?

**Answer:** Yes, by the same identity.

### 2.6 · W3 Practice Q6 · ORIGINAL
For an automatic filter searching for possible communications about attack plans, should the F-measure's parameter β be higher or lower?

**Answer:** Higher. **Why:** F_β = (β²+1)PR/(β²P+R); larger β favors **recall**, which matters when missing a threat is costly.

### 2.6a · VARIANT
An email spam filter where blocking a legitimate email is very costly. Higher or lower β?

**Answer:** Lower (β<1 favors precision).

### 2.7 · W3 Practice Q7 · ORIGINAL
What is nDCG capable of but DCG is not?
- A) Compare two systems on a set of queries  B) Compare two systems on one query  C) Work with multi-level judgments  D) Work with binary judgments

**Answer:** A. **Why:** nDCG is normalized into [0,1] by the ideal DCG, so values are comparable across queries. Both handle multi-level and binary judgments, and both work for a single query.

### 2.7a · VARIANT (True/False)
"DCG@k is always between 0 and 1."

**Answer:** False. nDCG@k is.

### 2.8 · W3 Practice Q8 · ORIGINAL
Why is pooling useful? A) So that we don't need to judge every document. B) So that we don't need humans to do judgment. C) So that all documents can be judged efficiently.

**Answer:** A.

### 2.8a · VARIANT (True/False)
"A new system that did not contribute to the pool is evaluated fairly by pooled judgments."

**Answer:** False. Docs it retrieves that no pooled system returned are unjudged (assumed non-relevant), biasing against it.

### 2.9 · W3 Practice Q9 · ORIGINAL
Which is **not** correct? A) Precision@10 is easy for users to interpret. B) MAP and nDCG are good for comparing ranking algorithms. C) DCG is better than nDCG because its value is within [0,1].

**Answer:** C.

### 2.9a · VARIANT (check all that apply)
Which are frozen in the Cranfield methodology? A) Document collection B) Queries C) Relevance judgments D) The ranking algorithm

**Answer:** A, B, C.

### 2.10 · W3 Practice Q10 · ORIGINAL
In PR curves, curve A is above B at every recall level. What can you say? A better / B better / no clear conclusion / equally good

**Answer:** A is better.

### 2.10a · VARIANT
The two PR curves cross. What can you conclude?

**Answer:** No clear winner overall; it depends on the recall region/user need.

### 2.11 · W3 Quiz Q1–Q3 · ORIGINAL
Scenario Q: 4 relevant docs in the collection. System A = [− + − − − − − − − −], System B = [+ + − − − − − − − −]. Give (a) P@10, (b) recall, (c) AP of each.

**Answer:** (a) A 1/10, B 2/10. (b) A 1/4, B 2/4. (c) AP(A) = (1/2)/4 = **1/8**; AP(B) = (1+1)/4 = **1/2**.

### 2.12 · W3 Quiz Q4 · ORIGINAL
X has higher precision at 10 than Y for a specific query. Can Y have a higher average precision on the same query? Yes/No

**Answer:** Yes. **Why:** AP depends on the ranks of all relevant docs, including those beyond rank 10.

### 2.12a · VARIANT
X has a higher AP than Y on a query. Can Y have a higher precision@10?

**Answer:** Yes, for the same reason.

### 2.13 · W3 Quiz Q5 · ORIGINAL
Can a retrieval system have an F1 score of 0.75 and a precision of 0.5? Yes/No

**Answer:** No. **Why:** Even with recall 1 and P=0.5, F1 = 2(0.5)(1)/1.5 = 0.667 < 0.75.

### 2.13a · VARIANT
Can a system have F1 = 0.6 and precision = 0.5?

**Answer:** Yes (recall 0.75: 2·0.5·0.75/1.25 = 0.6).

### 2.14 · W3 Quiz Q6 · ORIGINAL (True/False)
For any ranked list, precision at 10 is **always** higher than precision at 20.

**Answer:** False. **Why:** If ranks 11–20 are all relevant, P@20 can exceed P@10.

### 2.14a · VARIANT (True/False)
Recall at 10 is always less than or equal to recall at 20.

**Answer:** True (the cutoff only adds retrieved docs).

### 2.15 · W3 Quiz Q7 · ORIGINAL
What can you say about the PR curve? A) always monotonically increasing  B) the ideal system's PR curve is a horizontal line  C) always monotonically decreasing

**Answer:** B. **Why:** An ideal system has precision 1 at every recall level. Real curves zigzag.

### 2.16 · W3 Quiz Q8 · ORIGINAL
Which is correct about average precision? A) It combines precision and recall. B) It does not show the difference between ranks of relevant documents.

**Answer:** A. **Why:** AP is sensitive to rank positions and summarizes the PR curve.

### 2.17 · W3 Quiz Q9 · ORIGINAL
Which is **NOT** true about the Cranfield evaluation methodology? A) It simulates user queries. B) It does not involve humans to make relevance judgments. C) It simulates real document collections.

**Answer:** B.

### 2.18 · W3 Quiz Q10 · ORIGINAL
Which is **wrong** about nDCG@k? A) It discounts only top-ranked documents. B) It has a range between 0 and 1. C) It can be used to compare across queries.

**Answer:** A. **Why:** Every rank position is discounted by position, not only the top.

### 2.18a · VARIANT (check all that apply)
Which statements about gain-based metrics are true? A) CG ignores position. B) DCG discounts lower ranks. C) nDCG divides by the ideal DCG. D) nDCG requires binary relevance.

**Answer:** A, B, C. D is false (nDCG is designed for multi-level judgments).

### 2.19 · TOPIC · significance testing
What does a sign test do, and what does Wilcoxon add?

**Answer:** Sign test counts queries where B beats A (+) and A beats B (−); a balanced split means no significant difference. Wilcoxon also ranks the size of the differences.

### 2.19a · VARIANT
System B beats A by an average of 0.2 MAP, but wins on only 3 of 7 queries (large wins, small losses). Why is significance testing needed?

**Answer:** The average gain may come from a few queries; testing asks whether it holds reliably across queries instead of being an artifact of the particular query set.


---
# Section 3 · Probabilistic / Language-Model Retrieval (Week 4)
Review: [03-Probabilistic-LM-Retrieval.md](03-Probabilistic-LM-Retrieval.md)

### 3.1 · W4 Practice Q1 · ORIGINAL
Vocabulary {text, mining, research}. A unigram LM gives p(text)=0.4, p(mining)=0.2. What is the probability of generating "text mining research"?
- A) 0.032  B) 0.4  C) 0  D) 0.08

**Answer:** A. **Why:** Probabilities sum to 1 so p(research)=0.4. Words are drawn independently: 0.4×0.2×0.4 = 0.032.

### 3.1a · VARIANT
Vocabulary {a, b, c}. p(a)=0.5, p(b)=0.3. What is P("a c b")? And P("b c a")?

**Answer:** p(c)=0.2. P("a c b") = 0.5×0.2×0.3 = 0.03 and P("b c a") = 0.03 as well. **Why:** The unigram model ignores order.

### 3.2 · W4 Practice Q2 · ORIGINAL
Query Q = "food safety". D1 = "food quality regulations", D2 = "food safety measures". Using unsmoothed MLE and the unigram query-likelihood model, which is correct?
- A) P(Q|D1)=1/3, P(Q|D2)=1/9  B) 1/2, 1/2  C) P(Q|D1)=0, P(Q|D2)=1/9  D) P(Q|D1)=1/3, P(Q|D2)=0

**Answer:** C. **Why:** D1 lacks "safety" → 0. D2: (1/3)(1/3) = 1/9.

### 3.2a · VARIANT
Q = "data mining"; D1 = "data mining tools", D2 = "text mining". Unsmoothed MLE: P(Q|D1) and P(Q|D2)?

**Answer:** P(Q|D1) = (1/3)(1/3) = 1/9; P(Q|D2) = P(data|D2)·P(mining|D2) = 0·(1/2) = 0.

### 3.3 · W4 Practice Q3 · ORIGINAL (True/False)
Probability smoothing avoids assigning zero probabilities to unseen words in documents.

**Answer:** True.

### 3.3a · VARIANT (True/False)
"Smoothing mainly removes stop words from the query."

**Answer:** False. It reassigns probability mass to unseen words using the collection model; it also supplies IDF-like weighting and length normalization.

### 3.4 · W4 Practice Q4 · ORIGINAL (True/False)
S₁(Q,D)=P(Q|D) and S₂(Q,D)=log P(Q|D) give the same ranked list for the same query and corpus.

**Answer:** True (this is what the quiz marked correct; your first answer "False" was graded wrong). **Why:** log is strictly increasing, so it preserves order; it prevents underflow of products of tiny probabilities. Caveat: with an unsmoothed P(Q|D)=0 the log is undefined, which is one reason smoothing is used.

### 3.4a · VARIANT (True/False)
"Using log probabilities changes which document is ranked first."

**Answer:** False.

### 3.5 · W4 Practice Q5 · ORIGINAL
With Jelinek–Mercer smoothing, what happens to the smoothed probability of a word when λ is **decreased**?
- A) Closer to the ML estimate from the document  B) Closer to the collection probability  C) No change

**Answer:** A. **Why:** p(w|d) = (1−λ)·c(w,d)/|d| + λ·p(w|C). Smaller λ → more weight on the document.

### 3.5a · VARIANT
JM with λ=0.5. In document d (|d|=4), c(w,d)=2 and p(w|C)=0.4. Then for an unseen word u with p(u|C)=0.1, find the smoothed p(w|d) and p(u|d). If λ is increased to 0.9, does p(w|d) go up or down?

**Answer:** p(w|d)=0.5·0.5+0.5·0.4=0.45. p(u|d)=0.5·0+0.5·0.1=0.05. With λ=0.9: 0.1·0.5+0.9·0.4=0.41 → **down** (toward the collection value 0.4).

### 3.6 · W4 Practice Q6 · ORIGINAL
Why is smoothing necessary in the query likelihood model?
- A) If a term is neither in the query nor the document, the likelihood becomes −∞.
- B) If a term in the query is not in the document, the likelihood becomes −∞.
- C) If a term in the document is not in the query, the likelihood becomes −∞.

**Answer:** B. **Why:** log P(q|d)=Σ over query words; an unseen query word gives log 0.

### 3.7 · W4 Practice Q7 ⚠ · ORIGINAL
Which is **NOT** correct about the unigram model?
- A) P(A AND B) is the product of P(A) and P(B).
- B) P("A" "B" "C") equals P("C" "B" "A").
- C) The probability of generating the word A OR B is the sum of P(A) and P(B).

**Answer (from your selection):** C. **Why:** A and B are certainly true (independent draws; order irrelevant), so C must be the odd one: it only holds for a single draw, not across a sequence.

### 3.8 · W4 Quiz Q1 · ORIGINAL (True/False)
Using a unigram LM, P("today is Wednesday") ≠ P("today Wednesday is").

**Answer:** False (they are equal). **Why:** Order is ignored. An n-gram or grammar-aware LM would differ.

### 3.9 · W4 Quiz Q2 · ORIGINAL
Vocabulary {the, computer, science, technology}; p(the)=0.4, p(computer)=0.1, p(science)=0.2. P("the technology")?
- A) 0.0024  B) 0.3  C) 0.12  D) 0.5

**Answer:** C. **Why:** p(technology) = 1−0.7 = 0.3; 0.4×0.3 = 0.12.

### 3.9a · VARIANT
Vocabulary {red, green, blue, black}; p(red)=0.25, p(green)=0.25, p(blue)=0.1. What is P("black black red")?

**Answer:** p(black)=0.4 → 0.4×0.4×0.25 = 0.04.

### 3.10 · W4 Quiz Q3 · ORIGINAL
Q = "online course"; D1 = "online course catalog"; D2 = "affordable online education". Unsmoothed MLE. Which is correct?
- A) 2/3, 1/3  B) 0, 1/3  C) P(Q|D1)=1/9, P(Q|D2)=0  D) 1/9, 1/3

**Answer:** C. **Why:** D1: (1/3)(1/3). D2 has no "course" → 0.

### 3.11 · W4 Quiz Q4 · ORIGINAL
Same docs and query, JM smoothing with λ=0.5. Collection LM: p(online)=1/3, p(course)=1/3, p(education)=1/9. Which is correct?
- A) 1/9, 0  B) 1/9, 1/27  C) 1/18, 1/18  D) 1/9, 1/18

**Answer:** D. **Why:** D1: p(online)=½·⅓+½·⅓=⅓; p(course)=⅓ → 1/9. D2: p(online)=⅓; p(course)=½·0+½·⅓=1/6 → 1/18.

### 3.11a · VARIANT
Same setup but Q = "online education". Compute P(Q|D1) and P(Q|D2) with λ=0.5 and say which ranks higher.

**Answer:** D1: p(online)=⅓, p(education)=½·0+½·(1/9)=1/18 → **1/54**. D2: p(online)=⅓, p(education)=½·⅓+½·(1/9)=2/9 → **2/27**. D2 ranks higher (it contains both words).

### 3.12 · W4 Quiz Q5 · ORIGINAL
If every term count in a document doubles (collection LM unchanged), which is true?
- A) p(w|d) stays the same under Jelinek–Mercer  B) Unsmoothed query likelihood changes for some queries  C) p(w|d) stays the same under Dirichlet-prior smoothing

**Answer:** A. **Why:** ML estimate c/|d| is unchanged, so JM (a fixed mix of ML and collection) is unchanged. Under Dirichlet, (c+μp(w|C))/(|d|+μ) changes. Unsmoothed ML is unchanged too (B false).

### 3.12a · VARIANT
Document d: c(w,d)=2, |d|=4, p(w|C)=0.4, μ=4. Compute p(w|d) under Dirichlet. Then double all counts (c=4, |d|=8) and recompute.

**Answer:** (2+4·0.4)/(4+4) = 0.45. After doubling: (4+1.6)/(8+4) = 0.4667. It changes (JM would stay 0.45 at λ=0.5).

### 3.13 · W4 Quiz Q6 · ORIGINAL
With Dirichlet-prior smoothing, what happens to the smoothed probability of "the" when μ is **decreased**?
- A) Closer to the ML estimate  B) Closer to the collection LM  C) Closer to 1  D) No change

**Answer:** A. **Why:** μ pseudo-counts from the collection get less weight.

### 3.13a · VARIANT (check all that apply)
Which statements are true? A) Dirichlet is generally better for short keyword queries. B) JM is generally better for long, verbose queries. C) Under Dirichlet, longer documents are smoothed less. D) Under JM, shorter documents are smoothed more.

**Answer:** A, B, C. **Why:** JM uses the same λ for every document (so D is false); Dirichlet's α_d = μ/(μ+|d|) shrinks with length.

### 3.14 · TOPIC · what smoothing buys
Name the three roles of smoothing in the rewritten query-likelihood ranking function.

**Answer:** TF weighting (seen-word probability), IDF-like weighting (division by p(w|C)), and document-length normalization (α_d; longer docs less smoothing).

---
# Section 4 · Feedback, Web Search & Recommenders (Weeks 5–6)
Review: [04-Feedback-WebSearch-Recommenders.md](04-Feedback-WebSearch-Recommenders.md)

### 4.1 · W5 Practice Q1 · ORIGINAL
In PageRank, what is **NOT** a benefit of random jumping?
- A) Otherwise a disconnected page always has zero probability.
- B) Otherwise PageRank will favor nodes with fewer incoming links.
- C) Otherwise zero-outlink nodes will receive all the probability.

**Answer:** B. **Why:** Random jumping fixes A and C (dead ends, unreachable pages). It isn't about favoring nodes with fewer in-links; that is the opposite of PageRank's idea.

### 4.1a · VARIANT (True/False)
"In the random-surfer model, with probability 1−α the surfer follows an outlink and with probability α jumps to a random page."

**Answer:** True (α is the jump probability; your notes call the follow probability d = 1−α).

### 4.2 · W5 Practice Q2 · ORIGINAL (True/False)
Modern web search engines often combine many features (content-based and link-based scores) to rank documents.

**Answer:** True. (You first answered False, which was graded wrong.)

### 4.3 · W5 Practice Q3 · ORIGINAL (True/False)
PageRank uses only inter-document links when computing a document's score, without considering the document's content.

**Answer:** True. (False was graded wrong.) **Why:** PageRank is a query-independent link-structure score; it is *combined* with content scores in a full engine.

### 4.4 · W5 Practice Q4 · ORIGINAL
Can a crawler that only follows hyperlinks identify hidden pages that have no incoming links?

**Answer:** No.

### 4.4a · VARIANT
A "seed page" is needed because…

**Answer:** The crawler discovers pages only by following links from URLs it already has.

### 4.5 · W5 Practice Q5 · ORIGINAL
Which is **NOT** a feature of incremental crawling? A) Learns from past experience (daily vs monthly updates) B) Targets frequently accessed pages C) Targets a subset of pages (e.g., all pages about "automobiles") D) Targets frequently updated pages

**Answer:** C (that is focused crawling).

### 4.6 · W5 Practice Q6 · ORIGINAL
Which gets a larger PageRank? A) A site that links out to many others but none link to it. B) A site that many others link to but that links to no one.

**Answer:** B.

### 4.7 · W5 Practice Q7 · ORIGINAL
Which is **NOT** a reason PageRank is efficient? A) Each iteration is a simple matrix multiplication B) The dimension of M is usually large C) M is usually sparse

**Answer:** B.

### 4.8 · W5 Practice Q8 · ORIGINAL
In PageRank, which statement is true about transition probabilities?
- A) The number of parameters in the transition matrix is smaller than its degrees of freedom.
- B) P(A→B) is the same as P(B→A).
- C) The sum of probabilities of jumping from one page to all other pages is one.

**Answer:** C. **Why:** Each row is a probability distribution; M is not symmetric.

### 4.9 · W5 Practice Q9 · ORIGINAL
In the original PageRank algorithm, which page gets the most probability? A) A page that only has incoming links B) A page with equal numbers of incoming and outgoing links

**Answer:** A.

### 4.10 · W5 Practice Q10 · ORIGINAL
Which feedback does **not** involve humans? Relevance / Pseudo / Implicit

**Answer:** Pseudo.

### 4.10a · VARIANT
Order the three feedback types from most to least reliable and say what each assumes.

**Answer:** Relevance (explicit judgments) > implicit (clicks = relevant, skips = non-relevant) > pseudo (top-k assumed relevant, no human). Pseudo is the least reliable but costs no effort.

### 4.11 · W5 Quiz Q1 · ORIGINAL
What size are chunks in GFS? 16MB / 32MB / 128MB / 64MB

**Answer:** 64 MB.

### 4.11a · VARIANT
In GFS, which component stores the file metadata and chunk locations, and which stores the actual bytes?

**Answer:** The master (metadata, namespace, chunk locations); chunkservers hold the data. The client asks the master for locations, then reads the chunk directly from a chunkserver.

### 4.12 · W5 Quiz Q2 · ORIGINAL (True/False)
MapReduce does not allow parallelizing the creation of the inverted index.

**Answer:** False.

### 4.13 · W5 Quiz Q3 · ORIGINAL (True/False)
In MapReduce, the Reduce function is only called once no matter how many pairs the map function produces.

**Answer:** False. Reduce is called once per unique key.

### 4.13a · VARIANT
Word count over 3 documents containing the words {a, b, a, c, b, a}. How many reduce calls, and what does each emit?

**Answer:** 3 reduce calls (keys a, b, c) emitting (a,3), (b,2), (c,1).

### 4.14 · W5 Quiz Q4 · ORIGINAL
What does the map function output to the reduce function? A single string / key-value pairs / compressed bitfeed / line-delimited keys

**Answer:** Key-value pairs.

### 4.15 · W5 Quiz Q5–Q6 · ORIGINAL
Which are challenges in web search? Scalability / low-quality information / dynamics of the web / all of the above

**Answer:** All of the above.

### 4.16 · W5 Quiz Q7 · ORIGINAL
Which type of feedback requires the user to make **explicit** judgments? Pseudo / Implicit / Relevance feedback

**Answer:** Relevance feedback.

### 4.17 · W5 Quiz Q8 · ORIGINAL (True/False)
PageRank can only be used for link analysis.

**Answer:** False.

### 4.18 · W5 Quiz Q9 · ORIGINAL
Which feedback type is considered the least reliable? Pseudo / Relevance / Implicit

**Answer:** Pseudo.

### 4.19 · W5 Quiz Q10 · ORIGINAL
Does normalization affect the ranking from the PageRank algorithm? Yes/No

**Answer:** No (it may change absolute values only).

### 4.20 · W5 Quiz Q11 · ORIGINAL (check all that apply)
True about PageRank? A) The transition matrix is symmetric. B) Values of the transition matrix range from [0,1]. C) It's an iterative algorithm.

**Answer:** B and C.

### 4.20a · VARIANT (check all that apply)
Which are true? A) M is usually sparse. B) A page with no outlinks (dead end) breaks the probability sum unless handled. C) PageRank depends on the user's query. D) Pages with many in-links from highly ranked pages tend to score higher.

**Answer:** A, B, D. **Why:** PageRank is query-independent.

### 4.21 · TOPIC · Rocchio
Describe Rocchio feedback in one sentence, and say how to avoid topic drift.

**Answer:** Move the query vector toward the centroid of relevant documents (and away from non-relevant ones), q' = αq + β·mean(rel) − γ·mean(nonrel). Keep a relatively high weight on the original query, and truncate the vector to the top terms.

### 4.22 · W6 Practice Q1 · ORIGINAL
In collaborative filtering, measuring user similarity with cosine: which is correct?
- A) It will not be biased by user activity (less/more activity of users).
- B) It solves the problem of missing values.

**Answer:** A (graded correct). B is false: unrated entries remain missing.

### 4.23 · W6 Practice Q2 · ORIGINAL (check all that apply)
Which tasks can be solved as a classification problem? Ranking / Spam filtering / Recommendation

**Answer:** All three (your screenshot flagged "didn't select all the correct answers" when Ranking was left out).

### 4.24 · W6 Practice Q3 · ORIGINAL
In recommendation/filtering, which heuristic is **NOT** correct?
- A) The same user will like similar items.
- B) If a user likes one item, he/she will dislike other items not similar to the one liked.
- C) Similar users will like the same items.

**Answer:** B.

### 4.25 · W6 Practice Q4 · ORIGINAL (check all that apply)
Reasons learning-based algorithms became popular in retrieval: more information needs (spam, diversity) · more features available · more methods available for combining

**Answer:** All three.

### 4.26 · W6 Practice Q5 · ORIGINAL
When a new user arrives, which will **NOT** help recommendation? Ask them to select a few liked items / ask for a short self-description / recommend randomly selected items

**Answer:** Random recommendations.

### 4.26a · VARIANT
Name the two classic problems that make recommendation (filtering) hard.

**Answer:** Data sparseness and cold start (also: an immediate, binary decision).

### 4.27 · W6 Quiz Q1 · ORIGINAL
What is a recommender system?

**Answer:** A system that predicts users' interests and recommends items based on the prediction.

### 4.28 · W6 Quiz Q2 · ORIGINAL
In Beta-Gamma threshold learning, more training examples means: less exploration / more exploration?

**Answer:** Less exploration. **Why:** The threshold moves toward the learned optimal value as evidence accumulates.

### 4.29 · W6 Quiz Q3 · ORIGINAL
What is the central idea of Beta-Gamma threshold learning?

**Answer:** Heuristic adjustment (lowering) of the threshold, interpolating between the zero-utility threshold and the optimal threshold, to explore.

### 4.29a · VARIANT
Why do threshold-learning systems need exploration at all?

**Answer:** Labels are censored (only delivered documents get judged) and there are few labels; delivering documents near or below θ reveals preferences, at the cost of some bad deliveries.

### 4.30 · W6 Quiz Q4 · ORIGINAL
Which is **NOT** a reason recommender systems are difficult? Data sparseness / High user expectations / Cold start

**Answer:** High user expectations.

### 4.31 · W6 Quiz Q5 · ORIGINAL
Content-based filtering is based on: query similarity / item similarity / user similarity?

**Answer:** Item similarity.

### 4.32 · W6 Quiz Q6 · ORIGINAL
Which is **NOT** part of the DUS triangle? Services / Data / Users / Internet Providers

**Answer:** Internet Providers.

### 4.33 · W6 Quiz Q7 · ORIGINAL
Which is a user similarity measure? Cosine / Pearson correlation / Both / Neither

**Answer:** Both.

### 4.34 · W6 Quiz Q8 · ORIGINAL
Which is **NOT** a property of search engines? Ad hoc information need / Has pre-existing good knowledge about a user's need / Users take initiative

**Answer:** Has pre-existing good knowledge about a user's need (that describes push/filtering).

### 4.35 · W6 Quiz Q9 · ORIGINAL
User similarity belongs to: content-based filtering / collaborative filtering?

**Answer:** Collaborative filtering.

### 4.35a · VARIANT
For each, say content-based or collaborative: (i) "users who liked X also liked Y", (ii) "recommend articles whose text matches the keywords in your profile", (iii) predicting a missing rating by a weighted average of similar users' ratings, (iv) a binary classifier built on a user's liked-document text.

**Answer:** (i) collaborative, (ii) content-based, (iii) collaborative (memory-based), (iv) content-based.

### 4.36 · TOPIC · push vs pull vocabulary
Classify each: profile, query, search, recommendation, filtering.

**Answer:** Profile = long-lived need (push side). Query = one-shot need (pull). Search = pull. Recommendation = push. Filtering = push, reuses a retrieval scorer with a threshold on a stream.

---
# Section 5 · Text Mining & Topic Models (Weeks 7–8)
Review: [05-Text-Mining-Topic-Models.md](05-Text-Mining-Topic-Models.md)

### 5.1 · W8 Quiz Q1 · ORIGINAL
Unigram LM θ over {the, global, warming, effects}: p(the)=0.1, p(global)=0.2, p(warming)=0.4, p(effects)=X. What is X? 0.2 / 0.3 / 0.1 / 0

**Answer:** 0.3 (1 − 0.1 − 0.2 − 0.4).

### 5.1a · VARIANT
p(x)=0.3, p(y)=0.5 and the vocabulary has exactly three words. What is P("x z")?

**Answer:** p(z)=0.2 → 0.3×0.2 = 0.06.

### 5.2 · W8 Quiz Q2 · ORIGINAL
Same θ. Which is **NOT** true?
- A) P("the global warming effects"|θ) < P("global warming effects"|θ)
- B) P("the text mining"|θ) = 0
- C) P("global warming"|θ) = 0.08
- D) P("global warming"|θ) > P("warming global"|θ)

**Answer:** D. **Why:** A is true (extra factor 0.1). B is true ("text" is outside the vocabulary). C = 0.2×0.4 = 0.08. D is false because the unigram model ignores order: the two are equal.

### 5.3 · W8 Quiz Q3 · ORIGINAL
θ₁ and θ₂ over {concert, music, data, software}: θ₁ = (0.1, 0.1, 0.4, 0.4); θ₂ = (0.4, 0.4, 0.1, 0.1). P(θ₁)=P(θ₂)=0.5. To generate a document, first pick **one** model, then generate **all** words from it. P("data software")? 0.05 / 0.6 / 0.085 / 0.5

**Answer:** 0.085. **Why:** 0.5·(0.4·0.4) + 0.5·(0.1·0.1) = 0.5·(0.16+0.01).

### 5.3a · VARIANT
θ₁ = {a: 0.6, b: 0.4}, θ₂ = {a: 0.2, b: 0.8}, P(θ₁)=0.3, P(θ₂)=0.7. P("a b") when the model is chosen **once per document**?

**Answer:** 0.3·(0.6·0.4) + 0.7·(0.2·0.8) = 0.072 + 0.112 = **0.184**.

### 5.4 · W8 Quiz Q4 · ORIGINAL
Same models as 5.3, but now the model is chosen **independently for each word**. P("data software")? 0.125 / 0.0125 / 0.0625 / 0.625

**Answer:** 0.0625. **Why:** p(data) = 0.5·0.4+0.5·0.1 = 0.25; p(software)=0.25; 0.25².

### 5.4a · VARIANT
Using the models and priors from 5.3a, choose the model independently for each word. What is P("a b")?

**Answer:** p(a)=0.3·0.6+0.7·0.2=0.32; p(b)=0.3·0.4+0.7·0.8=0.68; product = **0.2176** (≠ 0.184, so the two generative stories differ).

### 5.5 · W8 Quiz Q5 · ORIGINAL
In EM, which step improves the parameter values to increase the model likelihood? Both / E-step / M-step

**Answer:** M-step. **Why:** E-step computes posteriors over hidden variables with the current parameters; M-step re-estimates parameters from the fractional counts.

### 5.5a · VARIANT (compute)
Two-component mixture with fixed background, λ_B=0.5. For a word w: p(w|θ_B)=0.3, p(w|θ_d)=0.1 (current estimate). What is the E-step posterior p(z=topic|w)?

**Answer:** 0.5·0.1 / (0.5·0.1 + 0.5·0.3) = 0.05/0.20 = **0.25**.

### 5.6 · W8 Quiz Q6 · ORIGINAL (which is NOT true)
- A) In EM, the model likelihood monotonically **decreases**.
- B) EM is hill-climbing and can only be guaranteed to reach a local maximum.
- C) EM is guaranteed to converge no matter the initial values.
- D) In each iteration, all the words in the data are processed at least once.

**Answer:** A. **Why:** EM increases (never decreases) the likelihood. B, C and D are true.

### 5.6a · VARIANT (True/False)
"EM always finds the global maximum of the likelihood."

**Answer:** False. Local maximum; use several random restarts.

### 5.7 · W8 Quiz Q7 · ORIGINAL (which is NOT true)
For a two-component mixture where each component is a unigram LM:
- A) Adding many occurrences of word W to the collection raises W's probability in both distributions.
- B) Changing the order of words in all documents doesn't affect the mixture.
- C) If W is the most frequent word and one distribution gives it a small probability, the other would give it a higher probability.
- D) Because both distributions are unknown, EM would not converge.

**Answer:** D.

### 5.8 · W8 Quiz Q8 · ORIGINAL (which is NOT true)
Two-component mixture, one distribution fixed to a background LM; λ = P(choose background).
- A) Probabilities of all vocabulary words in the other distribution always sum to 1.
- B) If λ=0, the other distribution assigns high probability to common words like "the".
- C) If λ=0 and W is the most frequent word, P(W|background)+P(W|other) is always 1.
- D) Probabilities of common words in the other distribution get smaller if λ increases.

**Answer:** C.

### 5.8a · VARIANT
For the same model, what happens to P("the"|topic) as λ increases from 0.1 to 0.8, and why?

**Answer:** It decreases (toward 0): a larger background weight lets the background explain "the" so the topic distribution spends its mass on content words.

### 5.9 · TOPIC · why the background helps
Why does adding a fixed background model make the topic distribution show content words?

**Answer:** Components both **collaborate** (explain the data) and **compete** (each sums to 1); the topic gains likelihood by putting mass on words the background explains poorly, i.e., content words.

### 5.10 · W7 TOPIC · paradigmatic vs syntagmatic
Classify: (a) Monday/Tuesday, (b) car + drive, (c) cat/dog. How is each type discovered?

**Answer:** (a) paradigmatic, (b) syntagmatic, (c) paradigmatic. Paradigmatic = substitutable, found by high **context similarity**; syntagmatic = can combine, found by high **co-occurrence**.

### 5.10a · VARIANT
Two words have very similar Left1/Right1 context vectors. Which relation is suggested? What would a high co-occurrence of two words suggest?

**Answer:** Paradigmatic; syntagmatic.

### 5.11 · W7 TOPIC · EOWC
What does EOWC compute, and what are its two flaws with fixes?

**Answer:** Σ xᵢyᵢ where xᵢ=c(wᵢ,d₁)/|d₁|: the probability that random words from the two contexts match. Flaws: (1) frequency dominance → sublinear TF/BM25 transform; (2) stop words weighted equally → IDF.

### 5.12 · W7 TOPIC · NLP steps
Order the steps: syntactic analysis, inference, POS tagging, semantic analysis.

**Answer:** POS tagging → syntactic analysis → semantic analysis → inference.

### 5.13 · W7 TOPIC · representation spectrum
Which text representation does this course focus on, and why?

**Answer:** Sequence of words (BOW level): robust, easy and accurate, minimal manual effort, effective for most mining tasks.

### 5.14 · W7 TOPIC · human sensors
What makes text a "subjective" sensor reading compared with a physical sensor? How far back does mining go?

**Answer:** Humans observe the world and express it in their own words (perspective, bias), unlike a thermometer. Mining reverses the process: language → content → the observer → the real world.

### 5.15 · W7 TOPIC · limits of "topic = a term"
Name three problems and how a word distribution fixes them.

**Answer:** Too coarse/ambiguous, can't cover related words, brittle coverage. A distribution gives multiple weighted words, covers vocabulary variation, and the same word can carry different probability in different topics.

### 5.16 · TOPIC · PLSA vs LDA
How do PLSA and LDA differ, and what is PLSA's parameter-count problem?

**Answer:** LDA = PLSA with Dirichlet priors on coverage and topics; parameters don't grow with the number of documents, and new documents get probabilities. PLSA has k|V| + Nk parameters, growing with N (overfitting).

---
# Section 6 · Categorization, Clustering, Opinions & Context (Weeks 9–12)
Review: [06-Categorization-Clustering-Context.md](06-Categorization-Clustering-Context.md)

### 6.1 · W9 Practice Q1 / W10 Practice Q1 · ORIGINAL
Which is **NOT** a use of text clustering? Grouping similar pictures together / document clustering / word clustering / clustering websites by their text

**Answer:** Grouping similar pictures. **Why:** Text clustering operates on textual content.

### 6.2 · W9 Set 2 Q1 / W10 Quiz Q1 · ORIGINAL
What is **NOT** a motivation for text clustering?
- A) Removing spam documents based on a small collection of human-annotated spam documents
- B) Linking / near-duplicate removal  C) Creating structure over text  D) A high-level overview of a large collection

**Answer:** A (supervised → categorization).

### 6.3 · W9 Practice Q2 / W10 Practice Q5 · ORIGINAL (check all that apply)
Difference between direct and indirect evaluation of clustering:
- A) Indirect requires a user-specified application to test with.
- B) Direct requires a human-annotated gold-standard clustering.
- C) Direct evaluation is inherently better.
- D) EM results don't depend on initialization.

**Answer:** A and B.

### 6.3a · VARIANT
Which evaluation is more practical for clustering a very large collection, and why?

**Answer:** Indirect: annotating a full gold standard is impractical; test the application with vs without clustering.

### 6.4 · W10 Quiz Q3 · ORIGINAL
Which evaluation method is more applicable for clustering results of a large collection? 

**Answer:** Indirect evaluation (with/without clustering for an application).

### 6.5 · W9 Practice Q3 · ORIGINAL
Agglomerative clustering with single-link, two clusters. Similarities: D4–D5 0.9; D1–D6 0.85; D2–D3 0.85; {D1,D6}–{D4,D5} 0.82. What are the two clusters?

**Answer:** {D1, D4, D5, D6} and {D2, D3}. **Why:** merge D4–D5; then D1–D6 and D2–D3 (0.85 ties); the strongest remaining cross-link is 0.82 between {D1,D6} and {D4,D5}. Single-link uses the **max** pairwise similarity.

### 6.5a · VARIANT
Items A,B,C,D with sims A–B 0.9, C–D 0.8, B–C 0.5, A–C 0.4, B–D 0.2, A–D 0.1. After merging to two clusters {A,B},{C,D}, what is the similarity between them under (i) single-link, (ii) complete-link, (iii) average-link?

**Answer:** (i) 0.5 (closest pair B–C), (ii) 0.1 (farthest pair A–D), (iii) (0.4+0.1+0.5+0.2)/4 = 0.3.

### 6.6 · W9 Set 2 Q2 / W10 Quiz Q2 · ORIGINAL
For agglomerative clustering which is TRUE? A) It requires specifying a similarity measure. B) It is top-down. C) The depth of the hierarchy is exactly log₂N.

**Answer:** A.

### 6.7 · W9 Set 2 Q3 / W10 Quiz Q6 · ORIGINAL
Which hierarchical clustering variation is **least** sensitive to outliers?

**Answer:** **Average-link** (lecture + Week 10 quiz notes). ⚠ Your Week 9 file answers "Complete-link," which conflicts with the lecture. Single-link is the most sensitive (chaining).

### 6.8 · W10 Practice Q2 · ORIGINAL
Which is true about the maximal likelihood of a set of documents?
- A) Reversing the word order of a document doesn't change it.
- B) Doubling every token doesn't change it.
- C) Swapping two word identities globally doesn't change it.

**Answer:** A. **Why:** Unigram/multinomial likelihood depends only on counts.

### 6.9 · W10 Practice Q3 · ORIGINAL
Correct about K-means and PLSA? 

**Answer:** Both require the user to specify the number of clusters/topics. (Both are also iterative and initialization-dependent.)

### 6.9a · VARIANT (True/False)
"K-means converges to the global optimum."

**Answer:** False; a local optimum (run several restarts).

### 6.10 · W10 Practice Q4 · ORIGINAL
Disadvantage of model-based clustering?

**Answer:** It is difficult to substitute a different similarity measure (the generative assumptions fix what "similar" means).

### 6.11 · W10 Quiz Q4 / W11 Quiz Q4 · ORIGINAL
Which category do Naive Bayes classifiers belong to? Generative / discriminative. And, which is **not** discriminative: k-NN / SVM / logistic regression / Naive Bayes?

**Answer:** Generative. Naive Bayes is the one that is **not** discriminative.

### 6.12 · W10 Quiz Q5 · ORIGINAL
Which task is unsupervised in general? Text categorization / text clustering

**Answer:** Text clustering.

### 6.13 · W10 Quiz Q7 · ORIGINAL
Which algorithm involves a process close to EM? Naive Bayes / K-means / agglomerative clustering

**Answer:** K-means. **Why:** Assignment ≈ hard E-step; centroid update ≈ M-step.

### 6.13a · VARIANT
What is the main difference between K-means and the mixture-model clustering fit by EM?

**Answer:** K-means makes hard assignments; the mixture model gives each document a probability for every cluster (soft).

### 6.14 · W9 Practice Q4 / W11 Practice Q2 · ORIGINAL
Multi-label classification. Per-category counts: c1 TP=3, FP=0, FN=0; c2 TP=2, FP=1, FN=0; c3 TP=2, FP=0, FN=1. Which statement is **NOT** true?
- A) P(c1)=R(c1)=1  B) F(c2)=F(c3)=4/5  C) P(c3)=2/3 and R(c3)=1

**Answer:** C. **Why:** For c3, P = 2/(2+0) = 1 and R = 2/(2+1) = 2/3; the statement swaps them.

### 6.15 · W9 Practice Q5 / W11 Practice Q3 · ORIGINAL
Same data. Micro-averaged precision and recall?

**Answer:** P = R = 7/8. **Why:** pooled TP=7, FP=1, FN=1.

### 6.15a · VARIANT (compute)
10 documents. c1: TP=4, FP=2, FN=1, TN=3. c2: TP=1, FP=1, FN=3, TN=5. Give P and R for each category, F₁ for c1, accuracy over all 20 decisions, micro P/R, and macro-precision.

**Answer:** c1: P=4/6=2/3, R=4/5; F₁(c1)=2·(2/3)(4/5)/(2/3+4/5)=**8/11**. c2: P=1/2, R=1/4. Accuracy = (4+3+1+5)/20 = **13/20**. Micro: TP=5, FP=3, FN=4 → P=5/8, R=5/9. Macro-P = (2/3+1/2)/2 = **7/12**.

### 6.16 · W9 Set 2 Q4 / W11 Quiz Q1 · ORIGINAL
5 documents × 2 categories (a correct decision is y(+) or n(−)). c1: TP=2, FP=1, FN=0; c2: TP=2, FP=2, FN=1. Precision and recall of c1 and c2?

**Answer:** P(c1)=2/3, R(c1)=1; P(c2)=1/2, R(c2)=2/3.

### 6.17 · W9 Set 2 Q5 / W11 Quiz Q2 · ORIGINAL
Classification accuracy for the same classifier? 

**Answer:** 6/10 (4 correct in the c1 column + 2 correct in c2, out of 10 decisions).

### 6.18 · W9 Set 2 Q6 / W11 Quiz Q3 · ORIGINAL
Micro-averaged recall for the same table?

**Answer:** 4/5 (pooled TP=4, FN=1).

### 6.19 · W9 Set 2 Q7 / W11 Quiz Q7 · ORIGINAL (check all that apply)
Disadvantages of classification accuracy:
- A) It can't assign different weights to different decisions.
- B) It can't deal with skewed data properly.
- C) For imbalanced data, high accuracy doesn't imply good performance.
- D) It gives different results for different datasets.

**Answer:** A, B, C. (D is true of every metric, not a specific disadvantage.)

### 6.19a · VARIANT
98% of documents are in category 1. A classifier labels everything "category 1". What are its accuracy and its recall for category 2?

**Answer:** Accuracy 98%; recall for category 2 = 0. **Why:** Accuracy hides the failure on the small class; macro-averaging would expose it.

### 6.19b · VARIANT
Which averaging lets large categories dominate the result: micro or macro?

**Answer:** Micro (pooled decisions). Macro gives each category equal weight.

### 6.20 · W9 Set 2 Q8 / W12 Quiz Q2 · ORIGINAL
Which is **NOT** true about contextual text mining? 
- A) Context is commonly used. B) Context can partition text and give meaning to topics. C) Context does not influence both coverage and content variation of topics.

**Answer:** C.

### 6.21 · W11 Practice Q1 · ORIGINAL (True/False)
Sentiment classification can be treated as a text categorization problem.

**Answer:** True.

### 6.22 · W11 Practice Q4 · ORIGINAL
Which is **NOT** true? 
- A) Naive Bayes is generative while k-NN is discriminative.
- B) Logistic regression estimates d+1 weights for d features.
- C) k-NN tries to estimate d+1 weights associated with d features.

**Answer:** C. **Why:** k-NN is instance-based and has no weights.

### 6.23 · W11 Practice Q5–Q6 · ORIGINAL
Training set (3 docs, one labeled Spam). With MLE (no smoothing), P(Spam)? And which test document is most likely spam: it is the one whose words appear only in the spam doc (e.g., "No fees")?

**Answer:** P(Spam) = 1/3 (relative frequency). "No fees" scores highest because both words are characteristic of the spam class only.

### 6.23a · VARIANT (compute)
Training: d1 "win money now" (Spam); d2 "meeting today" (Ham); d3 "money meeting" (Ham). V = {win, money, now, meeting, today}. (a) MLE P(Spam)? (b) With Laplace smoothing compute P(win|Spam) and P(win|Ham). (c) Classify d = "win money" with Laplace smoothing and give P(Spam|d).

**Answer:** (a) 1/3. (b) Spam has 3 tokens: (1+1)/(3+5) = 2/8; Ham has 4 tokens, "win" count 0: 1/(4+5) = 1/9. (c) Spam score = (1/3)(2/8)(2/8) = 1/48; Ham score = (2/3)(1/9)(2/9) = 4/243; P(Spam|d) = 243/(243+192) = **81/145 ≈ 0.56** → Spam. Without smoothing, P(win|Ham)=0 ⇒ P(d|Ham)=0.

### 6.24 · W11 Practice Q7–Q9 · ORIGINAL
For a document d3 containing a word with zero count in category 1: (a) P(d3|θ₁) under unsmoothed MLE? (b) With Laplace smoothing, P(θ₁|d3) if P(d3|θ₁) ∝ (3/10)(1/10) and P(d3|θ₂) ∝ (2/10)(2/10) with equal priors? (c) Predicted category?

**Answer:** (a) 0 (one factor is zero). (b) (3/100)/(3/100+4/100) = **3/7**. (c) **Category 2** (3/7 < 1/2).

### 6.25 · W11 Practice Q10–Q11 · ORIGINAL
Test doc D6 has similarities to the training set: D1 0.85 (label 1), D2 0.7 (label 0), D3 0.6, D4 0.1, D5 0.3. Prediction with k=1? With k=2?

**Answer:** k=1 → label of D1 = **1**. k=2 → D1 (1) and D2 (0) tie → **0 or 1**.

### 6.25a · VARIANT
Test doc T has similarities D1 0.9 (A), D2 0.8 (B), D3 0.75 (B), D4 0.2 (A), D5 0.1 (A). Predict for k=1, k=2, k=3.

**Answer:** k=1 → A; k=2 → tie; k=3 → neighbors D1(A), D2(B), D3(B) → **B**.

### 6.26 · W11 Quiz Q5 · ORIGINAL
Features for text categorization: domain knowledge / error analysis / machine-learning methods / all of the above?

**Answer:** All of the above.

### 6.27 · W11 Quiz Q6 · ORIGINAL
Which is false about sentiment classification? A) Its input is an opinionated text object. B) Its output is an opinionated text object. C) Any text categorization method can be used.

**Answer:** B (the output is a sentiment label).

### 6.28 · W11 Quiz Q8 · ORIGINAL
"Tom thinks programming is difficult." What is the opinion holder?

**Answer:** Tom (the target is programming).

### 6.28a · VARIANT
"Sarah says this phone's battery is terrible." Give the holder, the target, and the sentiment.

**Answer:** Holder Sarah; target the phone's battery; sentiment negative.

### 6.29 · W12 Practice Q1–Q2 · ORIGINAL (True/False)
(a) NetPLSA leverages both the text and the network structure to mine topics. (b) NetPLSA smooths topic transitions by forcing neighbor nodes to have different topic coverage.

**Answer:** (a) True. (b) False — neighbors are pushed toward **similar** coverage (squared-difference regularizer).

### 6.29a · VARIANT
In the NetPLSA objective, what happens if the regularization weight λ is 0? If λ is 1?

**Answer:** λ=0 → plain PLSA (text only); λ=1 → ignores text, uses graph structure only.

### 6.30 · W12 Practice Q3 · ORIGINAL
CPLSA can be applied to which tasks? Temporal topic trends / spatiotemporal analysis / all of the above

**Answer:** All of the above.

### 6.31 · W12 Practice Q4 / Quiz Q4 · ORIGINAL
(a) Discover topics in Twitter whose coverage strongly correlates with airline prices. (b) Analysts want factors related to fluctuating currency exchange rates, using timestamped news from the past year. Which method? PLSA / LDA / CPLSA / iterative topic modeling with time-series feedback

**Answer:** Iterative topic modeling with time series (feedback/supervision) for both. **Why:** An external numeric time series must steer topic discovery; CPLSA conditions on context but doesn't optimize for correlation with a series.

### 6.32 · W12 Practice Q5 / Q8 · ORIGINAL
(a) Do US and non-US researchers focus on different topics within deep learning (publications with affiliation/location metadata)? (b) Find trending topics in different countries on Twitter with location information. Which technique?

**Answer:** Contextual PLSA (CPLSA) for both; location/affiliation is the context that conditions topic coverage.

### 6.33 · W12 Practice Q6 · ORIGINAL
What is the additional input, other than text, in causal topic mining?

**Answer:** Time (a time-aligned external series).

### 6.34 · W12 Practice Q7 · ORIGINAL
To measure causality between two series, which is true?

**Answer:** Granger testing is often used. (It tests whether one series improves prediction of the other beyond its own past.)

### 6.34a · VARIANT (True/False)
"Granger causality proves that one time series causes the other."

**Answer:** False; it shows lead/lag predictive relationships.

### 6.35 · W12 Quiz Q1 · ORIGINAL (True/False)
Opinion mining can be used to decompose ratings into different aspects.

**Answer:** True (e.g., LARA).

### 6.36 · W12 Quiz Q3 · ORIGINAL
Applications of Latent Aspect Rating Analysis: opinion-based entity ranking / aspect-level opinion summarization / reviewer-preference analysis / all of the above?

**Answer:** All of the above.

### 6.36a · VARIANT
What three things does LARA recover from review text plus the overall rating?

**Answer:** Latent aspects, per-aspect ratings, and per-aspect weights (the reviewer's preferences).

### 6.37 · W12 Quiz Q5–Q7 · ORIGINAL (True/False)
(a) Non-text data can also help text mining. (b) Text data can help interpret patterns discovered from non-text data. (c) CPLSA is an extension of PLSA.

**Answer:** All true.

### 6.38 · TOPIC · pick the method (scenario drill)
Which method fits? (i) Reviews with overall ratings → ratings per aspect. (ii) Co-authorship graph; neighbors should share topics. (iii) Tweets before vs after a product launch (compare wording and coverage). (iv) News versus a stock-price series; find topics that lead the price.

**Answer:** (i) LARA. (ii) NetPLSA. (iii) CPLSA (event impact / views and coverage). (iv) Iterative topic modeling with time-series feedback (Granger).

### 6.39 · TOPIC · PLSA vs one-topic-per-document clustering
In "p(d) = Σᵢ p(θᵢ) Πw p(w|θᵢ)^c(w,d)", where is the sum relative to the product, and is p(θᵢ) per document?

**Answer:** The sum is **outside** the product (the whole document comes from one cluster); p(θᵢ) is global, not per-document. PLSA picks a topic per word with per-document coverage π_{d,j}.

### 6.40 · TOPIC · k-means procedure
List the steps of K-means and say what the E-step and M-step correspond to.

**Answer:** Choose K; seed K centroids; repeat (assign each document to the nearest centroid = E-step; recompute each centroid as the mean of its documents = M-step) until assignments stop changing. Converges to a local optimum.

### 6.41 · TOPIC · macro vs micro
A system does well on a large category and badly on a small one. Which score looks better, micro or macro averaged, and why?

**Answer:** Micro, because pooled decisions are dominated by the large category; macro averages per-category scores so the small category pulls it down.

---
*End of Quiz Bank. 213 items: 119 ORIGINAL, 69 VARIANT, 25 TOPIC (some items bundle two or three linked sub-questions).*
