# Cloud Computing Concepts (C3), Part 1

**Programming Assignment (Machine Programming or MP)**  
For C3 Part 1 (also for use in CS425 Coursera section)

**Name:** Membership Protocol  
**Year:** 2022

## Important Dates

| Milestone | Date |
|-----------|------|
| Released | Week 1 of C3 Part 1 |
| Due | End of Week 6 of C3 Part 1 |

---

## 1. What is this MP about?

Implement a membership protocol similar to those discussed in class. Because it is infeasible to run thousands of cluster nodes over a real network, an emulated network layer (**EmulNet**) is provided.

Your membership protocol sits above EmulNet in a peer-to-peer (P2P) layer and below an Application layer. This forms a 3-layer protocol stack:

1. **Application**
2. **P2P**
3. **EmulNet**

### Requirements

Your protocol must satisfy:

- **Completeness** at all times: every non-faulty process must detect every node join, failure, and leave.
- **Accuracy** of failure detection when there are no message losses and message delays are small.
- When there are message losses, completeness must still be satisfied and accuracy must remain high.
- Must handle simultaneous multiple failures.

You may implement any membership protocol covered in class:

- All-to-all heartbeating
- Gossip-style heartbeating
- SWIM-style membership

Gossip or SWIM are recommended (you will learn more).

### Technology

- Template code is written in **C++**.
- Requires at least **C++11** (gcc 4.7+).

### Course Materials

On Course Week 6 (CS 425 version; position may vary in the Cloud Computing Concepts course), you will find:

1. A page to generate **submission tokens** and view grading results.
2. A page to launch the online programming environment (Theia IDE).

These pages also include an extra zip file containing the starter template code if you prefer to work offline.

Autograder scripts (unit tests) are provided so you can verify that your program meets all requirements (see Section 6).

### 1.1 Theia IDE Workspace

*(Beginning Fall 2020)* An embedded workspace is provided on the Coursera site for Coursera section students. It is an IDE similar to an open-source variant of VS Code.

- Starter files and the submission script are already present when you open the environment.
- If the workspace loads empty (no panels or files visible), manually reload the workspace and open the file editor pane.

**Brief overview:**

- Some assignments are split into two Coursera items:
  - One for copying a “submission token” and viewing results.
  - A separate “Ungraded Lab” item to launch the Theia IDE workspace.
- Although labeled “Ungraded,” you can still submit for a grade.
- The provided `submit.py` script asks for your email address and temporary submission token, then submits the assignment instantly.

**First-time setup:**

1. Click **Open Workspace**.
2. Highlight `lab-workspace` and click **Open**.
   - **Important:** Always work inside the `lab-workspace` folder. Only this folder is specially backed up and preserved in the cloud between sessions. Working elsewhere may result in lost work.
3. Click the file explorer icon (upper left) to view the file list.
4. Click a filename to open it for editing.
5. Open a Bash terminal: **Terminal → New Terminal**.

### 1.2 Backing Up Your Work

Work under `~/lab-workspace` (i.e., `/home/theia/lab-workspace`) so files are automatically saved to the cloud every few minutes.

To download a local copy:

```bash
cd ~/lab-workspace
make clean
zip -r backup.zip *
```

Right-click `backup.zip` in the file list and choose **Download**.

Instructions for testing and submitting appear later in this document.

### 1.3 Academic Integrity

All work in this MP must be individual (no groups).

- You may discuss the MP specification and related concepts with others.
- You may **not** discuss solutions or code, nor share code.
- Code may be checked for similarities in structure and ideas.
- You will learn the most by doing the work individually.

---

## 2. The Three Layers

The provided framework allows you to run multiple peer copies within one process using a single-threaded simulation engine.

### 2.1 Emulated Network: EmulNet

EmulNet provides the following functions for the membership protocol layer:

