---
question: "A Raft cluster has seven servers A–G. A proposed Raft variant uses four votes for elections and lets a leader mark a log entry committed once it has been stored on three servers. The rest of the algorithm is unchanged. Initially, every log is empty. A is elected leader in a term and replicates an entry X at index 1 to A, B, and C, and then marks X as committed. Can a different leader be elected later without X in its log? If yes, show a concrete sequence of events leading to its election. If not, state why Raft prevents a leader without X in its log from being elected."
researched: 2026-10-25
confidence: confident
versions:
  - "CS 425 / ECE 428 Fall 2026 Homework 3 (hw3.fa26.pdf)": "out 2026-10-12, due 2026-11-01; problem 9"
  - "CS 425 / ECE 428 Fall 2026 Lecture 18-B Raft (L18.B.FA26.pdf)": "Aishwarya Ganesan with Ram Kesavan; lectures page still marked Tentative on 2026-10-25"
  - "Ongaro and Ousterhout, In Search of an Understandable Consensus Algorithm": "USENIX ATC 2014; extended text at raft.github.io/raft.pdf, sections 5.2–5.4"
  - "Ongaro, Consensus: Bridging Theory and Practice": "Stanford PhD dissertation, August 2014, purl.stanford.edu/qr033xr6097; section 3.6.3 and Appendix B"
---

# Can a later Raft leader be elected without a 3-server commit?

## Answer

Yes. After A marks X committed on {A, B, C}, D can win a later term with votes from only {D, E, F, G}, and D’s log does not contain X.

For seven servers, four votes is an ordinary majority, so the variant’s election size still matches Raft. Three stored copies is not a majority. A 3-server commit set and a 4-server election set need not intersect: {A, B, C} ∩ {D, E, F, G} = ∅, because 3 + 4 = 7, which is not greater than 7. Leader Completeness is proved from that intersection. The unchanged up-to-date vote check only compares the candidate with each voter, and none of D’s voters store X, so they grant the votes.

Concrete sequence. Every server starts with an empty log, `currentTerm = 0`, and `votedFor` null. Crashes are fail-stop and last through the term-2 election.

1. A’s election timer fires. A sets `currentTerm = 1`, votes for itself, and sends `RequestVote` with an empty log.
2. B, C, and D grant that vote. Each is still in term 0, has not voted in term 1, and has an empty log, so A’s log is as up-to-date as the voter’s. The requests to E, F, and G are lost. A has four votes (A, B, C, D) and becomes leader for term 1.
3. A appends X at index 1 in term 1 and sends `AppendEntries`. B and C store X and acknowledge. The RPCs to D, E, F, and G are lost, so those four logs stay empty. Voting did not copy X onto D.
4. X is stored on exactly {A, B, C}. It is an entry from A’s current term, and the variant treats three stored copies as enough to commit, so A marks X committed.
5. A, B, and C crash and do not restart before the next election. They are the only servers that store X.
6. D receives no `AppendEntries` from the leader, so its election timer fires. D sets `currentTerm = 2` and votes for itself. D’s log is still empty.
7. D sends `RequestVote` for term 2 with an empty log. A, B, and C are down and cast no votes. E, F, and G are in a term below 2, have not voted in term 2, and have empty logs. The deny test fails on each of them: the voter’s last term is not later than D’s, and the voter’s log is not longer. Each grants the vote.
8. D has four votes (D, E, F, G) and becomes leader for term 2. D’s log does not contain X.

Any two 4-subsets of a 7-server cluster still intersect (4 + 4 = 8 > 7), so this variant still elects at most one leader per term. The lost property is Leader Completeness, which needs the commit set to meet every legal election set.

## Findings

