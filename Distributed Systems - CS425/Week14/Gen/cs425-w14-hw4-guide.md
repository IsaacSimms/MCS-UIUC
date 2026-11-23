# CS425: Week 14 — HW4 ("The Interview") approach guide

**Due Thursday Dec 3, 2026, 11:59 PM CT on Gradescope.** It covers Lecture 19 onward. Answer any **8 of the 10** problems. Only the first 8 that appear get graded, so put the ones you want graded first and drop the other two. Work must be typed (you can scan hand-drawn timelines), submitted as a PDF, with each problem starting on a new page and every page tagged with its problem number. Justify every answer. Apart from Q7 (the DRF paper) and Q9 (open internet, with citations), only course materials are allowed [HW4].

This is an outline and a set of concept walkthroughs, not an answer key. The repo is public and the work is graded.

## Picking your 8

Six problems test a **single rule from the slides** directly: Q2 serial equivalence, Q3 and Q4 locking and deadlock, Q6 timestamp-ordering validation, Q8 the DSM invalidate protocol, and Q10 NFS caching. If you know the rule, you can answer them by working through it, so they're the safest points. Q1 (Maekawa) and Q5 (linearizability) need a counterexample you build yourself. Q7 is arithmetic once the DRF setup is right. Q9 is a short researched essay. Its points are easy, but it takes the most writing time. A reasonable plan is to do the six rule problems first, then whichever two of Q1, Q5, Q7 and Q9 feel quickest.

## Concept walkthroughs

**Q1: sequential Maekawa.** Start with the voting-set rules: every process is in its own set, any two sets intersect, and on the √N×√N grid each set is its row plus its column, size 2√N−1 [L19]. Safety comes from the intersection property. The process in both sets can vote for only one requester at a time, and serializing the requests doesn't change that. The deadlock example on the slides is a circular wait (P1→P3→P4→P2→P1), which happens because processes grab votes in *different orders* [L19]. Requesting in lexicographic order is the textbook resource-ordering fix for circular wait [L20-21, "Deadlock Prevention"], so you have to argue whether a cycle can still form when everyone acquires in one global order. Starvation is a separate question. Look at what a voter does with its queued requests when it gets a release, and whether some requester can be passed over forever.

**Q2: serial equivalence.** Two operations conflict only when they touch the same object and at least one of them is a write (read-write or write-write). An interleaving is serially equivalent iff all conflicting pairs execute in the same transaction order [L20-21]. For each part, list the conflicting pairs (`a`, `c`; reads of `b` never conflict with each other) and check the order of each pair. Part (c) has only 6 interleavings, so list all of them.

**Q3: ordered lock acquisition.** You need all three slide conditions for deadlock: exclusive locks, no preemption, and circular wait [L20-21]. Burns' scheme keeps the first two. For each definition of the "special field", the question is whether every transaction ends up with **the same total order** over objects. A key that depends on the transaction (access order) is a different thing from a globally unique key (ID, or a timestamp plus a unique nonce). Make sure the order is actually *total*, including how ties are broken.

**Q4: lock just-in-time, release just-after-last-use.** Compare this with two-phase locking. The slides' proof that 2PL implies serial equivalence depends on a growing phase followed by a shrinking phase. Gekko lets a transaction release one lock and acquire another later [L20-21]. For (a), try to build T1 and T2 so that one conflicting pair goes T1→T2 and another goes T2→T1. For (b), go back to the three necessary conditions.

**Q5: retry as idempotence.** In the RPC lecture, idempotent operations are the ones that are safe under at-least-once semantics [L20-21; L24]. The catch is that an operation can be idempotent *by itself* and still not be idempotent once other clients' operations land between the original and the retry. Linearizability requires one total order that respects real time: if A finishes before B starts, A comes before B. Sequential consistency only requires a total order that respects each client's program order, and it allows stale reads [L11]. Put C2's `W(x=3)` between C1's original write and its re-execution, then check what each model allows C2's reads to return. For (b), remember that the re-execution is the *same* program-order operation at C1. Ask whether some sequential order still explains everything C2 observed.

**Q6: OCC with timestamp ordering.** Use the slide rules exactly. A write to O is allowed only if every transaction that read or wrote O has a lower id. A read of O is allowed only if O was last written by a lower id [L20-21]. For each validating transaction, write out its read set and write set, compare them with the committed transactions it overlapped, and check which read happened before which committed write. Be careful with T3. It started reading `A` *before* T1's commit, so the question is which version of `A` it read.

