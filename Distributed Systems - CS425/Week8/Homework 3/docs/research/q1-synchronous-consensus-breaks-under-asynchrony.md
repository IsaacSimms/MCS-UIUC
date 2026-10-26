---
question: |
  One of the Earth programmers has written an algorithm for synchronous consensus (the same as that discussed in class), but the data center is asynchronous. Assume messages are reliable but may be delayed arbitrarily.
  i. Identify a step in the round-based synchronous consensus proof (discussed in class) that breaks down when the system is asynchronous, and explain why.
  ii. Give a counterexample with three processes that illustrates how the round-based synchronous algorithm breaks with the asynchronous model due to message delays.
researched: 2026-10-25
confidence: confident
versions:
  - "CS 425 / ECE 428 Fall 2026 Lecture 17 (Consensus), slides L15.FA26.pdf marked Final": "retrieved 2026-10-25 from https://courses.grainger.illinois.edu/cs425/fa2026/L15.FA26.pdf"
  - "CS 425 Fall 2026 Homework 3": "hw3.fa26.pdf, local copy matched to https://courses.grainger.illinois.edu/cs425/fa2026/hw3.fa26.pdf"
  - "Fischer, Lynch, Paterson, Impossibility of Distributed Consensus with One Faulty Process, JACM 32(2), April 1985, pp. 374–382": "sections 1–3 of the PDF linked from slide 19, https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf"
  - "Coulouris, Dollimore, Kindberg, and Blair, Distributed Systems: Concepts and Design, Addison-Wesley, 5th ed., 2011": "course assigns section 15.5.2; the section body was not available and was not used"
---

# One of the Earth programmers has written an algorithm for synchronous consensus (the same as that discussed in class), but the data center is asynchronous. Assume messages are reliable but may be delayed arbitrarily. i. Identify a step in the round-based synchronous consensus proof (discussed in class) that breaks down when the system is asynchronous, and explain why. ii. Give a counterexample with three processes that illustrates how the round-based synchronous algorithm breaks with the asynchronous model due to message delays.

## Answer

The class algorithm is the round-based synchronous consensus algorithm on slides 14–16 of Fall 2026 Lecture 15-A (course Lecture 17, slides marked Final). It assumes at most \(f\) crash-stop failures. Processes run in lockstep for \(f+1\) rounds. A round is longer than the maximum message delay, and the round ends on that timeout. Let \(\mathrm{Values}^r_i\) be the set of proposed values \(p_i\) knows at the start of round \(r\), with \(\mathrm{Values}^0_i = \{\}\) and \(\mathrm{Values}^1_i = \{v_i\}\). In each round, \(p_i\) multicasts only the new values, \(\mathrm{Values}^r_i - \mathrm{Values}^{r-1}_i\), then sets \(\mathrm{Values}^{r+1}_i\) to \(\mathrm{Values}^r_i\) union every set that arrives during the round. After round \(f+1\) it decides

\[
d_i = \mathrm{minimum}(\mathrm{Values}^{f+2}_i).
\]

The slide’s comment says this minimum is a consistent choice, for example by process id. The execution below uses \(v_i = i\), so the minimum value and the minimum process id in the final set are the same decision.

The synchronous proof (slide 16) says that after \(f+1\) rounds every non-faulty process has the same set. It proceeds by contradiction. If non-faulty \(p_i\) has a value \(v\) that non-faulty \(p_j\) lacks, then:

> \(p_i\) must have received \(v\) in the very last round.
> Else, \(p_i\) would have sent \(v\) to \(p_j\) in that last round.
> So, in the last round, a third process \(p_k\) must have sent \(v\) to \(p_i\), but then crashed before sending \(v\) to \(p_j\).
> Similarly, a fourth process sending \(v\) in the last-but-one round must have crashed; otherwise, both \(p_k\) and \(p_j\) should have received \(v\).
> Proceeding in this way, we infer at least one unique crash in each of the preceding rounds.
> This means a total of \(f+1\) crashes, while we have assumed at most \(f\) crashes can occur, a contradiction.

The step that breaks is the else line, **“Else, \(p_i\) would have sent \(v\) to \(p_j\) in that last round,”** read with the later clause that makes the same assumption explicit: **“otherwise, both \(p_k\) and \(p_j\) should have received \(v\).”**

