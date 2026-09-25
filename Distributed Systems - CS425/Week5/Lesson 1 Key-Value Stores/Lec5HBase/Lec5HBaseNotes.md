# A NoSQL System: HBase
- Based on Google's "blob-based" storage system, BigTable. Yahoo! open sourced the technology in the form of HBase.
- Apache project with major users such as meta
- API functions include:
Get/put (row) (by key).
Scan (a row range w/ filter).
MultiPut.
- Consistency > availability under partitions

## Architecture
- Zookeeper: A small group of servers running a consensus protocol. Zookeepers orchistrate the entire system.
- Multiple HRegionServer groups (each group contains a log)
- Each region contains multiple stores (the servers)
- each store has potentially more then one store file, with each store files having an "Hfile"
    Each store also has a "MemStore" which is essentially the RAM of that server, where writes first get written to before going to disk.
- Hadoop distributed file system: HBase also has the same Hadoop distributed file system, seen in other architectures.
- An HMaster server is able to communicate between the zookepers, the HregionServer, as well as the HDFS

### Storage Hierarchy
- An HBase table is split into multiple regions and duplicated accross servers
    The tables get further split into column families, a subset of columns with similar query patterns.
    One *store* per combination of column family plus region.
- The file itself is a SSTable as seen from other lectures
- HFiles are key-value style with some columns having sub fields within them, including key-values and other pieces of data within that one column

## Strong Consistency via logging flow
When clients send a request, it goes to the HRegionServer, which divvy's it up to the proper HRegion based on what keys (there could be multiple keys & HRegions included) the client is looking for.
From there, the who/what/when of that write gets written to the HLog by either the HRegion or the HRegionServer before any of the actual action gets taken to the MemStore of the store itself.
This allows for **Log Replay** for failure recovery. After recovery of a failure, replay any stale logs (uses timestamps to determine what got written and what did not) and add those edits to the MemStore.
### Cross-DataCenter Replication
- There is one master cluster accross the whole system
- Others are slave clusters to that master and replicate tables
- Master synchronously sends Hlogs to slaves
- Coordination amongst all clusters still handled by zookeepers
- Zookeeper has file system for storing control information. (Cluster identification numbers, state information, etc.)