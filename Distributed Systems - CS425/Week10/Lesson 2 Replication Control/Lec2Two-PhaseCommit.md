# Two-phase commits in replication control
Used when a transaction touches objects that are replicated across multiple servers. 
Every server must either commit or abort together. 
Two-phase commit is a protocol that forces this all or nothing decision across replicas.
Atomic commit problem (consensus): guarantee that all participant servers either apply the transaction’s updates or none of them do.

## Why a one-phase commit fails
One-phase commit: coordinator unilaterally decides commit or abort and broadcasts the decision.
- having a single coordinator tell every server to commit the change only works under no failures
- A server w/ corrupted data or one that cannot apply the update cannot intervene. all other servers already committed
- A server can crash after receiving commit message but before writing the updates to a stable storage.

## The two phases of two-phase commit (2PC)
Note: Every server participating gets a change to vote, then the coordinator decides **only** after collecting all votes
1. Prepare. 
Coordinator sends prepare. Each server writes its tentative updates to permanent storage > replies YES (commit) or NO (Abort)
2. Decision
**Every** server voted yes before timeout > coodinator sends commit > servers apply update to disk
If any NO >> coordinator sends abort

## Handling failures
- Crashes and lost messages must not leave some servers committed and others aborted.
- Server crash after voting Yes: tentative updates are already on disk, so recovery can finish the protocol.
- Coordinator crash: decisions and messages are logged; a new coordinator (or the recovered one) can resume.
- Lost Prepare: server times out and votes No (forces abort).
- Lost Yes/No: coordinator times out and aborts.
- Lost Commit/Abort: server repeatedly polls the coordinator until it learns the decision.

## Retain
2PC is how a transaction that spans multiple servers (or replica groups) reaches a single commit/abort outcome.
