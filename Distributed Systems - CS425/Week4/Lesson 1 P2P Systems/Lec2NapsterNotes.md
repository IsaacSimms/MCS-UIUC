# Notes about the internal details of the widely-developed P2P system, Napster

## Napster Structure
- On the control plane, Napster has a hub & spoke architecture. Each peer (client machine) registers with the Napster servers and interacts with the system via that registery.
The Napster servers hold teh directory like filenames, IP address info, ports, metadata. Servers do not store the data.
- On the data plane, it is *not* hub & spoke though. Files live on the collection on peer nodes. A TCP transfer between a requestor peer and a hosting peer is established to transfer data.
That data transfer doesn't go through Napster servers. 
That is what makes it P2P

## Napster search
- Client sends query up to servers -->
- Servers search their metadata lists using a ternary tree algorithm searching for the file -->
- Over TCP, the found metadata about which peers have the file the querying peer is looking for (candidate peers) -->
- The querying peer pings the candidate peers directly, searching one for effective bandwidths to transfer the file -->
- A first candidate peer that is found which has the bandwidth to transfer the file, does so.

## A peer joining a P2P system
Any P2P has tooling around this
- New peer sends request (a DNS query) to a specified URL for that service -->
- After DNS, message is routed to an "introducer", a server with a specific role which keeps track of some recently joined nodes in P2P system -->
- Introducer initializes new peers' into the neighbor table

## P2P system problems
- Centralized servers are bottleneck for congestion
- centralized servers become failure hotspots
- security is hard in this architecture, things like plaintext messages and passwords are common