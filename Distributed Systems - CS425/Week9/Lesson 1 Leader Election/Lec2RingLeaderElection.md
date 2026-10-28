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
- When that election message is received at a successor:
1. If *attribute* at the successor is lower, forward the message unchanged
2. If *attribute* at the successor is higher then overwrite with own id:attr and forward.
3. If *attribute* is the processess's own ID = this process has the globally highest attribute and becomes the coordinator/leader

### Elected message propagation
The newly elected leader sends out the "elected message" to neighbor. 
Every process that receives the elected message sets its local "elected variable" to the announced id and then FWDs the message.

### Message big O complexity
Best case: 2N total messages when the initiator is the highest. 
Worst case: 3N - 1 messages when the initiator os predecessor of highest attribute. 

### Multiple concurrent initiators are possible by keeping only the highest-initiator run.
- Evens out complexity to O(N)
- Under this multiple initiators architecture, each process caches the initiator of each election/elected message it receives.
- a process will suppress (not send) a message from any lower-id initiators then what's cached. (Can be setup to only the highest-id initiator election run completing)

#### Core
O(N) is the failure-free case through concurrent starts, filtered by initiator ID. 
Liveness: even in worst case, the election will terminate
Safety: even in worst case, every process knows which process is the highest attribute, and that it is the leader.

### Failures during protocol
**Note**: This ring based leader election algorithm is solid *only* under the assumption that there are no failures during the election run. 
Example: If the "would-be" leader crashes after its election message has begun circulating, the elected message may loop forever.
- Could have predecessor or successor keep tabs on each other and if the would-be leader fails, that predecessor/successor starts a new run.
(unreliable since what if the predecessor/successor fails too)
- Could also have the processesss's failure detectors scan for the failure.
- (any process that has received the election message starts scoping failure detector to the would be leader.)
failure detectors can also be incomplete/inaccurate.

**Having every process agree on leader election is largely impossible for the same reason that consensus in general is impossible in distributed systems.**