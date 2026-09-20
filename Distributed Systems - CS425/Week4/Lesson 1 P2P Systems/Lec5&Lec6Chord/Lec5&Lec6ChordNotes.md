# Chord (first P2P system designed from academia) 
This like hash tables are widely used in a variety of cloud computing architectures such as NoSQL Stores

## Distributed Hash Table
- Allows you to insert, lookup, and delete objects (files) within a dataset using keys
- A distributed hash tables is the same thing in a distributed setting

- Need to worry about things like load balancing, fault-tolerance, locality, efficiency
- previously discussed P2P systems are an unstructured distributed has table in a way (O(N) efficiency wth things like look latency)
- Chord is a structured P2P system (directly addresses efficiency with insert, lookup, delete) (O log(N) for things like memory, look latency)

## Chord
- Berkeley and MIT
- Nodes in the system select neighbors for a variety of tasks in an intelligent fashion. (certian rules)
- Uses consistent hasing on the node's address
    Peer's IP address and port number has a hash function applied to it, which creates a string.
    that is truncated to m bits, which becomes the peer id.
- Peers map to one of 2^m logical points on a circle. This creates a (ring of peers)
    Every peer knows its immediate clockwise successor in the ring

### Finger  table
- You can also use a **finger table**. Every node keeps a table with n + 2^i values in it. That is used to navigate to the next peer
    See "Distributed Systems - CS425/Week4/Lesson 1 P2P Systems/Lec5&Lec6Chord/FingerTables.png"
    "In a Chord P2P system with m=8, a peer with id 33 is considering the following peers for its i=3 finger table entry: 40, 42, and 44. Which one is the best (correct) choice?"
    33 + 2^3 = 41. That is the start, not the first successor peer. Meaning, 42 is the answer.

### How files get placed
- file names are mapped using the same, consistent has function
- file is stored (mapped on to point in the ring) at first peer with an ID greater than or equal to its key (which is mod 2^m).
- Let's say every slot in the ring is a "locker". Lets' say a file is given to a random locker via Unifrom hash. Whoever owns the next peer clockwise from that locker keeps the file.
    The more lockers there are between the two peers, the more data the peer that is clockwise in the rotation will hold.
- Similar logic holds up for routing queries around the ring/finger table

Note with consistent hashing: with K keys and N peers, each peer stores O(K/N) keys.

### Analysis
- Search takes O(log(N)) time
    at each step, distance between the query and peer with the file reduces by a factor of 2


## Failures in Chord (what happens, how it is accounted for)
- Remember, nodes are making specific hops via their finger tables to do things like query. Nodes only know about the handful of peers in their finger table.
    In chord, the query is only going to get handed to the key/node that gets you closest to the key you want without going past it.
    If a node is not in its finger table it does not know that key/node exists. 
    It will do specific hops to get to the node (or closest nearby) that is possible.
If a node is trying to route a query to a specific key, it does not know about those other nodes that it needs to hop though, that do not exist in its finger table. 
- To fix this, nodes do not maintain just successor entires.  they also maintain r, which is multiple successor entries
    r = 2log(N) in order to maintain lookup correctness
- Failure detector used to diagnose failed nodes. 
- THe peer that is storing the file which is being looked for is another failure. 
    To combat this, multiple copies of a file are stored at multiple nodes
    File is stored at successors and predecessors
    This also creates a load balancing behavior, where more then one node can satisfy a query

### High churn
Need to keep finger tables updated

#### new peers joining
Introducer node using DNS. The DNS server gives the new node an IP address of some node in the system.
That is used by the new node to figure out its own ID and place within the system, and then it routes itself to the new successor node that the DNS server has defined.
    New node uses the finger table of the node that is has been communciating with to initialize its own finger table.
    Some locker keys are copied over, because the ring values have shifted.
A stabilization protocol periodically runs at every node in the system. This forces finger table updates to current state, reducing the effects of churn.

#### peers leaving
Same behavior and architecture as a node failing

#### Stabilization protocol
- Important bc of concurrent peer join, leaves and failures causing loopiness of pointers and failure of lookups
    Loopiness means that the queries would just loop around forever due to being unable to hop to a node that is in the finger table but failed/left
- Checks for and updates pointers & keys
- Every node runs this
- Involves a constant number of messages
- strong stability = O(N^2) stabilization rounds