```cpp
void *ENinit(Address *myaddr, short port);
int ENsend(Address *myaddr, Address *toaddr, string data);
int ENsend(Address *myaddr, Address *toaddr, char *data, int size);
int ENrecv(Address *myaddr, int (*enq)(void *, char *, int), struct timeval *t, int times, void *queue);
int ENcleanup();
```

- `ENinit`: Called once by each node to initialize its own address (`myaddr`).
- `ENsend` / `ENrecv`: Used by a peer to send and receive waiting messages.
  - `ENrecv` enqueues a received message via the provided `enqueue()` function pointer.
  - The third and fourth parameters (`t` and `times`) are currently unused.
- You can assume `ENsend` and `ENrecv` are reliable when there are no message losses in the underlying network.
- `ENcleanup`: Called at the end of the simulator run to clean up the EmulNet implementation.

These functions are designed so they can later be mapped onto TCP socket implementations.

> **Do not modify** the files `EmulNet.cpp` / `EmulNet.h`. They will be replaced during testing.  
> Only use the above functions to access the EmulNet layer. Do not access EmulNet data structures directly.

### 2.2 Application: Application

This layer drives the simulation. See files `Application.{cpp,h}`.

- Look at the `main()` function.
- Runs in synchronous periods (via the `globaltime` variable).
- During each period:
  - Some peers may be started.
  - Some peers may be caused to crash-stop.
  - For each alive peer, `nodeLoop()` is called.
- `nodeLoop()` is implemented in the P2P layer (`MP1Node.{cpp,h}`) and:
  - Receives all messages sent for this peer in the last period.
  - Checks whether the application has any new waiting requests.

> **Do not modify** the files `Application.cpp` / `Application.h`.

### 2.3 P2P Layer

Files `MP1Node.{cpp,h}` contain the code for this layer.

- Currently has limited functionality.
- This is where you implement the membership protocol.
- Can later be extended to provide functionalities such as file insert, lookup, remove, etc.

---

## 3. What does the Code do currently?

As provided, the code prints debugging messages into `dbg.log` with the format:

```
node address [globaltime] message
```

- Turn debugging on or off by commenting/uncommenting `#DEFINE DEBUGLOG` in `stdincludes.h`.

Two message types are currently defined in the P2P layer (`MP1Node.cpp`):

- `JOINREQ`
- `JOINREP`

Currently, `JOINREQ` messages are received by the **introducer**. The introducer is the first peer to join the system (typically `1.0.0.0:0` on Linux due to big-endianness).

**Best place to start:** Have the introducer reply to a `JOINREQ` with a `JOINREP` message.

The next section lists all functionalities you must implement.

---

## 4. What do I Implement?

All your code goes into the P2P layer in `MP1Node.{cpp,h}`.

> **Do not make changes to any other file** other than `MP1Node.cpp` and `MP1Node.h`. Other files will be replaced.

You must implement:

- `nodeLoopOps()`
- `recvCallBack()`

Both are invoked by `nodeLoop()` to periodically perform protocol routines. They should provide the functionalities described below. You have considerable flexibility in implementation details, except that your final submission must work with the other files unchanged.

### Required Functionalities

- **Introduction:** Each new peer contacts a well-known peer (the introducer) to join the group via `JOINREQ` and `JOINREP` messages.
  - Currently, `JOINREQ` messages reach the introducer, but `JOINREP` is not implemented.
  - `JOINREP` messages should specify the cluster member list.
  - The introducer does not need to maintain a full list of all peers; a partial list of fixed size is acceptable.

- **Membership:** Implement a membership protocol that satisfies:
  - Completeness at all times (for joins and failures).
  - Accuracy when there are no message delays or losses.
  - High accuracy when there are losses or delays.

Recommended: gossip-style heartbeating or SWIM-style membership (all-to-all is also acceptable, though you will learn less). See lecture slides for details.

You will probably need to modify the class/struct members and the `MsgTypes` enum in `MP1Node.h`. Handle new message types in separate `Process` functions similar to those for `JOINREQ`/`JOINREP`.

