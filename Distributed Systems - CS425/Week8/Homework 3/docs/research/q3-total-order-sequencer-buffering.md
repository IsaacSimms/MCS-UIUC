---
question: |
  You realize that you should have used total ordering in the previous timeline (Q2). Total ordering uses a sequencer, which is a new process not included in the three processes shown above. Fortunately for you, while this is an asynchronous system, you can assume that (i) the above timeline shows the relative physical times of multicast send events, and (ii) the latency between any process Pi and the sequencer is zero (note that other process-to-process communications still have latency, as shown above). Commander Brand asks you to list all messages that will be buffered at each of the processes. Please show your full work; don't just give lists or counts of messages.
researched: 2026-10-25
confidence: confident
versions:
  - "CS 425 / ECE 428 Fall 2026 Lecture 16 (Multicast), L16.FA26.pdf": "Final on the Fall 2026 lecture page; PDF CreationDate and ModDate Thu Oct 22 09:32:15 2026 CDT; 62 pages. Course page dates that session 2026-10-15 and links this file as the multicast deck."
  - "CS 425 / ECE 428 Fall 2026 Homework 3, hw3.fa26.pdf": "Out 2026-10-12, due 2026-11-01 23:59 US Central. Local file and the same PDF at the Fall 2026 course site. Figure measured on a 160 dpi raster of page 3 (1360×1760)."
  - "CS 425 / ECE 428 Fall 2026 Lecture 16-b (virtual synchrony), L16-b.FA26.pdf": "PDF ModDate Thu Oct 22 09:33:56 2026 CDT. Checked only to rule it out."
  - "CS 425 / ECE 428 Spring 2026 Homework 2": "Due 2026-03-11. Used only for that semester's figure convention about omitted self-messages. Not the Fall 2026 problem."
---

# Which Q2-timeline messages does sequencer total order buffer?

## Answer

NHX buffers **E2, S2, and its own N2**. Earth buffers **nothing**. Saturn buffers **N1, its own S2, and N2**.

Nothing is held because its sequence number is late. With zero sequencer latency, every process learns `<M, S(M)>` at the physical send time of M, which is at or before the payload arrives on a drawn arrow. A payload is buffered only when it is already in hand and it is not the next undelivered sequence number. Held messages are delivered, in sequence order, at the later instant when the missing predecessor is delivered.

Sequence numbers follow the left-to-right order of the six send events: **E1 = 1, N1 = 2, S1 = 3, E2 = 4, S2 = 5, N2 = 6**. The sender is in the multicast group, and the figure draws no self-arrow, so each sender receives its own payload at its send event. That self-copy still waits for the sequencer rule. E1, N1, S1, and E2 are the next number at their senders, so those four self-copies are delivered at send time and are not buffered. N2 at NHX and S2 at Saturn are not the next number, so those two self-copies are buffered.

### Figure, in send order

Times below are horizontal pixel positions on a 160 dpi raster of homework page 3. Only order is an input to the algorithm. The gaps that decide buffering are all larger than about 13 pixels, and the two close shafts at Earth (S1's arrival versus E2's send) stay separate components.

