# Notes on this weeks quiz
Nail down Gossip protocols and failure detection

On failure detection, understand how to parse heartbeats and when values in a membership list are going to get updated.
Three fields in the membership list:
The identifier (this is static and used to identify which node the row is about, lets say C for these notes)
The heartbeat count (C increments this, all other nodes copy it when this value is higher then what they already had)
The local clock (this is owned by the node who's membership list this is. This is updated when the heartbeat count is updated)

Understand how different values behave when heartbeat frequency increases/decreases
decreasing frequency = longer gap between heartbeats 
increases false positive rate but decreases bandwidth
and vice versa

Understand how MTTF is calculated
the mean time to failure divided by the total number of servers. Let's say 10,000 machines, the MTTF (mean time to
failure) of a single server is 48 months.

48 / 10,000 = 0.0048 months.
Convert to hours:
0.0048 * 30 days * 24 hours in one day = 3.456 hours