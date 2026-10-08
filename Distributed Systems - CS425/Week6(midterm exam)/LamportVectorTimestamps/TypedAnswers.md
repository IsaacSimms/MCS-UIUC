## Lamport Timestamps
- With Lamport Timestamps: 
In lamport timestamping each process is only holding on to a single slot/integer, tracking only itself. 
1. Local or send: timestamp = previous clock + 1 (increment) A send puts that value in the message
2. Receive: process looks at the local timestamp it already had and comes to the timestamp that came in on the message. Takes whichever is larger, increments it, and that is its new value.

### Lamport Practice midterm question, answer:

P0:
start: 0
Send(M01): 1
Send(M02): 2
Receive(M21): 4
Send(M03): 5
Send(M04): 6

P1:
start: 0
local event(E11): 1
Send(M11): 2
Receive(M02): 3
Receive(M24): 11

P2:
start: 0
Receive(M01): 2
Send(M21): 3
Send(M22): 4
Receive(M31): 7
Send(M23): 8
Receive(M04): 9
Send(M24): 10
Receive(M32): 12

P3:
start: 0
Local event(E31): 1
Receive(M22): 5
Send(M31): 6
Receive(M03): 7
local event(E32): 8
Receive(M23): 9
Receive(M11): 10
Send(M32): 11

## Vector Timestamps
- Vector timestamps are one integer (slot) per process, not a single int like in Lamport.
(P0, P1, P2, P3) = (0, 0, 0, 0) upon initialization

Let's say that P0 sent a message to P1:
1. Local event or send: 
Process who just had the action increments its own slot in its own vector by 1. The other slots are left alone.
That whole vector (post increment) is that events timestamp, and that gets put in the message on send. (not a single int)
So in this example, P0 has its slot incremented.
2. Receive: 
Every process slot in the vector timestamp sent gy P0 is compared to the vector timestamp currently held by P1. 
The highest value is taken for each slot. Then, The process slot of the process that just received the message is incremented.
In this example, P1 has its process slot incremented.

### Vector Timestamp Midterm practice question answer:

P0:
start: 0,0,0,0
Send(M01): 1,0,0,0
Send(M02): 2,0,0,0
Receive(M21): 3,0,2,0
Send(M03): 4,0,2,0
Send(M04): 5,0,2,0

P1:
start: 0,0,0,0
local event(E11): 0,1,0,0
Send(M11): 0,2,0,0
Receive(M02): 2,3,0,0
Receive(M24): 5,4,7,3

P2:
start: 0,0,0,0
Receive(M01): 1,0,1,0
Send(M21): 1,0,2,0
Send(M22): 1,0,3,0
Receive(M31): 1,0,4,3
Send(M23): 1,0,5,3
Receive(M04): 5,0,6,3
Send(M24): 5,0,7,3
Receive(M32): 5,2,8,8

P3:
start: 0,0,0,0
local event(E31): 0,0,0,1
Receive(M22): 1,0,3,2
Send(M31): 1,0,3,3
Receive(M03): 4,0,3,4
local event(E32): 4,0,3,5
Receive(M23): 4,0,5,6
Receive(M11): 4,2,5,7
Send(M32): 4,2,5,8