- Homework 3, problem 9, is this question: seven servers, election threshold 4, commit threshold 3, the rest of Raft unchanged, logs initially empty, X stored on A, B, and C and then marked committed. — [T1] CS425 Fall 2026 Homework 3 (`/home/isaacsimms/Desktop/MCS-UIUC/Distributed Systems - CS425/Week8/Homework 3/hw3.fa26.pdf`; https://courses.grainger.illinois.edu/cs425/fa2026/hw3.fa26.pdf)
- A candidate wins an election by receiving votes from a majority of the full cluster in one term. Each server votes for at most one candidate per term. For seven servers that majority is four, so the variant’s election count is the ordinary Raft majority. — [T1] Ongaro and Ousterhout, USENIX ATC 2014, §5.2 (https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf)
- The same election rule is what Fall 2026 states: a candidate waits for a majority, each server gives out one vote per term, and two candidates cannot both accumulate majorities in one term. — [T2] CS425 Fall 2026 Lecture 18-B, “Election Basics” and “Elections: Safety” (https://courses.grainger.illinois.edu/cs425/fa2026/L18.B.FA26.pdf)
- In unmodified Raft, the leader that created an entry commits it once the entry is stored on a majority of the servers. The leader’s commit rule counts replicas only for an entry from its current term; that commit also commits preceding entries. — [T1] Ongaro and Ousterhout, USENIX ATC 2014, §5.3 and §5.4.2; Figure 2 commit rule (https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf)
- Fall 2026 states the same commit rule as “acks from a majority (including itself)” and, on the safety slide, “committed: on a majority, including an entry from current leader’s term.” The variant replaces that majority with three servers. X is from A’s current term, so the current-term half of the rule is already satisfied when A marks X committed. — [T2] CS425 Fall 2026 Lecture 18-B, “Normal Operation” and “Safety: Intuition” (https://courses.grainger.illinois.edu/cs425/fa2026/L18.B.FA26.pdf)
- Leader Completeness: if a log entry is committed in a given term, then that entry is present in the logs of the leaders of all higher-numbered terms. — [T1] Ongaro and Ousterhout, USENIX ATC 2014, Figure 3 (https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf)
- The proof assumes the committed entry was replicated to a majority and the later leader received votes from a majority, and concludes that some voter both stored the entry and voted for the later leader. That voter is what produces the contradiction with the up-to-date check. — [T1] Ongaro and Ousterhout, USENIX ATC 2014, §5.4.3 step 2 (https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf)
- The dissertation makes the same step explicit: an immediately committed entry is one acknowledged by a quorum, a successful election has votes from a quorum, and “any two quorums overlap,” so some voter both holds the entry and votes in the later election. Election Safety uses that same overlap, together with one vote per term. — [T1] Ongaro dissertation, August 2014, Appendix B, Lemma 2 and Lemma 8 step 5(c); the §3.6.3 sketch matches the ATC argument (https://purl.stanford.edu/qr033xr6097)
- Fall 2026 teaches the same overlap as the reason a new leader must hold the committed entry: the electing majority overlaps the majority that holds the entry, so some voter V has it, and V grants the vote only when the candidate’s log is at least as up-to-date. — [T2] CS425 Fall 2026 Lecture 18-B, “Safety: Intuition” (https://courses.grainger.illinois.edu/cs425/fa2026/L18.B.FA26.pdf)
- The up-to-date check is per voter. `RequestVote` carries the candidate’s last log index and term. The voter denies the vote when its own log is more up-to-date: later last term wins; if the last terms are equal, the longer log wins. A candidate elected by a majority whose logs it matches or beats therefore holds every entry present on that majority. It holds every committed entry only because that majority meets the commit majority. — [T1] Ongaro and Ousterhout, USENIX ATC 2014, §5.4.1 and Figure 2 (https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf)
- Fall 2026 writes the deny test as `(lastTermV > lastTermC) || ((lastTermV == lastTermC) && (lastIndexV > lastIndexC))`, and states that the leader has the most complete log among the electing majority. Two empty logs fail that deny test, so a voter with an empty log grants the vote to a candidate with an empty log. A voter whose last entry is term 1 denies a candidate whose log is empty. — [T2] CS425 Fall 2026 Lecture 18-B, “Restrictions on Leader Election” (https://courses.grainger.illinois.edu/cs425/fa2026/L18.B.FA26.pdf)
- Servers fail by stopping. A follower that receives no `AppendEntries` before its election timeout starts an election. Safety does not depend on timing, so A, B, and C staying down through D’s election is inside the model. — [T1] Ongaro and Ousterhout, USENIX ATC 2014, §2 and §5.2 (https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf); [T2] CS425 Fall 2026 Lecture 18-B, failure model and “Heartbeats and Timeouts” (https://courses.grainger.illinois.edu/cs425/fa2026/L18.B.FA26.pdf)
- On these sizes the overlap premise is false. Commit set {A, B, C} and election set {D, E, F, G} are disjoint. Every pair of 4-subsets still intersects, which is why one-leader-per-term survives, while a committed 3-set can miss an entire winning election set. — [T1] derived from the majority-overlap step in USENIX ATC 2014 §5.4.3 and dissertation Appendix B Lemma 8, applied to the thresholds in Homework 3 problem 9

## Recommendation

Answer yes, and give the term-1 / term-2 sequence above. The calling session can treat the intersection arithmetic as the whole solution: the unchanged rules still run, and they do not pull X into D’s log because no member of D’s 4-vote set stores X.

Fall 2026 and the paper agree on the rule this variant still uses. Both place Leader Completeness on overlap between the commit set and the electing set, and both define those sets as majorities. The variant keeps the election majority (4 of 7) and drops the commit set to 3, so the shared premise no longer holds. There is no source conflict to resolve.

## Ruled out

- “A later leader still must contain X, because Leader Completeness is unchanged.” The property is a theorem whose proof uses two majorities. The variant’s commit set is not a majority, and Lemma 8 step 5(c) does not apply to it.
- “The up-to-date check alone blocks D.” That check consults only voters. E, F, and G have empty logs, so they grant the vote. A, B, and C would deny it, and they are down; D already has four votes without them.
- “X was never really committed, because Raft refuses to commit from a replica count of three.” Section 5.4.2 and Figure 8 forbid committing a previous-term entry by counting replicas. X is from A’s current term. The variant changes the count from a majority to three and leaves that current-term rule in place.
- “The scenario needs two leaders in one term.” It does not. D’s election is term 2. Any two election sets of four still intersect, so Election Safety still holds.
- Local CS425 notes. A search of `/home/isaacsimms/Desktop/MCS-UIUC/Distributed Systems - CS425` found no Raft lecture notes. Week 7 Paxos notes discuss majority intersection for Paxos only.
- No instructor or author Q&A was used. The homework, the Fall 2026 deck, the ATC paper, and the dissertation already answer the question.

## Open questions

None for this question. The Lecture 18-B PDF was still marked Tentative on the Fall 2026 lectures page at fetch time. A later final deck would not change the answer: the ATC paper and the dissertation already contain the overlap proof the slides summarize.
