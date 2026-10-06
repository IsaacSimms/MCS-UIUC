# Consistent Cuts: a continuation of the global snapshot algorithm

## Cut
Cut = a time frontier at each process and each channel (frontier = one point on each process timeline. and the channel crossings that fall on the same line/connect it all together)
- Before the frontier = in the cut. After the prontier != in the cut
- Recorded process state is exactly the events in teh cut at that process. The recorded channel state is the messages whose send is in and whose receive is out. 

## Consistent cuts
**A cut that obeys causality**
> If e is in the cut and f --> e, then f is in the cut

Equivalent exam test on a message arrow:
- send in, receive in — ok (already delivered)
- send out, receive out — ok (not yet sent, relative to the cut)
- send in, receive out — ok (in transit; belongs in the channel)
- send out, receive in — illegal (effect without cause)

## Lecture example
### The lecture’s bad cut
G → D, and the frontier includes D but not G. Receipt is in, send is out. Causality violated. That is not a snapshot.

### The lecture’s good cut
The 1.2 run. Process states S1, S2, S3. Channels empty except C21 = ⟨G→D⟩. G is in (send before sender recorded). D is out (receive after receiver recorded). Arrow crosses the frontier forward, so it is channel state, not a violation. That snapshot is a consistent cut.

## Theorem
Any run of Chandy-Lamport creates a consistent cut.
### Example
e_i and e_j are events occuring at P_i and P_j such that:
- e_i --> e_j

The snapshot algo enures:
- If e_j is in the cut then e_i is also in the cut
- That is: if e_j --> (P_j records its state), then:
    It must be true that e_i --> (P_i records its state).

