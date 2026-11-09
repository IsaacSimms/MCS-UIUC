# Structure of networks in distributed systems
Note: This topic is *not* about networks as in networking. "Networks" under this context refers to a network/graph, as in the way to organize data. 
## Network/graph definition
A network (also known as a graph) is a set of nodes (vertices) which are connected together via a set of edges. 
The vertices is the *thing* that has state. (the user in a social media platform's graph).
The edges are the *connections* which intertwine those vertices. (the following/follower relationships between those users on that same platform)
There are multiple different attributes that can make a network complex: 
- Structural: the scale is huge
- Evolution: The vertices and their relationships are constantly changing over time
- Diversity: some vertices prompt many more edges then others, some edges are far more important then others, etc. 
- Node complexity: Vertices themselves can be complicated entities
- Emergent phenomena: Simple end behavior can have systemtic, complex system-wide behavior

Many systems (particularly distributed ones and or/natural ones) are modelled as graphs. Networks are large, dynamic, and emergent. 

### Two notable network properties
- Clustering coefficient (CC)
How likely it is that two neighbors of a node are themselves connected 
Given that nodes A, B, and C are the nodes in question:
CC = Probability(A - B edge | A - C edge and C - B edge)

- Path length
The number of edges in the shortest path between two nodes.
Common to take this measurement, averaged over all the pairs.
Short path length = can get to any other node in the system in a small number of hops. (with long path length meaning the opposite)

- this is also where the connection archicture can be defined:
    - Extended ring (also known as lattice)
    Nodes are arranged in a circle w/ each node connecting to its nearest neighbors on the other side (and potential for connection with a few other nearby nodes)
    High CC but paths are short. Local clusters get built but it is far/inefficient to traverse the accross the whole network.
    - Random graph
    The same number of total nodes and edges as in a lattice. But, every edge is placed completely at random. 
    This includes no preference to nearby nodes. 
    This causes the CC to be low, but paths to be short. Does not build clustering architecture but random long-range edges causes any two nodes to be reachable within a couple hops. 
    - Small-world networks
    Initialized and largely maintained as a lattice. But, small fraction of local edges are rewired to distant nodes (could be over time)
    High CC *and* short paths.

## Small world networks
- Initialized and largely maintained as a lattice. But, small fraction of local edges are rewired to distant nodes (could be over time)
High CC *and* short paths.

- Common for naturally evolved networks to come out this way
- Networks that grow incrementally w/ a preferential model of growth then to follow this architecture. 
grow incrementally = built over time by adding one node and its edges, one after the other. (as apposed to all nodes and/or edges appearing all at once)
Preferential model of growth: A rule stating that when a new node arrives it connects to an existing node (v) with probability proportional to v's current degree (number of neighbors)

### Definition of degree (under the small world network context)
Degree of a vertex = number of its immediate neighbor vertices. 
Degree distribution = probability of a given node having "k" edges
    k = num of edges a node has (degree)
    tail = the right hand side of a degree distribution. The probability of nodes with a large k
        A light tail means almost no nodes in the system have a high degree. 
**Types of degree distributions**
- Regular graph = every node has the same k
- Gaussian = most nodes have near some average of k, with a tail that falls off quickly
- Random graph = exponential decay, e ^ -ke
    Light tail. Degree is concentrated around a typical value; the chance of a node with degree much larger than average drops exponentially fast. No real hubs.
- Power law = k ^ *a*
Heavy tail. Most nodes still have a small k but the probability of a high degree falls polynomially.

Note: A lot of small world networks are power law graphs
MOst nodes have a low degree, but a few hubs have a very high degree. 
(Think social media network)
Random node removal leaves the giant component intact. Targeted removal of high-degree nodes rapidly disconnects the graph.

## Dynamics on networks
When a system is "dynamical" the state changes over time according to fixed rules (Such as differential equations or iterative updates)
Common for small world networks to involve dynamical systems
When each node is a dynamical system coupled to its neighbors, system wide phenomena such as self-synchronization can imerge. 