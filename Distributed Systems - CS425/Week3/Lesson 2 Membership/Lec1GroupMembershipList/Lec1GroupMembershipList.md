### Failures are the norm
If everything is fine in the software (which doesn't happen) things are always going to fail hardware side
Let's say a full machine is only going to have one piece of hardware fail every ten years (120 months) (which is very optimistic)
And let's say that you have 120
That means your **mean time to failure (MTTF)** is 1 month
12,000 would make the MTTF is now 7.2 hours

If a distributed system does not account for failure you could lead to loss of data, interrupted processes, loss of revenue, corrupted states/data, etc.

### Failure detection
Software ( a distributed program) that detects failures ina process and reports to your workstation

Process in this context is defined as:
    A group-based system:
        Datacenters
        REplicated servers
        distributed databases
    Crash-stop / fail-stop process failures

## The membership list in distributed systems, explained
Each process in the system keeps its own list. Each list is that process's estimate of the system. Failures in the system update that list.
    The list is most, if not all of the other processes running in the system
    That list is accessed by many different applications

    Membership protocol is what keeps the membership list up to date
        The protocol updates the list on departure failure, addition, and when a process leaves
        The protocol usually gives process time to respond when when failure is detected
        Protcol has to communcaiate over unreliable network connection so packets may drop etc.

The "quality of the symantics of the list" can vary based on implementation. Meaning, how complete the list is, how reliably its updated, etc. 
    Strongly consistent membership:
        Complete list of processes that is consistent at all times across all processes in the system.
        example: virtual syncrony. A well known distributed computing paradigm used in production to this day
    Gossip stye, SWIM
        rely on a weakly consistent list

    SCAMP,T-MAN,Cyclon
        rely on partially consistent list

**There are two important sub processes that are integral to the membership list topology, the failure detection and the dissemination**

