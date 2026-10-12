---
title: CS425 MP1 gossip membership
status: ready
updated: 2026-10-12
project: Distributed Systems - CS425/Programming/MP1
---

# CS425 MP1 gossip membership

## TL;DR

Implement gossip-style membership in `MP1Node.cpp` and `MP1Node.h` only. Each of the 10 simulated nodes keeps one local list with one row per member, sends that whole list to every other known member every tick, and deletes a row only after its heartbeat has been stale for more than 20 ticks. The finished program must make `./Tester.sh` print `Estimated overall grade: 90 out of 90`, and the lossy run must not `logNodeRemove` any node that did not actually fail.

## Problem Statement

The starter at `Distributed Systems - CS425/Programming/MP1/` simulates a 10-node cluster on one process. `Application` is the driver, `EmulNet` is the network, and `MP1Node` is the membership layer. `JOINREQ` is already sent to the introducer `1.0.0.0:0`. `recvCallBack` and `nodeLoopOps` are empty, so no node answers a join, no membership list is maintained, and no failure is ever logged.

The grader reads `dbg.log` lines produced by `Log::logNodeAdd` and `Log::logNodeRemove`. Those lines appear only if this implementation calls them. `submit.py` uploads only `MP1Node.h` and `MP1Node.cpp`. Every other source file is replaced on the grader, so behavior has to come from those two files.

## Requirements

Functional:

1. After a run of `testcases/singlefailure.conf`, `testcases/multifailure.conf`, and `testcases/msgdropsinglefailure.conf`, every node has called `logNodeAdd` for all 10 members, including itself. The grader's join count is 100 unique `(observer, joined-node)` pairs.
2. On `singlefailure.conf`, the other 9 nodes each call `logNodeRemove` exactly once for the one node that failed at t=100, and for nobody else.
3. On `multifailure.conf`, five nodes fail at t=100. Each of the five survivors calls `logNodeRemove` exactly once for each of those five nodes, and for nobody else. The grader's per-failure accuracy count is exactly 20 removal lines that do not name that failed address.
4. On `msgdropsinglefailure.conf`, joins and failure completeness still meet requirements 1 and 2 while 10% of sends are dropped from t=50 through t=300. No surviving node calls `logNodeRemove` for a node that did not fail.
5. A new peer joins by `JOINREQ` / `JOINREP`. `JOINREP` contains every member the introducer knows at the moment it replies.
6. After a node is in the group, each tick updates only that node's own heartbeat, then sends every current row to every other current member.
7. A received row is applied to the receiver's own list. A new id is inserted and logged once. A strictly greater heartbeat replaces the stored heartbeat and sets `timestamp` to the receiver's current `globaltime`. An equal or lower heartbeat does not change the row.
8. A row whose `globaltime - timestamp` is greater than `TREMOVE` (20) is erased, `logNodeRemove` is called once, and that id is never inserted again during the run.
9. `recvCallBack` and `nodeLoopOps` perform the work above. `nodeLoop` already calls them and must keep that order.

Non-functional:

10. The project builds with the existing Makefile (`g++ -std=c++11 -Wall`). No new translation unit.
11. A gossip or `JOINREP` payload for 10 members stays far under `MAX_MSG_SIZE` (4000).

## Constraints

