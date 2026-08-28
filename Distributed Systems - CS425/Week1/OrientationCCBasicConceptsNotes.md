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