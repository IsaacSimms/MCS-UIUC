# Implementations of Gossip in prod settings

## Example implementations
- Clearinghouse and Bayou projects: email and database transactions PODC ’87
- refDBMS system [Usenix ’94
- Bimodal Multicast ACM TOCS ’99
- Sensor networks Li Li et al, Infocom ’02, and PBBF, ICDCS ’05
- AWS EC2 and S3 Cloud (rumored). ’00s
- Cassandra key-value store (and others) use gossip for maintaining membership lists
- Usenet NNTP (Network News Transport Protocol) ’79

## NNTP Inter-Server Protocol
- Each client uploads and downloads news posts from news server
- Each server retains news posts for awhile, transmits them lazily, and deletes them after awhile