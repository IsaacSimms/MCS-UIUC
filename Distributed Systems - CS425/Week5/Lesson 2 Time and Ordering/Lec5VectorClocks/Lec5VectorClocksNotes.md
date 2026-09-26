# Vector Clocks: a type of timestamp ordering in distributed systems
- used in key-value stores
- each process uses a *vector* of integer clocks
- suppose there are N processes in a group. 
Each vector at each process is going to have N elements.
Lets say there is process i and process g within that group. the *j*th element of the vector clock at process i is process i's knowledge of hte latest event at process j

## Assigning vector timestamps
- the vector clocks get incremented, simpler to lamport timestamps
- if an operation or send event happens at process i, only the *i*th element of the other processes vector clock is updated.
Each message always carries the send-events timestamp.
The *i*th element in the vector clock gets incremented then the process's vector clock is incremented

**Vector Timestamps obey causality**