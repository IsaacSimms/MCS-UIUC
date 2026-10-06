# How to implement multicast ordering (FIFO multicast discussed first)

## Data structure used
- FIFO multicast
- prcesses P1...PN
- Pi maintains a vector of sequence numbers Pi(1...N)
- Pi(j) is the last sequence number Pi received from Pj

## updating rules
- Send multicast at process Pj:
Pj(j) = Pj(j) + 1 — next sequence number this sender has ever used.
"Include the new pj(j) in multicast emssage as its sequence number. "Put that scalar in the message. Receivers do not get the rest of the vector."

- Recieve multicast: If Pi recieves a mulicast from Pj with sequence number S in message:
Deliever only if this is the next one in the slot from that sender. **S = Pi(j) + 1**
    - deliver message to application
    - set pi(j) = pi(j) + 1

- *Else* buffer this multicast until above condition is true (the gap case)

## Example the lecture walks
Four processes, all (0,0,0,0).
- P1 sends with seq 1. A receiver at (0,0,0,0) sees 1 == 0+1, delivers, becomes (1,0,0,0).
- A receiver that gets P1’s seq 2 first sees 2 ≠ 0+1, buffers. When seq 1 arrives and is delivered, 2 == 1+1, so the buffered message delivers and the slot becomes 2.
Same check independently at P2, P3, P4. Each receiver’s vector is local. There is no agreement step.

## Total ordering implementation. Popular approach is sequencer-based
- A special process is elected as leader/sequencer
1. Send multicast at process Pi:
    – Send multicast message M to group and sequencer
2. sequencer:
    - Maintains global secquence number S (initalized to zero)
    - When receives multicast from M, sets S = S + 1, and multicasts <M, S>
3. Receive multicast at process Pi:
    – Pi maintains a local received global sequence number Si (initially 0) 
    – If Pi receives a multicast M from Pj, it buffers it until it both
       1. Pi receives <M, S(M)> from sequencer, and
       2. Si + 1 = S(M)
    - Then deliver it message to application and set Si = Si + 1


## Causal ordering
Remember: If multicast(g, m) --> multicast(g, m'), any correct process that delivers m' has already delivered m. The arrow is Lamport happens-before on group multicasts. Slide says “received”; the rule is on deliver.

### Data structure for causal orering
- similar to FIFO multicast as listed above w/ different updating rules
Pi(1..N), initially 0. Pi(j)) = highest sequence Pi has delivered from Pj. Same slots as FIFO. The difference is what is attached to the message.

### Send at Pj = 
1. Pj(j) = Pj(j) + 1
2. The entire vector at Pj is included in the multicast message as its sequence number. (the other slots in the vector are a record of what is delievered before message send, so causality can be obeyed)

## Deliver at Pi message M from Pj = 
Buffer until both are true:
1. M(j) = Pi(j) + 1. (this is next message from this sender)
2. For all k != j. M(k) ≤ Pi(k). Every multicast the sender had delivered is already delivered here.

Once both conditions true deliver and set Pi(j) = M(j). Do not copy the rest of M over Pi.

## Example
All start (0,0,0,0).

- P1 sends (1,0,0,0). At a receiver: slot 1 is next, other slots are 0 ≤ 0. Deliver. Receiver becomes (1,0,0,0).
- P2 sends (0,1,0,0) without having delivered P1. Slot 2 is next, M(1) = 0 ≤ 1. Deliver. No edge from M1:1 to M2:1.
- P4 delivers M2:1 first, so P4 is (0,1,0,0), then sends. Piggybacked vector is (0,1,0,1). A receiver that has not delivered M2:1 fails M[2] ≤ Pi[2] and buffers until it has.


This architecture is causal and implements FIFO because of the buffer rules listed above.Conditio 1 is FIFO and condition 2 blocks cases that FIFO misses. 
Reme