| Message | Seq | Send x | Payload arrivals on drawn arrows | Held where |
|---|---|---|---|---|
| E1 | 1 | E ≈ 298 | NHX ≈ 330, S ≈ 610 | nowhere |
| N1 | 2 | NHX ≈ 427 | S ≈ 500, E ≈ 552 | S only |
| S1 | 3 | S ≈ 693 | E ≈ 730, NHX ≈ 1125 | nowhere |
| E2 | 4 | E ≈ 743 | NHX ≈ 841, S ≈ 1105 | NHX only |
| S2 | 5 | S ≈ 845 | E ≈ 860, NHX ≈ 996 | NHX and S (S is the sender's own copy) |
| N2 | 6 | NHX ≈ 882 | S ≈ 954, E ≈ 1104 | NHX (own copy) and S |

### NHX

Local counter starts at 0. Sequence announcements for all six messages are already known by the time each payload is received.

1. **E1** arrives at ≈ 330, sequence 1. Counter is 0, so deliver immediately. Counter = 1. Not buffered.
2. **N1** is NHX's own send at ≈ 427, sequence 2. That is the next number. Deliver at the send. Counter = 2. Not buffered.
3. **E2** arrives at ≈ 841, sequence 4. The next number is 3 (S1), which has not arrived. Buffer E2.
4. **N2** is NHX's own send at ≈ 882, sequence 6. Still waiting for 3. Buffer N2.
5. **S2** arrives at ≈ 996, sequence 5. Still waiting for 3. Buffer S2.
6. **S1** arrives at ≈ 1125, sequence 3. Deliver S1. E2, S2, and N2 are already buffered and are now the next three numbers, so deliver them at this same instant in that order: E2, then S2, then N2. Counter = 6.

Buffered at NHX: E2, N2, S2.

### Earth

1. **E1**, Earth's own send, sequence 1, at ≈ 298. Deliver at the send. Counter = 1.
2. **N1** arrives at ≈ 552, sequence 2. Next number. Deliver. Counter = 2.
3. **S1** arrives at ≈ 730, sequence 3. Next number. Deliver. Counter = 3.
4. **E2**, Earth's own send, sequence 4, at ≈ 743. S1 was already delivered at ≈ 730, so E2 is the next number. Deliver at the send. Counter = 4.
5. **S2** arrives at ≈ 860, sequence 5. Next number. Deliver. Counter = 5.
6. **N2** arrives at ≈ 1104, sequence 6. Next number. Deliver. Counter = 6.

The only close pair is S1's arrival (shaft meets the Earth rule at x = 730) and E2's send (separate shaft meets it at x ≈ 743). S1 is left of E2, so Earth never holds E2. Every payload at Earth arrives in sequence order. Buffered at Earth: none.

### Saturn

1. **N1** arrives at ≈ 500, sequence 2. Sequence 1 has not arrived. Buffer N1.
2. **E1** arrives at ≈ 610, sequence 1. Deliver E1, then deliver the buffered N1. Counter = 2. E1 itself is not buffered.
3. **S1**, Saturn's own send, sequence 3, at ≈ 693. N1 was delivered when E1 arrived at ≈ 610, so S1 is the next number. Deliver at the send. Counter = 3. Not buffered.
4. **S2**, Saturn's own send, sequence 5, at ≈ 845. The next number is 4 (E2), which has not arrived. Buffer S2.
5. **N2** arrives at ≈ 954, sequence 6. Still waiting for 4. Buffer N2.
6. **E2** arrives at ≈ 1105, sequence 4. Deliver E2, then the buffered S2, then the buffered N2. Counter = 6.

Buffered at Saturn: N1, S2, N2.

## Findings

- The Q3 figure is the Q2 multicast timeline printed at the top of homework page 3. Problem 3 says to reuse it, with a sequencer that is not one of NHX, Earth, or Saturn. — [T1] CS425 Fall 2026 Homework 3, problem 3 (`hw3.fa26.pdf`, page 3; same file at https://courses.grainger.illinois.edu/cs425/fa2026/hw3.fa26.pdf)
- Assumption (i) makes left-to-right order of the multicast **send** events physical time. Assumption (ii) sets latency between any Pi and the sequencer to zero, and the parenthesis keeps every other process-to-process latency equal to the drawn arrows. — [T1] CS425 Fall 2026 Homework 3, problem 3 (`hw3.fa26.pdf`, page 3)
- "Between any process Pi and the sequencer" is what makes the problem solvable: the sequencer is not drawn, so its messages are not the arrows. Both directions of that channel are the zero-latency exception. Otherwise the arrival time of `<M, S>` would be unspecified. — [T1] CS425 Fall 2026 Homework 3, problem 3 (`hw3.fa26.pdf`, page 3)
- Fall 2026 multicast slides, marked Final, are `L16.FA26.pdf` (course lecture page, Multicast Communications, 2026-10-15). Virtual synchrony is a separate deck, `L16-b.FA26.pdf`, and the lecture page says virtual synchrony is not in the syllabus for on-campus and Chicago students. — [T2] CS425 Fall 2026 lectures page (https://courses.grainger.illinois.edu/cs425/fa2026/lectures.html)
- Receive means the multicast layer got the message; deliver means the upcall to the application. A message that has been received and not delivered is buffered. If Pi sends m, Pi also receives m, because Pi is in the group. — [T2] L16.FA26.pdf, "Receive vs. Deliver" slide (page 6 of the deck)
- Sequencer algorithm used here: Pi sends M to both the group and the sequencer. The sequencer keeps S, initially 0; on receiving M it sets S = S + 1 and multicasts `<M, S>`. Pi keeps Si, initially 0, and on receiving M from Pj buffers M until both `<M, S(M)>` has arrived from the sequencer and Si + 1 = S(M). Then Pi delivers M and sets Si = Si + 1. The slide asks why the second condition is needed, which is the out-of-order hold. — [T2] L16.FA26.pdf, "Sequencer-based Approach" (deck page 29; image of that slide checked, not only the text extract)
- The same deck's previous slide says the sequencer assigns contiguous sequence numbers 1, 2, 3, … so a process can wait for a missing number. — [T2] L16.FA26.pdf, "Problem with the First Cut Approach" (deck page 28)
- Because Pi-to-sequencer latency is zero, the sequencer receives each send in the physical send order and assigns 1 through 6 in that order. Because sequencer-to-Pi latency is also zero, `<M, S(M)>` is at every process at that same send instant. Condition 1 of the hold-back rule is therefore already true whenever a drawn payload arrives. — [T1] Homework 3 problem 3 (`hw3.fa26.pdf`); [T2] L16.FA26.pdf deck pages 28–29
- The payload that the hold-back rule calls "M from Pj" is the group multicast, not a second copy inside `<M, S>`. The rule names those as two receives. The drawn arrows are the only positive latencies the problem leaves in force, so they are the payload arrivals. If `<M, S>` itself delivered a zero-latency payload to everyone, every process would observe sends already in order and the drawn arrows would not change the buffer. — [T2] L16.FA26.pdf deck page 29; [T1] Homework 3 problem 3 (`hw3.fa26.pdf`)
- The figure has exactly twelve message arrows: two leaving each of the six sends, one to each other process. The right-pointing arrowheads at the ends of the three rules (x ≈ 1176) are the time axes, not messages. No arrow returns to its sender. — [T1] Homework 3 page 3 figure, measured on the 160 dpi raster `/tmp/hw3-figs/hi-3.png` (from `hw3.fa26.pdf`)
- Transcription of those twelve arrows, arrowhead at the receive end, x on that raster. A line that crosses a rule and continues is not a receive.
  - E1 at E x ≈ 298 → NHX x ≈ 330 (arrowhead on NHX) and → S x ≈ 610 (arrowhead on S).
  - N1 at NHX x ≈ 427 → E x ≈ 552 (arrowhead on E) and → S x ≈ 500 (arrowhead on S). The S-bound arrow crosses Earth near x ≈ 462 and does not end there.
  - S1 at S x ≈ 693 → E x ≈ 730 (meets the Earth rule and does not continue above it) and → NHX x ≈ 1125 (arrowhead on NHX). The NHX-bound arrow crosses Earth near x ≈ 906.
  - E2 at E x ≈ 743 → NHX x ≈ 841 (arrowhead on NHX) and → S x ≈ 1105 (arrowhead on S).
  - S2 at S x ≈ 845 → E x ≈ 860 (upward arrowhead on E, nothing above that point) and → NHX x ≈ 996 (arrowhead on NHX). The NHX-bound arrow crosses Earth near x ≈ 920.
  - N2 at NHX x ≈ 882 → E x ≈ 1104 (downward arrowhead on E) and → S x ≈ 954 (arrowhead on S). The S-bound arrow crosses Earth near x ≈ 918.
  Labels sit beside the sends and are slightly left of several vertices (E1 label ≈ 268–291, S1 label ≈ 654–677, S2 label ≈ 810–836). Vertices above were taken from the shafts, not from the label ink. — [T1] Homework 3 page 3 figure (`hw3.fa26.pdf` raster)
- Send order by those vertices is E1, N1, S1, E2, S2, N2. The tightest send gaps on the raster are S1 ≈ 693 versus E2 ≈ 743, and S2 ≈ 845 versus N2 ≈ 882. Neither pair overlaps. — [T1] Homework 3 page 3 figure (`hw3.fa26.pdf` raster)
- At Earth, S1's shaft hits x = 730 on the rule and drifts left as it goes down toward S1. E2's shaft hits x ≈ 743 and drifts right toward Saturn. On the row just below the Earth rule they are disjoint components. S1 is therefore received at Earth before E2 is sent, which is why Earth does not buffer E2. — [T1] Homework 3 page 3 figure (`hw3.fa26.pdf` raster)
- At Saturn, N1's arrowhead (x ≈ 500) is left of E1's arrowhead (x ≈ 610), which is left of S1's send (x ≈ 693). That is why N1 is buffered and S1's own copy is not. E2's arrowhead (x ≈ 1105) is right of both S2's send (x ≈ 845) and N2's arrival (x ≈ 954), which is why those two wait for E2. — [T1] Homework 3 page 3 figure (`hw3.fa26.pdf` raster)
- At NHX, E1 (x ≈ 330) precedes N1's send (x ≈ 427), which precedes E2 (x ≈ 841), N2's send (x ≈ 882), S2 (x ≈ 996), and S1 (x ≈ 1125). After N1, the next required number is S1, so E2, N2, and S2 wait until S1 arrives. — [T1] Homework 3 page 3 figure (`hw3.fa26.pdf` raster)
- Spring 2026 Homework 2, question 1, says that for its FIFO/causal figure, messages a process sends to itself are omitted and "are received and delivered instantaneously (at the same time when the sender issues the multicast)." That sentence is a different semester and a FIFO/causal question. Read as a blanket delivery rule, it contradicts Fall 2026 L16, which delivers a received multicast only when it is the next sequencer number. Fall 2026 wins. What is kept from the older homework is the diagram convention that an omitted self-copy is received at send time. Delivery of that copy still uses the Fall 2026 hold-back rule. Without a self-receive, Saturn could never deliver S1 and so could never deliver sequence numbers 3 through 6, and NHX could never deliver N2. — [T2] CS425/ECE428 Spring 2026 Homework 2, question 1 (https://courses.grainger.illinois.edu/cs425/sp2026/assets/hw/hw2.pdf); [T2] L16.FA26.pdf deck pages 6 and 29
- A web-search snippet of L16.FA26.pdf added a bullet, "You don't have to send the actual payload to sequencer (just message id is enough)." That sentence is not on deck page 29. The slide image and the text extract both say the sequencer multicasts `<M, S>` and the receiver waits for M from Pj and for `<M, S(M)>`. The snippet was discarded. — [T2] L16.FA26.pdf deck page 29

## Recommendation

Use the three lists above, with the per-process walk, as the worked solution. Include the two own-message holds (N2 at NHX, S2 at Saturn). The tradeoff is that a reader of the Spring 2026 FIFO/causal figure note might treat every own message as delivered at send time and drop those two from the lists. That reading fights the Fall 2026 sequencer slide: the sender does receive its own multicast, and that receive is delivered only when it is the next sequence number. E1, N1, S1, and E2 happen to pass that test at send time; N2 and S2 do not.

## Ruled out

- ISIS-style total order, where receivers propose priorities and a sequencer (or the ISIS protocol) later confirms a final priority. Spring 2026 Homework 2 question 2 is that algorithm. Fall 2026 problem 3 names the sequencer, and L16's implementation slide is the `<M, S>` hold-back, not proposed priorities.
- Virtual synchrony (`L16-b.FA26.pdf`). Separate deck. The Fall 2026 lecture page says it is not in the on-campus/Chicago syllabus. It is not the algorithm problem 3 describes.
- Delivering `<M, S>` itself as a zero-latency payload and ignoring the drawn arrows. That empties every buffer and makes the timeline irrelevant. The slide treats M-from-Pj and `<M, S(M)>` as different receives, and problem 3 keeps the drawn latencies.
- Buffering a message only because its sequence number has not arrived. Under assumption (ii) the sequence number is present from the send instant, and every payload arrival is at or after that instant.
- Causal or FIFO hold-back from problem 2. Problem 3 replaces that rule with sequencer total order. A message can be delivered here in an order causal delivery would reject, as long as every process uses the same sequence.
- Local notes at `Distributed Systems - CS425/Week7/Lesson 2 Multicast/Lec2&Lec3ImplementingMulticastOrdering.md` and `Lec1MulticastOrderingNotes.md`. They restate the L16 sequencer bullets. They were not used as the source of any claim above.
- Coulouris/Dollimore/Kindberg/Blair section 15.4 is the reading listed for this lecture. The section text was not retrieved, so no textbook contradiction is recorded. See open questions.

## Open questions

- The assigned textbook section 15.4 was not fetched. If that section forwards the multicast only through the sequencer, it is a different algorithm from L16, and L16 would still be the one to follow. That check was not done.
- No instructor Q&A (Piazza or otherwise) was read. Nothing at tier T3 confirms or contradicts the own-message holds.
- E1's two shafts meet the thick Earth rule over roughly x = 291–305, and E2's arrowhead meets the Saturn rule over roughly x = 1100–1120. Both spreads stay on the same side of every comparison used above. A redraw that needs an exact delivery tick, rather than the buffer set, would still have that few-pixel slack.
