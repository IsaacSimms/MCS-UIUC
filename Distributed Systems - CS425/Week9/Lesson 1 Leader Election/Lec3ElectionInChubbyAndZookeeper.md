# Leader election in Chubby (google architecture) and Zookeeper (Apache architecture)
Both systems use different forms of consensus style approaches to solve leader election.
Generally, prod systems are paxos like.
They are *safe* but *eventually live*
Both Google's Chubby and Zookeeper fall under this category

## Chubby
A distributed lock system from google.
Internal google storage systems such as BigTable and Megastore rely on chubby for file locking and writing configuration files.

### election in chubby
Involves a small, locked replica group with exactly one master (at all times).
A an election protocol is required to elect that master
- potential leader tries to get votes from other servers in the group
- each server votes for at most one leader
- server with majority votes becomes new leader and informs other servers.
#### safety
A majority vote + intersecting quorums give safety.
Leader must have majority votes, any two quorums of servers are going to have interasections and any one server can only vote once, meaning two leaders cannot be elected.

#### Eventually live
In practice elections take a few seconds.
Paxos style, protocol termination is not guaranteed since failures may mean no server ever gets elected.

#### Leases
leases = after an election finishes other servers promise not to run another election "for awhile" (a period of time.)
awhile = a set period of time, usually a few seconds, that time duration is called the "master lease"

Master lease can be renewed by master as long as it continues to win a majority during election.
lease technique promotes automatic re-election when master fails.

## Zookeeper
A centralized configurations and coordination service. (maintain config information across distributed system).
Requires a leader at all times.

Uses a variant of paxos (Zab = Zookeeper Atomic Broadcast) for leader consensus.
Common realization lets each server create a new id (called "sequence number"). The highest id among the servers becomes the leader.
To account for failures, each process monitors only the server with the next highest id.
If a server is monitoring the leader and the leader fails, that server becomes the leader

### Fast leader election
Zookeeper default for choosing a new leader
1. Every server with no leader enters a *LOOKING* state
2. in that state, server increments logical clock and votes for itself, proadasting a vote containing:
- its server id
- highest transaction id
- current election epoch
3. when a diff server's vote is receieved the server will compare:
- highest epoch wins
- then highest transaction id wins
- then higher server id is tie breaker.
4. if incoming vote is better it changets own vote and rebroadcasts
5. once server has obtained majority votes in current round, that candidate becomes prospective leader and election ends.
6. Zab synchronization / two-phase step is run by new leader 

### Two-phase commit
1. phase one is prospective leader sends a *NEW_LEADER* message to all following servers
2. Each follower accepts proposal and replies with ACK. When leader has gotten a majority of ACKs, the new leader sends *COMMIT* message and then is allowed to resume normal broadcast.