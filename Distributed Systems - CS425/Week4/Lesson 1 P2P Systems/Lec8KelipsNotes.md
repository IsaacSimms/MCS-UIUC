# Kelips: P2P system with constant lookup cost in a distributed has table
-  does not use a virtual ring like chord/pastry. 
- this system uses an "affinity group" (k) architecture
    k = square root of N
    each peer is hashed to an affinity group.
        Use same hashing algorithm as other architectures then take modulo k on that value. That returned value is what decids which affinity group the peer should go in.
    Each peer is apart of exactly one group.
    Each affinity group holds nodes who's ID is within a defined  range.
- A node knows about all other peers in its affinity group *and* one contact node from each of the other affinity groups.

## File and Metadata architecture
- Files get stored at whichever peer uploaded the file to begin with (like Gnutella, not like chord or pastry)
- Metadata like a hashed name of the file and a pointer to the peer that contains that file, is stored within the entire affinity group.
    Metadata needs to be periodically refereshed from the source node.
    Timeout of metadata impleemented to prevent issues bc od churn.
### Lookup
- Sorta like the reverse process of storing a file. Hash the file name you are looking for --> use that hashed name to locate the affinity group which contains the file (uses the contact peer) -->
Contact peer routes that request to the peer with the file
- Churn of the contact peer can cause more round trips on queries, increasing time complexity
- Lookup memory cost is O(square root of N)

### Membership lists
- Nodes maintain gossip-based membership list of all the peers within their affinity group
- Nodes also maintain a membership list for the peers across all affinity groups
- Dissemination timeframe about membership lists is O(log(N))

