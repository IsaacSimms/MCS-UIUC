# Define a Cloud

## Note
- Modern cloud computing is very complicated. 
- The scope of the modern cloud is both quite wide and quite deep. 
- There is no single one definitio of what ***"The cloud"*** is.

## the simple, working definition.
*Designed to be good enough to allow us to get into the nuts and bolts, technical stuff around distributed / cloud computing*
**The cloud = Lots of storage + lots of compute nearby**
Important things to consider with this definition:
- Note that the two things are not the other way around (i.e. the definition is not lots of compute with data nearby)
The world we live in, and the cloud compute environment, is data intensive. You can't really move the data around all that easily and you need to bring the comput to it. 
- The above definition is only defining what the core of cloud computing is. There is a huge amount of infrastructure around cloud computing that was not explicitly defined there. 
This includes things like virtual networking, authentication services, Administration and IT style services, hardware services, and much much more.

## What is the cloud? "The cloud = Lots of storage + lots of compute nearby" explained
**Two types**
### A single-site cloud (one datacenter)
- Compute nodes      (the CPUs, GPUs, disks, memory, etc.) these nodes are grouped into server racks. Racks typically share the same switch and power
- Switches           (connects the racks)
- a network topology (wires together the datacenter and outside world) (tree-like hierarchical architecture common within the datacenter. i.e. a switch connects the rack together, then core switches connect the rack switches together.)
- Storage            (nodes that are connected to the network but only do data stores. lots of SSDs)
- Front-end          (sends-receives jobs, client requests, the output of compute, etc. User facing)
- sortware Services  (the software layer that allows all of this to work and serve many different users concurrently. Think the Azure tenant architecture, virtual networking, etc.)
- and more
### Multi-site cloud (many datacenters, geographically distributed)
Each site in the multi-site cloud has all of the above listed things.
But, there are simply multiple sites.
It is common for each site within an organization to have the same tech stack. Same types of hardware, same software used, etc.