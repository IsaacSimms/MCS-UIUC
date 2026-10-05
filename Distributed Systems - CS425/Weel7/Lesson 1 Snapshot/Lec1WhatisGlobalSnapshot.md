# What a global snapshot is how to calculate it, what it captures


## Definition
- **A representation of the global state of a distributed system**
- local state of each process + every channel's in-transit messages (sent but not yet received)
- *instantaneous* at each process and channel
- Syncing clocks and sampling at time t does not work due to syncing issues and clock error missing causality

## why it exists
- checkpointing: restart after failure from saved global state
- garbage collection: detect and remove objects with no pointers from any server
- deadlock detection: wait-for cycle across machines that is hung, detect and remediate
- termination detection: confirm patch jobs (Folding@home, SETI@Home) have finished

## Why "Sync clocks, record at time t" fails
- sync always has no zero amount of error. 
- does not record channel state.
- does not capture causality

## State
Any event changes effects the global state. This includes:
- send
- recieve
- local step

Translations obey causality. Snapshot taken on every execution in the series of steps (causal path) that the system is taking as it completes any sort of action.