Those lines are valid only because a round is longer than every message delay. In that model, a process that still holds \(v\) at the start of a round and does not crash gets \(v\) to every non-faulty process before the round ends. The else line is how the proof rules out “\(p_i\) already held \(v\) before the last round.” Once that is ruled out, the proof can blame a crash in the last round, then a distinct crash in every earlier round, and count \(f+1\) crashes.

In the asynchronous model there is no maximum transmission delay. The lecture states that directly: no bound on process speed, arbitrary clock drift, and no bound on message delay. The homework keeps the channels reliable, so a sent message is eventually delivered, and drops the bound, so the delivery can sit past any finite round timeout. “\(p_j\) does not have \(v\) when the round ends” then no longer means “the holder of \(v\) crashed before sending it.” The same local view is produced by a correct process whose message is late. The else line does not force \(p_j\) to hold \(v\), the “must have crashed” line does not follow, and the count of \(f+1\) crashes never starts. The opening claim, that \(f+1\) rounds leave every non-faulty process with the same set, is no longer proved.

The delta multicast makes the failure sharper. A value is transmitted only in the round in which it is new. If that one message misses the receiver’s remaining rounds, later rounds do not repeat it.

**Counterexample.** Three processes \(p_1, p_2, p_3\), proposals \(v_1 = 1\), \(v_2 = 2\), \(v_3 = 3\), crash bound \(f = 1\). The code therefore runs two rounds and decides the minimum of \(\mathrm{Values}^3_i\). No process crashes, so the run is inside the bound the proof assumes. Every process ends each round with a finite local timeout and unions only messages that have arrived by then. Two messages are delayed until after the receiver has already written its decision. Every other message arrives during the sender’s round.

| Moment | \(p_1\) | \(p_2\) | \(p_3\) |
|---|---|---|---|
| Start of round 1 | \(\{1\}\) | \(\{2\}\) | \(\{3\}\) |
| Round-1 multicast (the whole initial set is new) | sends \(\{1\}\) to \(p_2\) and to \(p_3\); both copies are held until after those two have decided | sends \(\{2\}\) to \(p_1\) and \(p_3\), both on time | sends \(\{3\}\) to \(p_1\) and \(p_2\), both on time |
| Start of round 2 | \(\{1,2,3\}\) | \(\{2,3\}\) | \(\{2,3\}\) |
| Round-2 multicast (new values only) | sends \(\{2,3\}\). The proposal \(1\) is already in \(\mathrm{Values}^1_1\), so it is not sent again. These messages arrive on time | sends \(\{3\}\), on time | sends \(\{2\}\), on time |
| After round 2, \(\mathrm{Values}^3\) | \(\{1,2,3\}\) | \(\{2,3\}\) | \(\{2,3\}\) |
| Decision \(d_i = \mathrm{minimum}(\mathrm{Values}^3_i)\) | \(1\) | \(2\) | \(2\) |

\(p_1\), \(p_2\), and \(p_3\) are all correct, and each writes a decision. \(p_1\) decides \(1\) and \(p_2\) decides \(2\). The requirement that fails is agreement: non-faulty processes must decide the same value. Both outputs were proposed, so integrity holds in this run, and all three processes do decide, so this run is not a termination failure. The class validity condition (“if every process proposes the same value, that value is the decision”) is not the condition this run breaks, because the three proposals differ. Agreement is enough to show that the algorithm does not solve consensus here.

Walk the broken proof on this run. Let \(p_i = p_1\), \(p_j = p_2\), and \(v = 1\). The final sets differ. \(p_1\) did not receive \(1\) in the last round; \(1\) was its own proposal at the start. The else line says \(p_1\) would then have sent \(1\) to \(p_2\) in round 2. Round 2’s multicast from \(p_1\) is \(\{2,3\}\). The only message that carried \(1\) was the round-1 send, and that message is still in transit when \(p_2\) decides. \(p_1\) never crashes. There is no third process \(p_k\) that died between the send to \(p_1\) and the send to \(p_2\). The proof would need \(f+1 = 2\) crashes to explain the mismatch. The execution has zero crashes, and the decided values still differ.

