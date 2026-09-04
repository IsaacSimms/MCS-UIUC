# More on the internals of MapReduce and the YARN scheduler

### Externally, to the actual MapReduce process (so, the engineer working on it)
User writes a map function and a reduce function.
submits the job --> gets the result.
Is abstracted away from the parallel/distributed programming work that is going on under the hood.

## Internally, there are multiple moving pieces
Some of those things the user does not see:
    Parallelization of map
    transferring data between map and reduce
    parallelization of reduce
    Implementation of storage for map input, map output, reduce input, and reduce output.
*This forces no reduce task starting before all maps are finished. There is a barrier between the two functions.*
    This is because if a map task is running, there is a chance it produces a <key,value> pair for a key that has already been processed by a reduce function. 
        Not entirely true in all circumstances. You can still have reduce tasks start if you can programatically verify that the currently running map function will not produce a key that is included in the set of keys the reduce task will process.

### MapReduce in Cloud/distributed systems
Parallelization of MapReduce is "easy"/inherent: 
    Each map task is inherently independent from each other.
    All map output records get assigned to their own, independent Reduce task.
        Things like partitioning functions lead to clean load balancing here. for further parallelization needs
    Each Reduce  task is inherently independent from each other.
    The storage:
        Map input goes into a distributed file system, accessable from many different tasks
        Map output uses local file system to that server/computer but the reduce input is able to read from multiple remote disks(local file systems)
        Reduce output is placed back in a distributed file system.

### Process:
**see InternalWorkingsMapReduceProcess.png**
Start:
- Blocks of data in the distributed file system (DFS)
- Each DFS is assigned to a map task
- Those map tasks are assigned out to different servers (a single server can own more then one map task)
- Those servers process the map task, and then assign the Map output to Reduce tasks. (each Reduce task can take map output from more then one server. **Remember, reduce task assignment is based on the keys**
- Each reduce task is assigned to a single server
    Note: the Map output is written to local disk. The Reduce task assignment and subsequent server assignment is a remote read.
- the result of Reduce tasks are written to the DFS.

## YARN scheduler
YARN = Yet another resource negotiator
Used in Hadoop 2.x and onward
In YARN each server is treated as a collection of containers. (a container has the same CPU and RAM)
YARN does not run MapReduce logic, or any other apps. It hands out and manages CPU and memory across many machines. Multiple apps (MapReduce, Spark and more) can share the same cluster of machines under YARN.

There are three componenets to YARN:
- Global Resource Manager (RM)
    "Global Boss"
    Does the scheduling (capacity, FIFO, etc.)
    Decides how many containers an app gets. But does not monitor tasks or run logic.

- Per-server node manager (NM)
    A local YARN agent that lives on each server.
    Tells the RM the server's available CPU/Memory
    Starts the container, kills, it, monitors it, runs heartbeats on it, when told to by RM.
    Runs the daemon and some server specific functions

- Per-application (i.e. the jobs) Application Master (AM)
    The owner of any one specific job.
    Runs the negotiation between the RM and NMs for containers. (its the one that reports to the RM saying I need x size of compute and memory)
    Detects task failures, handles speculations
    Exits when jobs finish and reports that.
