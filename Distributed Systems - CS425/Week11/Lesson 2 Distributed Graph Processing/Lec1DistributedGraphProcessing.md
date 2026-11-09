# Distributed Graph processing

## Graph Definition
Graph = a data structure consisting of a set of vertices (nodes) and a set of edges (connections) that connect pairs of vertices. 
Edges my be direted (one-way) or undirected (two-way) between nodes. 
Edges can optionally carry's weights and/or labels.
Do no get graphs confused with plots. Graphs require a network style (interconnected) topology

## Distributed Graph processing defintion
Analyzing graphs to large to fit on a single machine by partitioning their vertices across a cluster of servers. 
Each server repeatedly performs local updates on its vertices (i.e. gather neighbor values, applying a computation, scattering the results). 
This is done until the algorithm converges. 

### Graph processing operations
- need to derive proprties and info from graphs
- need to summarize graphs into statistics
- need matching
- etc.
Graphs become very large and difficult to process (especially on one box) quite quickly 

## Typical flow
- works iteratively
- each vertex is assigned a *value* (& each vertex is assigned to a server)
- Flow (on each iteration, each vertex)
1. Gather = collect current values of all immediate neighbors (vertices who join it directly with an edge)
2. Apply = Does some computation (to get new value) from its own previous value + the gathered neighbor values
3. Scatter = Write the new value and send it to its neighbors
- The process terminates after either a fixed amount or iterations or after the vertices stop changing values.b
- Often times a barrier is implemented to ensure all messages are delivered before the next superstep begins.
**Bulk Synchronous Parallel (BSP)** = a parallel computation model that does the division of work into supersets
In BSP, each super step every processes does these three things (notice that the graph processing steps are present):
1. Local computation (gather + apply work for vertices)
2. Communcation (the scatter messages to other processors)
3. Global barrier applied: no processor is allowed to start the next superstep until every processor has finished the current one and all messages have been delivered.

## Assigning vertices to servers (vertex placement)
- Hash-based: Hash (vertex ID) modulo the number of servers = the vertex's placement
Note: The same consistent-hasing idea used in P2P systems.
Simple and load balanced. 
Remote edges possible
- Locality-based: Assign vertices with more neighbors to the same server as its neighbors.
Cuts cross-server traffic (reducing communication volume.)
Sophisticated partionioning schemes are often requried and costly

## Pregel (google's solution)
- Uses master/worker architecture:
    - Master
Maintains a list of workers.
Monitors those workers and restarts on failure.
Provides a web-UI for monitoring job processes. 
Assigns vertex partitions, drives superstpes. 

    - Worker
Loads partition from master.
Processes the vertices allocated to it.
Communicates with other workers.

- Persistent data in a distributed storage system (common for google to use GFS or BigTable)
- data is temporary stored on disk
- Checkpointing = master periodically instructs works to save state of their paritions to persistent storage. Used for recovery.
- Failure detection = checkpoints and periodic pings back and forth between master and workers.

### Pregel execution flow   
1. Many copies of the program begin executing on a cluster.
2. The master assigns a partition of vertices to each worker; each worker loads its vertices and marks them active.
3. The master instructs every worker to perform one iteration: each worker computes on its active vertices, sends messages (which must arrive before the barrier), and waits at the barrier; when all workers reach the barrier the master starts the next iteration.
4. Computation halts when some iteration ends with no vertices active and no messages still in transit.
5. The master instructs each worker to save its portion of the final graph.

#### speed
Performance example (single-source shortest paths): a 1-billion-vertex tree finishes in ~180 s with 50 workers and ~20 s with 800 workers; 
a 50-billion-vertex instance finishes in ~12 min on 800 workers.