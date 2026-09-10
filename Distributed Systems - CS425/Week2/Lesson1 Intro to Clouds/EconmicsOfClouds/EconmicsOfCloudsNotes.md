# How to the economics of clouds works

### remember 
2 types of clouds:
    Public
Service to any paying customer (as long as conditions are meet such as auth)
    Private
Only accessible to employees of that org (that org owns the entire stack)

## Example
Service requires 128 servers with 1024 cores, and 524TB of storage
### Outsource cloud
Old data but AWS costs from 2009:
0.10 per CPU hour
0.12 per GB montStorage = $ 0.12 × 524 × 1000 ~ $62 K
Total = Storage + CPUs = $62 K + $0.10 × 1024 × 24 × 30 ~ **$136 K**
### Own the cloud
Storage ~ **$349 K / M**
Total ~ **$1555 K / M **+ 7.5 K (includes 1 sysadmin / 100 nodes)

**This is just one example. It is not always a given that cloud is going to be cheaper then on-prem. Especially as projects scale and persist**
This is generally true if:
$349 K / M < $62 K (storage)
$1555 K / M + 7.5 K < $136 K (overall)
*Notice, the cloud provider benefits from storage the most*