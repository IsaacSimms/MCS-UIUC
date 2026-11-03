# Transactions in distributed systems

## Definition
- A transaction under this context is a sequence of client operations on server objects that is treated as a single indivisible unit.
Indivisible = other clients see neither intermediate states nor interference.
These operations transform server data from one consistent state to another. 
- It either completes entirely (commit)
- or has no effect (abort)

### Must preserve ACID properties:
1. Atomicity (all or nothing): transation either fully commits its effects or has no effect on system (most important)
2. Consistency: server moves from one consistent state to another
3. isolation: concurrent transactions do not see each other's intermediate states or interference.
- No access to intermediate results/states of other transactions
- free from interference by operations of other transactions
4. Durability: once committed, the effects survive a crash.

ACID must be maintained during:
- client and server failure
- transactions running concurrently (multiple clients)
- transactions distributed (across multiple servers)

## Naive concurrency fails
- lost updates: T1 and T2 both read ten seats on a flight. now they both have a working value of x = 10 >
both decrement the value and return 9 >
both clients return 9 to the server, so the servers now hold x = 9. one of the decrements was lost
- inconsistent retrival:
Total of 25 seats across two flights, flight A and B. T1 starts an operation to move 5 flights from A to B >
T2 initiates an operation to sum all seats accross both flights during that operation. Since those 5 seats are in a transient state between A and B, T2 reads 20 instead of 25. 

## Serial equivalence and conflicting operations
With transactions, **concurrency for throughput but the outcome must be indistinguishable from serial order**

