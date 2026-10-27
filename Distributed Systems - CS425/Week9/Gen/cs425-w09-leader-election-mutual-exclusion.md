# CS425: Week 9 — Leader election and distributed mutual exclusion

> 🧭 **Week 9 (Oct 19–25), Course Part 2 begins.** Readings: Coulouris §15.3 (elections) and §15.2 (distributed mutual exclusion). Two problems, one underlying theme: getting a group of processes to agree on *who* gets to act, using nothing but messages.

## Why these two problems belong together

Leader election and mutual exclusion both make one process special: the coordinator, or the process in the critical section. Garcia-Molina makes the link explicit: when communication never fails, "being coordinator" is like having entered a special critical region (Garcia-Molina 1982). The difference is what happens afterward. A mutex holder eventually calls `exit()`. A leader keeps the job until it crashes, and when it crashes everyone has to *learn* who replaced it. You have already seen leaders at work: the sequencer in total-order multicast is one (CS425 L17), and Paxos needs a distinguished proposer to make progress. This week is about how that leader gets picked, and how processes take turns when nobody holds a privileged role.

## Election: the problem statement is the whole game

The CS425 formulation: any process may call an election, a process calls at most one at a time, several may call at once, and together the runs must still produce one leader, which must not depend on who started it (CS425 L17). At the end of a run:

- **Safety:** every non-faulty process has `elected` equal to the *same* non-faulty process with the best attribute (usually highest id), or `Null`.
- **Liveness:** the run terminates, and every non-faulty process ends with a non-`Null` value.