- Edit only `Distributed Systems - CS425/Programming/MP1/MP1Node.cpp` and `MP1Node.h`. Do not edit `Application`, `EmulNet`, `Log`, `Member`, `Params`, `Makefile`, `Tester.sh`, `submit.py`, or any `.conf` file.
- `submit.py` zips only `MP1Node.h` and `MP1Node.cpp`. Helpers, the removed-id set, and any new message type live in those two files.
- Leave `TFAIL` at 5 and `TREMOVE` at 20. Do not use `TFAIL` as a delete time or as a reason to stop sending. Suspicion is "still in the list, still gossiped." Removal is only `age > TREMOVE`.
- `finishUpThisNode` stays a no-op. Its body is `return 0;` so the existing `int` signature is defined. Do not free `memberNode` there. The destructor already does that when `shouldDeleteMember` is true.
- Do not add a `LEAVE` message. `Application::fail` only crash-stops a node by setting `bFailed`. A failed node never runs `recvLoop` or `nodeLoop` again and never rejoins.
- Do not change the `JOINREQ` bytes that `introduceSelfToGroup` already writes. Parse them with the same offsets.
- `Log::logNodeAdd` / `logNodeRemove` are the only join/remove logs the grader counts. Do not invent a second log string for those events.
- Emulator facts the logic depends on:
  - `EN_GPSZ` is `MAX_NNB` from the conf file. All three graded confs set `MAX_NNB` to 10.
  - `TOTAL_RUNNING_TIME` is 700. `STEP_RATE` is 0.25. Node `i` is started when `globaltime == (int)(0.25 * i)`, so every node has been started by t=2.
  - Each tick, `mp1Run` receives first (every live node), then runs `nodeStart` or `nodeLoop`. A message sent at time t is received at time t+1. There is no extra delay.
  - `fail()` runs after `mp1Run` in the same tick. A node that fails at t=100 still executes `nodeLoop` at t=100, then never runs again. Its last gossip is sent at t=100 and received at t=101.
  - `DROP_MSG` 1 makes `Application::fail` set `dropmsg` from t=50 through t=300. Each `ENsend` is then dropped independently with probability `MSG_DROP_PROB` (0.1). Dropped sends return 0 and are gone.
  - `ENsend` also drops the message when `size + sizeof(en_msg) >= MAX_MSG_SIZE` or the buffer is at `ENBUFFSIZE` (30000). Ten full-list messages a tick are nowhere near either limit. Messages addressed to a failed node sit in the buffer until `ENcleanup` because that node no longer receives. Sending to a dead node for about 20 ticks, not for the rest of the run, stays far under the buffer cap.
  - Addresses are 6 bytes: `int` id in bytes 0–3, `short` port in bytes 4–5, which is what `ENinit` and `Address::getAddress` use. Node ids are 1 through 10, port 0. The introducer is id 1 (`getJoinAddress` / `Application::getjoinaddr`). On this little-endian host the log text is `1.0.0.0:0` through `10.0.0.0:0`. Build `Address` values with `memcpy` of the id and port. Do not parse dotted quads.
  - `MemberListEntry` already stores `id`, `port`, `heartbeat`, and `timestamp`. Use it. Do not modify `Member.h`.
  - The removed-id set is a field of `MP1Node`, not of `Member`, because `Member.h` is replaced by the grader.
  - `checkMessages` passes each queued buffer to `recvCallBack` and does not free it. `ENrecv` allocated that buffer with `malloc`. `recvCallBack` must `free(data)` on every return path.
  - `nodeLoop` returns immediately when `bFailed`. It always drains messages. It calls `nodeLoopOps` only when `inGroup` is already true. `JOINREP` handling runs inside `checkMessages`, which is before `nodeLoopOps` in the same call, so the joiner can gossip on the tick it becomes a member.
  - `DEBUGLOG` stays on. Do not wrap `logNodeAdd` or `logNodeRemove` in new conditions.

## Key Decisions

> **Decision:** Gossip-style membership. Each node holds one list of `(id, port, heartbeat, local timestamp)` and merges by strictly greater heartbeat.
> **Rationale:** This is the protocol the course builds `TFAIL` / `TREMOVE` for, and it is what the 90-point tests exercise.
> **Alternatives considered:** All-to-all heartbeats with no membership payload. SWIM ping / indirect ping.

> **Decision:** Done means `./Tester.sh` reports 90/90, and a live node is not removed during the 10% drop window.
> **Rationale:** The writeup requires completeness under loss and high accuracy under loss. `Tester.sh` scores joins and completeness on `msgdropsinglefailure.conf` and does not score accuracy there. The 10% probability and the t=50–300 window come from that conf plus `Application::fail`, not from a separate sentence that names "10%".
> **Alternatives considered:** Treating a green `Tester.sh` as enough even if live nodes are deleted while drops are on.

