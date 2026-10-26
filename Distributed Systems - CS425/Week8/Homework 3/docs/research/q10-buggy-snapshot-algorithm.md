---
question: |
  In your snapshot algorithm, for process Pi:
  - If Pi is the Initiator, Pi creates special messages called "Marker" messages, and then follows the rest of the algorithm below.
  - For any process Pi that receives a marker on incoming channel Cki (note that k does not exist for the Initiator):
    if (this is the first Marker seen by Pi) // always true at the Initiator at the initiation point
      Pi records its own state first
      Marks the state of channel Cki as "empty"
      for j=1 to N except i, k
        Pi sends out a Marker message on outgoing channel Cij
      Starts recording the incoming messages on each of the incoming channels at Pi: Cji (for j=1 to N except i, k)
    else // already seen at least one Marker message
      Stop recording Cki and mark that channel's state as the sequence of messages that have been received on all channels Cji (where j=1 to N except i) since Pi received its first marker
  - Terminate when all processes have received (N-1) markers each
  i. Is this algorithm correct? If yes, state the proof. If not, provide a counterexample (draw a timeline).
  ii. How would you fix this algorithm? Try to have a minimal number of fixes.
  Do not answer part iii. It is optional, worth no points, and out of scope.
researched: 2026-10-25
confidence: confident
versions:
  - CS 425 / ECE 428 Fall 2026 Lecture 13 (Snapshots): L13.FA26.pdf, marked Final, PDF timestamp 2026-10-08
  - CS 425 Fall 2026 Homework 3: hw3.fa26.pdf, out 2026-10-12, due 2026-11-01
  - Chandy and Lamport, Distributed Snapshots: ACM TOCS Vol. 3, No. 1, February 1985, pp. 63-75
---

# Homework 3 Problem 10: buggy snapshot algorithm

## Answer

The algorithm is not correct. Two lines produce a bad snapshot on a legal FIFO run, and the same run never terminates. Part iii is omitted.

Model used below: the Lecture 13 model. N processes, one unidirectional FIFO channel each way between every pair, no losses, no duplicates, no failures. Markers are not application messages. N = 3. P1 is the initiator. Because the problem says k does not exist at initiation, the run skips "mark Cki empty" and the "except k" exclusions at P1, so P1 still sends a marker on C12 and on C13 and starts recording C21 and C31. The failures below are at P2 and P3, where k is real.

### i. Counterexample

Application messages: X on C12 after P1's marker on C12, and Y on C21 after P2 has recorded. Nothing else. Markers are written `Mij` (the marker P_i sends on Cij).

```
step     1            2             3              4         5          6            7          8         9
P1    record S1                                                                                          recv Y
      send M12,M13                                                                                       C21 log
      rec C21,C31                                                                                        = <Y>
P2                                 recv M12                  recv X    recv M32               send Y
                                   S2*, C12=<>                         else:
                                   send M23 only                       C32=<X>
                                   rec C32 only                        (no M21 exists)
P3                   recv M13                                                      recv M23
                     S3*, C13=<>                                                   C23=<>
                     send M32 only
                     rec C23 only
```

FIFO is per channel: on C12, M12 is ahead of X. C32 is a different channel, so X can arrive at P2 before M32. The ordered log is:

1. P1 records S1, sends M12 and M13, starts recording C21 and C31.
2. P3 receives M13. First marker, k=1. Records S3. Sets C13 = `<>`. Sends a marker only on C32. Starts recording only C23.
3. P2 receives M12. First marker, k=1. Records S2. Sets C12 = `<>`. Sends a marker only on C23. Starts recording only C32.
4. P1 sends application message X on C12.
5. P2 receives X on C12. C12 stays `<>`. X is not stored on C12.
6. P2 receives M32. This is not its first marker. The else line sets C32 to the messages received on all of P2's incoming channels since step 3. That sequence contains X. Recorded C32 = `<X>`.
7. P3 receives M23. Else line: no application message has arrived at P3 since step 2. C23 = `<>`.
8. P2 sends application message Y on C21. No marker was ever sent on C21.
9. P1 receives Y. Recording of C21 has been on since step 1, so the open log is `<Y>`.
10. P1 has received 0 markers. Nothing toward P1 is still in flight. P2 has received M12 and M32. P3 has received M13 and M23. Termination ("each process has received N−1 = 2 markers") does not occur.

