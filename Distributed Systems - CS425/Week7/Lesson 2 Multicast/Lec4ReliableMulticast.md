# Reliability in multicast messaging
## TL;DR
“Everyone receives every multicast” is fine until a sender crashes mid-send. Then some correct processes have the message and others do not. Reliability is orthogonal to FIFO / causal / total: you can stack them. The formal contract talks only about correct processes: integrity (at most once), validity (a correct sender eventually delivers its own multicast), agreement (if one correct process delivers m, every correct process in the group does). Basic multicast — sender unicasts to each member over reliable point-to-point — fails agreement if the sender dies after a prefix. Fix: on first receipt, a receiver re-multicasts m to the whole group, then delivers. One correct recipient is enough to finish the job.

## Reliable multicast
Loosely says that every process in the group receives all multicasts. However, more percisely, need all *correct* (non-faulty) processes to receive the same set of multicasts as all other correct processes.
(Faulty processes are unreliable)
- reliability is orthogonal to ordcering.
- can implement reliable-FIFO, reliable-Causal, Reliable-Total, Reliable-Hybrid (reliable variations of all discussed stacks)

## Implementing reliable multicast
- Assumption: system has reliable unicast (TCP) available
- First-cut: Sender process (of each multicast M) sequentially sends a reliable unicast message to all group recipients
But what if sender fails, some correct processes have received multicast M while others did not receive it.
- That first cut protocol gets extended by receivers "helping" sender.
WHen receiver receives multicast M for the first time, it sequentially sends M to all other processes in the group. (not efficient but reliable)

