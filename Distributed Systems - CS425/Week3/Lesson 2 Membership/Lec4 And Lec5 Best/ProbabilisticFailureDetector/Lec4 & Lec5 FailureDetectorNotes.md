# The optimal failure detector systems in Membership architecture

### Remember
Completeness --> Guarantee always
Accuracy     --> denote as probability PM(T)
Speed        --> denote as T (time units)
Scale        --> Nodes (N) * load (L) comparison 

## All-to-all heartbeating
Process = a sequential heartbeat, with an I++ counter
occurs every T units
**L = N/T**

### Gossip-style
process propagation is every tg units equalling the gossip period, sending O(N) gossip messages
**L=N/tg = N*log(N/T)**

All-to-all heartbeating (including gossip style) are sub-optimal because they are not using dissemination, and trying to have each process detect the failure independently
    For optimal failure detection, using a separate failure detection component would be more optimal

## Best practice failure detection protocol (SWIM)
SWIM = Scalable Weakly-Consistent Infection-Style Membership protocol

SWIM fixes this by not using heartbeats, instead using a small number of ack messages (pings) every protocol period. 
    Protocol period = T' time units
    every T', pi sends a ping to a random pj. If pj receives a ping, it sends back an ack.
        If that first ping fails, process pi will attempt to ping pj again by pinging different randomly selected processes (K) and having those processes ping pj
        If the pi process receives any ack for pj, even if indirect, it is satisfied 

Remember, hearbeating does not scale well because the membership list is O(N) every T_Gossip, the first detection time is O(N), and the load on the system is O(N) as well. (linear scale)
But, SWIM is a **constant rate for all of these metrics** even as the system scales. Amount of false positives and message loss is fixed

First detection time = e/(e-1) periods (constant) (e = euler's number, 2.718)
Process load         = constant (8L* for 15% loss)
False positive rate  = tunable but changing K (False positives drop off exponentially as K is increased)
Completeness         = deterministic (time bound) and within O(log(N))

### Time bound completeness
Each membership element gets selected at least once by another process every traversal of the list
    done through round robin pinging & random permutation of the list after each traversal
Any failure is detected, in worst case, 2N-1 protocol periods
    (still preserves failure detection properties)