What each broken line does in this run:

- At step 2 the send loop is `for j=1 to N except i, k` with i=3 and k=1, so P3 sends a marker only on C32. It does not send one on C31.
- At step 3 the same loop with i=2 and k=1 sends a marker only on C23. It does not send one on C21.
- At step 6 P2 has already seen a marker. The else line sets C32 to every application message received on every incoming channel since step 3. That set is `<X>`. X arrived on C12, and P1 sent X after recording S1.
- At steps 8–9 there is still no marker on C21. P1 has been recording C21 since step 1, so Y is appended there. P2 sent Y after recording S2.
- Marker receipts: P2 has 2 (M12, M32), P3 has 2 (M13, M23), P1 has 0. No marker toward P1 is in flight. The termination line, "every process has received (N-1) markers," is never reached.

The closed state C32 = `<X>` is already wrong at step 6, before termination. Under the Lecture 13 receive rule the same delivery stores on C32 only the application messages that arrived on C32 after P2 started recording C32. There are none, so C32 = `<>`. X is also absent from C12, which was set empty when M12 arrived. The Lecture 13 channel state is the messages that cross the cut on that channel: send before the sender records, receive after the receiver records. X's send is after S1, and X's receive is after S2, so X crosses no cut. Putting X in the snapshot means the recorded global state contains a message whose send is outside the sender's recorded state.

Y is the other broken line showing up as a channel log. A legal channel state cannot contain Y, because Y was sent after S2. The missing marker on C21 is what would have closed C21 before Y. The run never produces that marker, so C21 is never a finished snapshot state and the algorithm does not terminate.

The same schedule with the two line fixes below finishes as {S1, S2, S3} and six empty channels: markers also go out on C21 and C31, C32 stays `<>`, M21 precedes Y and closes C21 as `<>`, and M31 closes C31 as `<>`.

This run does not need a "receive in the cut, send out of the cut" arrow. Process recording times still follow the first marker that actually arrives. The recorded *channel* component is what is illegal, and termination fails.

### ii. Minimal fixes

Three substitutions. The first two are what make the snapshot and termination match Lecture 13. The third only stops initiation from naming a channel the problem says does not exist. Leave every other line, including the termination sentence and the "start recording … except i, k" line.

1. Broken send loop, first-marker branch:

```
for j=1 to N except i, k
    Pi sends out a Marker message on outgoing channel Cij
```

Replace with:

```
for j=1 to N except i
    Pi sends out a Marker message on outgoing channel Cij
```

k stays excluded on the next line only ("start recording Cji for j except i, k"). That line already matches the slide.

2. Broken else branch:

```
Stop recording Cki and mark that channel's state as the sequence of
messages that have been received on all channels Cji (where j=1 to N
except i) since Pi received its first marker
```

Replace with:

```
Stop recording Cki and mark Cki as the application messages that
arrived on Cki since recording was turned on for Cki
```

For every channel that reaches this branch, recording was turned on at the first marker, so the time window is unchanged. The change is which channel's messages are saved.

3. Broken empty-channel line, same first-marker branch, at the initiator:

```
Marks the state of channel Cki as "empty"
```

Replace with: do this only when a marker actually arrived on Cki. The initiator records its state, sends on every outgoing channel, and starts recording every incoming channel, and it does not mark a channel empty.

After (1) and (2), each directed channel carries one marker, each process receives exactly N-1 markers, one per incoming channel, and the existing termination line is the right end condition. It does not need a rewrite.

## Findings

