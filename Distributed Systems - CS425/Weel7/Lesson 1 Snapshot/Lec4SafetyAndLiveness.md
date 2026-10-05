# Safety and Liveness: two desired properties in distributed systems (detected by global snapshots)

## Two guarantees
Two forms of correctness in distributed systems that are often confused. keep them distinguised.

### Liveness
Means something good will happen eventually
- eventually != bounded time. Running long enough = it happens
- Real world: someone wins the marathon eventually. A criminal is eventually jailed. 
- Distributed system: Computation eventually fails/terminates. Failure detection is complete (every failure is detected). Consensus is sound (every process eventually decides)

### Safety
Means something bad never happens
- Real World: Peace treaty means war never starts. an innocent is never jailed.
- Distributed system: no deadlock, no orphaned object, no broken consensus with two processes deciding on different values.

## Both at once
**Difficult to have both safety and liveness in an asynchronous system**
- Failure detection: completeness (liveness) and accuracy (safety) cannot both be guaranteed.
- Consensus: eventually deciding (liveness) and only correct decisions (safety) cannot both be guranteed as they contradict. (why we see the introduction of eventual liveness)

## Language of global states
System moves from S --> S' only be causal steps

- Liveness of Pr at S: S satisfies Pr, or some causal path from S reaches an S' that satisfies Pr.
- Safety of Pr at S: S satisfies Pr, and every S' reachable from S also satisfies Pr.

## What the snapshot can detect
Stable property: once true, stays true.
Chandy-Lamport detects these because the cut is causally correct. Not because it froze the system.

- Stable liveness: computation has terminated.
- Stable non-safety: a deadlock exists; an object is orphaned (no pointers left)

Detection is one-directional. Snapshot state S* sits causally between the pre-snapshot state and the state when the algorithm finishes.