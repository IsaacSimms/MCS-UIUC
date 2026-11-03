# Serial Equivalence
**correctness criterion for concurrent transactions**
Note: You could satisfy the ACID properties in transactions simply by only executing those transactions one at a time. But, this would be terriblely inefficient (reduced transactions per second)
Implementing architecture that accomplishes serial equivalence allows for *concurrent* transactions while still satisfying ACID properties.

## Definition
An interleaving of operations from multiple transactions is *serially equivalent* if there exists a serial schedule.
Produces an identical final system state. 

Interleaving = mixing the operations of several transactions into one sequence while still preserving the relative order of operations *inside* each individual transaction.

Serial schedule = a schedule in which transactions are executed one after the other with no interleaving. 
each transaction’s operations run consecutively from start to finish before the next transaction begins.

Serially equivalent = An interleaving operation set is serially equivalent if there exists some serial schedule of the same transactions that produces the identical final system state.
The concurrent execution is correct exactly when its result matches what would have happened under pure serial execution in some order.
**Serial equivalence is the correctness criterion for concurrent transactions**. Interleaving is acceptable 'exactly' when the final system state matches some serial execution fo the same transactions.
This holds if and only if every pair of conflicting operations appears in a consistent relative order across all shared objects.
*to be serially equivalent, the interlaving transactions (say O) must produce the same final system state as a different interleaving of those same transactions (say O')