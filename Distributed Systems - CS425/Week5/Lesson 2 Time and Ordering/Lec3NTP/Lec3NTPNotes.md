# NTP = Network time protocol. A standard for synchronizing clocks on the internet
- NTP servers are organized into a tree
- each client = a leaf of a tree
- each node synchronizes with its tree parent

child node sends message to parent to stat protocol --> the parent responds with "message 1" & the parent records the time it sends message one (ts1) -->
child records the time it receives the message (tr1) -->  child sends message 2 and records time as ts2 --> parent recieves the message and records time as tr2 -->
Parent sends the values ts1 and tr2 to child --> child uses all four values to set its clock

- Offest o = (tr1 - tr2 + ts2 - ts1) / 2
See offset screenshots

Even with this protocol in place, there is a non-zero error around clock synchronization