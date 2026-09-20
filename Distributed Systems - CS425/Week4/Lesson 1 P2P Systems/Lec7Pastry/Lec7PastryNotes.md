# Pastry: A P2P system that came out of academia
- Assigns ID to nodes using a virtual ring (like chord)
- Uses a **Leaf Set**: each node knows its direct successor(s) *and* its direct predecessor(s) (neighbors on each side) (semi-similar to chords successors/predecessors)

### Pastry neighbors
- the ID assigned to each peer is a series of bits
- uses prefix matching to create a routing table
    To figure out how to route something, a peer is going to look at the ID of neighbor peers. The section at the beginning of the string that match is considered the matching prefix. 
    Peers will route to the neighbor with the largest matching prefix
- Bc routing is based on prefix matching, that logic has a O(log(N)) complexity
    Hops in the underlying network are short
    see "Distributed Systems - CS425/Week4/Lesson 1 P2P Systems/Lec7Pastry/PastryRouting.png"
