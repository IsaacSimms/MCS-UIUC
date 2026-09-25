# The magic value of "X" specified alongside every read or write query
How do you set this value of x? Enter the:

## Cap Theorem
**The idea**: In a distributed system, you are able to satisfy at **most** 2 out of the following 3 guarantees:
- Consistency: all the nodes in the system are seeing the same data at any time (i.e. reads return the last written value by any client)
- Availability: the systems allows operations 24/7/365 and those operations are quick (all keys anytime)
- Partition-tolerance: the system works regardless of network partitions (two networks that cannot talk)

### Availability
read/writes can happen all the time.
This is important bc any increase in latency is very poor for the user experience.
Milliseconds of latency felt by the client equates to huge loss in revenues, so much so cloud provider SLAs revolve around availability

### Consistency
ALl nodes see all the same data at anytime. 
Important for systems that are sensitive to source of truth. (Think things like banking services or flight booking software)

#### Eventual consistency
A weak form of consistency that is used by systems that are opting for strong availability and partition tolerance over strong consistency. 
- If there is not anymore writes to a key, then all values converge over time. 
- If writes to the key continue, the system still attempts to converge on a value within that field, and that leads to a wave like update cycle.
- Can lead to the return of stale values to clients, particularly with many back to back writes.
- But, works well and does not sacrifice the other two prongs of CAP during periods of low writes.

### Partition Tolerance
Partitions in networks can happen within a datacenter itself for multiple reasons. (hardware, DNS, etc.)
You want a system to function for the end user and be resilient to these failures.
If you where to think in small scales this might not seem important but it becomes vital as you start to scale. 

### CAP notes
In today's cloud environments partition-tolerance is so vital, you are essentially implying that a system must choose between availability and consistency. (small hardware failures can lead to relatively small network partitions but without partition tolerance, you end with catastrophic failure)
- Cassandra chooses a weak consistency for strong availability and partition tolerance. (Cassandra uses eventual consistency)
- Traditional SQL RDBMSs choose strong consistency and partition tolerance over availability

The real world validity of CAP theorem is what has lead to the  rise in NoSQL architectures.

*RDBMS provides ACID (Atomicity consistency, isolation, and durability). Key value systems like cassandra provide BASE ("basically aviliable soft-state eventual consistency) w/ availability > consistency*

## The value of x in Cassandra
ack = acknowledge
Remember what x means: the corrdinator in cassandra fans out to N replicas that own the key a client is querying for. When the first **X** number of those servers ack, the coordinator acks the client. 
You are essentially going to be playing with the CAP guarantees by changing the value of X.
Cassandra allows the client to choose a consistency level for each operation (read/write) i.e. choosing what X equals:
- ANY: any one server ack, could not be server w/ replica. fastest (high availability low consistency)
- ALL: all replicas must ack before acking the client. (slowest but strongest consistency)
- ONE: At least one replica w/ the key-value (faster then ALL but still cant tolerate failure)
- QUORUM: a quorom of acks from all replicas in all datacenters are gathered before acking the client.

### Quorum = majority (50%)
Lets say that 5 replicas have a given key-value. At least three out of those 5 replicas need to ack to the coordinator, then the coordinator will ack to the client. 
This is regardless of teh topology of the distributed system.
When using Quorum the client specifies a value of R (less than or equal to the total number of replicas). R determines the read consistency level that the system cares about.
In turn, the coordinator waits for R replicas to respond before acking the client. 

Quorum is a nice way to do this piece of architecture, faster then ALL but better consistency then ANY or ONE.
They are a popular design decision in key-value NoSQL stores.

In Cassandra the QUORUM consistency level across the whole system applies to all replicas in all datacenters. 
Next, there is also LOCAL_QUORUM: The quorum in the coordinator's DC, which is faster bc it only waits for first DC client contacts
Lastly, there is also a EACH_Quorum which outlines that each DC has its own quorum. 

This supports each datacenter doing its own quorum along with the larger system, including hierarchial replies.

