# Paxos: an answer to the consensus problem in asynchronous distributed systems

## What paxos claims/solves (not actually solving consensus)
- Safety: consensus is not violated. No two decisions.
- Eventual liveness: if messages and failures are well behaved sometime in the future, a decision is likely. No bound. No guarantee.
- FLP is intact. A failed process is still indistinguishable from a slow one, so a round can be stalled forever.

## Round mechanic
- Rounds are asynchronous with no clock sync.
- each round has a unique ballot id
- If you are in round j and hear round j+1, abort and move to j+1. Timeouts are allowed and may be pessimistic (false leader death).
- Each round is broken into phases

## Rounds
### Phase 1 - election
Potential leader is chosen and picks a ballot id higher then anything else it has send. sends it to all. (multiple leaders are allowed).
- If potential leader sees a higher ballot id, it cant be leader
- Processes log received ballot ID on disk.
- If quorum is reached on who the leader is, then that processes is the leader. (it has already accepted a value v' in an earlier round, the reply carries v'.
Majority of OKs ⇒ you are the leader. No majority ⇒ start a new round.)

### Phase 2 - Bill
- Leader send proposed value v to all.
- If any Phase 1 reply carried a prior accepted v', propose that v'. Do not invent a new value over an accepted one.
- Recipient logs the proposal on desk and replies ok.

### Phase 3 - Law
- Leader waits and hears a majority of OKs. Once confirmed, it lets everyone know the decision.
- This decision is logged on desk and decision variables are set to this.

### No return
means the point in the phases when the value is guaranteed to be what is decided, even if all processes where to fail. Right around the end of bill phase and beginning of law phase. 

## Why safety is guranteed
If some round is able to get quorum on proposed value and accepting it (no-return) then subsequently at each round either: that round chooses the value or the round fails.

## Failures
- Process crash: a majority need not include it. On restart, the log supplies the last ballot and any accepted value.
- Leader fails: another round starts
- message drops: if round is flaky then the round will restart
- protocol may get stuck in a never ending loop under a flaky system (impossibility result not violated but if things go well in the future, consensus reached)