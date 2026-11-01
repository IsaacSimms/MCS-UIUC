# Raft: a consensus algorithm for distributed systems

## Defintion
Raft: a leader-based consensus algorithm which revolves around a replicated log of commands.
A collection of servers use that log to execute teh same state machine in the same order, even if a minority of them fail. 


## What a state machine is
A state machine is a deterministic program that keeps some internal state and on receiving a command updates that state and produces an output.
Deterministic program: the state machine's next state andoutput are a pure function of its current state and the command/action it is applying.
In raft:
- state machine starts from a known initial state
- given the same sequence of commands and initial state, it always produces the same sequence of states and outputs (definition of determinism)
- the only way to change its state is by applying those commands in order.

## Leader-driven design and terms
Every server does not propose. Raft elects one server leader to coordinate tasks, manage resources, make decisions, etc. Only the leader is allowed to accept new client commands and append the log.

Strong leader + term + one vote per term = builds on earlier leader-election and majority ideas from the course.

## Log matching & leader catching up
In raft, every server keeps a copy of the log
- Again, the log stores exact sequence of client command that every server's state machine must execute.
- In a healthy cluster w/ an elected leader every new client command follows a single deterministic path that keeps every server's log identical
- After network partition or leader crash, servers can hold different suffixes of the log. 
Raft does ont live those differences in place, the new leader systematically overwrites or extends every follower's log until it is identical to its own.

## The commit rule
An entry is committed (and therefore safe to apply) only when it is stored on a majority.
*And* at least one entry from the leader's current term is also stored on a majority.

Commit rule = majority + current-term entry on a majority. This is what gives leader completeness and state machine safety.

## How the election works
**Raft is not ring based, it is a leader-based majority-quorum algo**

1. Servers are in one of three states. Follower, leader, candidate. Time is divided into terms, at most one leader in any term.
2. A follower that times out without hearing from a leader becomes candidate. Increments its own term > 
votes for itself >
asks others for votes > 
Becomes leader only if it receives votes from a *majority* of servers AND its *log is as up-to-date as all voters*
3. Note election restrictions and timeouts listed below
4. After leader elected, clients send commands only to leader. The leader appends each command to its own log >
send AppendEntries RPCs to followers
5. Every AppendEntries carries the index and term of the immediately preceding entry. 
A follower accepts and appends only if that preceding entry matches; otherwise it rejects, the leader decrements nextIndex for that follower, and retries. 
On a match the follower truncates any conflicting tail.
6. An entry is committed to log only when it is stored on a *majority* and at least one entry from the leader's current term is also stored on a majority.
The leader advances its commit index and informs followers.
7. Follows commit entries to state machine in order. all servers follow that same order and stay consistent
8. heartbeats = empty AppendEntries. Keeps followers from starting new elections and propegate the last commit index while the leader is idle.

### Election restriction and randomized timeouts.
A candidate becomes leader only when it gets majority votes *and* its log is at least up-to-date as every voter's log.

Election timeouts are drawn uniformly at rnadom. That randomness prevents indefinite split-vote livelocks.

Without the up-to-date restriction, a new leader might not contain a committed entry; the restriction is what gives Leader Completeness.

### AppendEntries consistency check
Each AppendEntries sent to followers contain a "prevLogIndex" and a "prevLogTerm"
- follower rejects if it does not have a matching entry at index/term
If that happens leader decrements "nextIndex" for that follower and retries
- When the preceding entry matches, the follower truncates any conflicting tail and appends the new entries.