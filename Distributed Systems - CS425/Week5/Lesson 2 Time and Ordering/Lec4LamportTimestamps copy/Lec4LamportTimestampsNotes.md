# Lamport Timestamps 
- A way of ordering events in a distributed system without synchronizing clocks
Assigning timestamps to events that are not absolute time. Timestamps obey causality. (one event leads to another)
Almost all distributed systems use some form of logical timestamps, including lamport timestampts.

## Logical ordering
- define logcal relations "Happens-Before" style denoations among pairs of events.
--> is use to denote "Happens-Before"
1. If on same process a --> b if time(a) < time(b)
2. if p1 send m to p2 send(m) --> receive(m)
3. transitivy means if a --> b and b --> c then a --> c
"Happens-Before" creates a partial order among events, does not account for all events in a system, particularly if two processes do not communicate.

## Rules for assigning timestamps
- each process has a local counter with has an int.
initialized to zero. 
A process increments its counter when a send or an instruction happens at it. The counter is assigned to the event as its timestamp.
- A message send carries its timestamp.
- On a message receive event the counter is updated by max(local clock, message timestamp) + 1 (this is done so that if two events are causality related the timestamps obey causality order.)
- Two different events, in two different processes, that do not have a causal path are known as concurrent events.
Lamport timestampts not guaranteed to be ordered or unequal in concurrent events
