# Generated practice multiple choice (midterm style)

Select the ONE BEST answer. Answer key is at the bottom, don't scroll until you're done.

---

1. Event e1 has Lamport timestamp 5 and event e2 has Lamport timestamp 9. Which of the following is TRUE?
a. e1 happened before e2
b. e1 and e2 are concurrent
c. e2 did not happen before e1
d. Nothing can be inferred about e1 and e2

c

---

**Use this run for questions 2, 3, and 4.** Three processes, all clocks start at 0 (Lamport) / (0,0,0) (vector). Events listed in order on each process:

- P1: local event `a`, Send(m1 → P2), local event `b`, Receive(m3)
- P2: Receive(m1), Send(m2 → P3)
- P3: local event `c`, local event `d`, local event `e`, Receive(m2), Send(m3 → P1)

1. The Lamport timestamp of Receive(m3) at P1 is:
a. 4
b. 6
c. 7
d. 8



1. The vector timestamp of Receive(m3) at P1 is:
a. (3, 2, 5)
b. (4, 2, 5)
c. (4, 2, 6)
d. (2, 2, 5)

1. How many events in this run are concurrent with event `b` at P1?
a. 3
b. 5
c. 7
d. 9

---

5. A Cassandra-like store has N = 6 replicas per key. You need every two write sets to overlap AND every read set to overlap every write set. Which (W, R) works?
a. W = 3, R = 4
b. W = 4, R = 2
c. W = 4, R = 3
d. W = 2, R = 5

6. In a system that only guarantees eventual consistency, which run is IMPOSSIBLE?
a. A client reads a stale value after its own write was acknowledged
b. Two clients reading the same key at the same moment get different values
c. A read returns the value of a write that was issued only after that read's result came back to the reader
d. Replicas disagree for a short time after writes to the key stop

7. Which statement about consistency models is TRUE?
a. Sequential consistency requires all operations to be ordered by real time across all clients
b. Linearizability is a weaker model than sequential consistency
c. Sequential consistency requires one global order that respects each client's program order, but that order may disagree with real time across different clients
d. Causal consistency is stronger than sequential consistency

8. A Cassandra ring has nodes in clockwise order N1, N2, N3, N4, N5, N6, N7, N8. Racks: N1, N3, N7 in rack 1; N2, N4, N5 in rack 2; N6, N8 in rack 3. NetworkTopologyStrategy places the first replica of a key at N4. Where does the second replica go?
a. N3
b. N5
c. N6
d. N7

9. In Cassandra, instead of a Bloom filter per SSTable, you store the full list of keys present in that SSTable. Which is the best description of the tradeoff?
a. No more false positives, but much more memory per SSTable (and lookups get more expensive as the list grows)
b. Eliminates the false negatives that Bloom filters produce
c. Uses less memory and eliminates false positives
d. Writes get slower because the SSTable must be re-sorted on each lookup

10. Running Cristian's algorithm, the client measures RTT = 10 ms. The minimum client→server latency is 1 ms and the minimum server→client latency is 2 ms. The accuracy of the client's clock after synchronization is:
a. ±1.5 ms
b. ±3.5 ms
c. ±5 ms
d. ±7 ms

11. A Chord ring has 64 points (m = 6) and peers 5, 18, 30, 44, 57. A message for key 3 starts at peer 30. Using the Chord routing algorithm (successor check, then closest preceding finger), the path is:
a. 30 → 44 → 57 → 5
b. 30 → 57 → 5
c. 30 → 5
d. 30 → 57 → 5 → 18

12. Gossip-style failure detection. At node A, the entry for C is (C, heartbeat = 50, local time = 180). T_fail = 40. At A's local time 205, A receives a gossip containing (C, 48). At local time 212, A receives (C, 51). No further gossip about C arrives. What is A's entry for C after time 212, and at what local time does A mark C as failed?
a. (C, 50, 180), failed at 220
b. (C, 51, 205), failed at 245
c. (C, 51, 212), failed at 252
d. (C, 48, 205), failed at 245

13. In SWIM with round-robin pinging plus a random permutation of the membership list after each traversal, the WORST-CASE number of protocol periods before a failed process is first detected is:
a. e/(e − 1)
b. O(log N)
c. 2N − 1
d. Unbounded

14. In a Gnutella overlay, every peer has exactly 4 neighbors and there are no cycles within 3 hops of peer A. A sends a Query whose TTL lets it travel at most 3 hops. Peers never forward duplicates or forward back to the sender. How many peers (not counting A) receive the Query?
a. 12
b. 36
c. 52
d. 64

15. A cluster has 4 racks, machines named S<rack><machine>. A Map task's input block has replicas on S11, S12, S31. The only free containers are on S22, S32, S41. Where is the Map task scheduled?
a. S22
b. S32
c. S41
d. Nowhere, the task cannot be scheduled

16. A MapReduce job runs on 10 machines with 4 containers each. There are 100 map tasks (30 s each) and 60 reduce tasks (20 s each). Each map task produces 50 MB of output, and the shuffle runs over a 4 Gbps network. Assuming map, shuffle, and reduce run one after the other, the total job time is about:
a. 115 s
b. 130 s
c. 140 s
d. 210 s

