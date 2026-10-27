# Process leader election in distributed systems

## Definition
In a group of processes, elect exactly one non-fault leader for special coordination tasks and make every non-faulty process agree on the leader's identity. 
"Leader is responsible for coordinating replicas.
Systems such as Apache Zookeeper and Google's Chubby require leader election, and NTP server architectures.
That election must satisfy:
- safety (a faulty process is never elected and there is never more then one process elected)
- liveness (eventually terminate w/ a leader)
This should be independent of the process that starts the election, and must re-run if a leader crash is detected by a failure detector.

This definition is the goal of election algorithms

## System model (assumptions) of election algorithms
- There are "N" processes
- Each process has a unique ID
- messages are *eventually* delievered
- failures may occur during the election protocol and the system needs to be tolerant to such failures. 

### assumptions for calling a leader election algorithm
- any process can call an election
- a process can call for at most one election at a time
- multiple processes can call for a leader election simultaneously (and still yield a single leader)
- the result does not depend on which process called it.
- at the end of an election protocol, the non-faulty process with the best (Highest) election attribute is the one that gets selected. 
Common for protocols to use largest ID, could also use IP address, fastest CPU, most disk space, etc.