### 4.1 Logging

Logging events is critical because the grader scripts (Section 6) examine the logs.

`Log.{cpp,h}` provides:

- `LOG()`: Prints node status into `dbg.log`.
- `logNodeAdd` and `logNodeRemove`: Call these whenever a process adds or removes a member from its membership list.

The grader scripts look for these log entries.

**Function signatures (conceptual):**  
These functions take two address parameters:
1. Address of the recording process.
2. Address of the process being added or removed.

---

## 5. What are these Other Files?

- `Params.{cpp,h}`: Contains `setparams()`, which initializes several parameters at simulator start, including:
  - Number of peers in the system (`EN_GPSZ`)
  - Global time variable `globaltime`
  - etc.

- Remaining files (`Member.cpp` / `Member.h`): Contain necessary definitions and declarations. See descriptions in the files. **Avoid modifying these files.**

### Why is the Code Structure So Involved?

Two reasons:

1. **Conversion to a real application:** All `EN*()` functions can be replaced with socket-based send/receive. Once the periodic functionalities (e.g., `nodeLoop()`) are replaced with a periodically waking thread, and appropriate conversions are made for `nodeStart()` and `recvLoop()`, the implementation can run over a real network.

2. **Debugging and measurement:** This structure allows easy debugging (and performance measurement via traces) of the membership protocol on a single host machine. This is far easier than debugging hundreds of processes on a real network. Once the simulation engine works, the implementation can be converted to run over a real network.

---

## 6. How do I Test my Code?

### 6.1 Testing

**Compile:**
```bash
make
```

**Execute:**
```bash
./Application testcases/<test_name>.conf
```

Configuration (`.conf`) files contain parameters:

```
MAX_NNB: val
SINGLE_FAILURE: val
DROP_MSG: val
MSG_DROP_PROB: val
```

- `MAX_NNB`: Maximum number of neighbors.
- `SINGLE_FAILURE`: 1/0 flag for single vs. multi-failure scenarios.
- `MSG_DROP_PROB`: Message drop probability (0 to 1).
- `DROP_MSG` / `MSG_DROP`: 1/0 flag that decides whether messages will be dropped.

**Tester script:** `Tester.sh` tests your membership protocol implementation in 3 scenarios and grades each on 3 metrics.

**Scenarios:**
1. Single node failure
2. Multiple node failure
3. Single node failure under a lossy network

**Metrics (for each scenario):**
1. Whether all nodes joined the peer group correctly.
2. Whether all nodes detected the failed node (**completeness**).
3. Whether the correct failed node was detected (**accuracy**).

Each is represented as configuration files inside the `testcase` folder.

### 6.2 Grading

The MP is worth a total of **90 points**.

When you run the grader, it reports whether you passed all tests (out of 90). Add code so that your submission passes all tests on the Coursera grading platform.

### 6.3 Submission Instructions

Use the provided test runner (`Tester.sh`) to test your solution locally as many times as you want. Ensure you are using at least C++11 (gcc 4.7+).

**Run the grader locally:**
```bash
bash ./Tester.sh
```

Once satisfied, use the provided submission script to submit to Coursera:

```bash
python3 submit.py
```

**Before submitting:**
- Back up all your files and work in a different directory.

**Submission process:**
- The script prompts for login details.
- **Login ID:** The email address you use with Coursera.
- It also asks for a **submission token**.
  - This is the single-use key you generate on the Coursera instructions page for this assignment.
  - This is **not** your Coursera account password.
  - Generate a fresh submission token each time you wish to resubmit.

You can check your submission score on the Coursera programming assignments web page under the **My submission** tab. It lists a log of submissions and results.

> Note: It can take a while (sometimes a few hours) for a submission to be graded. Be patient.  
> If you make multiple submissions, the one with the highest score is considered for grading.