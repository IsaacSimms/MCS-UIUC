# The multiple choice questions section from practice exam:

1. In an asynchronous system, which of the following is TRUE?
a. Messages are not delayed beyond a pre-fixed known latency
b. Clocks of different processes are synchronized to within a known bound
c. Failures are not allowed to occur
d. None of the above

Answer: d
|                   | Synchronous  | Asynchronous |
|-------------------|--------------|--------------|
| Process step time | known bounds | no bound     |
| Message Delay     | known bounds | no bound     |
| Clock drift       | known bounds | no bound     |

a and b are synchronous assumptions and c is orthogonal to timing models.

2. A Mapreduce task is running on a cluster with 4 racks, each with 2 machines.
The machines are named as S<rack number><machine number>: S11, S12, S21,
S22, S31, S32, S41, S42. A Map task needs to access as input a block that has
replicas on machines S21, S22, S41. Where will the task be scheduled, if the only
free containers in the cluster are available at the following machines: S11 and S42
a. S11
b. S42
c. Somewhere
d. Nowhere – this task cannot be scheduled

Answer: d
This has to do with how map tasks are scheduled once a container is free. (not a property of the job and does not apply to reduce jobs) When the scheduler is scheduling a task, it will attempt to do so in this order:
- Node-local: Schedule task on machine that stores replica (all busy in this example)
- Rack-local: Schedule task on same rack, as replica *diff machine* (S41 is in rack 4, same rack as machine S42 which has the replica)
- Off-rack: anywhere else that has a free container at the time in which the task is needed

3. A datacenter run by an upstart company called DataStones consumed about 100
kWh so far in 2015 AD. If only 80 kWh of this 100 kWh was used in running IT
equipment (servers, routers, etc.), then the PUE of DataStones’ datacenter is:
a. 0.8
b. 1.25
c. 1.33
d. 300
e. (100-75)/75 = 0.33
f. None of the above

Answer: b
PUE = Power Usage Effectiveness
The ratio describing how much of a distributed system's power usage is consumed by IT equipment (servers, storage, network gear) vs the entire systems consumption. 
That also includes things like cooling, lighting, etc. Always above 1.
PUE = total facility energy / IT equipment energy

4. A BitTorrent client C is trying to download a file with four blocks 0 through 3. C
is talking to three neighboring nodes (clients) A, B, D. Client A currently is
storing blocks 0, 2, 3; while B is storing blocks 0, 1, 2; while D is storing blocks 2,
3 only. Which blocks should the client C fetch FIRST?
a. 0
b. 1
c. 2
d. 3

Answer: b
Under BitTorrent, a local rarest-first methodlogy is used for downloading/fecthing content from clients.
BitTorrent does not pull blocks in their order and does not prefer the most plentiful/available block.
It prefers the piece fewest neighbors have, so that piece does not vanish from the neighborhood.

5. In a system of three processes sending unicasts, an event e1 has a vector
timestamp of (1, 2, 30) while an event e2 has a vector timestamp of (0, 2, 301).
Which of the following statements is TRUE?
a. e1 happened before e2
b. e2 happened before e1
c. e1 and e2 are concurrent
d. We can’t tell what the causality relation between e1 and e2 is

Answer: 
Vector timestamping:
- Each process keeps one vector, each slot in the vector is a proccess clock. PRocess has a slot for its own events.
- ANother proccess's slot counts how many of that process's events this process heard about through messages.
- On local event or send: increment own slot. 
- On receive: take the max of your own vector and the message's vector, slot by slot. *After* that, increment your slot. **A process never bumps someone else's slot except by taking that max from a message**
- Comparing two events: Walk the slots. 
    If every slot of vector a is less then or equal to vector b, and at least one is strictly less, a happened before b.
    If vector A is strictly ahead in one slot and vector b is strictly ahead in another, they are concurrent. (each vector has seen something the other has not)
    Notes: A tie in one slot is irrelevant. Every slot does not need to be strictly larger or smaller to make event timeline comparision. Equal vectors in every slot = same event. Does != concurrency.

6. In Hadoop, which of the following entities is responsible for scheduling
decisions?
a. AM
b. RM
c. NM
d. M&M
e. All of the above

Answer: b (resource manager)
Hadoop is an open source implementation of MapReduce (leveraging a distributed file system).
Job is split into map and reduce tasks. YARN acts as orchestrator, placing those tasks in containers on cluster machines. 
- AM (Application master): There is one per job. Communicates with RM for containers, tracks the job's tasks, and restarts failed tasks. 
- RM (resource manager): One per cluster. Decided which free container is given to which request. *Considered the scheduler in Hadoop*
- NM (Node manager): One per machine. Launces and monitors containers on that machine after RM assigns it to them. Does not choose which tasks runs. 

7. A set of Cassandra clients uses the QUORUM consistency level for both reads
and writes. Then, assuming no failures:
a. Once a client C has received an ack for a write W, any subsequent reads by
C will see the value written by W or subsequent writes
b. Once a client C has received an ack for a write W, any subsequent reads by
any client will see the value written by W or subsequent writes
c. Both above statements are true

Answer: c
- Cassandra is a DynamoDB style replicated key-value store architecture. A corrdinator node sends each read or write request to replicas of that key. 
The client then picks how that node w/ the replica communicates with them/answers.
- QUORUM = the minimum number of replicas that must answer a read/write request before the operation counts as done. **In cassandra that number is a majority of nodes w/ replica... N/2 + 1 nodes
- As it relates to the question: The client that sent a read/write will not receive an ack of that action until a majority (QUORUM is reached) of nodes with that key have received and execution on that operation. 
Therefore, after the client receives the ack for that operation: any future read/write on that key, by that initial client or anyone else, will hit at least one node that has received the initial operation, once this future operation gets QUORUM as well. 
Therefore both answers are correct.

8. Which of the following statements is TRUE about MapReduce/Hadoop?
a. A Reduce task writes its data into the distributed file system (HDFS).
b. Each Reduce reads its input from exactly one Map task.
c. A Map task reads its input data from the native file system.
d. A Reduce task reads its input data from the distributed file system (HDFS)

Answer: a
- Map reads from HDFS
- Map Writes to mappers local disc
- *Shuffle*
- Reduce reads from all mapper's local disc with a key partition is is assigned/looking for
- Reduce writes to HDFS
- There is a shuffle between the map and reduce steps. This is to group together all the values with the same keys (regardless of which map task those keys came from). Reducer pulls one partition form every mapper

9. Which of the following systems prefers availability over consistency, under
partitions?
a. Cassandra
b. HBase
c. A traditional relational database (e.g., MySQL).
d. None of the above

Answer: a
| System                               | Under a network partition             |
|--------------------------------------|---------------------------------------|
| Cassandra, Riak, Dynamo, Voldemort   | Availability. w/ eventual consistency |
| HBase, HyperTable, BigTable, Spanner | Consistency. w/ may reject request    |
| Traditional RDBMS (MySQL)            | Consistency over availability         |

10. A modified gossip protocol uses a spanning tree to get the multicast to half of the
processes. This takes O(log(N)) time. Thereafter you have the choice of either pull
or push gossip. Which will complete faster, i.e., reach a given fraction of infected
processes with the same given probability, but earlier?
a. Push
b. Pull
c. Both complete at about the same speed (or time)

Answer: b
Push finishes a tail sooner under this gossip protocol for multicast. 
At fraction $f$ infected, a random contact is useful with probability $1-f$ for push and $f$ for pull.
From $f = 1/2$ upward, push's hit rate falls and pull's rises. A push mostly lands on a node that already has the message.
 An uninfected node pulling almost always lands on one that has it.