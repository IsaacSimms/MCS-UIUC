---
question: |
  Solve the k-leader election problem (for a given integer value k), to avoid the monopoly of a single leader. It has to satisfy the following two conditions:
  Safety: For each non-faulty process p, p's elected = a set of k non-faulty processes with the lowest ids, OR = NULL.
  Liveness: For all runs of election, the run terminates AND for each non-faulty process p, p's elected is not NULL.
  Modify the Ring election Algorithm described in the lecture to create a solution to the k-Leader Election problem. You may make the same assumptions as the original algorithm. Analyze your algorithm the same way as in class (without failures) for Safety and Liveness. Then comment on/prove how many failures your algorithm can tolerate while guaranteeing Safety and Liveness.
researched: 2026-10-25
confidence: confident
versions:
  - "CS 425/ECE 428 FA2026 leader election slides (L17.FA26.pdf, marked Final)": "deck titled Lecture 17; PDF metadata 2026-10-23; schedule row dated 2026-10-20, HTML row number 18, reading Section 15.3"
  - "CS425 FA2026 Homework 3 (hw3.fa26.pdf)": "out 2026-10-12, due 2026-11-01; problem 6"
  - "Chang and Roberts, CACM": "vol. 22, no. 5, May 1979, pp. 281-283; doi:10.1145/359104.359108"
---

# k-Leader Election by Modifying the Ring Election Algorithm

## Answer

Modify the Fall 2026 ring election (one clockwise neighbor, `Election` then `Elected`, highest initiator wins if several processes start) so the token carries a set of at most k ids and each process keeps the k smallest ids seen on that token. With no crashes the token’s return to its initiator is the k lowest ids on the ring; the `Elected` wave writes that set into every process. Both safety and liveness hold in a failure-free run. The same ring assumptions tolerate **0** crash failures: one crash-stop during the run is enough to lose liveness, and a crash of a member of the decided set is enough to lose safety.

The original algorithm is the ring election in the Final deck `L17.FA26.pdf` (CS 425 / ECE 428, Fall 2026, Aishwarya Ganesan with Ram Kesavan, acknowledgement Indranil Gupta), linked from the 2026-10-20 Leader Election row. It is the lecture’s Chang-and-Roberts-style unidirectional ring, not the Bully algorithm later in the same deck. A repo search under `Distributed Systems - CS425` found no local ring-election note.

### Assumptions (same as the lecture ring, plus the given k)

These are load-bearing. Dropping one of them changes the proof or the failure bound.

1. There are N processes in one logical ring. Process p has a communication channel only to its clockwise successor. Every message travels clockwise. The deck compares this ring to Chord’s ring.
2. Identifiers are unique and totally ordered. For this problem the attribute is the id, and a smaller id is better. The lecture’s scalar algorithm elects the highest attribute; the homework requires the lowest ids, so the comparison is reversed.
3. Every process is given the same integer k, with 1 ≤ k ≤ N. Processes do not need to know N. Termination is “this initiator’s token came back,” which is well-defined on a cycle.
4. A message sent to a live successor is eventually delivered. The no-failure proof uses eventual delivery only. It does not use a timeout or a known delay bound. (The Bully half of the same lecture does use timeouts, and the deck ties Bully’s liveness to synchrony.)
5. Any process may call an election. A process calls at most one election at a time. Several processes may call at once. The result must not depend on which of them called.
6. The safety and liveness proof in the next section assumes no process crashes and no channel breaks during the run. That is the lecture’s analysis assumption: “assume no failures occur during the election protocol itself.”
7. `elected` starts as NULL. NULL is distinct from the empty set. A decided value is a set of k ids.

### Modified algorithm

State at each process:

- `elected`, initially NULL
- `bestInit`, initially smaller than every id (the lecture’s cache of the highest initiator id seen)

`kmin(X)` is the set of the min(k, |X|) smallest ids in X.

