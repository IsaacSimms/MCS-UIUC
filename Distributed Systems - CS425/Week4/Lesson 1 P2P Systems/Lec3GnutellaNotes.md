# Gnutella: The first fully distributed P2P system
- no servers, clients (called peers/servents in this architecture) themselves take on that responsibility
- peers store their own files and store peer pointers (IP addresses and other metadata) to other nodes
- creates an overlay graph (bc it is "overlaid on top of the internet)
    each edge in the graph is an internet path

## How search works
- Gnutella architecture "routes" messages based on 5 different protocols for different types of messages
    - Query (search)
    - QueryHit (response to Query)
    - Ping (probing network for other peers)
    - Pong (reply to ping)
    - Push (initiate file transfer)

### Message format
All data fields (other then IP address) are stored in little-endian format

Each query message contains a descriptor header with the follwing info:
- Descriptor ID (unique accross entire system)
- Payload descriptor (what type of message (Ox..))
- TTL (Time To Live) (One Byte) (decremented at each hop between peers. Message is dropped when TLL = 0. Starts between 7-10)
- Hops
- Payload length (number of bytes)
Then the actual payload

Query hit contains the following info:
- number of hits
- Same descriptor ID and payload descriptor
Info abt responder:
- port
- ip_address
- speed
- Result(fileindex, filename, size)
- servant_id(an identifier for the responder)

Every peer keeps track of where they got a query query message from. When a queryhit is returned, it is reverse routed following that path.

### What happens after QueryHit it returned
- requestor selects only the "best" queryhit responder to work with. Then, initiates an HTTP request directly with that responder's ip + port (a push message)
- Responder replies with file packets over HTTP
- reply has a range field, how much of the total file is being sent over in this specific message. Important for picking up the file transfer after a dropped connection
- The requestor and the responder will first try to communicate directly. If that fails, such as due to firewalls, the reverse queryhit path will be used through the overlay to take the same network jumps that produced the queryhit to begin with.
    Responder establishes a TCP connection at IP_address w/ ports specified.

### Avoiding excessive traffic
- the list of recently received messages to avoid duplicates or spam
- query is only FWDed to neighbors
- each query only FWDed once
- QueryHit reverse routed only, until making descriptor ID
- dropping messages that are flooding (beyond TTL)

### Ping-Pong
Used by peers to update membership list

#### Ping
- Flooded out and TTL restricted and done periodically. (find immediate neighborhood) (small 1 or 2 or 3 hop neighbors)
- bc the rate of churn (peers entering and leaving the system) is so high in a P2P system, this happens regularly

#### Pong
- a return to a ping message
- returns to ping with the peer's port, IP address, num of files shared, and num of KB shared.
    numb of files and KB used by neighbors to perfer peers who have shared more