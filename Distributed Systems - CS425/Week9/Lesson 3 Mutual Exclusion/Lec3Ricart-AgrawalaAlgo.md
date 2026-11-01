# Ricart-Agrawala' Algorithm
*Improving the previously discussed architecture*
**This satisfies the already defined system model**

## Definition
- A token-free distributed mutual exclusion algo.
Uses a notion of causality and multicast w/ lower waiting times to enter critical section then ring or leader based approaches.
- Each process that wants the critical section multicasts a timestamped request and waits for a reply from every other process.
- Replies are deferred/handled according to Lamport timestamp logic (earliest request always granted first)
- This = safety and casual ordering w/ constant delay (cost is O(N) messages)

## Flow
See "Distributed Systems - CS425/Week9/Lesson 3 Mutual Exclusion/Lec3RaAlgoMEssageFlow.png"
1. Enter at process P_i
- multicasts a request to all processes
- includes lamport timestamp (T, P_i) w/ T = current lamport at P_i
2. waits until all other processes have responded positively to request
3. Requests are then granted in order of causality
In case of concurrent events, the "P_i" part of the request is used to break ties. 

## Process replying immediately vs deffering
**Remember: a process that receives a request must decide whether to grant it now or hold it until later**
On receiving an above described timestamp a process replies *immediately* unless:
- that process is already inside the critical section
- It itself is waiting ond its own request has a *smaller* timestamp (meaning it must get served first)
In these cases the process enqueues the request and replies to the sending process only after it leaves the critical section.

### Safety
Two processes cannot be inside the critical section, still ensuring safety.
The total order on Lamport timestamps plus the “reply only if not earlier” rule guarantees mutual exclusion.

### Performance
- this algo elimites the long worst-case wait of the ring. But pays in huge message volumes.
(a process in the critical section is getting and queuing all requests for critical section from all other processes). 
- Bandwidth = 2(N - 1) messages per critical section entry. w/ N multicast messages if the critical section is available.
- client delay = one parallel round trip
- Synchronization delay: one message (the deferred reply to the next waiter).
Ordering is by increasing Lamport timestamp (causal order).
Retain: Constant delay, linear message cost; the opposite of the ring’s constant message cost and linear delay.