**Start** (process `myId` calls an election):

- If `myId ≤ bestInit`, return. This process has already started, or it has already seen a higher initiator.
- Otherwise set `bestInit ← myId` and send `Election(init = myId, S = kmin({myId}))` to the successor.

**On `Election(init, S)`:**

- If `init < bestInit`, discard the message. This is the lecture’s rule that a lower-id initiator’s `Election` is suppressed.
- Otherwise set `bestInit ← init` and `S' ← kmin(S ∪ {myId})`.
- If `init = myId`, the token has gone around the ring. Set `elected ← S'` and send `Elected(init = myId, S = S')` to the successor.
- Otherwise send `Election(init, S')` to the successor.

**On `Elected(init, S)`:**

- If `init < bestInit`, discard it.
- Otherwise set `bestInit ← init` and `elected ← S`.
- If `myId ≠ init`, forward `Elected(init, S)` to the successor. The initiator does not forward, so the wave stops when it returns.

The scalar “overwrite with my id if I am better and I have not forwarded yet” rule is what this replaces. On a winning token the process always folds its own id in with `kmin` and forwards. Extinguishing that token early would drop ids that have not been seen yet. Extinction remains only across initiators: a lower initiator id is suppressed, which is slide 27’s rule, unchanged.

For k = 1 the decided set is the singleton of the minimum id. The control structure is still the lecture’s (`Election` lap, then `Elected` lap, highest initiator id survives). The difference from a literal inequality flip is that the minimum is accumulated on one lap and announced by the initiator, rather than by waiting for an unchanged winning id to travel a second lap. The decided process is the same one a flipped comparison would elect.

### No-failure analysis (lecture style)

Fix a run in which at least one process calls `start`, no process crashes, and every send is eventually delivered. Let K\* be the set of the k smallest ids in the ring. Unique ids make K\* unique.

**Absorption.** `kmin(kmin(A) ∪ {x}) = kmin(A ∪ {x})`. If A ∪ {x} has size at most k, both sides are A ∪ {x}. If it has more than k elements, every id among the k smallest of A ∪ {x} is either x or one of the k smallest of A, so it already sits in `kmin(A) ∪ {x}`.

**Invariant I1 (one token’s prefix).** For the token of an initiator p0, label the ring p0, p1, …, p_{N−1} in clockwise order. Let S0 be the set p0 sends, and let Si be the set pi sends for i ≥ 1. Then Si = `kmin({id(p0), …, id(pi)})`. Base case: S0 = `kmin({id(p0)})`. Inductive step: pi sends `kmin(S_{i−1} ∪ {id(pi)})`, which equals `kmin({id(p0), …, id(pi)})` by absorption.

**Invariant I2 (a token that returns has seen the whole ring).** The initiator sends one `Election` and does not forward `Election`. Each other process forwards that initiator’s token at most once, to its unique successor. The only cycle is the ring, so if the initiator receives `Election(init = p0, S)`, the token crossed every ring edge once. By I1 the set that p_{N−1} sends is `kmin` of every id, which is K\*. The initiator’s local `kmin(S ∪ {id(p0)})` equals K\* again. A token that some process discarded because `init < bestInit` does not return, so it never assigns `elected`.

**Invariant I3 (announced value).** `Elected` is sent only by an initiator that has just received its own `Election` back, and the set in that message is K\*. Every assignment `elected ← S` therefore writes K\* or leaves the variable NULL. No process writes any other set.

**Safety.** At every moment, for every process p, `elected` is NULL or K\*. K\* contains k processes. Under the no-failure assumption every process is non-faulty, so K\* is a set of k non-faulty processes with the lowest ids. This is the homework safety condition. It is the lecture’s safety condition with the “one best process” replaced by that set: a non-null value is a particular correct result, and NULL is allowed until the announcement arrives. Processes that have already written K\* agree, because I3 allows only that set.

