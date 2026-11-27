# Lecture: Distributed Shared Memory (Lecture A)

Cloud Computing Concepts, Part 2 (Indranil Gupta). CS425 Week 12. Follows Lecture 12.2, NFS and AFS.

(Agent generated)

## TLDR

Distributed shared memory (DSM) lets processes on different machines read and write shared memory as if they were threads on one machine, while the system moves memory pages over the network behind the scenes. The main design question is how to keep copies of a page coherent, and the lecture's answer is the invalidate protocol (many readers or one writer) with page size as the key tuning knob.

**Distributed shared memory:** an abstraction that gives processes on separate machines the illusion of a single shared address space. The unit of sharing is the **page**, and a page fault triggers DSM software that fetches the page from another node.

## Key sections and what to retain

### 1. DSM versus message passing

DSM lets you write `x = y` instead of explicitly sending and receiving messages, and the network is hidden under the memory access.

- Normal programming over a network uses message passing (send/receive, RPC). DSM turns this inside out: processes access shared pages, and a **page fault** traps into DSM software, which fetches the page over the network.
- Each abstraction can be built on top of the other: DSM can be implemented with messages, and message passing can be implemented on shared memory.
- The transparency has a price: any access might silently turn into a network transfer, and the system must keep copies coherent.

**Builds on:** the transparency trade-off from distributed file systems. Hiding the network costs consistency work.

**Retain:** DSM is paging over the network, with the page as the unit of transfer and coherence.

### 2. The invalidate protocol (page states and owner)

Many processes can safely read a page at once, but a writer needs to be alone, so the protocol enforces many-readers-or-one-writer.

- Each page is in state **R** (any number of read-only copies, no writer) or **W** (exactly one copy, held by the owner, who may read and write).
- Each page has one **owner**: the process with the latest version. Being owner does not mean being the only holder when the page is in R.
- Cases to replay from memory:
  - **Read, you hold R:** read locally, with no messages. No W copy can exist.
  - **Read, you have no copy, page is R:** fetch a copy from a holder and join the copy set. Reads invalidate nothing.
  - **Read, you have no copy, someone holds W:** ask that holder to **degrade to R** first, then copy. Copying without degrading would let the writer keep writing behind your back.
  - **Write, you are owner in R:** multicast **invalidations** to the other R holders, then switch to W.
  - **Write, you have no copy:** invalidate every other copy, fetch the latest data, and become owner in W.

**Retain:** a write always leaves the writer with the only valid copy. A read never invalidates anything.

### 3. Page size and false sharing

Bigger pages mean fewer transfers but more chance that unrelated data gets dragged along, so the page size must balance the two.

- **False sharing:** two processes write different variables that happen to sit on the same page. Under invalidate, the page ping-pongs between them even though they share no data.
- Page too large: false sharing and wasted bandwidth.
- Page too small: many separate transfers to cover a process's locality of interest.
- The best size is application dependent. IVY (Li and Hudak) found about 1 KB to be a good compromise.

**Retain:** page size is a trade between false sharing (large) and transfer count (small).

### 4. Invalidate versus update

There are two ways to keep copies coherent after a write: kill the other copies, or send them the new value.

- **Invalidate:** a write invalidates all other copies, so only one writer holds the page. It is the usual default and is what the lecture develops.
- **Update:** many processes hold W copies, and every write is multicast to the others. It wins when sharing is heavy, writes are small, and pages are large.

**Retain:** invalidate is the default, and update is the alternative for write-heavy sharing of small values.

### 5. Consistency in DSM

DSM can follow any consistency model from earlier in the course, from linearizability and sequential consistency down to eventual consistency. A stronger model means more messages per access, and a weaker one means less transparency to the programmer.

**Retain:** the choice of consistency model sets DSM's cost. The page protocol alone does not fix it.

## Recap

- DSM is a shared address space built from pages moved over the network, triggered by page faults.
- Pages are in R (many readers) or W (one owner, alone), and every page has one owner holding the latest version.
- Reads never invalidate. A write invalidates all other copies and makes the writer the owner.
- A read of a page held in W requires the writer to degrade to R first.
- Page size trades false sharing (too large) against too many transfers (too small).
- Invalidate is the usual default. Update is the alternative for heavy sharing with small writes.
