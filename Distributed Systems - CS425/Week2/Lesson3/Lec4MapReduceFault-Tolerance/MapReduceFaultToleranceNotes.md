# How MapReduce deals with failures in clusters
*This is an extension of previous lectures and will use termonolgy that is defined elsewhere, such as the YARN componenets. 

### Server side failure
- NMs regularly sends server heartbeats to the RM.
    If the Server fails its heartbeat, the RM will report that to the AMs effected by that server failure. The AMs take action to request new servers or whatever is required of them.
- The NM is keeping track of all applications and AMs running on its server.
    If the task fails while in progress, the task gets marked as idle and restarted.
- AMs regularly sends heartbeats to the RM.
    If the AM fails tis heartbeat, the RM restarts the AM, which then syncs with its running tasks
- RM failure (usually detected by an external process such as ZooKeeper)
    Any production Hadoop/YARN architecture is going to have 2 RMs. One active and one on standby.
    RMs/YARN keep checkpoints. (checkpoints are periodic)
    If the primary RM fails, 