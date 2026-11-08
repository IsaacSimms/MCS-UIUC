# Distributed Graph processing

## Graph Definition
Graph = a data structure consisting of a set of vertices (nodes) and a set of edges (connections) that connect pairs of vertices. 
Edges my be direted (one-way) or undirected (two-way) between nodes. 
Edges can optionally carry's weights and/or labels.
Do no get graphs confused with plots. Graphs require a network style (interconnected) topology

## Distributed Graph processing defintion
Analyzing graphs to large to fit on a single machine by partitioning their vertices across a cluster of servers. 
Each server repeatedly performs local updates on its vertices (i.e. gather neighbor values, applying a computation, scattering the results). 
This is done until the algorithm converges. 

### Graph processing operations
- need to derive proprties and info from graphs
- need to summarize graphs into statistics
- need matching
- etc.
Graphs become very large and difficult to process (especially on one box) quite quickly 