> **Decision:** Every tick, send the full current list to every known member except self.
> **Rationale:** N is 10, so this is about 90 small messages per tick. A direct send each tick makes five or twenty consecutive drops vanishingly rare, which keeps `TFAIL` 5 and `TREMOVE` 20 valid under the lossy test. The per-node list is the protocol, not extra state. One row per member is a few hundred bytes.
> **Alternatives considered:** One random peer per tick. Two random peers per tick. Both need a longer timeout to avoid false removals, and both were rejected after the lossy accuracy bar was set. Nested lists (a copy of every other node's full list) were rejected. The list that is written is always the receiver's own list.

> **Decision:** Keep a stale row in the list and in outgoing gossips until `globaltime - timestamp > 20`. Call `logNodeRemove` only then, once.
> **Rationale:** Deleting at `TFAIL` lets a later gossip insert the dead node again and log a second removal. The multi-failure check wants exactly one removal line per survivor per failed node. The 15 ticks between 5 and 20 are the wait before delete. Own heartbeat is refreshed every tick, so the local row's age stays 0.
> **Alternatives considered:** Delete and log as soon as age exceeds 5. Treat `TREMOVE` as an extra 20 ticks on top of `TFAIL` (delete at 25). Skip sends to anyone already older than `TFAIL`.

> **Decision:** `JOINREP` carries every member the sender currently knows, not a fixed-size subset and not a hardcoded list of 10.
> **Rationale:** Ten entries fit in one message. The joiner logs those members immediately. Anyone not yet in the introducer's list arrives on a later gossip, which is required because several nodes start on the same tick and their `JOINREQ`s are only received on the next tick.
> **Alternatives considered:** A partial introducer list.

> **Decision:** Gossip and `JOINREP` entries on the wire are `id`, `port`, and `heartbeat` only. `timestamp` is local and is set to `par->getcurrtime()` only when this node inserts the row or accepts a strictly greater heartbeat. Ids that have been removed are ignored for the rest of the run.
> **Rationale:** The time column is the local time of the last heartbeat change. Copying a timestamp off the wire, or refreshing it when the heartbeat did not increase, resurrects a dead node. The simulator never restarts a crashed process, so a removed-id set is safe and is what keeps the removal count exact.
> **Alternatives considered:** Putting `timestamp` in the message and rejecting unknown ids whose timestamp is already older than `TREMOVE`.

> **Decision:** Scope of this pass is the membership protocol in the two `MP1Node` files. Coursera upload is a later manual step.
> **Rationale:** `submit.py` needs a fresh Coursera token and the student's email. Those are not part of the protocol design.
> **Alternatives considered:** Including submission in the implementation phases.

## Deferred

- Coursera submission via `python3 submit.py`.
- Voluntary leave. The simulator never sends one.
- Fanout of 1 or 2, and any retuning of `TFAIL` / `TREMOVE` that those fanouts would require.
- SWIM, and all-to-all heartbeats that carry no membership list.
- The CRUD confs named in `README.md`. They are not part of `Tester.sh` and the files are not in `testcases/`.

## Implementation Phases

### Phase 1 — Join and gossip merge

**Objective:** Every live node inserts all 10 members into its own list and logs each insert once. Failure deletion is not in this phase.

**Tasks:**

1. In `MP1Node.h`, add `GOSSIP` to `MsgTypes` without removing `JOINREQ`, `JOINREP`, `UPDATEREQ`, or `UPDATEREP`. Add a private `std::set` of removed `(id, port)` pairs (`#include <set>`). Declare private helpers for address conversion, upsert, serialize-and-send, and the three message handlers. Keep the existing public method signatures.
2. In `initThisNode`, after `initMemberListTable`, insert this node into `memberList` with `memberNode->heartbeat` and `timestamp = par->getcurrtime()`, then call `log->logNodeAdd` once for self. Do this for every node, including the introducer.
3. Leave the `JOINREQ` send in `introduceSelfToGroup` byte-for-byte as it is. The layout is `MessageHdr`, then 6 address bytes, then one unused byte, then `long` heartbeat. `msgsize` is `sizeof(MessageHdr) + 6 + sizeof(long) + 1`.
4. Implement `recvCallBack`. Read `msgType` from the front of `data`. `free(data)` before every return. Ignore `env` and use `memberNode`. Return `true` after a handled message.
5. `JOINREQ` handler: copy the address from offset `sizeof(MessageHdr)` and the heartbeat from offset `sizeof(MessageHdr) + 6 + 1`. Upsert that member. Send a `JOINREP` of the current list back to that address.
6. `JOINREP` handler: set `memberNode->inGroup = true`. Upsert each packed entry. Do not clear the list first. Self is already present, so self is not logged a second time.
7. `GOSSIP` handler: upsert each packed entry. Do not change `inGroup` here.
8. Upsert rules: if `(id, port)` is in the removed set, do nothing. If a row exists and `incoming heartbeat > stored heartbeat`, store the heartbeat and set `timestamp` to `par->getcurrtime()`. If a row exists and the heartbeat is not greater, do nothing. If no row exists, push a `MemberListEntry` with `timestamp = par->getcurrtime()` and call `logNodeAdd` once.
9. Serialize `JOINREP` and `GOSSIP` with a cursor, not a struct array. Layout: `MessageHdr`, then `int` count, then count records of `int id`, `short port`, `long heartbeat` packed back to back. Use `sizeof` for each field so the reader and writer share one layout. `malloc` the buffer, `ENsend` it from `memberNode->addr`, then `free` it.
10. `nodeLoopOps` for this phase: increment `memberNode->heartbeat`, upsert self with that new heartbeat so the local timestamp becomes `globaltime`, then `ENsend` the full current list to every other row. Do not send to self. Do not delete anyone yet.
11. Unknown message types are ignored.

**Acceptance criteria:**

- `make clean && make` from `Distributed Systems - CS425/Programming/MP1` exits 0.
- `./Application testcases/singlefailure.conf` exits 0.
- This check prints 100:

```bash
grep joined dbg.log | cut -d" " -f2,4-7 | sort -u | wc -l
```

Failure-removal lines may be absent. That is expected until Phase 2.

### Phase 2 — Delete stale members once

**Objective:** Survivors log each real failure once and never log anyone else. This is the graded completeness and accuracy behavior.

**Tasks:**

1. In `nodeLoopOps`, after refreshing self and before sending, scan every non-self row. If `par->getcurrtime() - timestamp > TREMOVE`, call `logNodeRemove` once, insert `(id, port)` into the removed set, and erase the row. Then send the list that remains.
2. Compare timestamps as integers. A self row refreshed in task-order of Phase 1 step 10 has age 0, so it is not removed. Still skip self explicitly.
3. Do not call `logNodeRemove` if the id is already in the removed set. Insert into the set in the same step as the erase.
4. Leave rows with `TFAIL < age <= TREMOVE` in the list and in the outgoing payload, and still send to those addresses.
5. Do not refresh `timestamp` when applying a gossip whose heartbeat is not strictly greater. That is what allows age to reach 20 after a node stops sending.

**Acceptance criteria:**

- From `Distributed Systems - CS425/Programming/MP1`, `./Tester.sh` prints `Estimated overall grade: 90 out of 90`.
- The three scenario lines each show full marks: single failure 10/10 join, 10/10 completeness, 10/10 accuracy; multi failure 10/10 join, 10/10 completeness, 10/10 accuracy; message-drop 15/15 join, 15/15 completeness.

### Phase 3 — Lossy-run accuracy

**Objective:** Confirm the bar `Tester.sh` does not score: during the 10% drop window, removals name only the node that actually failed.

**Tasks:**

1. `./Tester.sh` leaves `dbg.log` from the last scenario, `msgdropsinglefailure.conf`. If that log was overwritten, rerun only `./Application testcases/msgdropsinglefailure.conf`.
2. Read the single failed address from `Node failed at time` lines (`awk` field 1, the log line starts with a space). Count `removed` lines that do not contain that address, and `removed` lines that do.

**Acceptance criteria:**

- The failed-address extraction yields one address.
- Unique `removed` lines that do not contain that address: 0.
- Unique `removed` lines that contain that address: at least 9.
- `./Tester.sh` still prints `Estimated overall grade: 90 out of 90`.

## Progress

- [ ] Phase 1 — Join and gossip merge
- [ ] Phase 1 — `make clean && make` exits 0
- [ ] Phase 1 — join pair count is 100 on `singlefailure.conf`
- [ ] Phase 2 — Delete stale members once
- [ ] Phase 2 — `./Tester.sh` prints 90 out of 90
- [ ] Phase 3 — Lossy log has zero removals of non-failed nodes and at least 9 removals of the failed node

## Testing Strategy

Run everything from `Distributed Systems - CS425/Programming/MP1`. The graded command is `./Tester.sh`. It recompiles, runs the three confs, and overwrites `dbg.log` on each run. `./Tester.sh -v` shows compiler and program output.

Join lines look like ` 1.0.0.0:0 [t] Node 2.0.0.0:0 joined at time t` because `Log::LOG` writes a leading space. `cut -d" " -f2` is the observer. That is why the Phase 1 check uses fields 2 and 4–7.

Removal lines contain the word `removed` only when `logNodeRemove` was used. The multi-failure accuracy check is `sort -u` on the whole line, and the line includes `removed at time %d`, so two removals of the same pair at different times count as two lines and the score drops. One log per pair is required, not "at least one".

The failed node is chosen with `rand` and differs across runs. Checks must take the failed address from `dbg.log`. Do not hardcode an id.

There is no unit-test harness. Do not add one in another file. The acceptance commands above are the tests.

## Rollback / Risk Notes

- Reverting `MP1Node.cpp` and `MP1Node.h` returns the tree to the starter.
- The easy way to fail multi-failure accuracy is a second `logNodeRemove` for the same pair, or a removal of a live node. The removed-id set and the "strictly greater heartbeat" rule exist to prevent that.
- Refreshing `timestamp` on an unchanged heartbeat makes failures invisible and completeness stays 0.
- Parsing `JOINREQ` without the extra byte reads the heartbeat from the wrong offset and can insert a garbage member, which then fails accuracy.
- Leaking `recvCallBack` buffers will not by itself fail the grader, but freeing them is part of this contract because `ENrecv` mallocs a buffer per message for 700 ticks.

## Reference Files

- `Distributed Systems - CS425/Programming/MP1/MP1Node.cpp` — `introduceSelfToGroup` `JOINREQ` layout, empty `recvCallBack` and `nodeLoopOps`, `nodeLoop` call order.
- `Distributed Systems - CS425/Programming/MP1/MP1Node.h` — `MsgTypes`, `TFAIL`, `TREMOVE`.
- `Distributed Systems - CS425/Programming/MP1/Member.h` — `Address`, `MemberListEntry`, `Member::memberList`.
- `Distributed Systems - CS425/Programming/MP1/Application.cpp` — `mp1Run` receive-then-send order, `fail()` at t=100 and the drop window.
- `Distributed Systems - CS425/Programming/MP1/EmulNet.cpp` — one-tick delivery, drop condition, `MAX_MSG_SIZE` check.
- `Distributed Systems - CS425/Programming/MP1/Log.cpp` — `logNodeAdd` / `logNodeRemove` text and the leading space on each `dbg.log` line.
- `Distributed Systems - CS425/Programming/MP1/Tester.sh` — the 90-point checks.
- `Distributed Systems - CS425/Programming/MP1/testcases/singlefailure.conf`
- `Distributed Systems - CS425/Programming/MP1/testcases/multifailure.conf`
- `Distributed Systems - CS425/Programming/MP1/testcases/msgdropsinglefailure.conf`
- `Distributed Systems - CS425/Programming/MP1/submit.py` — uploads `MP1Node.h` and `MP1Node.cpp` only.
- `Distributed Systems - CS425/Programming/MP1/Instructions/InstructionsCloudComputingConcepts.md` — assignment writeup.

## Cold-start

Read `Distributed Systems - CS425/Programming/MP1/Instructions/docs/artifacts/cs425-mp1-gossip-membership.md` and continue from the plan. Honor Constraints and Key Decisions; do not re-open them. Start at the first incomplete Progress item. Confirm only if Open Questions block progress. This file alone is not permission to edit code. Wait until the user asks to implement or continue.
