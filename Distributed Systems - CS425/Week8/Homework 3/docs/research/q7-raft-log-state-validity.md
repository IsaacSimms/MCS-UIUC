---
question: |
  Commander Brand, Pilot Cooper, and you look at the Raft state for the 5-node cluster (servers S1, S2, ... S5). The current term is 3, and S1 is the leader. Servers S1, S2, and S3 have three log entries whose term numbers are 1 at log positions 1, 2, and 3. Servers S4 and S5 have two entries whose term numbers are 2 at log positions 1 and 2. Is this a valid cluster state in Raft? If yes, show the sequence of transitions that lead to this state. If not, describe which steps in Raft's algorithm prevent this state from occurring.
researched: 2026-10-25
confidence: confident
versions:
  - Raft extended paper: Ongaro and Ousterhout, "In Search of an Understandable Consensus Algorithm (Extended Version)", 20 May 2014, https://raft.github.io/raft.pdf (extended version of the USENIX ATC 2014 paper)
  - Raft TLA+ specification: Diego Ongaro, raft.tla, copyright 2014, https://github.com/ongardie/raft.tla/blob/master/raft.tla (fetched 2026-10-25; repo README says this file is slightly updated relative to the dissertation copy)
  - CS 425 / ECE 428 Fall 2026 Lecture 18-B: L18.B.FA26.pdf, PDF timestamp 23 Oct 2026, https://courses.grainger.illinois.edu/cs425/fa2026/L18.B.FA26.pdf (lectures page still labeled the Raft deck Tentative)
  - CS 425 Fall 2026 Homework 3: hw3.fa26.pdf, out 12 Oct 2026, local path Week8/Homework 3/hw3.fa26.pdf
---

# Is the term-3 Raft log with [1,1,1] on S1–S3 and [2,2] on S4–S5 valid?

## Answer

Yes. This is a reachable Raft state. Fall 2026 CS 425 does not change the algorithm: Lecture 18-B restates the paper’s election restriction, log matching, leader completeness, and previous-term commitment rule, and the assigned reading is the extended Raft paper, sections 2 and 5. The worked answer therefore follows that paper.

Final snapshot, after the sequence below. Entry cells are the term stored in that log index. Every server’s `currentTerm` is 3. S1 is the only leader. No entry is committed.

| Server | Role | Index 1 | Index 2 | Index 3 |
|---|---|---|---|---|
| S1 | leader, term 3 | 1 | 1 | 1 |
| S2 | follower, term 3 | 1 | 1 | 1 |
| S3 | follower, term 3 | 1 | 1 | 1 |
| S4 | follower, term 3 | 2 | 2 |  |
| S5 | follower, term 3 | 2 | 2 |  |

Nothing in that table is committed. Leader completeness obliges later leaders to keep an entry only after it is committed. Both divergent prefixes miss that bar: the term-1 entries were never stored on a majority during term 1, and the term-2 entries are stored on only two servers.

### Sequence

A majority of five is three. An empty log is less up-to-date than any log that has an entry (formal spec: last term 0, length 0). Servers fail by stopping and later recover the log, `currentTerm`, and `votedFor` from stable storage. Messages may be lost. Terms may advance on one server before another.

**Term 1.** All logs are empty and every `currentTerm` is 0. S1 times out, becomes a candidate, increments to term 1, and votes for itself. S2–S5 are empty, so S1’s log is as up-to-date as theirs. They grant the vote. S1 wins and appends three client entries. Each is stamped with term 1, so S1’s log is `[1, 1, 1]`. Those AppendEntries are lost. S1 never sees a majority ack, so it does not commit them. S1 is then partitioned from the other four. It still believes it is leader of term 1. Its log stays `[1, 1, 1]`.

**Term 2.** S2–S5 receive no RPCs and S4 times out first. S4 increments to term 2 and votes for itself. Its log is empty. S2, S3, and S5 are also empty, so they grant the vote. S1 does not answer. S4 has a majority `{S2, S3, S4}` and becomes leader. The only server that holds `[1, 1, 1]` is outside that majority, so the election restriction does not look at S1. S4 appends two entries, both stamped term 2. Its log is `[2, 2]`. It replicates both entries to S5 only. S5’s empty log accepts them. S4 then crashes, before any successful AppendEntries to S2 or S3. The crash preserves S4’s log and term on disk. S2 and S3 are still empty, at term 2.

