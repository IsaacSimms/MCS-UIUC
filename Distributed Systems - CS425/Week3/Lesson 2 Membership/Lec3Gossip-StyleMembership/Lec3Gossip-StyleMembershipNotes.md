# How gossip-style failure detection works
It is a form of all-to-all heartbeating

All-to-all heartbeating as discussed in the previous lecture, but with improvements to get gains in accuracy

## Gossip-style failure detection
Each node hold a membership list
    Each process has a list that contains a row for every other process in the system, as this is a all-to-all heartbeat topology
    each row in the list has three columns. The address (which node is this row for), the heatbeat counter, and time (local time that heartbeat counter was last updated).
each node periodically gossips their membership list to a few of its neighbor nodes in the system. Upon receipt, the local membership list for each node is updated.
    When the list from a neighbor is received, it merges that list row by row. If the list from the neighbor has a heartbeat counter that is larger then what it has, it takes that new metric. (and time)

There is a defined threshold for timing out.(known as T_fail) If a row's timer surpasses that threshold, mark that process as having failed. 
    However, don't delete that process immediately. wait a defined number of seconds before deleting that member from the list (known as T_cleanup)
        This is done to prevent edge cases where proccess will keep deleting failed processes out of their membership lists and then adding the failed process back as a new process from neighbor nodes over and over. 

## analysis
T_gossip is the protocol period, the fixed time in which each node runs a gossip
- A single heartbeat period takes O(log(N)) time to propogate as long as there are no bottlenecks such as network
- The amount of time it takes the heartbeat to propagate is inversely proportionate to bandwidth allowed
- If T_gossip is decreased you get a higher bandwidth (same amount of things happening in a shorter period of time)
    dissemination is faster and detection time drops
    **T_gossip is a tradeoff between detection time and bandwidth**
- If T_fail and T_cleanup are increased you get longer detection times but better accuracy
- 