**Q7: DRF.** Note that the course link in the HW (`courses.engr.illinois.edu/cs425/fa2026/nsdi_drf.pdf`) returned 404 today, but the USENIX copy loads [DRF]. Section 4.1 sets it up like this: if `x` and `y` are the task counts, maximize them subject to the CPU constraint, the memory constraint, and **equal dominant shares**. In the paper's example (9 CPU, 18 GB; ⟨1 CPU, 4 GB⟩ and ⟨3 CPU, 1 GB⟩) that gives x=3, y=2 [DRF §4.1]. First find each job's dominant resource as a share of the 40-CPU / 80-GB cluster, the same way the slides do [L23.B]. Then build the same system. Two traps: CPUs must be integers but memory can be fractional, and the paper itself says DRF "need not always equalize" shares once a resource is exhausted [DRF §4.1]. Check every result against both capacities.

**Q8: DSM invalidate.** Invariants: the owner holds the latest version. In R state the owner has an R copy and others may too, but nobody has a W copy. In W state **only the owner has a copy** [L25]. To write, a process multicasts invalidations (and asks for a copy if it lacks one), waits for acks, marks the page W and becomes the owner [L25]. Before working through the steps in each case, check that case against those invariants. The question warns that some cases contain errors, and it asks you to name *all* of them.

**Q9: researched essay (≤1 page, cite URLs).** The L26 slides give you the definitions of data parallelism (same model, different data) and model parallelism (the model graph split across devices). Pregel's checkpoint, ping and reload loop is the pattern for (c) [L26]. You still have to compare pipeline parallelism with both and pick a real training system's fault-tolerance mechanism from its own documentation or paper, and cite it.

**Q10: NFS caching.** On the client, a cached block is valid if `T − Tc < t` (the freshness interval) or if `Tm_client = Tm_server`. Dirty blocks are written back on `close()`, `fsync()`, memory pressure or timeout [L24]. On the server, delayed write keeps data in memory and flushes about every 30 s, while write-through goes to disk before acking [L24]. Use a three-row table (A/B/C) by three columns (t=5, 37, 70). For each cell, ask two questions: is C2 allowed to answer from its cache, and if it asks the server, what does the server have in memory or on disk at that time? The reboot at t=39 only matters if the server delayed its writes.

## Gotchas

- "Prove or give a counterexample" questions (Q2b, Q3, Q4) lose points for an example without a timeline. Write the operations out step by step.
- Don't mix up deadlock-freedom with starvation-freedom (Q1c), or serial equivalence with deadlock (Q4a vs. Q4b).
- This is the last HW before the Dec 11–13 Coursera final, and the final covers HW1–4, so the work counts twice [lectures page].

## Sources
- [HW4] CS425 FA26 Homework 4 — https://courses.grainger.illinois.edu/cs425/fa2026/hw4.fa26.pdf
- [L11] Lecture 11, KV Stores & Consistency Models — https://courses.grainger.illinois.edu/cs425/fa2026/L11.FA26.pdf
- [L19] Lecture 19, Mutual Exclusion — https://courses.grainger.illinois.edu/cs425/fa2026/L19.FA26.pdf
- [L20-21] Lectures 20–21, RPCs, Concurrency Control & Transactions — https://courses.grainger.illinois.edu/cs425/fa2026/L20-21.FA26.pdf
- [L23.B] Lecture 23B, Scheduling — https://courses.grainger.illinois.edu/cs425/fa2026/L23.B.FA26.pdf
- [L24] Lecture 24, Remote & Distributed File Systems — https://courses.grainger.illinois.edu/cs425/fa2026/L24.FA26.pdf
- [L25] Lecture 25, Distributed Shared Memory — https://courses.grainger.illinois.edu/cs425/fa2026/L25.FA26.pdf
- [L26] Lecture 26, Graph Processing & ML — https://courses.grainger.illinois.edu/cs425/fa2026/L26.FA26.pdf
- [DRF] Ghodsi et al., "Dominant Resource Fairness," NSDI 2011 — https://www.usenix.org/legacy/event/nsdi11/tech/full_papers/Ghodsi.pdf
- [lectures page] CS425 FA26 schedule — https://courses.grainger.illinois.edu/cs425/fa2026/lectures.html
