# Classical algorithm used to calculate global snapshot in a distributed system (Chandy-Lamport)

## Definition/TLDR
Any process can start it. Records itself, then sends a marker on every outgoing channel and starts logging incoming app messages.
- Marker is not an app message; on a FIFO channel it is a separator
- First marker a process sees = record itself, that channel is now empty, same flood markers go out, start logging incoming app messages again.
- If/when another marker hits that channel: close it. Channel state = app messages that arrived after logging marker started and before last marker.
- Done is considered when every process has recorded every channel and has been closed by a marker.

## System model (required)
- N processes
- Between each ordered pair, two uni-directional channels: Cij = Pi → Pj
- FIFO inside a channel. No cross-channel order.
- No failures. Messages arrive intact, once, not dropped.
Later papers relax these. This lecture does not.

### Requirements
- Snapshots dont iunterfere with normal application actions or require apps to stop operating
- every app is able to record its own state (application defined process state, heap registers, program counter, etc.)
- global state collected in distributed manner
- Any process can initiate the snapshot

## Rules/Flow
### Initiator Pi
- records its own state
- send marker on every outgoing C_ij ((N - 1) channels)
- Start recording app messages on every incoming C_ji
  

### On receiving a marker on incoming channel
#### First marker that process has seen
- record own state
- mark that channel as empty
- send marker on every outcoing channel
- start recording every incoming channel
#### Not first marker   
- State of channel (C_ki in this example) = app messages recorded on channel since recording was turned on
- stop recording

## Example the lecture walks
3 processes. P1 initiates, records S1, Markers out, recording on C21 and C31.
- P3’s first Marker (on C13): record S3, C13 = ⟨⟩, record C23, Markers out.
- P1’s later Marker on C31: C31 = ⟨⟩.
- P2’s first Marker: record S2, that arrival channel empty, record the other incoming, Markers out.
- One channel stays non-empty: C21 = ⟨message G→D⟩. Everything else empty.
Final snapshot = {S1, S2, S3} plus those six channel states. Algorithm has terminated; collector just gathers pieces.

## What to retain
- Marker = FIFO fence, not app data.
- Record on first Marker, not on a clock.
- Channel state is the gap between “I started recording this channel” and “Marker arrived on it.”
- Empty on the channel that delivered your first Marker is the FIFO invariant, not a special case.
- Correctness (“this is a consistent cut”) is the next lecture, not this one.