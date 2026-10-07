# Consensus Problems: An important distributed computing problem

## The lecture's hook
Cloud providers offer five 9s, seven 9s, etc. SLA and never 100% uptime. Not because of engineering slack but because of the impossibility of consensus in a distributed system.

### The consensus problem
- all servers receive all updates at the same time in the same order (reliable multicasts)
- keep their own local lists where they know about each other and when anyone leaves or fails, everyone is updates (membership detection)
- elect leader and everyone knows leader
- ensure mutually exclusive access to a resource (locking) (mutual exclusion)

#### what is common/consensus
- each server is a "process"
- **all groups of processes are attempting to coordinate with each other and reach agreement on a value of something**

#### attributes
- each process contributes a value. goal is to have all processes decide the same value. decision cannot be changed (agreement)
- validity = if all processes propose a value, thats what's decided
- integrity = decided value must have been proposed by a process
- non-triviality = there is at least one initial system state that leads to each of all the outcomes (0 or 1)

#### Formally 
N processes. Process p has
- input xp, initially 0 or 1
- output yp, initially b (undecided). May be written once.

Design a protocol so that at the end either every process has set yp = 0, or every process has set yp = 1.

## System models
- synchronous: message delay and clock drift are time bound. Consensus is solvable with bound crashes. Each step takes time between a known lb and ub. A bus, a Cray, a multicore chip.
- Asynchronous: no bound on process speed, message delay, clock drift, etc.A general and more challenging architecture to solve these problems under. A consensus protocol that works under asynchronous architectures but not vice versa.
But, asynchronous consensus is impossible to solve. There are worst-cast possible execution with failures and message delays. Powerful result (FLP proof). 
Safe and probabilist solutions have become popular for consensus.
