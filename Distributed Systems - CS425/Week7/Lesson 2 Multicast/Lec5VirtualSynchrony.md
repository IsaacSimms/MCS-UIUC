# Virtual Synchrony: How to combine membership protocol with multicast
- Attempts to preserve multicast ordering and reliability in spite of failures
- Combines membership protocol with a multicast protocol
- Uses in a variety of critical systems

## Views
- each process maintains a membership list called a *View*. A change to that list is called a *View Change* (leave, join, failure)
- Guarantee: **all view changes are delivered in the same order at al correct processes**
Can be delievered at different times at diff processes, but order is maintained

"If P1 delivers {P1}, then {P1, P2, P3}, then {P1, P2}, then {P1, P2, P4}, then P2, once it has joined, delivers {P1, P2, P3}, {P1, P2}, {P1, P2, P4}. P2 never sees {P1}.

A multicast M is delivered in view V at Pi if Pi delivers V, then delivers M, then later delivers the next view. The gap between two view deliveries is the view."

