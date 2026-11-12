# Single-processor scheduling

## Definitions
- Scheduling: Under this context scheduling means the process of deciding which jobs/tasks to run, when they run on which resources. 
Both concurrency and constraints such as hardware  (CPU, memory, etc.) are at play
- single-processor scheduling: solving the problem of ordering a set of tasks that each have their own processing and arrival time onto one processor so as to meet chosen performance goals. You want:
1. Good thorughput or response/completion time for tasks
2. High resource utilization

Always make the objective explicit; different metrics produce different optimal policies.

## FIFO / FCFS
Tasks are kept in the queue ordered by arrival time (first-in-first-out). When processor is free, head of queue is processed until completion.
Simple to implement, fair with respect to arrival order. A special case of priority scheduling.
but: average completion time is often high, a long task blocks a short task that arrived after it. 

## STF (Shortest Task First)
Ready tasks are sorted by running time. (organized with shortest running time task at the head)
When processor is free = shortest remaining task is selected adn run to completion

A known disadvantage is starvation: a continual stream of short tasks can prevent a long task from ever running.

**STF is generally optimal** the average completion time of STF is the shortest among all scheduling approaches (at the time of this lecture)
This is particularly true for batch jobs where the system is supposed to receive job --> go off and complete --> come back with result

## Round robin
Tasks are run in pieces/chunks. A fixed quantum (time sliced) is used to orchestrate the pieces.
The head of the queue is run for one quantum --> the state is saved (preempted) --> that task is placed at the end of the queue --> the next task is run for at most one quantum
Gives a "fair share" of the resources to each of the tasks.
Round-robin is good for interactive workloads that are realtively quick and uniform to process for each task, and each task needs to be completed uniformly quickly. 
(User needs quick responses from an interactive system)
