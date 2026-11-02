```markdown
# Quiz notes

## 1. A ring of processes with the following node ids in clockwise order is running the Ring Election protocol discussed in lecture: 10, 3, 2, 4, 7, 6, 8, 9, 5 (this list does not include the failed leader). The process with id 2 initiates a new leader election run, in order to elect the highest-id process as leader. Assuming no further failures, the total number of messages incurred until the protocol terminates is:

**Context.** Ring-based leader election (Chang–Roberts): an initiator sends its ID clockwise; a receiver forwards a strictly higher ID, replaces a lower ID with its own and forwards that, and upon receiving its own ID declares itself leader and circulates a single leader-announcement message.

**Correct answer.** 25

**Why.** With the clockwise order 10→3→2→4→7→6→8→9→5, process 2 starts by emitting Election(2). Each subsequent process injects its own higher ID when it sees a smaller one, producing 16 election messages until Election(10) returns to 10. 10 then emits a Leader(10) announcement that traverses the remaining 9 hops. Total = 16 + 9 = 25.

---

## 2. Your colleague proposes a Modified version of the Ring Election algorithm discussed in lecture. The only design decision is different in this modified version is that the initiator node (instead of the would-be coordinator node) is the one who keeps track of Election messages; the initiator also waits for an unmodified “Election” message to circulate once around the ring – when it receives this, the initiator then forwards the “Elected” message, and subsequently stops the Elected message when it circulates once around the ring. This modified algorithm:

**Context.** The standard ring election places announcement responsibility on the elected coordinator (the highest ID) after it sees its own Election message return. The modification moves that bookkeeping and announcement duty to the original initiator.

**Correct answer.** Is not live when the initiator process fails

**Why.** The initiator is the only process authorized to recognize that an unmodified Election has completed a full lap and to originate the Elected message. If it crashes after starting the election but before finishing those steps, no other process takes over, so the protocol never reaches the announcement phase and never terminates.

---

## 3. In a Google Chubby system of 6 servers, what is the minimum size of quorum sets?

**Context.** Chubby runs Paxos among its replicas. Paxos safety requires that every pair of quorums intersect, obtained by taking majority sets (more than half the servers).

**Correct answer.** 4

**Why.** With 6 servers a set of size 3 is not a majority (two disjoint groups of 3 can be formed). A set of size 4 cannot be disjoint from another set of size 4, guaranteeing the intersection property.

---

## 4. Someone designs a Maekawa-style mutual exclusion system for 6 processes with the following voting sets. P1: {P1,P2,P3}; P2: {P2,P3,P4}; P3: {P3,P4,P5}; P4: {P4,P5,P6}; P5:{P5,P6,P1}; P6:{P6,P1,P2}. The resulting algorithm:

**Context.** Maekawa obtains mutual exclusion via voting sets. Safety requires every pair of voting sets to have a non-empty intersection. Liveness is provided by the Lamport-timestamp grant rule (grant to the lowest timestamp, queue the rest).

**Correct answer.** Is Live but not Safe

**Why.** S1 ∩ S4 = ∅, so two processes can both collect all required permissions and enter the critical section, violating safety. The timestamp ordering rule still ensures that the oldest request can always make progress, so the algorithm remains live.

---

## 5. In a synchronous system of N=12 processes running the Bully algorithm (with attribute = id) for leader election, the coordinator as well as the next (N/3-1), or 3, processes with the next highest ids after the coordinator fail simultaneously (at the same instant of time). Thereafter, no more processes fail. In this version of the Bully algorithm, the old (failed) coordinator is also sent Election messages. Then the exact worst-case (maximum) number of messages that are sent by the Bully algorithm until the leader election algorithm has run completely is:

**Context.** Bully algorithm: a process sends Election to all higher-id processes (including failed ones); alive higher processes reply with Answer and start their own election; the highest survivor sends Coordinator to all lower-id processes. Worst case is when the lowest-id process initiates.

**Correct answer.** 95

**Why.** Processes 9–12 fail; highest survivor is 8. Process 1 initiates, causing processes 1–8 each to send Election to all higher ids: 11+10+9+8+7+6+5+4 = 60. Answers from alive higher processes: 7+6+5+4+3+2+1 = 28. Process 8 sends 7 Coordinator messages. Total 60+28+7 = 95.

---

## 6. A new open-source system (intended for asynchronous systems) uses a leader election protocol in a group of N processes that is akin to the following (you can assume that no additional processes join, fail from, or leave the group during the election). When a process discovers the leader has failed, it initiates an election. It sends out an “ElectMe!” message to all N-1 processes including itself. Every process has a unique priority (e.g., its id), and the ElectMe! message contains this priority. When a process receives an ElectMe! Message (notice that a process has to receive its own ElectMe! too and vote on it), immediately it does the following: it compares its own priority with that in the message. If its own priority is higher, it multicasts out an ElectMe! message to everyone; otherwise it responds back with a unicast “Vote” message. However, once a process has sent out a Vote message, it cannot send out any more Vote or ElectMe! Messages (i.e., a process can vote at most once). A process also can send out at most one ElectMe! message. Finally, when a process receives at least 2N/3 (i.e., a super-majority of N) Vote messages, it declares itself as a leader. There may be multiple correct answers below. Given that safety requires only the highest-priority process to be elected and everyone to know about this new leader, this protocol is (MULTIPLE answers):

**Context.** The protocol uses priority-carrying ElectMe! multicasts and at-most-once Vote replies, with a 2N/3 threshold for self-declaration. Safety requires only the highest-priority process to be elected and everyone to know about it.

**Correct answers.**
- Not live
- Not safe

**Why.** A non-highest process can collect votes only from processes with priority ≤ its own; in an asynchronous network that set can exceed 2N/3, so a non-highest process can declare itself leader. The protocol also never disseminates the outcome after declaration, so others may not learn the winner. Liveness fails because votes are at-most-once: if enough processes have already voted for an earlier ElectMe!, the true highest may never reach 2N/3 votes.

---

## 7. A group of 4 processes P1 through P4 are running the Ricart and Agrawala’s algorithm for mutual exclusion. Initially the critical section is empty. Then, simultaneously, two processes P1 and P3 initiate requests for the critical section. If the Lamport timestamps of the requests from P1 and P3 are respectively 110 and 108, then the process that gets access to the critical section first is:

**Context.** Ricart–Agrawala: a process enters the critical section only after collecting a REPLY from every other process. Concurrent requests are ordered by smaller Lamport timestamp (lower process id on ties).

**Correct answer.** P3

**Why.** Timestamps are 108 (P3) and 110 (P1). Because 108 < 110, every process replies immediately to P3 and defers the reply to P1. P3 obtains the full set of replies first.

---

## 8. A group of 4 processes P1 through P4 are running the Ricart and Agrawala’s algorithm for mutual exclusion. Initially the critical section is empty. Then, simultaneously, two processes P1 and P3 initiate requests for the critical section. If the Lamport timestamps of the requests from P1 and P3 are respectively 110 and 110, then the process that gets access to the critical section first is:

**Context.** Ricart–Agrawala: concurrent requests are totally ordered by (Lamport timestamp, process id). Smaller timestamp wins; equal timestamps are broken by smaller process id.

**Correct answer.** P1

**Why.** Both requests carry timestamp 110, so the tie is broken by process id. P1 < P3, therefore every other process replies immediately to P1 and defers its reply to P3. P1 collects the full set of replies first.

---

## 9. A group of 5 processes P1 through P5 are running the Ricart and Agrawala’s algorithm for mutual exclusion. Initially the critical section is empty. Then, simultaneously, three processes P2, P4 and P5 initiate requests for the critical section. Assuming all messages are unicast messages, the total number of messages exchanged until all of P2, P4, P5 release their critical section is:

**Context.** Ricart–Agrawala: each requester sends a unicast REQUEST to each of the other N-1 processes and must collect a unicast REPLY from each. Every REQUEST is answered by exactly one REPLY (immediate or deferred).

**Correct answer.** 24

**Why.** N = 5, three requesters. Each emits 4 REQUESTs and later receives 4 REPLYs: 3 × 4 × 2 = 24. Concurrency only changes when some REPLYs are sent; it does not change the number.

---

## 10. A group of 5 processes P1 through P5 are running the Ricart and Agrawala’s algorithm for mutual exclusion. Initially the critical section is empty. Then, simultaneously, three processes P2, P4, and P5 initiate requests for the critical section. If the Lamport timestamps of the requests from P2, P4, P5 are respectively 21, 21, 21, then the process that gets access to the critical section first is:

**Context.** Ricart–Agrawala: concurrent requests are totally ordered by (Lamport timestamp, process id). Smaller timestamp wins; equal timestamps are broken by smaller process id.

**Correct answer.** P2

**Why.** All three requests carry timestamp 21, so the tie is broken by process id. P2 has the smallest id among {P2, P4, P5}, therefore every other process replies immediately to P2 and defers its replies to P4 and P5. P2 collects the full set of replies first.
```