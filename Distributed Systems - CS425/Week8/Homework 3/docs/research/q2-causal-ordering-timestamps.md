---
question: |
  You see a chart of the multicast communications between your spacecraft New Horizons X (NHX), Earth station (E), and Saturn (S). If these stations use the Causal Ordering algorithm, mark the timestamps at the point of each multicast send and each multicast receipt. Also mark multicast receipts that are buffered, along with the points at which they are delivered to the application.

  The chart is the attached image q2-timeline.png (also on the full page hi-3.png). Processes are three horizontal timelines, top to bottom NHX, E, S, time left to right. Message labels are N1, N2, E1, E2, S1, S2. You must transcribe every arrow from the attached image yourself before answering. Earlier prose captions of this figure contradicted each other. Ignore any remembered caption. If an arrow's endpoints are ambiguous, say so and set confidence to partial. Do not guess.

  Put the transcription in Findings first: for each arrow, sender process, label if the label sits at the send, receiver process, and left-to-right order against the other events on each timeline.
researched: 2026-10-25
confidence: confident
versions:
  - hw3.fa26.pdf: Fall 2026 CS425 Homework 3, page 3 figure (embedded image 1458×552, XObject 16) and page 2 question text
  - L16.FA26.pdf: CS 425 / ECE 428 Fall 2026 Lecture 16, Aishwarya Ganesan with Ram Kesavan, ack Indranil Gupta, slides © IG
  - L16.FA24.pdf: CS 425 / ECE 428 Fall 2024 Lecture 16, compared for the delivered-versus-received wording only
---

# Causal-ordering timestamps on the NHX, E, and S chart

## Answer

Vector order is **[NHX, E, S]**, all processes start at [0, 0, 0]. The mark at a send is the vector piggybacked on that multicast (the sender’s vector after incrementing its own slot). That same vector is the timestamp at every receipt of that multicast. A receipt that passes both causal checks is delivered there, and only the sender’s slot is updated. A receipt that fails is buffered and does not change the local vector; it is delivered later, at the point named below.

Message timestamps:

| Multicast | Timestamp at the send and at every receipt |
|---|---|
| E1 | [0, 1, 0] |
| N1 | [1, 1, 0] |
| S1 | [1, 1, 1] |
| E2 | [1, 2, 1] |
| S2 | [1, 1, 2] |
| N2 | [2, 1, 0] |

Buffered receipts, and where they are delivered:

- **N1 at S** is buffered. It is delivered on S at the E1 receipt, immediately after E1 is delivered and before S1 is sent.
- **E2 at NHX** is buffered. It is delivered on NHX at the S1 receipt, immediately after S1 is delivered.
- **S2 at NHX** is buffered. It is delivered on NHX at that same S1 receipt, immediately after S1 is delivered. E2 and S2 are concurrent, so delivering E2 then S2 (the order they were received) and delivering S2 then E2 are both legal. Either way both deliveries sit at the S1 receipt, and NHX ends at [2, 2, 2].

Every other receipt is delivered at the arrowhead.

Redrawable event list. “Local” is the process vector after the deliveries that happen at that point.

**NHX, left to right**

1. Receive E1, timestamp [0, 1, 0]. Check: E-slot 1 = 0+1, NHX-slot 0 ≤ 0, S-slot 0 ≤ 0. Deliver. Local [0, 1, 0].
2. Send N1, timestamp [1, 1, 0]. Local [1, 1, 0].
3. Receive E2, timestamp [1, 2, 1]. E-slot 2 = 1+1, but S-slot 1 ≤ 0 fails. **Buffer.** Local stays [1, 1, 0].
4. Send N2, timestamp [2, 1, 0]. E2 is still buffered, so N2 does not carry E2 or S1. Local [2, 1, 0].
5. Receive S2, timestamp [1, 1, 2]. S-slot 2 = 0+1 fails. **Buffer.** Local stays [2, 1, 0].
6. Receive S1, timestamp [1, 1, 1]. S-slot 1 = 0+1, NHX-slot 1 ≤ 2, E-slot 1 ≤ 1. Deliver. Local [2, 1, 1]. Both buffered messages now pass. Receipt order: deliver E2 (set E-slot to 2, local [2, 2, 1]), then deliver S2 (set S-slot to 2, local [2, 2, 2]).

**E, left to right**