17. A datacenter has 5,000 servers, each with an MTTF of 60 months (assume 30-day months). The MTTF until the next server failure in the datacenter is approximately:
a. 0.36 hours
b. 8.64 hours
c. 14.4 hours
d. 12 days

18. A Cassandra key has 3 replicas, and one replica is down when a write arrives. What does the coordinator do?
a. Rejects the write until the replica recovers
b. Writes to the live replicas and keeps a hint, replaying the write to the down replica when it comes back
c. Permanently promotes a new replica on the same rack
d. Immediately triggers a read repair

---
---

## Answer key

1. **c.** Lamport only gives you: e1 → e2 implies L(e1) < L(e2). The reverse doesn't hold. L(e1) < L(e2) rules out e2 → e1, but e1 → e2 and concurrent are both still possible.

2. **c.** P1: a=1, Send(m1)=2, b=3. P2: Recv(m1)=max(0,2)+1=3, Send(m2)=4. P3: c=1, d=2, e=3, Recv(m2)=max(3,4)+1=5, Send(m3)=6. P1: Recv(m3)=max(3,6)+1=**7**.

3. **b.** P2: Recv(m1)=(2,1,0), Send(m2)=(2,2,0). P3: e=(0,0,3), Recv(m2)=max→(2,2,3) then bump own slot→(2,2,4), Send(m3)=(2,2,5). P1 before receive is (3,0,0). Max with (2,2,5) = (3,2,5), then bump P1's slot → **(4,2,5)**. (a) is the classic "forgot to increment after the max" trap.

4. **c.** b = (3,0,0). Nothing from P2/P3 reaches P1 before b, and nothing after b leaves P1. So all 7 events on P2 and P3 are concurrent with b. Check one: Recv(m2) = (2,2,4) vs (3,0,0). b is ahead in slot 1, behind in slots 2 and 3, so they're concurrent.

5. **c.** You need W > N/2 (4 > 3 ✓) and W + R > N (7 > 6 ✓). (a) fails W > N/2, (b) gives W + R = 6, not > 6, (d) fails W > N/2.

6. **c.** Eventual consistency allows stale reads (a), divergent reads (b), and convergence lag (d). But no model can return a write that didn't exist yet when the read finished. Compare the week 5 quiz: a write *acknowledged* after the read is possible, because the write can reach a replica before its ack gets back to the writer.

7. **c.** Sequential consistency = some single interleaving that respects every client's program order. Linearizability adds the real-time constraint. Strength order: linearizability > sequential > causal > session > eventual.

8. **c.** Go **clockwise** from the first replica until you hit a different rack. N5 is rack 2 (same as N4), so skip it. N6 is rack 3. N3 is the trap if you go counter-clockwise.

9. **a.** An exact key list has no false positives (and still no false negatives), but it costs memory proportional to the number of keys, and checking it is slower than a fixed number of bit checks.

10. **b.** Accuracy = (RTT − min1 − min2) / 2 = (10 − 1 − 2) / 2 = **3.5 ms**. 7 ms is the full width of the range, not the ± accuracy.

11. **b.** Fingers of 30 (aim points 31, 32, 34, 38, 46, 62): 44, 44, 44, 44, 57, 5. Key 3 is not in (30, 44], so take the farthest finger that doesn't pass 3: 57 (5 overshoots). At 57, the successor check works: 3 is in (57, 5], so forward to 5. Key 3 is stored at peer 5.

12. **c.** A lower heartbeat (48) is ignored. A higher heartbeat (51) replaces the entry and stamps A's *own* local time (212). Failure is declared T_fail after the last update: 212 + 40 = 252.

13. **c.** Round-robin + permutation guarantees every member is pinged once per traversal. The worst case is when the failure lands just after a process's turn in one traversal and its turn comes last in the next: 2N − 1. e/(e − 1) is the *expected* first detection time.

14. **c.** Hop 1: 4. Hop 2: each of those forwards to its 3 other neighbors = 12. Hop 3: 12 × 3 = 36. Total = 4 + 12 + 36 = **52**. QueryHits come back by reverse-routing along the same path.

15. **b.** No free container is node-local (S11, S12, S31 are all busy). S32 is in rack 3, the same rack as replica S31, so it's rack-local. That beats off-rack (S22, S41).

16. **c.** 40 containers. Map: ⌈100/40⌉ = 3 waves × 30 s = 90 s. Shuffle: 100 × 50 MB = 5,000 MB = 40,000 Mb = 40 Gb / 4 Gbps = 10 s. Reduce: ⌈60/40⌉ = 2 waves × 20 s = 40 s. Total = **140 s**. (a) uses fractional waves, and (b) forgets the shuffle.

17. **b.** 60 / 5,000 = 0.012 months × 30 × 24 = **8.64 hours**.

18. **b.** Hinted handoff keeps Cassandra "always writable". If *all* replicas are down, the coordinator buffers the write itself.