**Liveness, by the lecture’s message count.** Let I\* be the largest id among processes that call `start`. `bestInit` only ever stores an initiator id, so it never exceeds I\*. No process discards `Election` or `Elected` whose `init` is I\*.

I\*’s `Election` is therefore forwarded by all N − 1 other processes and delivered back to I\*. That is N `Election` transmissions. I\* then sends `Elected(I\*, K\*)`. Each other process stores K\* and forwards. That is N `Elected` transmissions. I\* does not forward `Elected`, so the wave stops. Nothing in this run re-sends a new wave. The run terminates after finitely many messages.

After those 2N deliveries every process, all of them non-faulty, has `elected = K\* ≠ NULL`. That is the homework liveness condition, argued the same way as slide 25: a finite circulation finishes, and the announcement leaves every process holding the correct result.

**Message complexity and completion time, one initiator.** N `Election` messages for one clockwise lap, then N `Elected` messages for one clockwise lap. Total 2N messages. Each hop waits for the previous hop, so the completion time is 2N message transmission times. Who the initiator is does not change the count: the k-set is built on the first lap.

The unmodified lecture algorithm is larger in the worst case because a scalar maximum may be overwritten on the way to the winner and then has to travel a full unchanged lap. The deck’s count for that algorithm, when the initiator is the ring successor of the would-be leader, is (N − 1) + N + N = 3N − 1 messages and 3N − 1 transmission times. Its best case, initiator already the winner, is 2N. The modified algorithm’s single-initiator cost matches that best case and does not have a separate 3N − 1 case.

**Several initiators.** The highest initiator id is never suppressed, so the paragraph above still supplies a run that finishes, and I2 says every token that does finish carries the same K\*. Safety is unchanged if a lower initiator’s lap also finishes and announces K\*. Worst-case message count: each of up to N tokens is forwarded at most N times, and each completed lap adds N `Elected` messages, which is O(N²). The deck’s corresponding statement for the scalar algorithm is that only the highest-id initiator’s run completes; it does not print an O(N²) figure on that slide.

### How many failures

**Zero crash failures.** The no-failure section shows 0 crashes are sufficient for both properties. One crash-stop during the run is not.

The algorithm never stores a second successor, never skips a dead neighbor, and never starts a timeout. Those are the same limits as the lecture ring. Slides 29–30 discuss a predecessor timeout and a failure detector as repairs, and they do not claim those repairs restore both properties: predecessors can crash in a cascade, and a failure detector need not be both complete and accurate.

**Liveness fails at 1 crash.** Let N = 3, ids 1, 2, 3, ring 1 → 2 → 3 → 1, and k = 1. Process 3 calls `start` and sends `Election(init = 3, S = {3})` to process 1. Process 1 computes S′ = {1} and then crashes before sending to process 2. Process 1’s only channel was that send. The token never returns to process 3, so `Elected` is never sent. Processes 2 and 3 stay at `elected = NULL`. The run does not terminate. Liveness fails. The crashed process is exempt from the “each non-faulty process” quantifier; the two live processes are not.

**Safety also fails at 1 crash, on a later crash point.** Same ring and k = 1, so K\* = {1}. Let the `Election` lap finish and let `Elected(init = 3, S = {1})` reach process 3’s successor, process 1. Process 1 sets `elected ← {1}` and crashes before forwarding to process 2. Process 1 is then faulty. Process 3 is non-faulty and its `elected` value contains a faulty process, so it is neither NULL nor a set of k non-faulty processes. Safety fails at process 3. Process 2 is non-faulty and still NULL, and no further `Elected` delivery occurs, so liveness fails at process 2 as well.

The lecture’s own failure slide is the scalar version of this fact: with the highest process crashed, `Election: 80` does not produce a finished election, and the deck states that liveness is violated. The modified algorithm uses the same single clockwise channel, so the same one-crash cutoff applies. It does not inherit a nonzero bound from anywhere in the deck.

