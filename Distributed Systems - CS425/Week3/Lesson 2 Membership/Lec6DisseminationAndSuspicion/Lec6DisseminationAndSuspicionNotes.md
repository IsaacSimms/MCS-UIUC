# Bring together failure detection, dissemination, and add suspicion to membership list priors

Dissemination     = the act of distributing information about a detected failure (also distributing info about processes joining and leaving group)
failure detection = the act of determining that a process has failed
Suspicion         = The provisional state where a process thinks that a membership-list entry "might be dead"

## Dissemination

### Multicast
Hardware/IP based multicast
Can be done but generally unreliable and requires multiple simultaneous multicasts


### point-to-point dissemination
TCP / UDP
Can be done but expensive

### Infection-style dissemination
zero extra messages floating around the system
    piggybacks off the failure detection messages

SWIM is an example of this
    The failure detection pings also carry the required dissemination information to each node

#### It is a form of epidemic style dissemination
- The ping/ack messages are going around the system at random (random pj for each pi is chosen each round)
- Each protocol period a node infects a constant number of peers (ping target plus K helpers)
- The tail of the process is bound. after lambda(log(N)), the expected number of nodes that have not seen the update is N^(-2(lambda)-2)
    This leads to every process having a buffer of recently failed, joined, or left processes
    The buffer can piggybacked.
    If a constant buffer size is required, garbage collect the buffer and prefer to remove old entries
- lambda(log(N)) = guarantee of weak consistency 

### Suspicion mechanism
- SWIM can lead to false positive rate that is to high if left unchecked
- False detections that are perturbed or packet losses/congestion. Indirect pinging may not always fix this (common failure when message losses are near the pinging host)
- Suspicion gives teh suspect process time/a change before delcaring it failed

- pi maintains a "state machine" for the pj view element
    This is in pi's membership list
    default is alive
    The state gets moved to suspected upon pj's lack of response to the ping and that info gets piggybacked/dissiminated
    After a timeout, pj's state in the state machine is changed to failed and that gets dissiminated

    pi can determine that pj is actually alive by receiving an ack from it, receiving a ping from it, or receiving a dissemination from other nodes outlining that pj is alive.

- To avoid a suspected process from flipping back and forth alive/dead, process will maintain an incarnation number itself
    the incarnation number for pi can only be incremented by pi (when it receives a suspect, pi message)
    similar to DSDV
    higher incarnation numbers over-ride lower ones when dissiminated
    failed incarnation overides everything else