- Problem 10 of CS425 Fall 2026 Homework 3 is this marker algorithm, and parts (i) and (ii) ask whether it is correct and for a minimal repair. Part (iii) is optional and worth no points. — [T1] CS425 Fall 2026 Homework 3 (`/home/isaacsimms/Desktop/MCS-UIUC/Distributed Systems - CS425/Week8/Homework 3/hw3.fa26.pdf`, also https://courses.grainger.illinois.edu/cs425/fa2026/hw3.fa26.pdf)
- Fall 2026 Lecture 13 is the class snapshot lecture, marked Final, reading Coulouris et al. section 14.5. The homework topics line assigns snapshots to Lectures 13–18. — [T2] CS425 Fall 2026 lectures page (https://courses.grainger.illinois.edu/cs425/fa2026/lectures.html); [T1] Homework 3 header (same PDF)
- Lecture 13 system model: N processes; both directions Cij and Cji between every pair; FIFO inside a channel and no order across channels; reliable, no duplicates, no failures. Any one process may initiate. Markers are not application messages. — [T2] L13.FA26.pdf slides 17–19 (https://courses.grainger.illinois.edu/cs425/fa2026/L13.FA26.pdf)
- Initiator, slide 19: record own state; send a marker on every outgoing Cij for j ≠ i; start recording every incoming Cji for j ≠ i. The initiator does not mark a channel empty. — [T2] L13.FA26.pdf slide 19
- First marker on Cki, slide 20: record own state; set Cki empty; send a marker on every outgoing Cij for j ≠ i, including the channel back to Pk; start recording incoming Cji for j ≠ i and j ≠ k. — [T2] L13.FA26.pdf slide 20
- Later marker on Cki, slide 20: stop recording and set Cki to the messages that arrived on Cki since recording of Cki was turned on. — [T2] L13.FA26.pdf slide 20
- The quoted send loop excludes k as well as i. On the N=3 run above, that is why P3 emits no marker on C31 and P2 emits no marker on C21. — [T1] Homework 3 problem 10; [T2] L13.FA26.pdf slide 20
- The quoted else branch stores, as the state of Cki, messages received on every incoming channel since the first marker. On the run above that stores X, which was sent on C12 after P1 recorded, as the state of C32. — [T1] Homework 3 problem 10; [T2] L13.FA26.pdf slide 20
- The quoted "start recording … except i, k" line matches slide 20 and is not a defect. — [T2] L13.FA26.pdf slide 20
- Slide 21's termination sentence: each process has received a first marker, or has sent one, and has received a marker on the remaining (N-2) incoming channels. The same deck's N=3 example records both of the initiator's incoming channels (C21 and C31), which is N-1, and records the non-initiator's other incoming channel after the first marker closed one. — [T2] L13.FA26.pdf slides 21 and 23–33
- Contradiction inside the winning source: a literal "(N-2) incoming markers for every process" disagrees with the initiator in the worked example, who closes N-1 incoming channels. Winner for what the algorithm records: slides 19–20 plus that example. "(N-2)" is the number of *additional* incoming channels after the channel that carried a non-initiator's first marker. The homework sentence "received (N-1) markers each" is one marker on every incoming channel, which is what the example does for both the initiator and the others. It stays. — [T2] L13.FA26.pdf slides 19–21 and 23–33
- A correct run's channel state holds a message only on the channel it traversed, and only when the send is before the sender's record and the receive is after the receiver's record. The lecture example's only non-empty channel is C21 = `<message G→D>`. — [T2] L13.FA26.pdf slides 33 and 40–42
- Slide 44's consistency argument: if a marker were missing on a channel of a happens-before path, FIFO would not force a marker to precede the later application message. The argument assumes a marker was sent on each link of that path. The quoted send loop drops the link back to k, so that assumption is false on Cik. — [T2] L13.FA26.pdf slides 43–44
- Paper, marker-sending rule: for every outgoing channel c, p sends one marker on c after p records its state and before p sends any further message on c. The quoted loop sends no marker on Cik. — [T1] Chandy and Lamport, ACM TOCS 3(1), February 1985, §3.2 (https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/Determining-Global-States-of-a-Distributed-System.pdf)
- Paper, marker-receiving rule: on the first marker on c, record local state and record c as empty; on a later marker on c, record c as the messages received along c after local state was recorded and before that marker. The saved sequence is the messages on c, not the messages on every incoming channel. — [T1] Chandy and Lamport 1985, §3.2
- Paper, §3.1: the recorded state of c must be the messages sent on c before the sender records, excluding those received on c before the receiver records. Recording a message that was not sent before the sender's record makes n and n' disagree. Example 3.1 is that inconsistency (a token counted in the sender and again on the channel). X stored on C32 is that kind of inconsistency: X is in the recorded global state and send(X) is not in P1's recorded state. — [T1] Chandy and Lamport 1985, §3.1, Example 3.1, equations (1)–(4)
- Paper, §3.3: if a marker is received on every channel, every process has recorded its state and the state of every incoming channel. With one marker sent on every outgoing channel of a complete pairwise graph, that is N-1 marker receipts per process. The homework termination line matches this once the send loop is repaired. The quoted send loop never puts a marker on the initiator's incoming channels, so the paper's "marker on every channel" premise is false and the run does not finish. — [T1] Chandy and Lamport 1985, §3.3
- Course versus paper, recorded because the class source wins: the paper allows a marker to go out any time after the local record and before the next application message on that same channel. Lecture 13 sends every outgoing marker in the record step. The paper's printed receive rule does not contain a separate "start recording" sentence; the course states it, and excludes the first-marker channel because that channel was just saved as empty. Both describe the same saved sequence on each channel. The homework is graded against the lecture's immediate-send, explicit-record rules. Those differences do not make the quoted else branch or the `except i, k` send loop correct. — [T1] Chandy and Lamport 1985, §3.2; [T2] L13.FA26.pdf slides 19–20
- A consistent cut requires that if f is in the cut and e happens-before f, then e is in the cut. The illegal message pattern taught with that definition is send outside the cut and receive inside the cut. The counterexample here is the channel-state failure from §3.1, plus non-termination, rather than that arrow pattern. — [T2] L13.FA26.pdf slides 38–39 and 42

## Recommendation

Use the timeline in the Answer as the part (i) figure, and the three substitutions as part (ii). Keep the repair to those lines so the writeup stays in the homework's own shape.

The tradeoff is how to treat the initiator. Splitting initiation back into the slide 19 block is clearer, and it is a larger edit than the problem's "minimal number of fixes" asks for. Guarding the empty-channel line, widening only the send loop, and narrowing only the else branch leaves the merged control flow in place and matches slides 19–20 on every channel that is actually recorded. Fix 3 does not change the counterexample, because that run already treats a missing k as "no channel to mark." Fixes 1 and 2 are the ones that remove the wrong C32 state and the stuck C21/C31 channels.

Leave the termination sentence as "(N-1) markers each." Changing it to the slide 21 parenthetical "(N-2)" would under-count the initiator, who still has N-1 incoming channels to close.

## Ruled out

- Proving the quoted algorithm correct. The N=3 run records C32 = `<X>` and never delivers a marker to P1.
- A second, separate timeline. One schedule exercises both broken lines.
- Rewriting the algorithm into the paper's delayed per-channel send. Lecture 13 is the algorithm this homework is written against, and the quoted pseudocode is already in the lecture's immediate-send shape.
- Deleting `except k` from the *recording* line. Slide 20 excludes k there on purpose: that channel was saved as empty when its marker arrived.
- Treating "(N-1) markers each" as a third bug. It matches one receipt per incoming channel. It is unreachable in the buggy run only because the send loop never emits those markers.
- Using the lecture's G→D picture as this counterexample. That picture is a correct run: G→D is in C21 because the send is inside the cut and the receive is outside it.
- Calling the X failure a "send outside, receive inside" cut. Both send(X) and receive(X) are after the local records. The failure is the channel component.
- Local notes as authority. `Lec2GlobalSnapshotAlgorithm.md` and `Lec3ConsistentCutsNotes.md` agree with slides 19–20 and 38–44 (marker on every outgoing channel, channel state is the gap on that channel, consistent-cut definition). They are the lowest source and were not used to decide the repair.
- Older CS425 decks (FA2016, FA2019, FA2022, FA2024) turned up in search snippets with the same send and else rules. Those PDFs were not opened. FA2026 Lecture 13 is the winner. The internal slide 21 versus example tension is recorded above from the Final deck itself.
- Coulouris et al. section 14.5, the reading listed for Lecture 13. No local copy was opened. The Final slides are the class source.
- Coursera "Cloud Computing Concepts" transcripts, the CEV GitBook snapshot page, and the decomposition.al walkthrough. Not used as evidence. The GitBook page is a third-party rendering of the same lecture rules; it was not cited.
- Instructor Q&A. No Piazza or Campuswire thread was accessible, so there is no [T3] claim.

## Open questions

- Whether the instructor wants the initiator fully un-merged into the slide 19 block. The three line edits are enough for the recorded states; a split initiator is equivalent and longer.
- Slide 21's "(N-2)" wording is loose for the initiator. The example resolves it. No Fall 2026 clarification of that slide, or of problem 10, was found.
- The 1985 outline never prints a "start recording" line. The course does. The saved channel sequence is the same. Nothing in problem 10 turns on the missing sentence.
