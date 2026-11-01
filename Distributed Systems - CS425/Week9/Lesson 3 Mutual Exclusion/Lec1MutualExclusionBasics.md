# Intro to Mutual exclusion

## Defintion
Mutual exclusion = requirement that at most one process executes a critical section (the piece of code that reads and updates a shared resource as an example) at any moment.
- prevents race conditions
Concurrent accesses from multiple proccess interleave and produce incorrect results.
(lost bank deposit when two processes read the same balance, add to it locally, and write back example.
Give mutually exclusive access to the account (or more likely, the code that fetches the account) then correctness would have been maintained)
race condition = correctness of a computation depends on the relative timing or interleaving of concurrent operations on shared state.
- Often enforced through message-passing protocols that guarantee safety (one process in critical section) and liveness (every request eventually granted)
- Also known as the critical section problem

## The critical section problem
enter();                 // request exclusive access
AccessResource();        // the critical section itself
exit();                  // release

- In this pseudo code example Every process that needs the resource wraps its update code between the two function calls.
- Only one process can be in that state at a time.
- The critical section is the piece of code that must not be executing in more than one process at any moment.
  
## uses of mutual exclusion
- distributed files systems
Locking files and directories
- accessing objects in a safe and consistent way (locking access function to bank account example)
- Server coordination
Work partitioned across servers
server coordination using locks
- Cubby and zookeeper both use it

## Solving mutual exclusion locally vs. distributed context
- One one machine a semaphore or mutex works because every process atomically reads and writes a shared int to determine ability to access. 
- No shared variable in distributed system, processes communicate by sending messages over network to coordinate. Must be this system model:
1.  safe (one process in  critical section at any time)
2. Liveness (every request for critical section is granted eventually)
3. ordering (requests are granted in the order they where made)