# Solving consensus in Synchronous system

## Assumption
Remember: These systems involve bounds on message delays, clock drift, and processor speeds.
Consensus is reached in these systems by crash-stopping out of bound processes
- Reliable channels inside the bound. A message sent in a round by a process that does not crash in that round arrives in that round.

## Algorithm (conesus in these systems)
Notes:
- all processes operate in rounds of time
- algo proceeds in f + 1 rounds using reliable communication to all non failed members
- Values_i^r = set of proposed values know to p_i at the begininng of round r
- Values^0_1 = {}; Values^1_i = {v_i}
for round = 1 to f+1 do
    multicast (Values^r_i − Values^{r−1}_i) // iterate through processes, send each a message
    Values^{r+1}_i ← Values^r_i
    for each V_j received
        Values^{r+1}_i = Values^{r+1}_i ∪ V_j
    end
end
d_i = minimum(Values^{f+2}_i)

With at most f crashes and bounded delay, every process runs f + 1 rounds, each round multicasting only the proposed values it has learned since the previous round and unioning whatever arrives before the timeout. After round f + 1 every surviving process holds the same set, so taking the minimum is a common decision. f + 1 rounds are required because each round can lose a value only if the process holding it crashes. 

## Why consensus attributes hold
- Termination. No wait for crashed processes after round bound
- Validity: set contains only propposed values
- Agreement: after f + 1 rounds every correct process has the same set, so the same min.

Proof by contradiction. Suppose two correct processes end with different sets. Some value v reached one and not the other. Walk backward: v crossed a process that had it and failed to deliver it onward. 
That process must have crashed in that round, otherwise the synchronous send would have landed. Each such loss costs a distinct crash, and the chain can be stretched across f+1 rounds. 
That is f+1 crashes. Bound is f. Contradiction.
So f rounds are not enough. An adversary crashes one process per round and can keep a value off one survivor until the end. Round f+1 is the round that cannot contain a new crash.