**Term 3.** Restore contact among S1, S2, and S3 only. Leave S4 crashed and delay S5 (its randomized election timer has not fired; a longer timer is the mechanism the paper uses so that one candidate wins).

S1’s term-1 AppendEntries reach S2. S2’s term is 2, so S2 rejects them and returns term 2. S1 sees a higher term, sets `currentTerm` to 2, and becomes a follower. Its log is not touched. No leader is sending heartbeats to this trio, so S1 times out, increments to term 3, and votes for itself. RequestVote carries last-log term 1 and last index 3.

- S2 is in term 2 with an empty log. The term-3 RPC moves S2 to term 3 and clears `votedFor`. S1’s last term 1 is newer than S2’s last term 0, so S2 grants the vote. S3 does the same.
- S5, if it answers, refuses: its last term is 2, which is newer than 1. S1 does not need S5.

S1 has votes `{S1, S2, S3}`, a majority, and becomes leader of term 3. On election it sets each follower’s `nextIndex` to 4 and starts AppendEntries.

S2 and S3 are empty, so the first attempts (`prevLogIndex` 3, then 2, then 1) fail the consistency check and S1 decrements `nextIndex`. The attempt with `prevLogIndex` 0 matches the empty prefix. S1 then sends the three term-1 entries. S2 and S3 store them as term 1. Re-replication does not renumber an entry. S2 and S3 now hold `[1, 1, 1]`.

**Bring S4 and S5 back.** Each restarts as a follower. Disk still has log `[2, 2]` and term 2. S1’s AppendEntries carry term 3, so each server sets `currentTerm` to 3 and stays a follower. The consistency check fails: S1’s preceding term does not match index 1 or 2 on these logs, and a heartbeat whose `prevLogIndex` is 3 falls off the end of a length-2 log. A failed check does not delete entries. Deletion happens only on a later successful AppendEntries, which removes the conflicting tail and then appends the leader’s entries. Until that RPC succeeds, S4 and S5 still hold `[2, 2]`.

That moment is the homework state. S1’s `commitIndex` is still 0: the term-1 entries are on a majority, but a leader commits by replica count only an entry from its current term. There is no term-3 entry yet.

## Findings

