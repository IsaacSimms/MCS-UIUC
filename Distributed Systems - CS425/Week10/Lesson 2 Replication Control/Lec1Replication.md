## Replication control in distributed systems

## Definition
How to handle operations (or transactions) when there are *objects that are stored at multiple servers, with or without replication*

Replication = Maintaining identical copies of an object, each hosted by a separate servers (copies known as replicas)
Done so System/data/objects survive failures, load balancing, offering high availability, scale. 
Clients still need to see a single logical copy. (For transparency and consistency)

### expanded on

- Fault-tolerance: k replicas tolerate failure of any $k-1$ servers.
- Load balancing: read/write operations are spread across the k replicas, lowering per-replica load by roughly a factor of k.
- Higher availability is the direct result.

### Availability arithmetic
If each server is down for a fraction of time (f), that object is only on that one server, then the time in which the object is reachable is associated directly with f. (1 - f)
However, the reachable timeframe rises sharply once you have more then one copy of that object. (1 - f^k)


## Two properties that must hold here
Clients should not notice that copies exist, and every client should observe the same logical state.
This is the main challenge of getting replication control in distributed systems right.

1. Replication transparency: A client shouldn't be aware of multiple copies server side. (hidden via frontend)
2. Replication consistency: All clients must see a single consistent copy of the data. (remember ACID for transactions)

## Passive vs active replication
Updates can be distributed/ordered by a single leader server or by making every replica server the same ordered stream
Both approaches rest on replicated state machines

- Passive: All updates go to *one leader* that totally orders those updates. 
Leader failure = leader election for new leader
- Active: Every replica is treated identically within the system. Updates are multicasted inside the replica group.
Total ordering + virtual syncrony makes every correct replica apply the same sequence. 


