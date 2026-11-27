# Lecture 12.2: NFS and AFS (Distributed File Systems, Lecture B)

Cloud Computing Concepts, Part 2 (Indranil Gupta). CS425 Week 12. Follows Lecture 12.1, File System Abstraction.

(Agent generated)

## TLDR

NFS and AFS are two ways to let many client machines use one shared file server while still looking like a local Unix file system. NFS keeps the server simple (stateless) and makes clients poll for freshness. AFS keeps whole files on the client and has the server notify clients when a file changes (callbacks), which lets one server handle many more clients.

**Stateless server:** a server that remembers nothing about its clients between requests, so every request must carry all the information needed to serve it (file handle, absolute offset, byte count).

## Key sections and what to retain

### 1. NFS design: stateless server and the VFS layer

NFS (Sun, 1980s) makes a remote directory look like part of your local file system, and its main design choice is that the server holds no per-client state.

- The client OS has a **Virtual File System (VFS)** layer. Each open file has a v-node that points either to a local inode or to a remote NFS server, so processes keep using ordinary file descriptors.
- Descriptor state (including the read-write pointer from Lecture 12.1) lives in the **client** kernel. The server sees only file handles and absolute offsets.
- A **file handle** identifies a file on the server: (filesystem id, inode number, inode generation number). The generation number stops a stale handle from silently pointing at a reused inode.
- Requests are therefore self-contained, such as `read(fh, offset, count)`. A repeated read is **idempotent**, so a client that gets no reply simply retries. This is why a server crash is cheap to recover from.
- Cost: because the server keeps no state, it must commit modified data to stable storage before replying to a write.

**Builds on:** the stateful Unix descriptor API from 12.1. NFS moves that state to the client so the server stays stateless.

**Retain:** statelessness gives easy crash recovery and idempotent retries, and the price is slower synchronous writes and no server-side knowledge of who caches what.

### 2. NFS client caching and the freshness rule

Clients cache blocks locally for speed, and since the server cannot tell them when something changed, each client decides for itself whether its cached copy is still good.

- Each cached block stores **Tc** (when the client last validated it) and **Tm_client** (the block's last-modified time as of that validation). The server holds **Tm_server**.
- At time T, with freshness interval **t**, a cached entry is valid if **(T − Tc < t) or (Tm_client = Tm_server)**.
- Check order: if the entry was validated within t, use it with no server contact. Otherwise ask the server for Tm_server. If it matches, keep the cache and reset Tc. If not, fetch the block.
- Typical t is adaptive: about 3 to 30 s for files and 30 to 60 s for directories (Solaris).
- Write policy trade-off: **delayed write** (flush about every 30 s) is fast but not consistent, and **write-through** is consistent but slow.

**Retain:** NFS gives **bounded staleness**, not strong consistency. Another client's write can stay invisible to you for up to t seconds.

### 3. AFS design: whole files and the workload assumptions

AFS is built around measured file usage, so it makes the common case cheap instead of treating every access as equally likely.

- Assumptions: files are small, most files are used by **one client at a time**, reads far outnumber writes, and access is mostly sequential.
- **Vice** is the server and **Venus** is the client process. On `open`, Venus fetches the **whole file** and caches it on **local disk**, where it survives reboots.
- Reads and writes act on the local copy. Changes go back to Vice only on `close`.
- Consistency is **close-to-open**: after a client closes a modified file, the next open elsewhere sees the new version. If two clients write concurrently, the **last closer wins**.

**Builds on:** NFS block caching. AFS caches whole files on disk, which cuts server traffic when most use is single-client.

**Retain:** AFS does not push writes as they happen. It publishes them on close.

### 4. AFS callbacks

Instead of each client repeatedly asking "has it changed?", the server promises to say so, and clients trust their cache until it does.

- When Venus caches a file, Vice records a **callback promise**: it will notify that client if anyone else updates the file.
- On a later open, Venus uses the cached copy with no server contact as long as the callback is intact. When another client closes a modified copy, Vice **breaks the callback** on every other client holding the file, and their next open refetches.
- Cost: the server now keeps **per-client state**. A rebooted client must treat all cached files as suspect and revalidate them, and callback state on the two sides can drift.

**Retain:** the central contrast is **NFS (stateless, client polls, bounded-stale) vs AFS (stateful, server callbacks, close-to-open)**. Callbacks remove most validation traffic, which is why AFS scales better.

### 5. NFS vs AFS side by side

|                    | NFS                                       | AFS                          |
| ------------------ | ----------------------------------------- | ---------------------------- |
| Server state       | Stateless                                 | Stateful (callback promises) |
| Cache unit         | Blocks, in client memory                  | Whole files, on client disk  |
| Freshness          | Client polls, `T − Tc < t` or Tm match | Callback broken by server    |
| Update visibility  | Within about t seconds                    | After the writer closes      |
| Concurrent writers | Interleaved at block level                | Last closer wins             |
| Strength           | Simple, easy crash recovery               | Scales to more clients       |

Measured result (Howard et al. 1988): NFS is slightly faster at low load, with a crossover at about load 3–4. At load 18, NFS server CPU is saturated near 100% while AFS sits near 40%.

**Retain:** the difference is a trade between server simplicity (NFS) and scalability through fewer server round trips (AFS).

## Recap

- Both systems present a remote file server through the normal Unix file API.
- NFS: stateless server, file handles with absolute offsets, idempotent retries, client-side caching with the freshness rule `(T − Tc < t) or (Tm_client = Tm_server)`.
- NFS consistency is bounded staleness, not strong consistency.
- AFS: Vice (server) and Venus (client), whole-file caching on local disk, writes sent back on close, callbacks instead of polling.
- AFS consistency is close-to-open with last-closer-wins.
- Statelessness buys crash simplicity and callbacks buy scalability, and each pays for it with the other's weakness.
