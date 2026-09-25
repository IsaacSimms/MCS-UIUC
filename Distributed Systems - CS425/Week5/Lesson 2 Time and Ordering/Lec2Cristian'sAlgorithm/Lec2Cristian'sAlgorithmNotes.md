# Notes about Cristian's Algorithm
It is an algo that uses an external time synchronization methodology for clock syncing.
All processes sync with a time server.

### What can go wrong
- by the time the message is recieved at the processes, time has changed
- inaccurate time sets
- message latencies
- inaccuracy cant be bounded in an asynchronous system

#### fixing these issues
Processe measures the round-trip-time of a message exchange between the time server and the process, and accounts for that during clock synchronization.
(adds minimum transition latency and other known overheads)

zs