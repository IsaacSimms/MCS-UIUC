# The ordering problem in Multicast

## What it is
- Multicast = one message to a group of progesses
- Broadcast = one message to all processes in a system (Expensive)
- a point to point message send from one process to one receiver process.
Commonly used to maintain the infrastructure within a distributed system. Replica writes an membership hearbeat in Cassandra (read/writes to the key are multicast within replica group), scoreboards (ESPN and FIFA), broker group exchanges (Stock exchange where set of broker computers are group), air traffic updates that arrive in order.
One sender can send multiple multicasts and multiple nodes can send multiple mutlicasts within a group.
- Two things emerging. You want **reliable** multicast where all computers receive the message, and you want **ordered** messages where they are received in roughly the same way they are sent.
- 
## Receive vs deliver
- Receive = lower level infrastructure layer received the data packet
- Deliever = upcall to the higher level application completed
- Gap = the buffer between the two. An ordering protocol steps in and delays deliver until the contract allows it (implemented later lectures)

## FIFO
- First in first out, meaning:
- Multicasts from each sender are delivered in sender order at every receiver. 
- Don't *really* care how the messages are delievered to any one receiver if they are from different processes.

"If a correct process sends multicast(g, m) and then multicast(g, m'), every correct process that delivers m' has already delivered m."

"Example: M1:1 then M1:2 from P1 must be delivered in that order everywhere. M3:1 from P3 may land before or after M1:2 at different receivers."

## Causal Ordering
Multicasts whose send events are causally related must be received in the same causality-obeying order at all receivers

"If send(m) → send(m') under Lamport happens-before, every correct process that delivers m' has already delivered m. The → here is induced by multicasts in group g (and local delivery), not by unrelated network traffic.

Example:
- M3:1 → M3:2, so that order everywhere.
- M1:1 → M3:1 (P3 delivered M1:1 before sending M3:1), so that order everywhere.
- M3:1 and M2:1 are concurrent. Different receivers may deliver them in different orders."

**Causal = FIFO** bc reply m' cannot be delievered before m. Concurrent posts can appear in either order as well. *Reverse is not necessarily true*

## Total Ordering
- known as atomic broadcasts
- Ignores send order of the multicasts. Every correct process that delivers both m and m' delivers them in the *same* order. (regardless of send order all recievers get message in the same order)

"Example delivery, same at every process: M1:1, then M2:1, then M3:1, then M3:2. Some messages are buffered so the order can be agreed."

Total != causal or FIFO. Total order can deliver a reply before the post ir replies to, as long as that happens at every receiver. Concurrent multicasts can be recieved in any order

## Hybrids
FIFO and causal are orthogonal to total.
- FIFO-total: per-sender order, plus one global order.
- Causal-total: happens-before respected, plus one global order. Strongest of the three-flavor set.