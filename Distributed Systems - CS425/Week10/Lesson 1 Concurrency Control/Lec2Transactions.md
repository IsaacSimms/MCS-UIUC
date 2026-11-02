# Transactions in distributed systems

## Definition
- A transaction under this context is a sequence of client operations on server objects that is treated as a single indivisible unit.
Indivisible = other clients see neither intermediate states nor interference.
These operations transform server data from one consistent state to another. 
- It either completes entirely (commit)
- or has no effect (abort)

### Must preserve ACID properties:
1. Atomicity (all or nothing): transation either fully commits its effects or has no effect on system
2. Consistency: server moves from one consistent state to another
3. isolation: concurrent transactions do not see each other's intermediate states or interference. 
4. Durability: once committed, the effects survive a crash.

