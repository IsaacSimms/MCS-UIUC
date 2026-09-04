# How MapReduce deals with failures in clusters
*This is an extension of previous lectures and will use terminology that is defined elsewhere, such as the YARN componenets. 

## Server side failure
- NMs regularly sends server heartbeats to the RM.
    If the Server fails its heartbeat, the RM will report that to the AMs effected by that server failure. The AMs take action to request new servers or whatever is required of them.
- The NM is keeping track of all applications and AMs running on its server.
    If the task fails while in progress, the task gets marked as idle and restarted.
- AMs regularly sends heartbeats to the RM.
    If the AM fails tis heartbeat, the RM restarts the AM, which then syncs with its running tasks
- RM failure (usually detected by an external process such as ZooKeeper)
    Any production Hadoop/YARN architecture is going to have 2 RMs. One active and one on standby.
    RMs/YARN keep checkpoints. (checkpoints are periodic)
    If the primary RM fails, the system cuts over to the standby RM.'

## Slow servers
- A slow node (server) is often referred to as a straggler
- **A slow node can (and often does) slow down an entire job**
    None of the reduce tasks can start until all map jobs are done (commonly) and the job is not considered completed until the last Reduce job is done. 
    Think "weakest link" here. 
- Stragglers can occur due to Bad disks, network badwidth, CPU, memory, power, etc.

Keep track of the progress of each task currently in flight. Perform a backup (replicated) execution of any task that is considered to be a straggler. 
When first replica is complete, the task is considered done.  *speculative execution*
    This is commonly completed by the AM

## Locality
Locality in this context: 
    Running the Map task on the same machine that already has the input, so you are not dragging the input over the network unnecessarily.
        Remember modern cloud systems hierarchical topology, keep data set on the same rack. 

Both GFS (Google file system, google's distributed file system) and HDFS (Hadoop Distributed file system) oth store three replicas of each chunk. These are typically stored on two different racks for fault tolerance purposes. Then:
    The MapReduce system attempts to schedule a map task on a node that contains a replica of the input data. 
        If that fails, it attempts to schedule the task on teh same rack as that node.
            If that fails to, the MapReduce system will schedule that task anywhere it can.
Generally, you will set up the Reduce Tasks on the same Racks as the corrisponding Map tasks but its a less concrete process. 
