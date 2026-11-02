# Maekawa's algo
- Fixes the problem with Ricart-Agrawala where messages are being sent/received from all processes in the group.
- **Process obtains mutual exclusion by asking permission from only a small subset of processes**
(Known as the voting set)
- Voting sets are constructed so that any two intersect, and that guarantees that at most only one process holds critical section (safety)

## Maekawa voting sets
- each process (P_i) is associated with at least one voting set (V_i)
each P_i multicasts its request only to members of V_i & enters the critical section only after all members of V_i have replied.
Remever, every pair of voting sets intersects and that each process votes for at most one requester at a time.
Meaning, if P_i wants the critical section but P_j has it but P_j is apart of V_j and not V_i, the union of V_i and V_j do not equal zero.
Therefore, at least one process that voted for P_k lives in both sets so that process will maintain safety.
- the intersection of any two voting sets must be non-empty 
This is a quorum concept
- each voting set set is of size K
- each process belongs to M other voting sets
- K = M = square root of N works best

## Flow
Processes initialized with this state:
state = released, voted = false

To enter critical section:
1. process sets state = wanted
2. multicast a "Request" to every process in its voting set
3. waiting until a "Reply" has arrived from every member of voting set
4. set state = held and enter critical section

To exit critical section
5. set state = released
6. Multicast a "Release" to every process in voting set

### When P_i receives a request from P_j
If state == held *or* voted == true, enqueue the request (does not reply yet)
Otherwise, reply to P_i immediately with voted = true

### WHen P_i receives a release from P_j
if local queue is empty, set voted = false
Otherwise, dequeue the head process (P_k), send "Reply" only to P_k, and keep voted = true

## Safety and liveness
- Any two voting sets share at least one process. That one process can only vote for one of the requesting processes at a time, maintaining safety. 
- But the basic algo can deadlock, preventing liveness:
Processes can form a circular wait in which each holds a vote for the next one needs. (There are deadlock free variants.)

## Performance
- 2 * square root N messages to enter critical section
- 2 * square root N messages to exit critical section
(Better then Ricart and Agrawala)
- Client delay = one round trip time
- Synchronization delay: 2 message transmission times
