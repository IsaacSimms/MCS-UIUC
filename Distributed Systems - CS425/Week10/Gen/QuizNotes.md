# Quiz notes

## 1. In an object-based system, object C1 has a method C1.M1 that calls object C2's method C2.M2. In which of the following cases is this call NOT a Remote Method Invocation? There may be MULTIPLE ANSWERS.

**Context.** Remote Method Invocation (RMI) is a call that crosses process (address-space) boundaries. Host location is irrelevant; only the process boundary decides whether the call is remote.

**Correct answer.** C1 and C2 reside in the same process.

**Why.** When both objects share the same process the invocation is ordinary local method dispatch. Every other listed case crosses a process boundary and is therefore an RMI.

---

## 2. A particular RPC system chooses big-endian representation for its integers. Now consider a little-endian x86 machine (using this RPC system) that needs to send an RPC call with an integer parameter represented in memory as four bytes, with each byte represented in a hexadecimal format. The integer is stored as follows in the x86 machine: (lowest address byte) 12-34-56-78 (highest address byte). In the marshalled RPC call message, this integer will be stored with:

**Context.** An RPC system’s wire format is independent of the sending host’s native endianness. Marshaling converts the host layout into the protocol’s chosen representation.

**Correct answer.** 78 in its lowest addressed byte

**Why.** The RPC system uses big-endian, so the most-significant byte occupies the lowest address in the marshalled message. On the little-endian host that byte is 78.

---

## 3. Some operations are called idempotent operations because they can be repeated multiple times without any side effects. RPCs that implement idempotent operations are a good fit for at-least-once call semantics. Which of the following functions is NOT idempotent? In the following, y is a local variable held at the server executing the called function, while x is an argument passed by the calling function.

**Context.** An operation is idempotent when repeated execution leaves server state identical to a single execution. At-least-once RPC may re-execute the procedure, so only idempotent procedures are safe.

**Correct answer.** int f(int x) { y = y+x; return 1; }

**Why.** Each execution adds x to the previous value of y, so the final state depends on the number of times the procedure runs. The other three functions assign a value determined solely by the current argument (or a constant) and are therefore idempotent.

---

## 4. The A in ACID stands for:

**Context.** ACID names the four guarantees provided by transactions. Atomicity is the all-or-nothing property.

**Correct answer.** The property that all transactions must be all or nothing in terms of updates reflecting on the server side

**Why.** A stands for Atomicity: either every update of the transaction takes effect or none do.

---

## 5. Which of the following ways will NOT prevent deadlocks from occurring (and persisting)?

**Context.** Deadlock prevention breaks one of the Coffman conditions (mutual exclusion, hold-and-wait, no preemption, circular wait).

**Correct answer.** Transactions are multi-threaded

**Why.** Read-only objects with only shared locks remove mutual exclusion. Abort-on-timeout supplies preemption. Strict increasing lock order eliminates circular wait. Multi-threading leaves all four conditions intact.

---

## 6. Which of the following increases concurrency (TPS) the most, while preserving correctness?

**Context.** Pessimistic concurrency control acquires locks before access and therefore blocks. Optimistic concurrency control lets transactions run freely and validates only at commit.

**Correct answer.** Optimistic Concurrency Control

**Why.** Exclusive locks serialize all accesses. Read-write locks allow concurrent readers but still force writers to wait. Optimistic control acquires no locks during execution and aborts only on detected conflict, yielding the highest throughput when conflicts are rare.

---

## 7. In a system supporting read-write locks, which of the following is FALSE?

**Context.** Read locks may be shared; a write lock is exclusive to its object. Promotion of a read lock to a write lock requires that no other transaction holds any lock on that same object. Locks on distinct objects never conflict.

**Correct answer.** A read lock on object O held by transaction T cannot be promoted if another transaction U holds a write lock on any other object O2.

**Why.** Promotion depends only on the lock state of the target object O. A write lock on an unrelated object has no effect.

---

## 8. With a per-replica availability of 1 Nine, what is the minimum number of replicas you need in order to get at least 5 Nines availability for an object?

**Context.** k nines means availability \(1-10^{-k}\). With independent replicas the object is unavailable only when every replica is unavailable, so unavailability is the product of the per-replica failure probabilities.

**Correct answer.** 5

**Why.** One nine means each replica fails with probability 0.1. Five independent replicas therefore fail together with probability \(0.1^5=10^{-5}\), which is exactly five nines.