1. Send E1, timestamp [0, 1, 0]. Local [0, 1, 0].
2. Receive N1, timestamp [1, 1, 0]. NHX-slot 1 = 0+1, E-slot 1 ≤ 1, S-slot 0 ≤ 0. Deliver. Local [1, 1, 0].
3. Receive S1, timestamp [1, 1, 1]. S-slot 1 = 0+1, NHX-slot 1 ≤ 1, E-slot 1 ≤ 1. Deliver. Local [1, 1, 1].
4. Send E2, timestamp [1, 2, 1]. Local [1, 2, 1].
5. Receive S2, timestamp [1, 1, 2]. S-slot 2 = 1+1, NHX-slot 1 ≤ 1, E-slot 1 ≤ 2. Deliver. Local [1, 2, 2].
6. Receive N2, timestamp [2, 1, 0]. NHX-slot 2 = 1+1, E-slot 1 ≤ 2, S-slot 0 ≤ 2. Deliver. Local [2, 2, 2].

**S, left to right**

1. Receive N1, timestamp [1, 1, 0]. NHX-slot 1 = 0+1, but E-slot 1 ≤ 0 fails. **Buffer.** Local stays [0, 0, 0].
2. Receive E1, timestamp [0, 1, 0]. E-slot 1 = 0+1, NHX-slot 0 ≤ 0, S-slot 0 ≤ 0. Deliver. Local [0, 1, 0]. Buffered N1 now passes (E-slot 1 ≤ 1). Deliver N1. Local [1, 1, 0].
3. Send S1, timestamp [1, 1, 1]. Local [1, 1, 1].
4. Send S2, timestamp [1, 1, 2]. Local [1, 1, 2].
5. Receive N2, timestamp [2, 1, 0]. NHX-slot 2 = 1+1, E-slot 1 ≤ 1, S-slot 0 ≤ 2. Deliver. Local [2, 1, 2].
6. Receive E2, timestamp [1, 2, 1]. E-slot 2 = 1+1, NHX-slot 1 ≤ 2, S-slot 1 ≤ 2. Deliver. Local [2, 2, 2].

## Findings

