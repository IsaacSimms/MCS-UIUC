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

### Epidemic Multicast analysis
Remember, there are protocol rounds and b random number of targets get message per round

In epidemic multicast, 
**beta = b / n**
Consider one particular infected node and one particular uninfected node. The probably that the one infected node picks the one uninfected node is the probably that the uninfected node is one of the b targets.
(an easier way to understand it would be each gossip period the infected node draws b targets uniformly from the other n processes)
 y = (n + 1) - (1/ n^cb-2)
    Defines a "headcount" of infected nodes after a chosen period of time.
    When c,b are set to small numbers independent of n, within clog(n) rounds (measurement of latency), all but 1 / n ^(cb-2) number of nodes receive the multicast (measurement of reliability)
    each node has tr transmitted no more then cblog(n) gossip messages (measure of lightweight)

#### failure tolerance in epidemic multicast
Packet loss:
    to analyze epidemic multicast with a 50% packet loss, replace b with b/2
        to achieve same reliability as 0% packet loss with 50%, double the amount of gossip rounds
Node failure:
    to analyze epidemic multicast with a 50% node failure, replace n with n/2 and b with b/2
        Same note applies.

##### Failing out early
The failure of nodes  & packet loss happen to all infected nodes all at once, so the gossip message is lost
    possible but improbable
    only take a few nodes being infected for a failing out of a epidemic multicast to be a eal possibility

#### Note
Log(N) is not constant in theory but it is a very slowly growing number. log(1000) = 10 while log(1b) = 30 and the log of all IPv4 addresses is 32
    and tt is common in practice to consider it constant
Both push and pull gossip protocols are not necassrily network topology aware

## Pull protocol
**In all forms of gossip including pull, it takes O log(N) rounds before N/2 get the gossip**
    This is the fastest you can spread a message for both push and pull. (a spanning tree with fanout of constant degree has O log(N) total nodes)
After N/2 rounds get the gossip, pull gossip becomes faster then push gossip
    - (Once more then half the nodes have the gossip, in push gossip, an infected node has a high likelyhood of pushing to a node that is already infected.
    But in pull gossip, after over half the nodes are infected, an uninfected node has a high likelyhood of pulling from an infected node)
    - Equation on this:
    After the "i"th round, let p_i be the fraction of non-infected nodes, Then:
    **p_i+1 = (p_i)^k+1**
    - this is considered a "super exponential where **the second half of pull gossip finishes in O(log(log(N)))

### Topology-aware gossip
Topology-aware gossip is a form of push/pull gossip but with a biased target picker that is defined to target some specific sub group of nodes in some way.
    Common to perfer nodes in your own subnet and rarely try to push/pull over WAN/router

Remember network topology is hierarchical

traditional push/pull problem:
    Random gossip selection --> core routers face O(N) load
network topology-aware push/pull fixes this by:
subnet i, which contains n_i nodes, pick a gossip target that is in your subnet with a probability of (1-1/n_i)
    This leads to a router load of O(1)
    dissemination time of O log(N)
