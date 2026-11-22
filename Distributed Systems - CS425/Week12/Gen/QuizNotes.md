# Quiz notes

## 1. A Unix-style file system read does not specify which offset in the file to start reading from. This is because this file system uses:

**Context.** `read(fd, buf, n)` carries no offset, so the kernel keeps the position between calls. It lives in the open file table entry that a descriptor refers to, and it is advanced automatically by `read` and `write`. `lseek` sets it explicitly.

**Correct answer.** One read-write pointer for each file descriptor, which is automatically advanced upon a read

**Why.** Each `open()` creates its own open file table entry with its own offset, and each `read` advances it by the bytes transferred. A single system-wide pointer would make processes interfere. A pointer advanced only via `lseek` ignores the automatic advance on `read`/`write`. A pointer per file would be shared across separate opens and also depends on `lseek`.

---

## 2. A distributed file system does not typically use read-write pointers. The reasons for this DO NOT include:

**Context.** DFS protocols such as NFS put the offset in each request because servers are stateless. The real reasons are statelessness, simpler servers, and idempotent operations.

**Correct answer.** Read-write pointers are buggy

**Why.** Stateless servers, simpler code with less data at servers, and idempotence are the actual design reasons. `read(file handle, offset, count)` can be retried safely, while a pointer-based read would return different data on retry. "Buggy" is not a design rationale. Pointers are state, and statelessness avoids state.

---

## 3. "Locality of access" (or "locality of reference" or even "locality of interest") refers to the fact that:

**Context.** Locality of reference is the principle behind caching. Access is not uniform, and recently accessed data is likely to be accessed again (temporal locality). Nearby data is also likely to be accessed together (spatial locality).

**Correct answer.** File pages that were accessed recently will be accessed soon in the future.

**Why.** This states temporal locality directly, which is why client and server caches pay off. Locality is not about uniform access frequency, file size, or the read/write ratio.

---

## 4. Which of the following principles is AFS NOT based on?

**Context.** AFS (Andrew File System) caches whole files on client disks and uses server callbacks to invalidate stale copies. It is designed around workload assumptions: small files, read-heavy access, and little concurrent sharing.

**Correct answer.** Most files are accessed simultaneously by multiple clients.

**Why.** AFS assumes the opposite: most files are used by one client at a time. That is why whole-file caching, rare callback breaks, and last-writer-wins on close are acceptable. Small files, one client per file, and more reads than writes are real AFS assumptions.

---

## 5. In a distributed shared memory system, the best value to set a page size to should be:

**Context.** In DSM the page is the unit of transfer and coherence. Too-large pages cause false sharing and wasted bandwidth. Too-small pages force many separate fetches to cover a process's locality of interest.

**Correct answer.** At or slightly larger than locality of interest

**Why.** A page sized to the locality of interest brings in what a process needs in one fetch. It avoids both the extra fetches of small pages and the false sharing of large ones.

---

## 6. Which of the following activities consumes most energy at a sensor mote?

**Context.** A sensor mote is a tiny battery-powered node with a sensor, a low-power microcontroller, small memory, and a short-range radio. Motes are unattended, so energy is the binding constraint. Radio communication costs far more than computation.

**Correct answer.** Transmitting messages

**Why.** Transmitting requires the radio's power amplifier to push the signal over the air, which is the dominant energy cost. Executing instructions is the cheapest activity, which is why motes aggregate and filter locally before sending. Some radios draw nearly as much power receiving as transmitting, but the standard course claim is that transmission costs the most.

---

## 7. In an NFS system, the freshness interval is set to 30 s. At time 10am:12min:25s, a client process with pid 356 accesses a locally cached copy of a file block, for which the client stores a last-modified timestamp of 10am:11min:35s, and the file block was last validated by the client at 10am:12min:3s. At the server, the last-modified timestamp of the file block is 10am:12min:4s. Then, the NFS client will:

**Context.** NFS clients cache blocks and validate them themselves, since the server holds no state and uses no callbacks. On each access the client first checks `T − Tc < t`. Only if that fails does it ask the server for the last-modified time and compare it with its cached one.

