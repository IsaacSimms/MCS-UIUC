# Expanding on Mutual exclusion in distributed systems
**Remember the system model outlined in previous lecture notes**
*There is no shared memory so mutual exclusion is obtained solely by message exchange*
That message exchange architecture must still maintaine the outlined system model

## Central solution
- Leader is elected (leader election algo) that leader holds a token & a queue for waiting requests.
- A process that wants the critical section sends request to the leader and waits for token >
gets token when entering critical section >
returns token when exting critical section > 
The leader can then hand the token back out immediately or enqueue the requester
- Safety guaranteed due to single token. Liveness guaranteed due to queue and every process forced to exit eventually.

This is simple and ordered but the leader is a single point of failure and a performance bottleneck.
Note the bandwidth, client delay,a nd synchronization delay incurred by this architecture.

## Ring-based token algorithm
- processes form a logical ring w/ exactly one token circulating
- a process that holds the token and wants the critical section, enters the section >
If that process does not hold the token it waits until the token arrives at it before entering section >
Upon exiting that section it FWDs token to successor >
If process receives the token and does not need to enter the critical section it FWDs the token to successor immediately. 
- Safety: Again, only one token. Liveness: token reaches every process
- performance: bandwidth is lower then leader since the token is already nearby, and less heirarchal architecture.
Both client delay and synchronization delay can be O(N) in worst case.
