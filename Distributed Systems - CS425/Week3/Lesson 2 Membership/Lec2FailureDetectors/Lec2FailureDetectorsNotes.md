## remember
Scalability is a must with membership lists
Many processes are all running the protocol and communciating over an inherently unreliable network
When one process crashes:
    Other proceses need to be able to detect that crash
    update their membership list accordingly
    communicate that information to other p

## failure detection terms
completeness = every failure is detected
accuracy     = there is no mistakes in that detection (false positives)
speed        = time to first detection of a failed process (we want it to be as small as possible, responsive)
scale        = load on each member process (load balanced) and network message load (low overall network node) (avoid single points of failure/bottlenecks)
heartbeat    = a sequence number used to represent the aliveness of a process. Incremented locally
    One process receives heartbeats from a different heartbeat. when heartbeat is received, it increments the sequence number. If heartbeat is not received, the number isn't updated. 
        If that happens for long enough the sending process is marked as failed. 

impossible to make a 100% accurate and 100% complete failure detection system
    especially true under the network bound nature of distributed systems
    Modern distributed systems take a tradeoff:
        100% complete failure detection (any failed process is detected) at the cost of accuracy (you get false positives)
        Not detecting a failed process is a huge loss. Lost or corrupted data, poorly performing applications, etc.

## Centralized heartbeating
A central process (pj) receive a heartbeat from many spoke processes (pi). If pi fails to do its heartbeat, mark it as failed.
    This is complete failure from the perspective of all processes - pj
    But, no good detection method on knowing when pj failures, and pj becomes an overload hotspot/bottleneck

## Ring heartbeating
Every process in the system is orchestrated into a ring topology
    each process sends a heartbeat to one or more of its neighbors
    quality of heartbeats and detection is the same.
Avoids the bottleneck issue of centralized heartbeating but is weak in that unpredictable and/or simultaneous failure of multiple nodes can go undetected.

## All-to-All heartbeating
Every process send out a heartbeat to all other process in the system
The load is high, but it is load balanced accross the system
The completeness is the best but you may get a lot of false positives, largely due to network inconsistencies.
The most preferred option out of the three presented 