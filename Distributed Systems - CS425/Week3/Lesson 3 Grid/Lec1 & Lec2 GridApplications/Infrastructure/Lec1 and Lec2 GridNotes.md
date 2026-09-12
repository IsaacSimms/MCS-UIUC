# The grid
- developed in the 1990s
- Its the stiching together of many high performance machines. storage, instruments, networks, etc. 
    An end user treats it, and uses it, as one single computer.
    Common in scientific computing and HPC (high performance computing)

- The grid can leverage and wire together machines from many different sites, and many different form factors (workstations, clusters, etc.)
- Use multiple resources at multiple different sites concurrently
- It's a shared high-end infrastructure that is usually used by multiple orgs

## Grid applications
- Grid applications are the workloads that consume the grid resources
    Weather modeling (RAMS), collider analysis, genome pipelines are examples
- The application/process is broken down into jobs. 
    - Some jobs need to be run concurrently
    - Other jobs take in outputs from other jobs as input, and output information for other jobs to take in (and by extension need to be run sequentially)
    - Jobs are connected via directed acyclic graph (dag)
    - Some jobs can be long lasting
    - Each job can be split into many tasks. 
        Tasks are run on a single processor/machine

## Grid scheduling
This makes scheduling one of the difficulties of job applications. Multiple jobs need to be scheduled and managed within a single site, and multiple sites need to be scheduled/managed

### 2-level scheduling infra
#### each site runs an intra-site protocol (runs the site) ("lower")
example include HTCondor protocol (high-throughout condor)
scheduling what job happens on what machine/processor within that site
Responsible for monitoring jobs, handling job failures, and publishing the files for specific jobs

##### HTCondor
high-throughput computing
a class of cycle-scavenging systems
    runs on a lot of workstations
    when a WKS is free, asks the central server(the global protocol) for tasks
    if a user interacts with that WKS in some way, stops tasks, but can also be run on dedicated machines

#### One of the sites also runs a "global" (inter-site) ("lower") protocol which is used to manage the orchestration between sites
- this is usually a standardized protocol, Globus protocol is a common example (i will refer to globus, but there are other global protocols)
- scheduling which job happens at which site
- Inacts transparency, meaning the internal structure of each side is invisible to globus, and globus does not care. 
- Responsible for external allocation of resources and tasks
    Talks with schedulers at each site, but does ont schedule the actual jobs on each machine.

##### Globus toolkit
- an open-sourced tooling kit maintained by a variety of orgs
- Contains:
    GridFTP = wide-area transfer of bulk data
    GRAM5   = submit, locate, cancel, and manage jobs (not a scheduler. the lower protocols do that)
    RLS     = naming service which translates from fire/dir name to targer location
    GSI     = Grid security infra
    Libraries
    Grid IO functionalities
- security is a major concern for grid architectures
    no one org owns the grid (federated)
    tooling such as SSO, mapping to local sec mechanisms, community auth, and delegation are used
        Delegation = cred/auth are inherited by subcomputations
        SSO        = one auth for the job across the distributed system