The same split is what “round length \(\gg\) maximum transmission delay” was ruling out. Any finite timeout the ported code uses can be exceeded by a reliable message. Once that happens, \(f+1\) rounds do not equalize the sets, and the minimum of those sets is not a common decision.

## Findings

- Homework 3, problem 1, asks for one step of the in-class round-based synchronous consensus proof that fails when messages are reliable and delay is unbounded, plus a three-process execution in which the same algorithm fails because of those delays. — [T1] CS425 Fall 2026 Homework 3 (`/home/isaacsimms/Desktop/MCS-UIUC/Distributed Systems - CS425/Week8/Homework 3/hw3.fa26.pdf`; same file as https://courses.grainger.illinois.edu/cs425/fa2026/hw3.fa26.pdf)
- The Fall 2026 consensus lecture is Lecture 17 on 10/13. Its slides are `L15.FA26.pdf`, marked Final, credited to Aishwarya Ganesan with Ram Kesavan and an acknowledgment to Indranil Gupta. Assigned reading is the impossibility paper, sections 1–3, and textbook section 15.5.2. — [T2] CS425 Fall 2026 lectures page (https://courses.grainger.illinois.edu/cs425/fa2026/lectures.html)
- A synchronous system has a bound on message delay, a known bound on clock drift, and a bound on each process step. An asynchronous system has no bound on process execution, arbitrary clock drift, and no bound on message delay. The lecture says a protocol for the asynchronous model also works in the synchronous model, and the converse is false. — [T2] L15.FA26.pdf, slides 10–11 (https://courses.grainger.illinois.edu/cs425/fa2026/L15.FA26.pdf)
- The in-class algorithm tolerates at most \(f\) crashes, runs \(f+1\) rounds with a timeout, and requires the round to be longer than the maximum transmission delay. It uses reliable communication. \(\mathrm{Values}^0_i = \{\}\), \(\mathrm{Values}^1_i = \{v_i\}\). Each round multicasts \(\mathrm{Values}^r_i - \mathrm{Values}^{r-1}_i\) and unions what arrives into \(\mathrm{Values}^{r+1}_i\). The decision is \(d_i = \mathrm{minimum}(\mathrm{Values}^{f+2}_i)\), annotated “consistent minimum based on say, id (not minimum value).” — [T2] L15.FA26.pdf, slides 14–15 (https://courses.grainger.illinois.edu/cs425/fa2026/L15.FA26.pdf)
- The proof claims that after \(f+1\) rounds every non-faulty process has the same set. The else step says that if \(p_i\) has \(v\) and \(p_j\) does not, then \(p_i\) received \(v\) in the last round, because otherwise \(p_i\) would have sent \(v\) to \(p_j\) in that round. The next lines infer a distinct crash in each round, \(f+1\) crashes in all, contradicting the bound \(f\). The backward step states the delivery assumption in words: otherwise both \(p_k\) and \(p_j\) should have received \(v\). — [T2] L15.FA26.pdf, slide 16 (https://courses.grainger.illinois.edu/cs425/fa2026/L15.FA26.pdf)
- Class consensus requires one common decision, written once. The lecture’s validity condition is: if every process proposes the same value, that value is chosen. Integrity: the decided value was proposed by some process. — [T2] L15.FA26.pdf, slides 7–8 (https://courses.grainger.illinois.edu/cs425/fa2026/L15.FA26.pdf)
- In the three-process run with \(f = 1\), proposals \(1, 2, 3\), and no crashes, delaying only \(p_1\)’s round-1 messages past \(p_2\)’s and \(p_3\)’s decisions leaves final sets \(\{1,2,3\}\), \(\{2,3\}\), and \(\{2,3\}\). The minima are \(1\), \(2\), and \(2\). That follows by executing the slide-15 pseudocode; it is not a separate published execution. — [T2] L15.FA26.pdf, slide 15 (https://courses.grainger.illinois.edu/cs425/fa2026/L15.FA26.pdf)
- FLP assumes a reliable message system that delivers every message exactly once, and still allows each message to be delayed arbitrarily long and delivered out of order. The paper makes no assumption on relative process speeds or on delivery delay, and it says processes have no synchronized clocks, so timeout algorithms cannot be used in that model. The theorem is that no consensus protocol is totally correct in spite of one fault: every partially correct protocol has an admissible run that never decides. Partial correctness already includes agreement (at most one decision value appears). — [T1] Fischer, Lynch, and Paterson, JACM 32(2), April 1985, §§1–3 (https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf)
- The lecture quotes that result and points at the same PDF: every protocol for asynchronous consensus has a possible nonterminating execution even with one faulty process. — [T2] L15.FA26.pdf, slide 19 (https://courses.grainger.illinois.edu/cs425/fa2026/L15.FA26.pdf)
- The Week 7 local note writes the same \(f+1\)-round delta multicast and the same decision, \(\mathrm{minimum}(\mathrm{Values}^{f+2}_i)\). Its proof sentence is the slide-16 inference: a value fails to move onward only if the holder crashes, because a synchronous send would arrive inside the round, and \(f+1\) such losses would be \(f+1\) crashes. It does not add a step or a counterexample beyond the slides. — local study note, below T1–T3 (`/home/isaacsimms/Desktop/MCS-UIUC/Distributed Systems - CS425/Week7/Lesson 3 Paxos/Lec2ConsensusInSynchronousSystems.md`), checked against [T2] L15.FA26.pdf

## Recommendation

Use the Answer as the study write-up. For a Gradescope solution, keep two pieces and cut the surrounding lecture summary: quote the else line from slide 16 (“Else, \(p_i\) would have sent \(v\) to \(p_j\) in that last round”) and the “should have received \(v\)” clause, say that both treat in-round delivery as guaranteed once the sender has not crashed, and then give the \(f = 1\) table in which \(p_1\) decides \(1\) and \(p_2\) decides \(2\) with no crashes. Name the broken requirement as agreement.

The tradeoff is which failure to lead with. The run above is the one that matches the question’s wording, “due to message delays,” because the class code ends rounds with a timeout and this run terminates with two different decisions. FLP’s theorem is the surrounding fact that no asynchronous protocol, including any repair that waits out every delay, is totally correct once a single crash is possible. Leading with FLP alone would skip the proof step and the three-process execution the problem asks for. The slides win where they and FLP emphasize different broken properties: the slides’ proof was an agreement argument inside bounded rounds; FLP’s theorem is a termination argument for every protocol.

## Ruled out

- Answering only “consensus is impossible asynchronously (FLP).” That is slide 19 and the assigned paper. Problem 1 asks for a step inside the synchronous proof and for an execution of this algorithm.
- A counterexample that drops or forges messages. The problem states that messages are reliable.
- A counterexample that crashes one process per round. That is the synchronous explanation of why \(f\) rounds are insufficient. It does not use arbitrary delay, and the worked run has zero crashes while staying inside \(f = 1\).
- Treating “round length \(\gg\) maximum transmission delay” as a line of the proof. It is the model assumption on slides 14–15. The proof step that uses it is the else / “should have received” inference on slide 16.
- The FloodSet decision rule that returns a default value when the final set is not a singleton. That rule is a different algorithm. The class decision line is the minimum of \(\mathrm{Values}^{f+2}_i\).
- Older Gupta decks (the 2018 Cloud Computing Concepts lecture and the Fall 2020–2024 CS425 decks) as separate sources. Search excerpts showed the same pseudocode and the same contradiction chain. Fall 2026 `L15.FA26.pdf` is marked Final and is the deck for this homework, so those earlier decks were not fetched after that PDF was read.
- Coulouris et al., 5th ed., §15.5.2, as evidence. The lectures page assigns it. The chapter text was not available. The worked answer follows the Final slides.

## Open questions

- The body of Coulouris, Dollimore, Kindberg, and Blair, 5th ed. (2011), §15.5.2, was not read. If that section names a different line as the critical step, the course priority still follows the Final Fall 2026 slides. This note does not record a contradiction with the book because the book was not opened.
- The lectures page links the 1983 PODS paper (ACM DL `10.1145/3149.214121`) and says to read sections 1–3. The text actually read is the JACM 1985 PDF linked from slide 19. They are the conference and journal versions of the same result. They were not diffed. Nothing in the JACM sections 1–3 changes the slide-16 step or the three-process run.
- The slide comment “consistent minimum based on say, id (not minimum value)” is ambiguous about whether the key is the proposal number or the process id. In the run, each proposal equals its process id, so both readings decide \(1\), \(2\), and \(2\).
