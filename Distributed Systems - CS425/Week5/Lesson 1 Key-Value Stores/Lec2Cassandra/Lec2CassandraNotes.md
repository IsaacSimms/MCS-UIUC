# Apache Cassandra: a distributed key-value store
- designed for distributed data center use
- open sourced later with apache license
- many companies use cassandra in some of their clusters: Netflix, Adobe, eBay, etc. 

## key --> server mapping
- which server stores the key-value pairs
    uses a virtual ring based distributed hash table.
Servers are mapped to points on a ring --> keys get mapped to points on the ring --> keys are stored in the next successor server on the ring
    However, there is no routing (finger) tables. Client sends request for a key to coordinator server --> the coordinator FWDs that request to the appropriate server with that key. 
        The "partitioner" is a tool the coordinator uses to FWD the request to the right server

## Data placement strategies
### SimpleStrategy
use of partitioner
1. RandomPartitioner      = hash partitioning (chord like)
2. ByteOrderedPartitioner = each server is assigned a range of keys.

### NetworkTopologyStrategy
use of multi-DC deployments within the network layer
- two or three replicas of data per DC
At each DC, data replica placed according to the partitioner, then go through servers counter clockwise until you hit a server that is in a different rack.

## Snitches
Maps IPs to racks and DCs
- configured in the cassandra.yaml
- multiple different types of snitches are used.
    - SimpleSnitch (topology unaware)
    - PropertyFileSnitch (uses config file to understand topology)
    - RackInferring (assumes network by octet topology) (a best guess as IPs may not always map to racks/servers exactly
    101.201.231.231 DC --> highest order, then DC, then rack, then server
    - EC2Snitch (uses Ec2)
    - etc.

## Writes
- lock free and fast w/ no reads or disk seeks but, always writable (graceful on failure)
    For always writeable, cassandra uses Hinted Handoff Mechanism.
        When replica is down, coordinator still writes to all other replicas and waits for that down one to come back up. if all replicas down, coordinator buffer writes.
- client sends write to coordinator (this could divvy it up per key, per client, or per query)
- coordinator uses partitioner to send that query to all replica nodes w/ that key
- coordinator sends acknowledgement to client after success

- One write ring per datacenter. 
    there is a per datacenter coordinator which coordinates with other datacenters. 

### Extras that happen while writing to a node.
- logged at the server's commit log
- make changes to **memtables** which are the in-memory representation of key-value pairs
- write to cache as well
- when memtable gets full, flush to disk via Sorted String table. (list of key-value pairs sorted by key)
    Index file: an SSTable containing keys, and their postion in a defined list of SSTables
#### Bloom Filter
- a bit array which will load the SSTable into memory (off heap in modern cassandra) so the check is RAM only.
- a way to represent a set of items.
- checking for existence of an item is cheap
- never false negatives, small probability of false positives

## Compaction
Data updates accumulate, and SStables & logs need to be compacted
- merging SSTables together by newest update what wins for each key
- runs locally on a server

## Deletes
- Items do not get deleted right away. A tombstone gets put on that key-value in the log
- during compaction, key-values with a tombstone get deleted

## Reads
- Similar to writes
- but coordinator contacts X replicas in the same rack and, contact multiple racks.
- latest timestamped value is returned to client
- If a read touches SSTables, it could touch multiple SStables if columns are split across multiple SStables. 

If there is not consistent, a background read repair operation gets initiated to bring all replicas up to the same value.

## Membership
- Any server in the cluster knows about all other servers in the cluster. This list gets updated automatically as servers join, leave, and fail.
- any server can be coordinator

### Gossip-Style
Cassandra uses a gossip style architecture in order to keep this list of servers up to date. 
Cassandra also uses suspicion mechanisms to determine if a server has failed. 
- accrual detector: the failure detector outputs a value (PHI) which represents suspicion. 
- the apps set a threshold based on the arrival time of gossip messages for how long PHI is for detection timeout