# Maekawa' algo
- Fixes the problem with Ricart-Agrawala where messages are being sent/received from all processes in the group.
**Process obtains mutual exclusion by asking permission from only a small subset of processes**
(Known as the voting set)
Voting sets are constructed so that any two intersect, and that guarantees that at most 