---

## 9. In a two-phase commit for transaction T, what is the earliest point of time that a responding server can commit its portion of the transaction T's updates?

**Context.** In two-phase commit a participant that has voted Yes is prepared but the global decision has not yet been made. Only the coordinator’s Commit message authorizes the participant to make its updates permanent.

**Correct answer.** Right after receiving a Commit message from the coordinator

**Why.** After logging and sending Yes the coordinator may still decide Abort. The participant must wait for the Commit message.

---

## 10. Someone builds an active replication system where there is only one front-end, and the front-end for each operation (read or write) forwards only one operation at a time to all the replicas and waits for all of the replicas to respond to the coordinator before sending back an answer to the client. For a read operation, the front-end sends back the highest timestamped value. Which consistency model does this system implement?

**Context.** A front-end that admits only one operation at a time and waits for every replica imposes a total order that respects real time.

**Correct answer.** Linearizability (or a notion of strict consistency)

**Why.** The one-at-a-time rule plus unanimous acknowledgment produces a single global real-time order, which is linearizability. Monotonic and causal consistency are weaker; per-key serializability does not require that global order.

---

## 11. Below you are shown a set of transactions and their operations in the order they are executed in real time. This execution is:

**Context.** Serial equivalence is decided by the serialization graph of conflicting operations (same object, at least one write). A cycle means no serial order is equivalent.

**Correct answer.** Not serially equivalent

**Why.** On x, T’s first Read precedes U’s Write (edge T → U) while U’s Write precedes T’s second Read (edge U → T). The cycle proves the schedule is not serially equivalent.

---

## 12. Two transactions T1 and T2 have instructions as follows (a and b are variables at the server): T1: write(a, foo, T1); read(b, T1); read(a, T1); T2: read(b, T2); write(b, bar, T2); write(a, baz, T2); Consider the following interleaving: read(b, T2); write(b, bar, T2); write(a, foo, T1); read(b, T1); write(a, baz, T2); read(a, T1). This execution is:

**Context.** Serial equivalence holds exactly when the serialization graph of conflicting operations is acyclic. Opposite conflict edges create a cycle.

**Correct answer.** Not serially equivalent

**Why.** T1’s write(a) precedes T2’s write(a) (edge T1 → T2) while T2’s write(b) precedes T1’s read(b) (edge T2 → T1). The cycle shows the schedule is not serially equivalent.

---

## 13. Two transactions T1 and T2 have instructions as follows (a and b are variables at the server): T1: write(a, foo, T1); read(b, T1); read(a, T1); T2: read(b, T2); write(b, bar, T2); write(a, baz, T2); Consider the following interleaving: write(a, foo, T1); read(b, T2); write(b, bar, T2); read(b, T1); write(a, baz, T2); read(a, T1). This execution is:

**Context.** Serial equivalence is decided solely by whether the serialization graph of conflicting operations is acyclic.

**Correct answer.** Not serially equivalent

**Why.** T1’s write(a) precedes T2’s write(a) (edge T1 → T2) while T2’s write(a) precedes T1’s read(a) and T2’s write(b) precedes T1’s read(b) (edges T2 → T1). The cycle proves the schedule is not serially equivalent.

---

## 14. Below, you are shown a set of transactions and their operations in the order they are executed in real time. This execution is:

**Context.** A cycle between any pair of transactions in the serialization graph is sufficient to prove the schedule is not serially equivalent.

**Correct answer.** Not serially equivalent

**Why.** On x, V’s first Read precedes U’s Write (edge V → U) while a later Read by V follows that Write (edge U → V). The cycle V → U → V shows the schedule is not serially equivalent.

---

## 15. Two transactions T1 and T2 have instructions as follows (a and b are variables at the server): T1: write(a, foo, T1); read(b, T1); read(a, T1); T2: read(b, T2); write(b, bar, T2); write(a, baz, T2); Consider the following interleaving: read(b, T2); write(a, foo, T1); read(b, T1); read(a, T1); write(b, bar, T2); write(a, baz, T2). This execution is:

**Context.** When every conflict edge points the same way the schedule is serially equivalent to that order. Reads do not conflict with other reads.

**Correct answer.** Serially equivalent

**Why.** Every conflict runs from T1 to T2: T1’s read(b) precedes T2’s write(b) and T1’s write(a) precedes T2’s write(a). The only edges are T1 → T2, so the graph is acyclic and the schedule is equivalent to T1 then T2.