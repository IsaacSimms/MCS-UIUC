# Pessimistic concurrency control
One of the two ways to prevent isolation from being violated in transactions

## Definition of Pessimistic concurrency control (mutual exclusion)
Strategy that assumes conflicts are likely and therefore blocks a transaction from accessing an object until it holds the appropriate lock. 
(as apposed to allowing the access and then checking for a lock later)
Standard protocol here is a two-phase locking (2PL). This guarantees serial equivalence by separating lock acquisition from lock release. 

- Each object has its own lock (with only one transaction inside the lock)
- Before read/writing to the object the transaction has to call the lock. but, once its in the object, it can do multiple things
- Transaction being inside the lock prevents other transactions from entering
- Another call to unlock

### Read-Write locks (per object)
*helpful in some modern situations bc some workloads are very read heavy.*
*Perfecting fine to allow read-read on single object, since that does not break serial equivalence*

- Each object gets two locks
A read mode lock
A write mode lock
- Rest of Pessimistic concurrency control applies. Just specifies read or write permissions on the object.

### Two-phase locking
- a transaction cant acquire or promote any locks after it has started releasing locks
- Transaction has two phases
1. Growing phase: Only able to acquire or promote locks
2. Shrinking phase: Only able to release lock
This guarantees serial equivalence because if two transactions conflict, the one that acquired the lock first must finish growing phase before the other can proceed. 
(enforces a consistent order on all conflicts)

### Deadlocking
Locking can create circular waits.
A deadlock occurs when exclusive locks are held, transactions are not preempted, and a cycle exists in the wait-for graph. 
Common remedies: acquire all locks at the start, use timeouts, or detect cycles and abort one transaction.
Deadlock prevention attacks one of the four Coffman conditions (mutual exclusion, hold-and-wait, no preemption, circular wait)

## Definition of Optimistic concurrency control
Strategy that allows transactions to proceed without locking and validates that their interleaving is serially equivalent only when they attempt to commit. 
On a failure the transaction is aborted w/ updates rolled back.
optimistic increases concurrency of transactions, leading to more transactions per second.
This leads to lower latency in non-transaction systems.
Preferred if conflicts are going to be rare.

### Basic approach
Transactions read and write at will >
check for serial equivalence at commit time >
abort and roll back if needed > 
abort cascade is possible (one aborted transaction causes other transactions to abort)

### Timestamp ordering (common)
Assign each transaction a timestamp and enforce order without locks.
TRansaction ID defined its position in serialization order.

Ensure that for a transaction T, both are true:
1. T’s write to object O allowed only if transactions that have read or written O had lower ids than T.
2. T’s read to object O is allowed only if O was last written by a transaction with a lower id than T.

### Multiversion concurrency control (less important to know)
Control system keeps multiple versios of each object. (One committed version and per-transaction tentative versions.)
- Objects have a committed version and one or more tentative (per-transaction) versions.
- Versions carry timestamps.
- A transaction is directed to the version that matches its timestamp order (“immediately previous”).
- This is still optimistic in spirit (no locks, versions reconcile the order) but reduces conflicts compared with single-version timestamp ordering.