**Correct answer.** Serve the file block from the locally cached copy at the client

**Why.** `T − Tc = 10:12:25 − 10:12:3 = 22 s`, which is less than 30 s, so the entry is fresh and the client uses the cache without contacting the server. The server's differing last-modified time is never checked here. Fetching the block would only follow a failed freshness check and mismatched timestamps.

---

## 8. In an NFS system, the freshness interval is set to 3 s. At time 10am:12min:25s, a client process with pid 356 accesses a locally cached copy of a file block, for which the client stores a last-modified timestamp of 10am:11min:35s, and the file block was last validated by the client at 10am:12min:3s. At the server, the last-modified timestamp of the file block is 10am:12min:4s. Then, the NFS client will:

**Context.** Same NFS validation rule as question 7. Check `T − Tc < t` first. If it fails, compare the client's and server's last-modified times. A match keeps the cache and resets Tc, and a mismatch means fetch the block.

**Correct answer.** Fetch the file block from the server

**Why.** `T − Tc = 10:12:25 − 10:12:3 = 22 s`, which is greater than 3 s, so the entry is not fresh. The client asks the server for the last-modified time and gets 10:12:4. That differs from the cached 10:11:35, so the cached copy is stale and the block is fetched.

---

## 9. A distributed shared memory system, using the invalidate approach, contains 4 processes P1 through P4. Currently, a page P is stored in read mode at processes P2 and P4, and P4 is the owner. A read from P1 will result in:

**Context.** In the invalidate approach, a page is either in read mode (many copies) or write mode (one copy, held by the owner). A read fault fetches a copy and adds the reader to the copy set. Only a write invalidates the other copies.

**Correct answer.** P1 fetching a copy of the page from either P2 or P4, and P4 remains the owner

**Why.** A read does not invalidate anything, so P2 and P4 keep their copies and P4 stays the owner. P1 joins the copy set. In read mode all copies are identical, so either holder can supply the data (the protocol is usually described as the owner supplying it). Invalidating both copies is wrong because reads don't invalidate. A failing read is wrong because the fault mechanism supplies the page.

---

## 10. A distributed shared memory system, using the invalidate approach, contains 4 processes P1 through P4. Currently, a page P is stored in read mode at processes P2 and P4, and P4 is the owner. A write from P3 will result in:

**Context.** In the invalidate approach, a write must leave the writer with the only valid copy. A write fault therefore invalidates every other copy and makes the writer the owner in write mode.

**Correct answer.** P3 invalidating the copies of P at P2 and P4, P3 fetching page P from P2 or P4, and then P3 becoming owner of P in write mode

**Why.** P3 has no copy, so the write faults. P2's and P4's copies are invalidated, P3 gets the page contents, and P3 becomes the owner in write mode. Letting readers coexist with a writer breaks coherence. The write does not fail, and P3 is not made to wait for readers to finish.

---

## 11. Which of the following consistency models are available under partitions?

**Context.** A consistency model is a contract about what values reads may return across replicas. A partition splits replicas so they cannot communicate. Under CAP, a system must trade consistency against availability when a partition occurs.

**Correct answer.** E. only (b) and (c)

**Why.** Causal consistency and eventual consistency are available under a partition. Each side keeps answering requests from local state and reconciles after the partition heals. Linearizability is not available, because it needs a single global order, so a cut-off replica would have to refuse requests or risk returning stale or conflicting data.

---

## 12. Consider the following sequence of events. Alice updates a post on social media. Alice calls Bob on his cell phone: "Check my social-media post!". Bob reads Alice's timeline. Under which of the consistency models can Bob be guaranteed to see Alice's post?

**Context.** The phone call is a link outside the storage system, so only a model tied to real-time ordering across clients can guarantee Bob sees the post.

**Correct answer.** A. Linearizability

**Why.** Alice's write completed before Bob's read began in real time, so a linearizable system must return it to Bob. Read my writes only guarantees that a client sees its own writes, and Bob is a different client. Eventual consistency promises only convergence at some unspecified later time, so Bob's read could still be stale.
