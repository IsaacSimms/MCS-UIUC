# The bully algorithm
A leader election algorithm in distributed systems

## Definition
- Elects a leader by always preferring the process with the highest id
- all processes know other process' ids
- when a process detects that the coordinator has failed:
If it knows that its own ID is the highest in the system that process elects itself as the coordinator & sends coordinator message.
Else, it sends messages to processes with higher IDs. via an election message. That election message is only sent to processes with a higher ID. (If the message times out with no replies, that process now knows it has the highest ID and elects itself.)
- When a process receives an election message under bully, those "higher id processes then the one that detected the failure. also start their own election messages.
Those election messages are still sent to just processes with a higher ID then itself. 
This includes the failed process, which was the original leader/bully. But that one fails due to the failed process.

## liveness and safety
Bully satisfies safety. It will always elect only the highest-ID non-failed process and all correct processes will agree on it.
It satisfies liceness only in the synchronous model. (timeout can be set to the known worse-case one-way latency (process time + message delay))

