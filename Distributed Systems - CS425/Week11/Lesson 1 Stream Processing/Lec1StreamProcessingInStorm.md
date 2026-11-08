# Stream processing in Distributed systems (Storm as architecture example)

## Definition
Stream processing = Continuous computation over an unbounded sequence of tuples that produces incremental results under a low-latency contraint. (rather then waiting for a finite dataset to complete)

## Why Stream Processing 
A good use case for stream processing is when there are large amounts of data that is constantly arriving.
I.e. social media trends, site analytics, intrusion detection, etc.
MapReduce is not a good fit here because MapReduce is a batch processing architecture. (And isn't meant to be continuously running)

## Apache storm
A distributed real-time computation system that processes unbounded streams of data (tuples).
**Low latency and high throughput**
### definitions
- *tuple* = ordered list of fields. 
(username, tweet) or (URL, IP, date, time) etc.
- *stream* = unbounded sequence of tuples
- *spout* = source process that emits streams
(a DB, a crawler, queue, etc.)
- *Bolt* = the subprocess that consumes input streams > performs work > emits new streams.
common in Storm systems that are doing operations such as filter, join, transform
Most of storm is already built and generic enough to apply to any use case. The bolt is what an engineer will write when building a storm system in any given architecture.
Bolts need to be fast because they are processing huge amounts of data.
#### Parallelism vis stream groupings (Parallelizing bolts)
    - Having multiple processes consittue a single bolt
    - Incoming streams are split among the defined tasks
    - Usually a single tuple is not split up, one tuple = one task
    - Three types of groupings are popular
        1. shuffle grouping =  Even, round-robin distribution of tuples accross the bolt's tasks.
        2. Fields grouping = subset of tuple fields get partitioned > all tuplies with the same (defined) key go to the same task
        3. All grouping = every bolt task receives every incoming tuple. (used in joins)
- *Topology* = directed graph of spouts and bolts that constitutes the application
(essentially, the long-running application)
#### Storm cluster architecture
- Master node
Runs a daemon caleld *Nimbus*   
Responsible for:
1. Distributing code around cluster
2. Assigning tasks to machines
3. Monitoring for failures of machines

- Worker node (runs a daemon called supervisor) 
1. run executor that contain actual tasks.
2. runs on a specific machine
3. Listens to master node for work being assigned to its machines

- zookeeper
coodinator between nimbus (master) and worker (supervisor). Stores their state.
tuple = failed when downstream "tuple tree" is not fully processes within a given timeout.
##### failures (anchoring)
**anchoring** = an anchor is an output to one or more inupt tuples (an emitted tuple is liked to one or more other input tuples.)
(Includes above logic and an explicit ack/fail via OutputCollector API)
Used to ensure reliability.
Failure of any anchored descendant causes the root spout tuple to be replayed.
(Forgetting to ack/fail can lead to mem leaks, use well.)