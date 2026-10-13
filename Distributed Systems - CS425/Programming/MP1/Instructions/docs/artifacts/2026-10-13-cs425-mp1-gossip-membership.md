# CS425 MP1 gossip membership

**Date:** 2026-10-13
**Type:** implementation
**Environment / Systems:** CS425 MP1 simulator in `Distributed Systems - CS425/Programming/MP1` (`g++ -std=c++11 -Wall`)

## TL;DR

Gossip membership is implemented in `MP1Node.h` and `MP1Node.cpp` only. `./Tester.sh` scored 90 out of 90, and the lossy run removed only the node that actually failed. `finishUpThisNode` returns 0 so the existing `int` signature is defined; callers ignore that value.

## Context & Goal

The starter left `recvCallBack` and `nodeLoopOps` empty, so joins were never answered and failures were never logged. The contract was the plan in `Instructions/docs/artifacts/cs425-mp1-gossip-membership.md`: each of 10 simulated nodes keeps one membership list, gossips the whole list every tick, and deletes a row only after its heartbeat has been stale for more than `TREMOVE` (20). The grader scores `dbg.log` lines from `Log::logNodeAdd` and `Log::logNodeRemove`. `submit.py` uploads only the two `MP1Node` files.

The thread started with a request for a function-by-function breakdown and any open questions before coding. There were no open protocol questions. Implementation followed, then a walkthrough of the blocks, then a question about the `return 0` in `finishUpThisNode`.

## Key Points Explored

- `nodeLoop` already receives, then runs `nodeLoopOps` only when `inGroup` is true. `introduceSelfToGroup` already sends `JOINREQ` (header, 6 address bytes, one unused byte, `long` heartbeat) to introducer `1:0`. Those stayed as they were.
- A node logs itself in `initThisNode` via `upsert`. The introducer sets `inGroup` and sends no request. Everyone else becomes a member when `JOINREP` arrives.
- `JOINREP` and `GOSSIP` carry `id`, `port`, and `heartbeat` only. `timestamp` is local and moves only when a heartbeat is strictly greater. `GOSSIP` was added to `MsgTypes` without removing the existing types.
- `nodeLoopOps` increments the local heartbeat, refreshes the self row, erases non-self rows whose age is greater than 20, logs each removal once, then sends the remaining list to every other member. `TFAIL` (5) is unused. Ids go into `MP1Node::removed` (`set<pair<int, short>>`) so a later gossip cannot reinsert them.
- `recvCallBack` frees every `ENrecv` buffer. `finishUpThisNode` does not free `memberNode`; the destructor does that when `shouldDeleteMember` is true.
- `Application::run` calls `finishUpThisNode` after the 700 ticks and discards the return. `nodeStart` also calls it if `introduceSelfToGroup` fails, then `exit(1)`; that join path always returns success in the current sender. Returning 0 does not end either caller. In this tree `SUCCESS` is already 0.

## Decisions & Outcomes

Shipped the protocol from the plan in the two `MP1Node` files. `make clean && make` exited 0 with no warnings.

`./Application testcases/singlefailure.conf` produced 100 unique join pairs. The failed address in that log was `3.0.0.0:0`, with 9 removal lines for it and 0 for anyone else.

`./Tester.sh` printed full marks on all three scenarios and `Estimated overall grade: 90 out of 90` (single failure 10/10 join, completeness, and accuracy; multi failure the same; message drop 15/15 join and 15/15 completeness).

The log `Tester.sh` left behind is `msgdropsinglefailure.conf`. Its failed address was `7.0.0.0:0`, with 9 removals of that node and 0 removals of any other. The failed id comes from `rand`, so these addresses are from those runs only.

## Open Questions / Next Steps

- Coursera upload via `python3 submit.py` was left as a manual step. It needs a fresh token and the student email.
- Progress checkboxes in `cs425-mp1-gossip-membership.md` were not updated.

## Artifacts

- `Distributed Systems - CS425/Programming/MP1/MP1Node.h` — `GOSSIP`, `removed`, private helpers. Implemented.
- `Distributed Systems - CS425/Programming/MP1/MP1Node.cpp` — join, merge, gossip, and one-time removal. Implemented.
- `Distributed Systems - CS425/Programming/MP1/Instructions/docs/artifacts/cs425-mp1-gossip-membership.md` — protocol plan this thread followed. Unchanged; progress boxes still open.
- `./Tester.sh` from the MP1 directory — graded check. Last run: 90/90.
