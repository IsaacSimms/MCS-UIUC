# Analysis of both the push and pull based gossip protocols

## Push protocol

### Claims:
    Is lightweight even in large groups
    spreads multicast messages quickly
    fault-tolerant

### Analysis / Theory 
Theory of this protocol is from the Epidemiology branch of mathematics
- Population of (n+1) individuals mixing homogeneously (each n is a node essentially)
- contact rate between any individual pair is beta
- Contact between infected and uninfected nodes turn the uninfected node into infected

### Differential equation for push protocol
see Distributed Systems - CS425/Week3/Lesson1 Gossip/Lec3GossipAnalysis/differentialequation.png
    Population of nodes = **n + 1** processes
    x = uninfected
    y = infected
    at all times **x + y = n + 1**
    At the start x_0 = n, y_0 = 1
    Homogeneous mixing: every pair of processes contacts as a Poisson process at rate **β** (beta)

#### The equation
see .png but:
**dy/dt = -beta(xy)**
xy = number of infrected-uninfected pairs
each pair contacts at rate of beta
each event drops x  by one

### Epidemic Multicast
Remember, there are protocol rounds and b random number of targets get message per round

In epidemic multicast, 
**beta = b / n**
Consider one particular infected node and one particular uninfected node. The probably that the one infected node picks the one uninfected node is the probably that the uninfected node is one of the b targets.
(an easier way to understand it would be each gossip period the infected node draws b targets uniformly from the other n processes)
