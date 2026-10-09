# What if questions (these are the practice exam ones)

In Gossip-style heartbeating, what if you decreased T_gossip? How does it
affect failure detection time, false positive rate, and bandwidth?

In a gossip-style heartbeating architecture every node contains a membership list. 
Every defined period of time every node will increment its own slot on that list and send it out to other nodes.
It will either send it out to one other node at random, or send it out to a small constant number.
T_gossip is that defined period of time. 

If you decrease T_gossip:
Failure detection time: If T_gossip is decreased nodes are updating and heartbeating their membership lists more often. Failure detection would be faster.

Failure detection false positive rate: Decreasing T_gossip shrinks the T_fail window. Now, a live node's heartbeat is more likely to be delayed or dropped before an observer sees that increase.
Marking that node as failed false positively

Bandwidth: Nodes are sending updated membership lists more frequency, leading to greater
strain on the network and computation.

(This answer is directionally correct, but could use more love to get the causality chain right)

b. Let us say we built a variant of Chord where we did not use finger tables
for routing and instead used only successor pointers? Will lookups be
successful? Why or why not? If yes, what is the lookup latency?

If we are going to take a Chord architecture and use only successor pointers instead of a finger table, you could still get a message from one peer to another peer/entry.
This would be done by The each peer using the successor check to forward the message from one successor to the next.
However, this would drastically decrease the performance of the system. The O(log n) lookup performance achieved by using finger tables is gone. The lookup latency of the Chord system would be determined solely by how many peers there are between the sender and the receiver. 
Worst case is the receiver is the predecessor to the sender, offering a O(N) hops efficiency.

c. In Kelips, what if you modified it to have only 10 (fixed) affinity groups,
but the number of nodes N is still large, and the rest of the system is
unmodified? What is the worst-case lookup cost and memory usage in
this modified system?

Kelips is a distributed hash table that spends memory to make lookups one hop. Nodes/files are hashed into "k" affinity groups. 
There is sqrt (N) (N = num of nodes) affinity groups. 
Every node has a heartbeat counter and contact info on every other node in their affinity node. 
Every node also has the heartbeat counter and contact info of one node in every other affinity group. 

A lookup hashes file to the group. If that is a local group, filetuple table answers directly.
If it is not, the node sends the query to its contact in the target group, which answers from file tubles.

If Kelips only have 10 fixed affinity groups instead of k, lookup would stay at one hop, unchanged.
This is because no matter how many affinity groups there are core kelips functionality remains unchanged. 
Filename still hashes to group id and query is still sent to that group directly if the requested file isn't local. 

But, Kelips is a memory hungry architecture. To answer for a file every node in the group stores the filetuple, and every node stores full membership of its own group in memory.
When there are fewer affinity lists there are more nodes in each list. Meaning to answer for a file, a node has to store a larger membership list in memory. Therefore, the fewer affinity lists there the more memory usage increases.