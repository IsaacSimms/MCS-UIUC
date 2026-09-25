# Different types of week consistency models 
The weak consistency described by Cassandras behavior is eventual consistency
    A very wek consistency where key writing must stop all together to get all keys to eventually have the updated value.

## Newer consistency models (weak to simi weak)
Trying to lean towards better consistency while still maintaining high ratios of the other CAP variables.
- Per-Key sequential: per key, app operations have a global order
- CRDTs: "Commutative REplicated Data Types". Data structures in which commutated writes give same result.
    If you reverse the order of two writes, the result is the same.
- Red-Blue operations: All client transactions are split into seperate buckets of operations (red/blue)
    Blue ops are executed in any order across DCs
    Red ops are executed in the same order at each DC

## Causal Consistency
Reads respect partial order based on information flow
If operation A could have influenced operation B, nothing is allowed to see B without having already seen A. Concurrency does allow for seeing things in different orders under this architecture.

## Strong consistency models
- Linearizability: Each operation by a client is visible instantaneously by all other clients. 
- Sequential Consistency: There is one order of operations that matches each client's program order. Those operations cannot be slid around in real time.