# Chord routing question from Midterm Practice

## Given
This question has three parts.
In a Chord P2P system, there are 256 points on the ring. Six machines join,
with the following peer ids: 1, 10, 100, 150, 200, 250.

### notes
Chord is a p2p system where each peer lives on a virtual ring. That virtual ring has 256 points. (0-255 entries on the ring)
 Each peer sits at its peer ID (its point on the ring. The ring is traveres clockwise.
Important to note that the arc wraps. So any entry after the highest peer in the ring gets wrapped back around to the lowest peer in the ring. (The highest peer's successor is the lowest peer)

## Part a
Indicate the successor entries of each node on the Chord ring.

## Part b
Show the finger table entries of machine with peer id 10.

## Part c
Use the Chord routing algorithm to route a message for key (file id) 2 starting
from peer id 150. There is no file replication, and each peer has exactly one
successor and no predecessors.

