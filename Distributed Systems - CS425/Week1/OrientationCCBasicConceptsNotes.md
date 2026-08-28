# Intro
This lecture is about basics of computer science that are applicable to distributed systems. Lots of term defintions and stuff.

## Data Structure
Queue: First-in First-out. Remove from head and insert at tail. Inserts and removals can happen concurrently.
Stack: First-in Last-Out. Removal and insertion both happen at the head. Insert == push and removal == pop.
Widely used.

## Process
Process == program in action. A program that is in active execution.
### componenets
**Program counter** = index into code. Where the program is right now within the code base, as far as execution goes.
**Stack**= used by functions to pass arguments and return values among themselves. If one function calls another, the called function can push the required arguments to
top of the stack. The caller can then pop those arguments off the stack.
Local variables are often maintained on top of the stack. AFter function is done, their popped.

Code will also create (***allocate*** from the hardware) new memory. This process is usually stored in a separate structure, **the heap**.
Registers are also associated with the heap. (registers are essentially the recently accessed variables within the process). Memory is also ***freed*** out of the heap.
(Even if that is done through garbage collection)

In distributed computing we will need to discuss multi-process communication. Most of what this course will discuss is cross process communication so things like the stack
and heap are going to stay separate. However, it is possible for procedure calls to cross that process boundary, and that will be discussed towards the end of the class.

A **Snapshot** of a process is an instance of a process in a specific place in time/execution. When discussing a snapshot, we are talking about all of these elements.

## Computer Architecture (simple)
CPU <--> Disk
Closer you get to CPU the more memory constrained the hardware becomes, but the processor is able to access that memory/data more efficiently/quickly
CPU: executes instructions. Coupled with registers, can be accessed very quickly by the execution process.
Cache: larger piece of memory then registers but slower. Still close to CP
Memory **RAM**: What is commonly referred to as the "working memory" for modern machines. Where modern applications store their current state for execution.
Cache and registers are both still types of memory for actice execution. But, handled at a lower level of abstraction then what most modern programming requires.
(Although, feel free to whip out some assembly language and move stuff in and out of registers by hand)
Disk: SSD, HDD, USB keys, etc. are all disks. Disks are external memory units for data/information/process storage. (External to the CPU, not necessarily the machine.)

## Flow
Mid-to-high level language gets written (C++,Java, etc.) --> compiled into machine (or interprated as "machine language" in the case of something like python) -->
At process execution time, CPU loads those instructions in batches into its memory cache & registers) -->
CPU also loads data and data changes through cache and into heap as well.
Memory is flushed to disk for permanent storage.

## Big 0() Notation
Basic ***industry standard*** way of analyzing algorithms, but more specifically **analyzing algorithmic performance**
Describes "upper bound" on behavior as variable is scaled to infinity. Often side of input
Analyzes runtime (or other metric, but its usually time)
**captures worst case performance in any given situation/metric**
Exp:
Algo A is O(foo) performant
this is saying that the algo takes < c * foo time to complete, where some constant is c. Beyond some input size of N.
Usually foo is a function of input size (N)
Common to see performances like O(N), O(N^2) O(log N)