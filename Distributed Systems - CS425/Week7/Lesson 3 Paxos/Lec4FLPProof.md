# FLP Proof
Revolves around the idea that consensus is impossible to achieve in an asynchronous distributed system.
It is a famous result/paper form the 1980s proving that is the case

## The Theorem
In an synchronous system, no consensus protocol always terminates if even one process may crash. Applies to every protocol. There is always a run of events in an asynchronous distributed system such taht the group never reaches consensus.

## Reason
A crashed proess is indistinguishable from a slow one. Wait for it and you can be stalled forever. Decide without that process and the adversary can still arrange both decisions were reachable. 

## The three terms
Configuration: Global state, process states plus message buffer
Bivalent: Both 0 and 1 are possible to reach.
Univalent: Only one decision is reachable. 

## Proof shape
some initial configuration is bivalent. For any bivalent config another bivalent config is also reachable. Possible that the delivery that would have decided is delayed due to failure, network partitions, etc. and that would cause an infinite run with no decision being made. 

It odes not forbid safety but does forbid guaranteed termination. It assumes asynchrony, since the synchronous f + 1 algo escapes due to stop-crash. 
