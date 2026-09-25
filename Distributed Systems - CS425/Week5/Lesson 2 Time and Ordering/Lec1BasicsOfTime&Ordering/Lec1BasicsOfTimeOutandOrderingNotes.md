# Time out and ordering Basics: Time in distributed systems
## Why you need synchronization
Distributed systems often times need to "arrive on time for the bus" to early, you wait for to long. (a violation of fairness) To late, you miss the "bus". (a violation of correctness)
Remember, through logs that are timestamped and timestamped operations are essential to many distributed systems. Servers are always reading and taking action based on the timestamped logs of other servers. 
If the internal clocks are out of sync, servers will get confused on when things happen and what should happen next, causing systemic issues across the system. 

## Why its challenging
- Each server has its own clock and its not a viable solution to have them share
- Processes in Internet-base systems follow asynchronous system model
    Meaning no bounds on message delays or processing delays.

## Definitions
- Asynchronous distributed system consists of a number of processes
- each process has a state (values of variables)
- each process takes actions to change its state (such as send/receive)
- Each process has its own execution clock.

however, something we need to do in distribute systems is order processes accross systems.

## Clock skew vs clock drift
remember each process (running on a host) has its own clock. When you compare two clocks from two different processes:
- Clock Skew = relative difference in clock values from two processes (the spacial difference between two cars on a road at a given time)
    Non-zero clock screw means the clocks are not synchronized
- Clock drift = relative difference in the clock frequencies of two processes (the different speeds of those two vehicles on a road)
    non-zero clock drift causes clock screw to increase

## Synchronization
Bringing clocks to the same value

How often do you want to do this? Depends on the maximum drift rate (MDR) of the clock. 
Absolute MDR is defined the processes time relative to UTC.
The max drift between two clocks is 2 * MDR (one clock could be ahead the other could be behind)
Given that M is the defined maximum acceptable skew, the clocks need to be synchronized every M / (2 * MDR)

### External Synchronization
Clocks are synced in respect to an external time source (which is connected to UTC or atomic clock)

### Internal synchronization
Each pair of processes in a group have clocks within a defined bond of D. |C(i) - C(j)| < D at all times for all processes