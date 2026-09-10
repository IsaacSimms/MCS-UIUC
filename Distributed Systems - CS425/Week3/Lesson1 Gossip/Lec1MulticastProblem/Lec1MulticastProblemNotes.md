# Gossip (epidemic) protocols

## The multicast problem
Gossip protocols are designed to fix the multicast problem. THere is technically a "multicast protocol" which is a form of gossip
- Multicast: A distributed group of nodes (either connected to the network or a host on the internet) is present, and one node has information that needs to be communicated to all nodes
- All nodes need to be able to communicate. Could be computers on the floor of the stock exchange or machines on the imaging rack of an enterprise hardware depo
- More then one node could have information that needs shared.
- More restrictive then somelike a broadcast protocol. Broadcast says all nodes get this thing. Multicast says this specific set of nodes who can interact with this protocol get this thing.
- The multicast protocol sits at the application level, not dealing with the underlying network (although that app level protocol often talks network such as IP multicast)

### Fault-tolerance and scalability
Mode nodes my drop packets or crash as they receive information from the multicast sender. (this is particularly true when there are 1000s of nodes)
Multicast protocol must not fail across all nodes because of one faulty node
The protocol needs to be scalable and not incur some crazy overhead as that scale increases

### Centralized
There is a sender and there is recipients
The sender uses a for or a while function style looped execution in order to go through all recipients
Sender sends UDP/TCP packets to recipients
    user datagram protocol        = connectionless and unreliable way of transporting messages
    Transmission control protocol = connection oriented protocol way of transmitting messages
#### problems
overhead on sender is very high
if sender fails (such as crashing during that for loop) it all comes down
This topology causes latency as one sender has to send to more recipients. More recipients, longet it takes. Causes **O(N)** complexity causing scaling troubles for all tree topologies 

### Tree-Based
The multicast protocol develops a spanning tree across all nodes
There is still a sender that will begin the message disbursement but some nodes that have already received the message are able to pass it to new nodes.
    A node will receive message from predefined parent node and send it to their predefined children nodes
    Tree topologies use either acknowledgements (ACKs) or negative acknowledgements (NAKs) to understand when multicast hasn't been received. Both ACK and NAK cause O(N) overhead
Examples include IPMulticast (network level) SRM, RMTP, TRAM, TMTP (application level)
    SRM (Scalable Reliable Multicast)
        Uses NAK
        uses random delays to avoid NAK storm
    RMTP (Reliable Multicast Transport protocol)
        Uses ACK
        ACKs only get sent to designated receivers which re-transmit the multicast
If the tree is balanced, you can get a complexity of **O(log(N)**
#### problems
Setting up the tree and maintaining that tree can be complicated and constant
Nodes that are close to the root sender and critical failure points