A failure after both waves have finished is outside the run. The lecture’s picture of election is: detect a dead leader, then run an election. The bound above is for crashes during the run that is supposed to establish the two conditions.

## Findings

- Homework 3 problem 6 asks for a modification of “the Ring election Algorithm described in the lecture,” under that algorithm’s assumptions, with a no-failure safety and liveness analysis in the class style, then a bound on how many failures still leave both properties true. Safety is: each non-faulty p has `elected` equal to a set of k non-faulty processes with the lowest ids, or NULL. Liveness is: every election run terminates, and every non-faulty p has `elected` not NULL. — [T1] CS425 FA2026 Homework 3, problem 6 (`/home/isaacsimms/Desktop/MCS-UIUC/Distributed Systems - CS425/Week8/Homework 3/hw3.fa26.pdf`)
- The Final Fall 2026 deck for this lecture is `L17.FA26.pdf`, titled “Lecture 17: Leader Election,” instructors Aishwarya Ganesan with Ram Kesavan, acknowledgement Indranil Gupta, PDF timestamp 2026-10-23. The course lecture table dates Leader Election to 2026-10-20, marks the pdf Final, names the reading “Section 15.3,” and numbers that row 18. The file name and the deck title both say Lecture 17. — [T2] CS 425/ECE 428 FA2026 lectures page (https://courses.grainger.illinois.edu/cs425/fa2026/lectures.html) and `L17.FA26.pdf` (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- Lecture safety: for every non-faulty p, `elected` is either one particular non-faulty process with the best attribute, or NULL. Lecture liveness: every election run terminates, and every non-faulty p has `elected` not NULL. The best attribute is the highest one. The usual choice is the highest id. — [T2] `L17.FA26.pdf`, slide 7 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- System model on that deck: N processes, unique ids, messages eventually delivered, failures may occur during the election. Any process may call an election, at most one call at a time, concurrent calls allowed, and concurrent calls must still produce one leader. The result must not depend on who called. — [T2] `L17.FA26.pdf`, slides 5–6 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- Ring topology: processes sit in a logical ring like Chord; pi sends only to p_{(i+1) mod N}; all messages go clockwise. — [T2] `L17.FA26.pdf`, slide 8 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- Ring protocol: a process that discovers the old leader has failed sends `Election` carrying its own id and attribute. On receipt, a greater attribute is forwarded; a smaller attribute is overwritten with the receiver’s own id and attribute and forwarded only if this process has not yet forwarded an election message; if the arriving id and attribute match the receiver, the receiver’s attribute is the greatest and it becomes the leader. The deck poses the “greatest (why?)” question and does not print a fourth branch. The branch that remains is: a smaller attribute at a process that has already forwarded is not forwarded. — [T2] `L17.FA26.pdf`, slide 10 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- The leader then sends `Elected` carrying its id. On `Elected`, a process sets `elected` to that id and forwards unless it is the new leader. — [T2] `L17.FA26.pdf`, slide 11 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- No-failure analysis on the deck: assume no failures during the protocol. Worst case is when the initiator is the ring successor of the would-be leader: N − 1 `Election` messages to reach that process, N further `Election` messages for an unchanged lap, N `Elected` messages. Message complexity and completion time are both 3N − 1. The deck concludes from that finiteness that liveness holds and that everyone knows the highest-attribute process (safety). Best case: the would-be leader is the initiator, 2N messages and 2N transmission times. — [T2] `L17.FA26.pdf`, slides 23–26 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- Concurrent initiators on the deck: put the initiator id on every message; cache initiator ids; suppress `Election` and `Elected` from lower-id initiators; replace the cache on a higher initiator id. Only the highest-id initiator’s run completes. — [T2] `L17.FA26.pdf`, slide 27 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- Failure slide: a crash of the highest process (the figure’s N80) is labeled as `Election: 80` circulating forever and as a liveness violation. — [T2] `L17.FA26.pdf`, slide 28 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- The deck’s repairs are: the predecessor of the crashed would-be leader can time out and start a new run, but that predecessor can crash too, and so on; any process that has seen `Election: 80` can use a failure detector and start a new run, but failure detectors need not be both complete and accurate. The deck does not state a positive number of crashes for which the ring protocol still guarantees both properties. — [T2] `L17.FA26.pdf`, slides 29–30 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- The same deck’s Bully algorithm assumes every process knows the other ids, uses timeouts, and is given liveness in a synchronous model where a worst-case one-way latency exists. In the asynchronous model the deck says Bully may never terminate, so liveness is not guaranteed. That is a different algorithm and a different assumption set from the ring. — [T2] `L17.FA26.pdf`, slides 33–34 and 45 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- The deck states that an election solution would yield consensus by taking the last bit of the elected id, and that election is therefore impossible in asynchronous systems because consensus is. This is why the failure-section patches are not presented as restoring both properties in the asynchronous model. The 0-crash bound for the modified ring algorithm above is the direct channel argument (one missing forwarder stops the lap), which matches slides 28–30, and does not depend on filling in the details of that reduction. — [T2] `L17.FA26.pdf`, slide 46 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- Chang and Roberts, CACM, May 1979: uniquely numbered processes in a circle, no central controller, n not known in advance. Their algorithm finds either the highest or the lowest number. Each participating process emits its number in one direction. A process that sees a higher number forwards it; a process that sees a lower number throws it away; a process that sees its own number is the unique extremum, because a message meets every other process before returning and only the extreme number is never extinguished. If not every process has started, an unmarked process that receives a message marks itself and emits its own number. — [T1] Ernest Chang and Rosemary Roberts, “An Improved Algorithm for Decentralized Extrema-Finding in Circular Configurations of Processes,” Communications of the ACM 22(5), May 1979, pp. 281–283 (https://people.scs.carleton.ca/~santoro/ChangRob.pdf)
- Chang and Roberts require the elected process to unmark everyone so a later election can run. They do not specify the lecture’s `Elected` circulation that writes `elected` at every process. The homework’s liveness condition needs that write at every non-faulty process, which the lecture’s `Elected` wave supplies. The worked algorithm keeps the lecture’s `Elected` wave. — [T1] Chang and Roberts 1979, “Startup Conditions” (https://people.scs.carleton.ca/~santoro/ChangRob.pdf); [T2] `L17.FA26.pdf`, slide 11 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- Chang and Roberts’ performance claims, for comparison only: best-case message passes 2n − 1 when all processes start in increasing clockwise order, worst case n(n+1)/2, average O(n log n). Time is linear in n; if only the process furthest from the maximum starts, they bound time by O(2n − 1). The lecture instead teaches a single-initiator worst case of 3N − 1 including the announcement lap. These are different counts of different variants (all-start extinction versus one initiator plus an `Elected` lap). The worked algorithm’s 2N figure is the count for the modified lecture protocol, not the paper’s average. — [T1] Chang and Roberts 1979, “Performance Analysis” (https://people.scs.carleton.ca/~santoro/ChangRob.pdf); [T2] `L17.FA26.pdf`, slides 25–26 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- Contradiction, failure model. Chang and Roberts, in the concluding remarks, consider one node that “vanishes” without taking a message and without disrupting communications. Under that model they say a crash of a non-maximum node does not affect the election; a crash of the maximum can still leave the maximum’s message circulating and elect nobody if the next-smaller message was already extinguished. The Fall 2026 deck shows a process crash and states that liveness is violated, and its ring has a channel only to p_{(i+1) mod N}, so a crash removes the process that was supposed to forward. The worked answer follows the deck: both properties are guaranteed for 0 crashes during the run, and not for 1. — [T1] Chang and Roberts 1979, “Concluding Comments” (https://people.scs.carleton.ca/~santoro/ChangRob.pdf); [T2] `L17.FA26.pdf`, slides 8 and 28 (https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- LeLann’s earlier ring method, as summarized by Chang and Roberts: every process emits its number, every process collects the numbers that pass it, and the maximum on the collected list is elected. Message count proportional to n². The k-set token in the worked algorithm keeps only k ids per message and uses one lap plus an announcement, which is the lecture’s two-wave shape rather than LeLann’s full-list collection. — [T1] Chang and Roberts 1979, introduction, citing G. Le Lann, “Distributed systems—Towards a formal approach,” Information Processing 77 (https://people.scs.carleton.ca/~santoro/ChangRob.pdf)
- No local ring-election note was found under `/home/isaacsimms/Desktop/MCS-UIUC/Distributed Systems - CS425` (filename search for election material; content search of the markdown notes hits Paxos “election” phases and sequencer leaders only). Local notes did not contribute a ring algorithm. — [T1] workspace search of that tree, 2026-10-25

## Recommendation

Use the algorithm and the 0-crash bound in the Answer as the worked solution for problem 6. It stays inside the lecture ring: one clockwise successor, `Election` then `Elected`, initiator ids, suppress a lower initiator, no-failure argument by a finite number of laps, then a separate failure argument.

The tradeoff is the lap count. Accumulating the k-set on the first lap makes the single-initiator cost 2N rather than the scalar algorithm’s worst-case 3N − 1. A coding that tried to keep the scalar “second unchanged lap” would need a new definition of when a set, rather than one id, has proved it is optimal. The return of the initiator’s token already supplies that proof, because a clockwise cycle meets every process before it returns. That is the same fact the lecture relies on when it asks why a returning id is the greatest.

Do not raise the failure bound by bolting on Bully’s all-to-all sends or a skip-to-next-live-neighbor rule. Both add assumptions the lecture’s ring does not use, and slides 29–30 and 45–46 already refuse to treat failure detectors and asynchronous timeouts as a way to get both properties back.

## Ruled out

- Treating Chang and Roberts’ “vanish without disrupting communications” remark as the failure bound. Recorded above as a contradiction. The Final Fall 2026 deck wins, and under that deck the bound is 0.
- Claiming the algorithm tolerates N − k crashes by skipping dead successors until k live processes remain. Skipping requires every process to know further membership and to detect failure. The lecture ring gives each process one successor. The deck’s detector repair is explicitly short of both completeness and accuracy.
- Using the Bully algorithm as the base. Same lecture, later slides, different assumptions (known ids, timeouts, synchrony for liveness).
- Using LeLann’s collect-every-id ring as the base. Correct for an extremum, and a k-prefix of a full collected list would also solve k-lowest, but it is not the algorithm the lecture analyzes, and its message count is quadratic even for one lap of full identifiers.
- Reading a local Week 7 or Week 8 ring-election note. None is in the CS425 tree.
- Third-party slide paraphrases of Coulouris Section 15.3, and any blog, tutorial, or forum writeup. Not used as evidence. Fall 2025 and Fall 2024 `L17` decks show the same ring protocol as Fall 2026; they were not needed once the Final Fall 2026 file was read.

## Open questions

- The schedule names “Section 15.3” as the reading and does not, on the Fall 2026 lectures page, name the book in that cell. The book text was not fetched. If Coulouris, Dollimore, Kindberg, and Blair Section 15.3 disagreed with `L17.FA26.pdf` in a corner case, the Final deck would still be the source for the worked answer.
- The homework does not say what to return when k > N or when fewer than k processes are non-faulty. Both make a set of k non-faulty processes impossible. The proof assumes a single given k with 1 ≤ k ≤ N and a run with no crashes, so those k processes exist.
- The HTML schedule numbers the 2026-10-20 Leader Election row as 18, while the deck title and file name say Lecture 17. Both point at `L17.FA26.pdf`. There is no second Fall 2026 ring-election deck in that table.
