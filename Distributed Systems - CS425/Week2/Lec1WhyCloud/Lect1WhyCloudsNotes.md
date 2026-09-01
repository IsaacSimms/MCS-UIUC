# Aspects that distinguish Cloud Computing from other (largely previous) versions of distributed systems

### Note
Cloud computing is large, and expected to grow
Significant portions of IT spending, enterprise running out of it, government reliance, etc. 
There are many different cloud providers, as we know. Some of which have different specializations
The big three public cloud (and gov) providers:
- AWS
- Azure
- GCP
VMWare (specialty in cloud computing but largely virtualization)
Cloudera
Salesforce
RightScale
etc.

### Service types using AWS as an example (definitely not a complete list)
Popular services, using AWS as example:
- EC2 (Elastic Compute Cloud): This is AWS's VM solution for a server with a full OS and all the goodies - people spend alot of money on these. Often pay per CPU hour used.
- S3 (Simple Storage Service): Data storage largely for backups, data lakes, logs, ML databases, etc. Often to pay per GB stored. 
- Lambda: AWS's event and function driven processing. Ranks high in usage and mindshare. Customers like it for glue code, automation, etc. But, its relatively cheap to run.
- EBS (Elastic Block Storage): BLock storage, used alot for access by EC2
Couple other service types:
- Google's app engine: this is a platform as a service (PaaS). You give google an application (the actual code, or a container if you choose).
Google runs your application on runtimes that **they** manage. And, they manage the underlying infrastructure.
- Azure Container App: A container app in Azure is essentially a serverless container host. You bring a container image, Azure runs that container closer to bare metal with Kubernetes running under the hood. 
What I mean by "Closer to the metal" is there is no OS or server layer that you as the customer are interacting with.

### There are two main categories of served Clouds
#### Public Cloud
- A public cloud will provide a service to any paying customer. (AWS or Azure will give you a VM in a public cloud tenant regardless of how you are.
As long as you are willing to pay for it.)
- Public does not mean "anyone has acccess to your stuff". Auth, network boundaries, security, etc. are all still in place.

#### Private Cloud
- Private clouds are only accessible to that org's employees.
- Azure provides cloud infrastructure to the US government. That cloud compute/storage is inaccessible to anyone outside of that ecosystem.
- If your company has an on-prem server ecosystem for cloud-like ops, you can think of that as a private cloud. Many companies will have both a private and public cloud.

### Misc why companies like cloud
- From a consumer's perspective, near instantanous access to whatever compute they want. This saves them time becuase they can spin up a VM with a cloud provider
in minutes instead of taking weeks to spin up new hardware internally. This also saves them money. Increase platform costs sure, but the IT savings are usually worth it.
- Startups love cloud compute because they can harness as much compute as they need, sometimes that is **alot**, without having to fork over huge up front costs.
- Relability and fault tolerance baked in for business critical workloads.