Coulouris states the same as E1/E2, where a process may still be at `UNDEF`, or it may crash (Coulouris Instructor's Guide, Ch. 15). Notice that "best attribute" means the best **among non-faulty processes**. A protocol that elects a dead process has violated safety, not just liveness.

### Ring election (Chang–Roberts style)

Processes sit on a logical ring and send messages clockwise. The initiator sends `Election(id)`. A receiver forwards a larger id. If the incoming id is smaller and it hasn't forwarded an election message yet, it replaces the id with its own. When a process gets its *own* id back, it has the maximum, so it sends `Elected(id)` around the ring (CS425 L17). The original idea is "selective message extinction": lower ids get swallowed, so only the maximum survives a full lap (Chang & Roberts 1979).

Counting messages trips people up, because the course and the paper count different scenarios:

- **CS425 (one initiator, includes the announcement):** worst case is when the initiator is the ring *successor* of the would-be leader. That's $N-1$ hops to reach the leader, $N$ more for its id to come back around, and $N$ for `Elected`, so $3N-1$ messages and $3N-1$ message times. Best case (the leader starts it) is $2N$ (CS425 L17).
- **Chang & Roberts (every process initiates, election phase only):** best $2n-1$, worst $n(n+1)/2$, average $O(n \log n)$ (Chang & Roberts 1979).

When several processes initiate, each message carries its initiator id, and processes suppress runs from lower-id initiators, so only the highest initiator's run finishes (CS425 L17). Failures are where it falls apart. If N80 crashes after its `Election:80` started circulating, that message goes around forever and liveness is lost. Re-running elections on a timeout or a failure-detector suspicion helps, but the detector is the weak point. An incomplete detector misses N80's death and safety breaks. An inaccurate one keeps suspecting a live N80 and starts new runs forever, so liveness breaks (CS425 L17).

### Bully (Garcia-Molina)

Every process knows every other id. If a process detects that the coordinator has failed and knows it has the highest id, it sends `Coordinator` to everyone below it and stops. Otherwise it sends `Election` only to processes with **higher** ids. If none answers before a timeout, it declares itself coordinator. If one answers `OK`, it waits for a `Coordinator` message, and if none arrives before a second timeout it starts over. A process that receives `Election` replies `OK` and starts its own election (CS425 L17). A process that recovers with the top id takes over even if the current coordinator is fine, which is where the "bully" name comes from (Coulouris Instructor's Guide, Ch. 15).

Costs (CS425 L17): the worst case is the lowest-id process detecting the failure. Then $N-1$ processes start elections, and the $i$-th highest sends $i-1$ `Election` messages, for $\frac{N(N-1)}{2} = O(N^2)$. Worst-case completion is still only **5 message transmission times**: Election from the lowest id, OK from the second-highest, Election from the second-highest to the dead highest, that timeout, then Coordinator. The best case is the second-highest detecting the failure. It sends $N-2$ `Coordinator` messages and finishes in one message time.

The fine print is the timeouts. Garcia-Molina's correctness argument assumes the network never fails: if a message isn't acknowledged within $T$ seconds, the receiver *really* has failed (his Assumption 8). It also assumes a node never pauses, and a node that is slow to respond must treat itself as failed and reset (Assumption 9) (Garcia-Molina 1982). Set $T$ too short in a real network and a slow but live high-id process looks dead. A lower process crowns itself while the "dead" one is still acting as coordinator, so you get two leaders. Bully is live in a synchronous model where worst-case latency is known. In an asynchronous model it may never terminate (CS425 L17). Garcia-Molina's own answer for partitions, the Invitation algorithm in §IV, gives up on a single global coordinator and gives one per group.

### Why no election algorithm is perfect

If you could solve election, you could solve consensus: elect someone and use the last bit of its id as the decision. FLP rules out consensus in an asynchronous system with even one crash, so it also rules out an election that is guaranteed both safe and live (CS425 L17). This is last week's impossibility result in a new form. In practice you keep safety and accept *eventual* liveness.

### Election in practice: quorums and leases

Chubby's replicas (typically five) run a consensus protocol. A candidate needs votes from a majority, plus promises not to elect anyone else for a **master lease** of a few seconds. The master keeps renewing the lease as long as it keeps winning a majority (Burrows 2006). Safety comes from quorum intersection: each server votes once and any two majorities overlap, so two masters can't exist at the same time. Liveness is only eventual. Google reports failovers of 4–6 s and occasionally up to 30 s (Burrows 2006; CS425 L17). ZooKeeper keeps its own leader through Zab, a leader-based atomic broadcast (Hunt et al. 2010). Its *client* election recipe is worth knowing in detail. Each candidate creates `ELECTION/guid-n_` with the `SEQUENCE|EPHEMERAL` flags, and the smallest sequence number is the leader. Each candidate watches only the next-lower znode, so a leader crash wakes one client and avoids a herd effect. The `guid` prefix covers the case where `create()` succeeded but the server crashed before replying (ZooKeeper Recipes).

## Distributed mutual exclusion

The model is `enter()`, `AccessResource()`, `exit()` over reliable FIFO channels, with **no process failures** (CS425 L18). Requirements: **safety** (at most one process in the critical section), **liveness** (every request is eventually granted), and the desirable **ordering** property, stated precisely by Coulouris as ME3: if one request happened-before another, entry is granted in that order (CS425 L18; Coulouris Instructor's Guide, Ch. 15). Three metrics are graded: **bandwidth** (messages per enter and exit), **client delay** (time to enter when nobody else is in or waiting), and **synchronization delay** (exit-to-next-entry time when exactly one process is waiting).

**Central server.** Send a request, get the token, return it. Safety holds because there is one token. The queue gives FIFO by arrival at the leader. The server is a bottleneck and a single point of failure. **Token ring.** Hold the token to enter and pass it on at exit. If you don't need it, pass it straight along. The token circulates even when nobody wants it.

**Ricart–Agrawala.** No token. To enter, set `WANTED` and multicast `Request⟨T, i⟩`, where $T$ is your Lamport timestamp, then wait for $N-1$ replies. When a request arrives, **defer** it if you are `HELD`, or if you are `WANTED` and your own pair is smaller. Otherwise reply immediately. On exit, reply to everything you deferred (CS425 L18). Ties break lexicographically on (timestamp, pid). The paper proves mutual exclusion, freedom from deadlock and freedom from starvation, and shows that $2(N-1)$ messages is optimal for a symmetric, fully parallel algorithm. Lamport's earlier algorithm needed about $3(N-1)$ (Ricart & Agrawala 1981). The subtle case is when $P_i$ replied to $P_j$ *before* making its own request. Then the Lamport clock forces $T_i > T_j$, so $P_j$ really did go first (CS425 L18). Failure handling is the weak spot: you need replies from **everyone**, so one silent crash blocks all requesters. The paper suggests timing out, probing with `ARE_YOU_THERE`, and once a failure is confirmed, treating it as an implicit REPLY and decrementing $N$ (Ricart & Agrawala 1981).

**Maekawa.** Ask a *voting set* instead of everyone. The requirements: every process is in its own set, any two sets intersect, all sets have size $K$, and each process sits in $M$ sets. Each voter grants at most one vote at a time, so the shared member of two sets can't vote for both, which gives safety (CS425 L18; Maekawa 1985). The size comes from counting:

$$
K = M,\qquad N = K(K-1) + 1 \;\Rightarrow\; K \approx \sqrt{N}
$$

The optimal sets correspond to finite projective planes, which exist when $K-1$ is a prime power (Maekawa 1985). The course's practical construction puts the processes on a $\sqrt{N}\times\sqrt{N}$ grid and takes the row plus the column, giving $2\sqrt{N}-1$ members: not optimal, but obviously intersecting (CS425 L18). The basic algorithm **can deadlock**. In the CS425 example with $N=4$, P1 waits for P3, P3 for P4, P4 for P2, and P2 for P1. Maekawa's paper avoids this by giving requests sequence numbers. A voter holding a vote for a younger request sends `INQUIRE` to that holder, and a holder that has already received a `FAILED` gives the vote back with `RELINQUISH` (Maekawa 1985). That is why the paper quotes $3(K-1)$ messages under light load and up to $5(K-1)$ under heavy load: "$c\sqrt{N}$, with c between 3 and 5."

| Algorithm | Messages per enter / exit | Client delay | Sync delay |
| --- | --- | --- | --- |
| Central server | 2 / 1 | 2 message latencies | 2 (release + grant) |
| Token ring | 1 by requester, up to N system-wide / 1 | 0 to N | 1 to N−1 |
| Ricart–Agrawala | 2(N−1), or N with HW multicast / N−1 | 1 round trip | 1 message time |
| Maekawa | 2√N / √N | 1 round trip | 2 message times |

*(Figures as stated in CS425 L18.)* The tradeoff to remember: Ricart–Agrawala brings delay down to $O(1)$ by spending $O(N)$ bandwidth, and Maekawa brings bandwidth down to $O(\sqrt{N})$ by paying one extra hop of sync delay (release to the voter, then vote to the next process) and adding a deadlock risk.

## Gotchas that show up on exams

- **Say which scenario you're counting.** "Ring election worst case" means $3N-1$ in CS425, which is one initiator and includes `Elected`. Chang–Roberts' $n(n+1)/2$ is every process initiating and counts the election phase only.
- **Bully's **$O(N^2)$** is message count. Its completion time is 5 message times.** Don't mix them up.
- **Ricart–Agrawala compares your *request* timestamp, not your current clock.** The rule is `(T_mine, me) < (T_req, j)`, using the `T` you stamped on your own outstanding request.
- **Maekawa's √N is per phase.** The course charges $2\sqrt{N}$ to enter and $\sqrt{N}$ to exit, and the grid sets are really $2\sqrt{N}-1$. The paper's total is $3\sqrt{N}$. Watch which convention a question uses.
- **Ring mutex sync delay is 1 to N−1, but client delay is 0 to N.** You might already hold the token, or you might have just passed it on.
- **Chubby locks are advisory.** Holding lock F neither is required to touch file F nor stops anyone else from touching it. Because a request can be delayed past a lock handoff, Chubby adds **sequencers** (lock name, mode and generation number, which servers can check) and a **lock-delay** of up to a minute after a holder fails (Burrows 2006).

## Implementation notes (C++)

Write each process as an explicit state machine (`RELEASED/WANTED/HELD`, or `idle/participant/elected`) driven by one event loop, so message handlers never race. Compare `std::pair<uint64_t,int>{ts, pid}` with `operator<` and you get the tie-break for free. Update the Lamport clock on every receive with `clock = max(clock, msg.ts) + 1` *before* you compare. For elections, stamp every message with (initiator, epoch), drop duplicates, and drop runs that a higher initiator has superseded. Base timeouts on `std::chrono::steady_clock`, not wall time, and derive them from the worst-case path (for Bully, that's 5 message times plus processing).

```c++
using Prio = std::pair<uint64_t,int>;          // (lamport_ts, pid)
bool defer = state == HELD || (state == WANTED && Prio{my_req_ts, me} < Prio{req.ts, req.pid});
if (defer) deferred[req.pid] = true; else send(req.pid, Reply{me});
```

*Next week (Week 10) moves on to concurrency control and replication. Today's leader-plus-quorum ideas come back there.*

## For the podcast

- **Audience:** a UIUC MCS student already in CS425 (Coursera DS4) who has already covered Lamport clocks, multicast ordering, FLP and Paxos. Don't re-explain those. Use them as hooks.
- **Emphasize:** the safety/liveness definitions for both problems; *why* each algorithm is safe (the largest id survives the ring; the shared voter in intersecting voting sets; the Lamport-clock argument); the message and delay counts; election ≡ consensus, so FLP applies; quorums plus leases in Chubby and ZooKeeper. **Skip** narrating the ring diagrams hop by hop, the semaphore review, and the code.
- **Say clearly:** Ricart–Agrawala ("RICK-art uh-GRAH-wah-lah"), Maekawa ("mah-eh-KAH-wah"), Garcia-Molina, Chang–Roberts, Coulouris ("koo-LOO-ris"), Chubby, ZooKeeper, Zab, "znode", "ephemeral sequential".
- **Formulas out loud:** "three N minus one" (ring worst case), "two N" (ring best case), "N times N minus one over two, so order N squared" (Bully messages), "five message times" (Bully completion), "two times N minus one" (Ricart–Agrawala per entry), "N equals K times K minus one, plus one, so K is about the square root of N" (Maekawa).
- **Misconceptions to call out:** Bully isn't "safe but slow", because bad timeouts can produce two leaders. Ricart–Agrawala isn't fault-tolerant: one crash stalls everyone. Basic Maekawa is safe but *not* deadlock-free. A Chubby lock doesn't by itself stop anyone from touching the resource.

## Sources

- CS425 FA2026 Lectures page (schedule and readings): [courses.grainger.illinois.edu/cs425/fa2026/lectures.html](https://courses.grainger.illinois.edu/cs425/fa2026/lectures.html)
- CS425 L17, Leader Election, FA2026 slides (Ganesan, Kesavan; slides © I. Gupta): [L17.FA26.pdf](https://courses.grainger.illinois.edu/cs425/fa2026/L17.FA26.pdf)
- CS425 L18, Mutual Exclusion, FA2025 slides (Gupta, Ganesan); the FA2026 deck is not linked yet: [L18.FA25.pdf](https://courses.grainger.illinois.edu/cs425/fa2025/L18.FA25.pdf)
- Coulouris, Dollimore, Kindberg & Blair, *Distributed Systems: Concepts and Design*, 5th ed., Ch. 15. The text itself was not accessible. I used the Instructor's Guide figures (15.2–15.8, © Pearson 2012) reproduced in WSU CS464's Ch. 15 slides: [eecs.wsu.edu/\~cs464/Chap15.pdf](https://eecs.wsu.edu/~cs464/Chap15.pdf)
- Ricart & Agrawala, "An optimal algorithm for mutual exclusion in computer networks," CACM 24(1), 1981. Course copy: [358527.ricart-agrawala.pdf](https://courses.grainger.illinois.edu/cs425/fa2023/358527.ricart-agrawala.pdf)
- Maekawa, "A √N algorithm for mutual exclusion in decentralized systems," ACM TOCS 3(2), 1985. Course copy: [p145-maekawa.pdf](https://courses.grainger.illinois.edu/cs425/fa2022/p145-maekawa.pdf)
- Garcia-Molina, "Elections in a distributed computing system," IEEE Trans. Computers C-31(1), 1982: [PDF](https://homepage.divms.uiowa.edu/~ghosh/Bully.pdf), [DOI 10.1109/TC.1982.1675885](https://doi.org/10.1109/TC.1982.1675885)
- Chang & Roberts, "An improved algorithm for decentralized extrema-finding in circular configurations of processes," CACM 22(5), 1979: [PDF](https://cse.iitkgp.ac.in/~agupta/distsys/LeaderElection-ChangRoberts.pdf), [DOI 10.1145/359104.359108](https://doi.org/10.1145/359104.359108)
- Burrows, "The Chubby lock service for loosely-coupled distributed systems," OSDI 2006: [chubby-osdi06.pdf](https://research.google.com/archive/chubby-osdi06.pdf)
- Hunt, Konar, Junqueira & Reed, "ZooKeeper: Wait-free coordination for Internet-scale systems," USENIX ATC 2010: [Hunt.pdf](https://www.usenix.org/legacy/event/atc10/tech/full_papers/Hunt.pdf)
- Apache ZooKeeper, "Recipes and Solutions" (leader election, locks): [zookeeper.apache.org/doc/current/recipes.html](https://zookeeper.apache.org/doc/current/recipes.html)
