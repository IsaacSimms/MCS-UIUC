# Chord routing question from Midterm Practice

## Given
This question has three parts.
In a Chord P2P system, there are 256 points on the ring. Six machines join,
with the following peer ids: 1, 10, 100, 150, 200, 250.

### notes
Chord is a p2p system where each peer lives on a virtual ring. That virtual ring has 256 points. (0-255 entries on the ring)
 Each peer sits at its peer ID (its point on the ring. The ring is traveres clockwise.
Important to note that the arc wraps. So any entry after the highest peer in the ring gets wrapped back around to the lowest peer in the ring. (The highest peer's successor is the lowest peer)

When a problem is asking for a "successor" of a peer in Chord, it is asking for the next peer clockwise on the ring. That is the successor to any other given peer on the ring. Peers do not store what entries they won necessarily. They won that peer 'x' is my successor, so x owns every entry between me and and it. This as stored as a **successor pointer** within the peer

### Finger table:
A shortcut list that sits on top of the successor pointer. A series of hops to other live peers in the ring. *Hop one is always a successor*. 1, 2, 3, 4, 5, 6, 7, 8,... ids always clockwise. Allows for O(log N) lookup.

The row(finger) is essentially a shortcut for that row as listed above, and the thing that is stored is the peer ID. 

For peer *n* on a ring size of *2^m*, there are m fingers, index d i = 0...m -1.
Distance of row i = 2^i.
start(i) = (n + 2^i) mod 2^m.

**building finger table of a peer:** (using peer 200 as an example)
1. Find the number of fingers in the finger table
log_2(num of points in ring) = number of fingers in table
For this question, there are 256 points on the ring, therefore:

log_2(256) = *8* fingers on the table (256 = 2^8).
These finger table rows are counted starting at 0, so 0-7 in this example.

log_2(x) can be found by doing: 
**log(x) / log(2)

2. Write the aim points (in this case 8) the peer in question asks about.
The aim point is the slot in the ring that row from the table is aimed at.
This is not the final answer, but used to find the owner of that slot.

Let's say the row in question is i. Take 2^i to find the aim point. If the value derived is above the total amount of points in the ring, subtract the amount of points on the ring from the value found to get aim point.
for 200:
Row 0: 2^0 = 1. Therefore, 200 + 1 = 201
Row 1: 2^1 = 2. Therefore, 200 + 2 = 202
Row 2: 2^2 = 4. Therefore, 200 + 4 = 204
Row 3: 2^3 = 8. Therefore, 200 + 8 = 208
Row 4: 2^4 = 16. Thereforem 200 + 16 = 216
Row 5: 2^5 = 32. Therefore, 200 + 32 = 232
Row 6: 2^6 = 64. Therefore, 200 + 64 = 264. 264 - 256 = 8
Row 7: 2^7 = 128. Therefore, 200 + 128 = 328. 328 - 256 = 72
*Final value listed is the "aim point*

3. The finger for a row is the next live peer at or clockwise from the aim point. 201 is the aim point of Row 0, peer ID 250 is the next live peer, therefore that is the value for Row 0 on the finger table. Final answer for the finger table of peer 200 is:
250, 250, 250, 250, 250, 250, 10, 100

### Forwarding a message in Chord
You'll need to be able to: Given a message is coming from peer ID x and is going to y entity, find out the path that the message goes. 
Let's say for an example, peer ID 100 is sending a message to entity 7

- First thing peer 100 is going to do a **successor check**
It will see if the entity that needs the message is between itself and its successor. (in this example, between 101-150) if it is, the peer will fwd that message to the successor as the only hop.

- Next, if that was not possible, the peer (100 in this example) opens up its finger table and throws out any finger that already passed key 7.
In this example, clockwise from 100 and "passed 7" means that the finger is sitting passed 255 (and on the other side of 7 is the owner.)

Basically, any finger pointing to 150, 200, and 250 have not passed seven, but a finger on 10 has.

    *This message eventually needs to land in 10 (closed peer clockwise to entity), but you can not overshoot direct hop to it. The only way to fwd a message to the appropriate peer is successor check*

This all is being done in an attempt to get as close to the entity as possible without going over. Cant go to 10, but go to closest (clockwise) finger on the table.

The finger table of peer 100 is the following: 150, 150, 150, 150, 150, 150, 200, 250.
Closest without going over is 250. **Fwd the message to 250.**

- Now that the mesage is at 250, the same thing happens at 250. 
1. Try to do a successor check. entity 7 is not between 250 and 1.
2. Look at 250's finger table, which is the following: 1, 1, 1, 10, 10, 100, 100, 150. Closest without going over is 1. Fwd message to 1's finger table.

- Now the message is at 1. Do the same thing at 1
1. Do a successor check. entity 7 is between 1 and 10. The message gets FWDed to 10

- final message path in this example is
100 --> 250 --> 1 --> 10


## Part a
Indicate the successor entries of each node on the Chord ring.

1 --> 10
10 --> 100
100 --> 150
150 --> 200
200 --> 250
250 --> 1

## Part b
Show the finger table entries of machine with peer id 10.

1. Find total number of fingers
log_2(number of points in ring) = log_2(256) = log(256) / log(2) = 8

2. Find aim points
Row 0 = 2^0 = 1. Therefore, 10 + 1 = 11
Row 1 = 2^1 = 2. Therefore, 10 + 2 = 12
Row 2 = 2^2 = 4. Therefore, 10 + 4 = 14
Row 3 = 2^3 = 8. Therefore, 10 + 8 = 18
Row 4 = 2^4 = 16. Therefore, 10 + 16 = 26
Row 5 = 2^5 = 32. Therefore, 10 + 32 = 42
Row 6 = 2^6 = 64. Therefore, 10 + 64 = 74
Row 7 = 2^7 = 128. Therefore, 10 + 128 = 138

3. use aim points to find final finder table (on or closest live peer clockwise from aim point)
100, 100, 100, 100, 100, 100, 100, 150

## Part c
Use the Chord routing algorithm to route a message for key (file id) 2 starting
from peer id 150. There is no file replication, and each peer has exactly one
successor and no predecessors.

1. Message starts at 150. Do a successor check at 150. Entity (2) is not between 151-200. So:
2. look at 150's finger table, which is 
Row 0 = 2^0 = 1. Therefore, 150 + 1 = 151
Row 1 = 2^1 = 2. Therefore, 150 + 2 = 152
Row 2 = 2^2 = 4. Therefore, 150 + 4 = 154
Row 3 = 2^3 = 8. Therefore, 150 + 8 = 158
Row 4 = 2^4 = 16. Therefore, 150 + 16 = 166
Row 5 = 2^5 = 32. Therefore, 150 + 32 = 182 
Row 6 = 2^6 = 64. Therefore, 150 + 64 = 214
Row 7 = 2^7 = 128. Therefore, 150 + 128 = 278. 278 - 256 = 22

200, 200, 200, 200, 200, 200, 250, 100
Farthest forward without going over is peer 250. **forward message to peer 250.**

3. message is at 250. do a successor check at 250. Entity (2). is not between 250-1. So:
4. Look at 250's finger table. which is:
1, 1, 1, 10, 10, 100, 100, 150
Farthest forward without going over is peer 1. **forward message to peer 1**
5. message is at 1. Do a successor check at 1. Entity (2) is between peers 1-10.
**Forward message from peer 1 to peer 10 via successor check**

Therefore, the final path the message will take is:
150 --> 250 --> 1 --> 10