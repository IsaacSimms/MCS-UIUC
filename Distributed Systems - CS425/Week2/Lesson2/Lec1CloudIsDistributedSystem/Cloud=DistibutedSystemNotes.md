# Relationship between a cloud and distributed system
(A cloud is a distributed system)

### A cloud:
- hundreds of machines server side
- thousands - millions of machines client side
- servers are networked and interacting with each other
- clients communicate with servers (usually multiple for any one given interaction)
- clients may be able to interact with each other in some circumstances

A group of servers communicating with each other essentially = a cluster i.e. a distributed system
A group of clients communicating with a server is also, by definition, distributed
P2P systems are also distributed

## Remember distinguishing features of Clouds
Massive scale         = many networked machines
on-demand             = client can access server at any time
data intensive        = lots of data are stored in these cloud clusters
Programming paradigms = MapReduce, Hadoop, etc. are all cluster based programming paradigms

"Cloud" has become a nickname for a distributed system in a way.

Core concepts of distributed systems persist through different paradigms and architectures. (Those concepts are what this class covers)