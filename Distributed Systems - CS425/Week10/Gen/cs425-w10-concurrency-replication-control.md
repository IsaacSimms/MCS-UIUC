# CS425: Week 10 — Concurrency control and replication control

> 🧭 **Week 10 (Oct 26 – Nov 1).** Topics: concurrency control and replication control. Readings: Coulouris §4.3 and the relevant parts of Ch. 5 (marshalling, RPC), §16.1, §16.2, §16.4 (transactions, locks), §17.1–17.3 and §17.5 (distributed transactions, atomic commit, distributed deadlocks), and §18.1–18.3 and §18.5 (replication, fault-tolerant services, transactions on replicated data). I checked these section numbers against the official 5th-edition contents ([cdk5.net](http://cdk5.net)). Note that §16.5 (OCC), §16.6 (timestamp ordering), §17.4 and the §18.4 gossip/Bayou/Coda case studies are *not* on this week's list, even though the lecture touches OCC and timestamps.

## One idea, two scales

This week asks one question at two scales. First, how do many clients share one server's objects without stepping on each other? That is concurrency control. Then, how do you keep the same guarantees once the objects live on several servers, some of them copies of each other? That is replication control and atomic commit. RPC is the connecting thread. In the course framing, each operation of a transaction is an RPC to a server, and the transaction either commits every effect or has none at all (CS425 L19-20).

RPC semantics are worth getting straight first, because everything later depends on them. A lost request, a lost reply, and a callee that crashed before or after executing all look the same to the caller. So exactly-once is out, and you pick a point on a small menu. If you retransmit and re-execute, you get **at-least-once** (Sun RPC). If you retransmit and also filter duplicates, replaying the cached reply, you get **at-most-once** (Java RMI). If you don't retransmit, you get **maybe** (CORBA). At-least-once is only safe for **idempotent** operations: `x = 1` is idempotent, `x = x + 1` is not (CS425 L19-20). Marshalling into a common data representation is what lets a big-endian caller talk to a little-endian callee (CS425 L19-20; Coulouris §4.3).

## Serial equivalence is the correctness bar

Two classic anomalies motivate everything. In a **lost update**, two transactions read seats = 10 and both write 9. In an **inconsistent retrieval**, a reader sums two accounts in the middle of a transfer and prints 20 instead of 25 (CS425 L19-20). The fix is the course's central definition. An interleaving is **serially equivalent** if some one-at-a-time ordering of the same transactions produces the same end result for every object *and* the same values returned to every client.

You check it with **conflicting operations**: read–write, write–read and write–write on the *same* object. Read–read pairs never conflict, and neither do operations on different objects. Two transactions are serially equivalent iff every conflicting pair between them runs in the same transaction order, so the pairs are either all (T1, T2) or all (T2, T1) (CS425 L19-20). In the lost-update example, the pairs come out as (T2, T1), (T1, T2), (T1, T2). They are mixed, so the interleaving is not serially equivalent.

A wording gotcha: Coulouris and CS425 say *serial equivalence*, Kung–Robinson also bases validation on "serial equivalence" (Kung & Robinson 1981), and the database literature (Bernstein–Hadzilacos–Goodman) says *serializable (SR)* and proves it by showing the serialization graph is acyclic (BHG Ch. 4, Theorem 4.1). For this course, treat them as the same conflict-ordering idea. Just use the course's term on exams.

## Pessimistic: locks and two-phase locking

Exclusive locks are mutual exclusion all over again. **Read–write locks** add concurrency because read–read doesn't conflict. Many readers can share an object, a writer needs it alone, and a reader that wants to write must **promote** its lock, which succeeds only if nobody else holds it (CS425 L19-20).

Locks by themselves don't give serial equivalence. You get it from **two-phase locking**: once a transaction releases any lock, it may never acquire or promote another. That splits it into a growing phase and a shrinking phase. The proof is a short contradiction. Suppose object O1's conflicts are ordered (T1, T2) and O2's are ordered (T2, T1). Then T1 must have released a lock before T2 acquired one, and T2 must have released a lock before T1 acquired one. Both can't be true under 2PL (CS425 L19-20).

**Strict 2PL** holds locks until commit or abort. Bernstein et al. give two reasons it's what nearly every system ships. First, commit is the earliest moment the scheduler *knows* the transaction won't need more locks. Second, strict executions are recoverable, **avoid cascading aborts**, and let abort simply restore before-images. Their fine print: only *write* locks have to be held past commit. Read locks can go at termination (BHG Ch. 3). Plain 2PL lets T2 read T1's uncommitted write (a dirty read). If T1 then aborts, T2 has to abort too. That cascade is exactly what strictness rules out.

### Deadlocks, including the one you didn't see coming

Locking brings deadlock. The necessary conditions are exclusive access, no preemption, and a cycle in the **wait-for graph**. There are three responses (CS425 L19-20):

1. **Timeouts:** abort if a lock doesn't arrive in time. This is simple but wastes work.
2. **Detection:** find cycles in the wait-for graph, globally via a snapshot, then abort a victim.
3. **Prevention:** break one of the conditions, for example by taking every lock up front.

Bernstein et al. point out that timeout tuning is a real tradeoff. If the timeout is too short, you abort transactions that were just slow. If it's too long, deadlocked transactions sit around waiting (BHG Ch. 3). The trap people miss is **lock-conversion deadlock**. T4 and T5 both read-lock x and then both try to upgrade to write. Each waits on the other's read lock, and 2PL forbids either from releasing it. This pattern shows up whenever a transaction scans with read locks and writes what it finds (BHG Ch. 3). In the distributed case (Coulouris §17.5), each server sees only part of the wait-for graph. A cycle can span servers even when every local graph is acyclic, which is why the course points you at global snapshots.

## Optimistic: validate at the end

Kung and Robinson's design splits a transaction into a **read phase** that writes only to private copies, a **validation** phase, and a **write phase** that publishes the copies only if validation passed (Kung & Robinson 1981). With serial transaction numbers where $t(i) < t(j)$, $T_j$ validates against an earlier $T_i$ if one of these holds:

1. $T_i$ finished writing before $T_j$ started reading.
2. $WS(T_i) \cap RS(T_j) = \emptyset$, and $T_i$ finished writing before $T_j$ started writing.
3. $WS(T_i) \cap (RS(T_j) \cup WS(T_j)) = \emptyset$, and $T_i$ finished its read phase before $T_j$ finished its read phase.

These three conditions are the whole theory. Coulouris names two validation styles (§16.5, outside this week's assigned sections). *Backward* validation checks your read set against the write sets of overlapping transactions that have already committed, and its only option is to abort yourself. *Forward* validation checks your write set against the read sets of transactions that are still active, so it gets to choose a victim. The course's "first-cut" version, which writes in place and checks at commit, is exactly what produces **cascading aborts** (CS425 L19-20). OCC pays off when conflicts are rare. Under contention it turns into repeated wasted work.

**Timestamp ordering** fixes the serialization order up front by transaction id. A write to O is allowed only if every transaction that has read or written O has a lower id. A read is allowed only if O's last writer has a lower id. Otherwise the transaction aborts (CS425 L19-20). Two details from Bernstein et al. are worth knowing. A rejected transaction restarts with a **larger** timestamp. That's the opposite of wound-wait/wait-die deadlock prevention, which keeps the old timestamp so the transaction doesn't starve. And **Thomas' Write Rule** ignores a late write that a newer write has already overwritten, rather than aborting, as far as write–write sync goes (BHG Ch. 4). Multiversion CC keeps tentative versions so that reads rarely abort. The slides also connect the idea to key-value stores: Cassandra/DynamoDB last-write-wins on physical timestamps (an old write can win under clock skew) and Riak's vector-clock siblings (CS425 L19-20).

## Replication control

With $k$ replicas that are each down a fraction $f$ of the time, availability is $1 - f^k$. At $f = 0.1$, three replicas give 99.9% (CS425 L21). The difficulty is keeping **replication transparency** (clients see one object) and **replication consistency** (clients see one consistent copy, with ACID for transactions). Front ends hide the replica group (CS425 L21).

**Passive replication** sends every update through a primary, which totally orders them. When the primary dies, you elect a new one. **Active replication** treats replicas symmetrically and multicasts each request to all of them. Both rest on the **replicated state machine** idea: the same deterministic machine, started in the same state and fed the same inputs in the same order, produces the same outputs (Schneider 1990, via CS425 L21). Active replication therefore needs total (or \*-total) ordering, plus virtual synchrony so that failures and joins are seen in the same order as messages (CS425 L21). The corollary for code: any nondeterminism in your handler, such as wall-clock reads, unordered-map iteration or thread timing, quietly breaks active replication.

Consistency models matter here. **Linearizability** means each operation appears to take effect instantaneously at a point between its invocation and its response, so real-time order is preserved. **Sequential consistency** (Lamport) only requires *some* legal sequential order consistent with each process's program order, so it is strictly weaker. Herlihy and Wing add a property engineers rely on: linearizability is **local** (if every object is linearizable, so is the whole system), while sequential consistency is not. They give a two-queue history in which each object alone is sequentially consistent but the combined history is not (Herlihy & Wing 1990). For transactions over replicas, the target is **one-copy serializability**: equivalent to a serial run on a single logical copy. A serial history over replicas can still fail 1SR (CS425 L21; BHG Ch. 8).

### Quorums

Gifford's weighted voting gives each copy some votes. A read collects $r$ votes and a write collects $w$, with $r + w > N$ (the total votes), so every read quorum overlaps every write quorum and **version numbers** identify the current copy (Gifford 1979). Copies with zero votes ("weak representatives") act as caches that can't affect correctness. Bernstein et al.'s quorum-consensus statement adds the second inequality you should memorize: both $2W > N$ *and* $R + W > N$. Two writes then always overlap, so version numbers stay totally ordered. A write reads the version numbers across its quorum, takes the maximum plus one, and writes that version (BHG Ch. 8). With majorities on both sides, tolerating one failure takes three copies (BHG Ch. 8).

| Concern | Passive (primary-backup) | Active (state machine) |
| --- | --- | --- |
| Ordering source | Primary's sequence | Total-order multicast |
| On failure | Run an election for a new primary | Virtual synchrony delivers the view change in order |
| Determinism needed | Only at primary | Every replica |

## Atomic commit across servers

When a transaction touches objects on many servers, every server has to commit or every server has to abort. That is the atomic commit problem, which is a form of consensus (CS425 L21). **One-phase commit**, where the coordinator just says "commit", fails because a participant gets no veto, for example when its object is corrupted. **Two-phase commit** fixes that:

- **Phase 1:** the coordinator sends `Prepare`. Each participant writes its tentative updates to stable storage and *then* votes Yes or No.
- **Phase 2:** if the coordinator collects every Yes before its timeout, it logs the decision and sends `Commit`. Otherwise it sends `Abort`.

The failure handling is where exam points live (CS425 L21):

- A participant that voted **No** may abort right away.
- A participant that voted **Yes** is stuck. It may not decide on its own and must wait, polling the coordinator if the decision message is lost.
- If `Prepare` is lost, the participant times out and aborts.
- If a vote is lost, the coordinator times out and aborts, then has to tell everyone.

Bernstein et al. name the stuck state the **uncertainty period**. They prove that if communication failures or total failures can happen, *every* atomic commit protocol can block (Prop. 7.1), and that no such protocol guarantees independent recovery (Prop. 7.2). The cooperative termination protocol, where an uncertain participant asks its peers, lowers the chance of blocking but doesn't remove it (BHG Ch. 7). The course's answer is to run Paxos for the commit decision so the coordinator isn't a single point of blocking, while keeping the rule that any No forces Abort (CS425 L21).

## Gotchas

- **2PL ≠ strict 2PL.** 2PL alone gives serial equivalence. Avoiding dirty reads and cascading aborts needs locks held to commit, and strictly speaking only the write locks (BHG Ch. 3).
- **Read→write promotion can deadlock with no second object involved.** One object and two upgraders is enough.
- **Under timestamp ordering, aborts aren't deadlocks.** TO never blocks, so it never deadlocks. It aborts instead, and the restarted transaction gets a new, larger timestamp.
- **2PC blocks on coordinator failure only for Yes-voters.** Participants that voted No or never voted can still abort on their own.
- **$R + W > N$ alone isn't enough when writes race.** Also require $W > N/2$ (unless something else, like transactional locking as in Gifford's setting, already serializes writers).
- **Sequential consistency ≠ linearizability ≠ serializability.** The first two are about single operations on objects (and only linearizability respects real time). Serializability is about multi-object transactions.

## C++ notes for your MPs

Acquire multiple locks in one global order, for example sorted by key, and use `std::scoped_lock(a, b)` for in-process mutexes, which applies a deadlock-avoidance algorithm. Give every transaction an id and make every commit-protocol message **idempotent** keyed on it: `Commit(txid)` applied twice must be a no-op, and so must `Abort(txid)` after an abort. Persist the vote (or tentative writes) and `fsync` *before* sending Yes. Compute timeouts with `std::chrono::steady_clock`. For at-most-once RPC, keep a dedupe table from `(client_id, seq)` to the cached reply.

```c++
enum class TxState { Active, Prepared, Committed, Aborted };
void on_commit(TxId t) {                      // idempotent
  auto& s = txs[t];
  if (s == TxState::Committed) return;        // duplicate: ack again
  apply_tentative(t); log_commit(t); s = TxState::Committed;
}
```

## For the podcast

- **Audience:** UIUC MCS students already in CS425 (Coursera DS4) who know Lamport and vector clocks, multicast ordering, Paxos, mutual exclusion and leader election. Use those as hooks rather than re-teaching them.
- **Emphasize:** the conflicting-operations test for serial equivalence; why 2PL works and why strict 2PL is what ships; the lock-upgrade deadlock; the Kung–Robinson three-phase idea; 2PC's uncertainty period and why it blocks; the two quorum inequalities; passive vs active replication; linearizability vs sequential consistency.
- **Skip:** narrating code, step-by-step slide transaction tables, and endianness trivia. Don't stray into gossip/Bayou (not assigned) or next week's stream processing.
- **Say clearly:** Coulouris ("koo-LOO-ris"), Kung–Robinson, Gifford, Bernstein–Hadzilacos–Goodman ("had-zee-LAH-kos"), Herlihy and Wing, Thomas' Write Rule, "two-phase locking" vs "two-phase commit" (different things that share a name), "one-copy serializability".
- **Formulas out loud:** "R plus W greater than N" and "W greater than N over two"; "availability is one minus f to the k"; "two-P-L" for locking, "two-P-C" for commit.
- **Misconceptions to call out:** that two-phase locking and two-phase commit are related protocols (they solve different problems); that OCC never aborts; that 2PC is non-blocking if you add timeouts; that replication automatically gives consistency; that last-write-wins is safe under clock skew.

## Sources

- CS425 FA2026 Lectures page (schedule, readings; Week 10 lecture decks listed as Tentative with no PDF yet): [courses.grainger.illinois.edu/cs425/fa2026/lectures.html](https://courses.grainger.illinois.edu/cs425/fa2026/lectures.html)
- CS425 FA2026 syllabus (textbook: Coulouris 5th ed.): [intro.FA26.pdf](https://courses.grainger.illinois.edu/cs425/fa2026/intro.FA26.pdf)
- CS425 L19-20, RPCs and Concurrency Control, **FA2025** slides (Gupta, Ganesan): [L19-20.FA25.pdf](https://courses.grainger.illinois.edu/cs425/fa2025/L19-20.FA25.pdf)
- CS425 L21, Replication Control, **FA2025** slides (Gupta, Ganesan): [L21.FA25.pdf](https://courses.grainger.illinois.edu/cs425/fa2025/L21.FA25.pdf)
- Coulouris, Dollimore, Kindberg & Blair, *Distributed Systems: Concepts and Design*, 5th ed., official contents (section numbers only; book text not accessed): [cdk5.net/contents](https://www.cdk5.net/contents)
- Bernstein, Hadzilacos & Goodman, *Concurrency Control and Recovery in Database Systems* (1987), Ch. 3 (2PL), Ch. 4 (TO, Thomas' Write Rule), Ch. 7 (atomic commit), Ch. 8 (replicated data, quorum consensus), free from Microsoft Research: [microsoft.com/en-us/research/people/philbe/book](https://www.microsoft.com/en-us/research/people/philbe/book/)
- Kung & Robinson, "On Optimistic Methods for Concurrency Control," ACM TODS 6(2), 1981: [OCC.pdf (CMU 15-721 copy)](https://www.cs.cmu.edu/~15721-f24/papers/OCC.pdf)
- Gifford, "Weighted Voting for Replicated Data," SOSP 1979: [gifford79.pdf (Swarthmore copy)](https://www.cs.swarthmore.edu/~newhall/readings/gifford79.pdf)
- Herlihy & Wing, "Linearizability: A Correctness Condition for Concurrent Objects," ACM TOPLAS 12(3), 1990: [HerlihyWing90.pdf](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf)
