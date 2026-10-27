# Ring based leader election

## The N processes are organized into a logical Ring
- The ring is unidirectional (similar to a Chord ring)
Each process has exactly one successor.
- all messages are sent clockwise around the ring
This includes election and elected messages.
- the i-th process p_i has a communcation channel: p_(i + 1) mod N

## The ring election protocol
**Key note: election message carries the best attribute seen so far from successor to successor. The Elected message is the propagation of the result**

### Flow
- any process which detects the old leader has failed (or randomly decides to start an election) send the initial election message. 
That message contains its id: *attribute*
(attribute being whatever is being used to decide the leader)
- When that election message is recieved at a successor:
1. If *attribute* at the successor is lower, forward the message unchanged
2. If *attribute* at the successor 