- The page-3 figure is a 1458×552 raster (PDF XObject 16). Ink was read from that image’s soft mask. Three horizontal timelines sit at y≈66 (NHX), y≈265 (E), and y≈463 (S), time left to right. Labels sit off the line at the send: N1 and N2 above NHX, E1 and E2 above E, S1 and S2 below S. — [T1] hw3.fa26.pdf (`/home/isaacsimms/Desktop/MCS-UIUC/Distributed Systems - CS425/Week8/Homework 3/hw3.fa26.pdf`, page 3 image)
- Arrow E1, label at the send on E: E → NHX. The NHX end is an arrowhead and is the leftmost event on NHX. — [T1] hw3.fa26.pdf (page 3 image)
- Arrow E1, same send: E → S. The S end is an arrowhead and is the second event on S, to the right of N1’s arrival. — [T1] hw3.fa26.pdf (page 3 image)
- Arrow N1, label at the send on NHX: NHX → E. The send is the second event on NHX, to the right of E1’s arrival. The E end is an arrowhead and is the second event on E, to the right of E1’s send. — [T1] hw3.fa26.pdf (page 3 image)
- Arrow N1, same send: NHX → S. The S end is an arrowhead and is the leftmost event on S. The shaft crosses the E timeline with no arrowhead there, so E has no N1-to-S receipt. — [T1] hw3.fa26.pdf (page 3 image)
- Arrow S1, label at the send on S: S → E. The send is the third event on S, to the right of E1’s arrival. The E end is an upward arrowhead and is the third event on E. — [T1] hw3.fa26.pdf (page 3 image)
- Arrow S1, same send: S → NHX. The NHX end is an arrowhead and is the rightmost event on NHX. The shaft crosses E with no receipt at E. — [T1] hw3.fa26.pdf (page 3 image)
- Arrow E2, label at the send on E: E → NHX. The send is the fourth event on E. The NHX end is an arrowhead and is the third event on NHX, right of N1’s send and left of N2’s send. — [T1] hw3.fa26.pdf (page 3 image)
- Arrow E2, same send: E → S. The S end is an arrowhead and is the rightmost event on S. — [T1] hw3.fa26.pdf (page 3 image)
- Arrow N2, label at the send on NHX: NHX → E. The send is the fourth event on NHX, right of E2’s arrival. The E end is an arrowhead and is the rightmost event on E. — [T1] hw3.fa26.pdf (page 3 image)
- Arrow N2, same send: NHX → S. The S end is an arrowhead and is the fifth event on S, right of S2’s send and left of E2’s arrival. The shaft crosses E with no receipt at E. — [T1] hw3.fa26.pdf (page 3 image)
- Arrow S2, label at the send on S: S → E. The send is the fourth event on S, right of S1’s send. The E end is an upward arrowhead and is the fifth event on E, right of E2’s send and left of N2’s arrival. — [T1] hw3.fa26.pdf (page 3 image)
- Arrow S2, same send: S → NHX. The NHX end is an arrowhead and is the fifth event on NHX, right of N2’s send and left of S1’s arrival. The shaft crosses E with no receipt at E. — [T1] hw3.fa26.pdf (page 3 image)
- Left-to-right event order is NHX: recv E1, send N1, recv E2, send N2, recv S2, recv S1. E: send E1, recv N1, recv S1, send E2, recv S2, recv N2. S: recv N1, recv E1, send S1, send S2, recv N2, recv E2. — [T1] hw3.fa26.pdf (page 3 image)
- On E, S1’s arrowhead meets the timeline near x=799 and E2’s two outgoing strokes leave near x=818–825, with a gap between the strokes. S1’s receipt is immediately left of E2’s send. The E2 label’s horizontal span sits above that neighborhood; the label marks the send, whose tails are the upward stroke and the down-right stroke. — [T1] hw3.fa26.pdf (page 3 image)
- Fall 2026 causal multicast: Pi[j] is the latest sequence number Pi has delivered from Pj. On send, Pj increments Pj[j] and piggybacks the whole vector. On receipt from Pj, buffer until M[j] = Pi[j]+1 and, for every k≠j, M[k] ≤ Pi[k]. Then deliver and set Pi[j] = M[j]. — [T2] L16.FA26.pdf (https://courses.grainger.illinois.edu/cs425/fa2026/L16.FA26.pdf), slides “Causal Multicast: Datastructures” and “Causal Multicast: Updating Rules”
- The same lecture says that if Pi sends m, Pi also receives m, because the sender is in the group. The chart draws no self-arrow; the send mark is that self-delivery. — [T2] L16.FA26.pdf, slide “Receive vs. Deliver”
- Fall 2024’s copy of this lecture says Pi[j] is the latest sequence number Pi has “received” from Pj, and its causality sentence says those multicasts “have been received.” The update line on that same slide still sets Pi[j] = M[j] only when the buffer conditions pass and the message is delivered. Fall 2026 is the homework’s term and says “delivered” in both the definition and the update. The worked answer follows Fall 2026, which also matches the update step printed in Fall 2024. — [T2] L16.FA24.pdf (https://courses.grainger.illinois.edu/cs425/fa2024/L16.FA24.pdf), slides “Causal Multicast: Datastructures” and “Causal Multicast: Updating Rules”
- The Fall 2026 causal example delivers a buffered message once a later delivery makes the checks true, and when two buffered messages both become deliverable it delivers them in the order they were received. The example also asks whether those two concurrent buffered messages could be delivered in the other order. — [T2] L16.FA26.pdf, “Causal Ordering: Example”
- Local Week 7 notes describe the same send increment, the same two buffer tests, and “set Pi(j) = M(j)” without copying the rest of M. They agree with L16.FA26 and were not used as the winning source. — local notes `Distributed Systems - CS425/Week7/Lesson 2 Multicast/Lec2&Lec3ImplementingMulticastOrdering.md`

## Recommendation

Use the timestamps, buffer marks, and delivery points in Answer as the worked solution. The load-bearing figure facts are that NHX delivers E1 before it sends N1, that S receives N1 before E1, and that NHX receives E2 and then S2 before S1, while E2 stays buffered across N2’s send. Index the vector as [NHX, E, S] and say so on the writeup, since the slides index P1…PN in an arbitrary order.

This pass was done inline in the current session, so context isolation was lost.

## Ruled out

- Treating a timeline crossing as a receipt. N1’s arrow to S, S1’s arrow to NHX, S2’s arrow to NHX, and N2’s arrow to S cross the middle timeline and have no arrowhead there.
- Updating a vector when a message is only buffered. That would put E2 and S1 into N2. Fall 2026 updates a slot when the message is delivered.
- Copying every component of M into Pi on delivery. The Fall 2026 rule sets only Pi[j] = M[j]. The other slots stay at whatever this process has already delivered, which is why a receiver can sit strictly above M in a concurrent slot.
- Reading the Fall 2024 word “received” as an instruction to count buffered messages. The update step on that slide still runs at deliver, and Fall 2026’s wording is the one that matches this homework term.
- Any earlier prose caption of the figure. Endpoints above were taken from the page-3 raster.

## Open questions

- After S1 is delivered at NHX, E2 and S2 are both deliverable and concurrent (E2 is [1, 2, 1], S2 is [1, 1, 2]). The lecture example delivers concurrent buffered messages in receipt order and also asks whether the reverse is allowed. Receipt order is E2 then S2. The reverse is also consistent with the written rule. The delivery point on the chart is the S1 receipt either way.
- The Birman–Schiper–Stephenson paper was not opened. Fall 2026 already states the rule used here.
