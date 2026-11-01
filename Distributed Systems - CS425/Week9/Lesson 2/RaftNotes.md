# Raft: a consensus algorithm for distributed systems

## Defintion
Raft: a leader-based consensus algorithm which revolves around a replicated log of commands.
A collection of servers use that log to execute teh same state machine in the same order, even if a minority of them fail. 


## What a state machine is
A state machine is a deterministic program that keeps some internal state and on receiving a command updates that state and produces an output.
Deterministic program: the state machine's next state andoutput are a pure function of its current state and the command/action it is applying.
In raft:
- state machine starts from a known initial state
- given the same sequence of commands and initial state, it always produces the same sequence of states and outputs (definition of determinism)
- the only way to change its state is by applying those commands in order.