- Problem 7 asks whether this 5-server log state can occur under Raft. Problem 9 is the problem that proposes a variant. Problem 7 does not change election quorums, commitment, or log rules. — [T1] CS 425 Fall 2026 Homework 3 (`Week8/Homework 3/hw3.fa26.pdf`; https://courses.grainger.illinois.edu/cs425/fa2026/hw3.fa26.pdf)
- The Fall 2026 Raft lecture assigns the extended paper, sections 2 and 5, at https://raft.github.io/raft.pdf. The deck says its figures are adapted from that paper and from the Raft user-study slides. It does not state a modified election rule, log rule, or commitment rule. — [T2] CS 425 Fall 2026 Lecture 18-B (https://courses.grainger.illinois.edu/cs425/fa2026/L18.B.FA26.pdf), slide 33 and lectures schedule (https://courses.grainger.illinois.edu/cs425/fa2026/lectures.html)
- “A candidate wins an election if it receives votes from a majority of the servers in the full cluster for the same term.” For five servers that majority is three. “There is at most one leader in a given term.” — [T1] Ongaro and Ousterhout, extended Raft paper, §5.2 and Figure 3 (https://raft.github.io/raft.pdf)
- The receiver grants a vote only when `votedFor` is null or already this candidate, and the candidate’s log is at least as up-to-date as the receiver’s. “Up-to-date” compares the last entry only: a later last term wins; if the last terms are equal, the longer log wins. The candidate must be at least as up-to-date as any log in the electing majority, because that is the majority that intersects every committed entry. Servers outside that majority do not get a veto. — [T1] extended Raft paper, Figure 2 (RequestVote) and §5.4.1 (https://raft.github.io/raft.pdf)
- The same comparison is what the lecture writes as a deny rule: voter V denies when `(lastTermV > lastTermC) || ((lastTermV == lastTermC) && (lastIndexV > lastIndexC))`. The slide’s gloss is that the leader has the most complete log among the electing majority. — [T2] Lecture 18-B, slides 16 and 28 (https://courses.grainger.illinois.edu/cs425/fa2026/L18.B.FA26.pdf)
- An empty log has last term 0 and length 0. A candidate is up to date enough when its last term is greater, or the last terms are equal and its log is at least as long. So `[1, 1, 1]` obtains votes from empty servers, and an empty candidate is refused by any server that already stores a term-1 entry. — [T1] `raft.tla`, `LastTerm` and `HandleRequestVoteRequest` (https://github.com/ongardie/raft.tla/blob/master/raft.tla)
- `votedFor` is “the candidateId that received vote in current term (or null if none),” and each server votes for at most one candidate in a given term. A newer term therefore starts with no vote. The spec does that assignment explicitly: an RPC with a higher term sets `currentTerm`, converts the server to follower, and sets `votedFor` to null; the same message is then handled under the new term. — [T1] extended Raft paper, Figure 2 and §5.2; `raft.tla`, `UpdateTerm` and `Receive` (https://raft.github.io/raft.pdf, https://github.com/ongardie/raft.tla/blob/master/raft.tla)
- A leader appends a new entry locally, stamped with its current term, then replicates. “A log entry is committed once the leader that created the entry has replicated it on a majority of the servers.” Losing the AppendEntries, or crashing before that majority exists, leaves the entry uncommitted. The leader never overwrites or deletes its own log. — [T1] extended Raft paper, §5.3, Figure 2, and Figure 3 (Leader Append-Only) (https://raft.github.io/raft.pdf)
- Log matching says that equal index and equal term imply the same command and the same prefix. It says nothing about the same index carrying different terms on different servers. Figure 7 and Figure 8 are legal states in which followers hold conflicting uncommitted terms. — [T1] extended Raft paper, §5.3 and Figures 7–8 (https://raft.github.io/raft.pdf)
- Within one log, the lecture states that entry terms are monotonically increasing, because a leader appends only in its current term and terms never go backward. Both `[1, 1, 1]` and `[2, 2]` satisfy that. The lecture’s catch-up example is a term-2 leader that appended two entries and crashed before a majority had them. — [T2] Lecture 18-B, slides 9, 21, and 24 (https://courses.grainger.illinois.edu/cs425/fa2026/L18.B.FA26.pdf)
- On a failed AppendEntries consistency check the leader decrements that follower’s `nextIndex` and retries. Followers’ `nextIndex` values are independent, so S2 and S3 can be brought to `[1, 1, 1]` while S4 and S5 have not yet matched. A conflicting tail is deleted only when the check succeeds. `prevLogIndex` 0 matches an empty prefix. — [T1] extended Raft paper, Figure 2 and §5.3; `raft.tla`, `HandleAppendEntriesRequest` (`logOk` is true when `mprevLogIndex = 0`) and `HandleAppendEntriesResponse` (https://raft.github.io/raft.pdf, https://github.com/ongardie/raft.tla/blob/master/raft.tla)
- “Raft never commits log entries from previous terms by counting replicas. Only log entries from the leader’s current term are committed by counting replicas.” Figure 2’s commit rule requires `log[N].term == currentTerm` in addition to a majority. The spec’s `AdvanceCommitIndex` has the same term test. A term-3 leader that has only `[1, 1, 1]` on a majority therefore leaves `commitIndex` at 0. — [T1] extended Raft paper, §5.4.2 and Figure 2; `raft.tla`, `AdvanceCommitIndex` (https://raft.github.io/raft.pdf, https://github.com/ongardie/raft.tla/blob/master/raft.tla)
- The paper’s reason for that rule is a state of the same shape as this homework. Figure 8(c): after S5 has been leader and has placed a different term at an index, S1 is elected again and replicates its older entry onto a majority, and that older entry is still not committed. Figure 8(d): the server that holds the higher term can still be elected later and can overwrite it. Figure 8(e): once a current-term entry is on a majority, that overwrite is impossible. — [T1] extended Raft paper, Figure 8 caption and §5.4.2 (https://raft.github.io/raft.pdf)
- The lecture teaches the same commitment trap: an older-term entry can sit on a majority while another server’s last term is higher, that other server can still be elected, and the older entry must not be treated as committed until a current-term entry is on a majority. — [T2] Lecture 18-B, slides 30–32 (https://courses.grainger.illinois.edu/cs425/fa2026/L18.B.FA26.pdf)
- Leader completeness: “If a log entry is committed in a given term, then that entry will be present in the logs of the leaders for all higher-numbered terms.” The §5.4.3 argument uses quorum intersection with the majority that accepted the committed entry, plus the up-to-date check on those voters. An entry stored on only one server in its creation term (the term-1 prefix during term 1) or on only two servers (the term-2 prefix) is outside that argument. — [T1] extended Raft paper, Figure 3 and §5.4.3 (https://raft.github.io/raft.pdf)
- “Log entries retain their original term numbers when a leader replicates entries from previous terms.” S1 in term 3 copies `[1, 1, 1]` onto S2 and S3 without rewriting those terms to 3. — [T1] extended Raft paper, §5.4.2 (https://raft.github.io/raft.pdf)
- Servers start as followers, including after a crash. Persistent state is `currentTerm`, `votedFor`, and the log. A restart keeps that state and comes up as a follower. The network may drop messages. A follower that receives no RPCs starts an election; randomized timeouts make it normal for one server to win before the others time out. Receiving an AppendEntries RPC from the current leader is what the follower rule counts, and the failure-model section allows partitions so that some servers miss a term entirely. — [T1] extended Raft paper, §2, §5.1, §5.2, §5.5, and Figure 2; `raft.tla`, `Restart`, `Timeout`, and `DropMessage` (https://raft.github.io/raft.pdf, https://github.com/ongardie/raft.tla/blob/master/raft.tla)
- The lecture’s election-timeout slide uses the same trigger: if `electionTimeout` elapses with no RPCs, the follower starts an election. Heartbeats exist to prevent that. — [T2] Lecture 18-B, slides 14–19 (https://courses.grainger.illinois.edu/cs425/fa2026/L18.B.FA26.pdf)

## Recommendation

Grade the state as valid and give the term-1 / term-2 / term-3 sequence above. The point a grader is probing is whether commitment, not mere presence on a server, is what the election restriction protects.

The sequence is tight in two places, and both are required by the paper rather than optional:

- S2 and S3 must still be empty when S4 is elected. If `[1, 1, 1]` were already on three servers in term 1, that term’s leader would have committed it, and an empty term-2 candidate could not get their votes.
- S4 must die after copying `[2, 2]` to S5 and before copying it to a third server. If the term-2 entries reached a majority, they would be committed, and S1’s less up-to-date log could not win term 3.

S4 and S5 refusing to vote for S1 is expected and does not block the election. Figure 8 is the paper’s own example of a leader whose log lacks a higher-term entry that still exists on another server.

## Ruled out

- “S4 and S5 are more up-to-date, so S1 cannot be leader.” Their last term is 2, so they deny S1. The election restriction is applied to voters in some majority, not to every server. `{S1, S2, S3}` is a majority, and at vote time S2 and S3 are empty.
- “Log matching forbids term 1 and term 2 at index 1.” Log matching fires only when the index and the term are both equal.
- “Leader completeness forbids S1, because somebody once created term 2 at index 1.” Completeness applies to committed entries. `[2, 2]` is on two servers. `[1, 1, 1]` was on one server during term 1. The later majority copies of `[1, 1, 1]` are previous-term entries under a term-3 leader, so replica count alone does not commit them.
- “A term-2 leader that already held `[1, 1, 1]` could overwrite indexes 1 and 2.” Leaders only append. A leader whose log was `[1, 1, 1]` would put term 2 at index 4, not at index 1.
- A Fall 2026 Raft variant. The lecture deck and the homework’s problem 7 use the paper’s rules. Problem 9 is where a variant is introduced.
- Local notes. A search of `Distributed Systems - CS425` for Raft notes found none.
- The dissertation PDF. The extended paper’s §5.4, including the Figure 8 counterexample and the §5.4.3 proof sketch, is the safety argument the course assigns. The TLA+ spec was used only for the bookkeeping Figure 2 compresses: empty-log last term 0, `votedFor` cleared on a term bump, and `prevLogIndex` 0 as the empty prefix. Those match the paper’s definitions; they are not a second algorithm.
- Blogs, forums, and secondary write-ups. Not used.

## Open questions

- Coursera’s CS 425 videos for MCS students are behind login, so their wording was not checked. The public Fall 2026 deck and the paper it assigns agree on every rule used here.
- The lectures HTML page still marks the Raft deck Tentative. The PDF itself is dated 23 Oct 2026, the day after the 22 Oct lecture, and it does not diverge from the paper.
- The state is reachable and then transient. The next successful AppendEntries from S1 will delete `[2, 2]` and replace it with `[1, 1, 1]`. The homework asks whether the state can occur, not whether it is the quiescent converged log.
- This note was written in the researching session because a nested research subagent was not used. Context isolation was not preserved.
