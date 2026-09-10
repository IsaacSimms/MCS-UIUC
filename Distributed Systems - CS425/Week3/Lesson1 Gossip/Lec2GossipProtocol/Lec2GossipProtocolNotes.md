# A continuation of lec 1 - Multicast but, discussing the underlying Gossip protocol

## Notes

Multicast group
    One multicast sender
    One multicast message (gossip message)
    multiple receiver nodes
    You can only have one message and one sender, but you can have multiple multicast groups in an infrastructure

### Push Gossip
Periodically the sender randomly selects a predefined number of recipients (b) and sends them a gossip message (often times UDP)
    b = the gossip fanout
    same nodes could be chosen multiple times
Once a recipient has received a message, it is considered an infected recipient.
    After a recipient is infected, it does the same thing. Sends out b copies of the message every predefined period of time.
    Each node is running its period of gossip independent of the other nodes (not synchronized)

### Pull Gossip
"Query" under this context means a gossip message that a node sends out, asking other nodes for new multicast messages
Nodes periodically poll a few randomly selected processes with a query for new multicast messages that it hasn't received

**Hybrid Pull-Pull variants of gossip also exist**
Usually involve a query going out from a node, with recent multicast messages it has received included within that query