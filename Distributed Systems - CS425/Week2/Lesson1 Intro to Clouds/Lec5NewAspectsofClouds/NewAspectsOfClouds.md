# This is a continuation of lecture 4

## On-demand access
Definition:
    Able to purchase or buy compute at any time, and in whatever quantities you want (for the most part)
    Usually charing by CPU hour, GB stored, etc.

## aaS classifications
HaaS: (Hardware as a service)
    Hardware as a service. You get access to the bare metal hardware being provided. Blank box, nothing is provided.
    This would be like you going out and buying your own servers. Except you don't own the server, someone else does. 
    Rare
    Lots of security risks and issues for a public cloud perspective.

IaaS: (Infrastructure as a service)
    The hardware is taken care of for you and usually partitioned through things like hypervisor.
    Consumer still manages things like the OS.
    Flexible computing and storage options. But, without many of the Security issues for the Cloud provider that HaaS has. 
    Virtualization: Software defined version of a physical resource. Multiple isolated environments on the same underlying hardware. You spin up VM on provider hardware.
    Its your VM start to finish, but their hardware. 
    One of the most popular products on public cloud.

PaaS: (Platform as a service)
    Cloud provider takes care of the hardware layer like IaaS, but also takes care of everything sitting on top of the Virtualization layer. You bring your codebase, they run it.
    Lets options as far as how your infra behaves, but less maintenance headache bc the cloud provider does all of the OS updates and all that for you. 
    Similar to IaaS in that you do get some flexible compute and storage options, but more rigid.

FaaS: (Function as a service)
    Function, time bound, event driven processing. 
    You define action (usually code executed or someone alerted or whatever) and trigger (time bound, event happened, etc.) Cloud executes action bc of trigger
    cheap

SaaS: (software as a service)
    You pay for software. The person who makes that software gives it to you.

## Computation-Intensive Computing
Same amount of data but high amounts of computing on or around that data. 
Weather projections is an example.

## Data-Intensive
Crazy amounts of data and often this becomes the bottleneck. 
Compute nodes to work on that data should be nearby to reduce latency

## New cloud programming paradigms
Lots of innovations on how to process data
and some how to move data around, organize it, etc.

MapReduce: Helpful for processing huge amounts of data. Batch processing large datasets in parallel accross a cluster, and orchestrating that processing.
Hadoop: A platform that implemented the MapReduce model at scale and introduced a distributed file system.
MapReduce is an interface, and Hadoop is an implementation.

