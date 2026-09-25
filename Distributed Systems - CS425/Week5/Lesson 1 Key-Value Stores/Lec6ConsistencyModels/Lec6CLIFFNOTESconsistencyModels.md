# Consistency models
- Defintion: A consistency model is a "contract" between the distributed system and the application. 
This model is used to ditate what results a system can return for any given operation (R = read & W = write)
This contract is implemented at the distributed system layer and applications are programmed against it.

- Remember the consistency spectrum from previous lectures.
Use the **weakest** model that is still appropraite for a given app/system setup.
This axis exists because of the restains from CAP. Partition happen and you need to be able to survive them, so stores need to pick a side on the availability vs consistency front.
remember BASE vs ACID & what the acronyms mean.

## Consistency contract types
This lecture reviews multiple different types of consistency models discussed in other lectures. Eventual, casual, linearizability, sequential, etc.
Review those as needed. But not reviewing those here, as they are discussed in previous lectures at a high level.

## Session guarantees - Session based consistency models
A session is one client's consecutive strech of ops. This part of the contract guarantees that session for that one client. "give that client a sane view, even if other clients might see a mess for them"

versions: of session guarantee conssitency model:
- Monotonic reads: reads cannot go back in time. If client issues R_1, R_2 must observe the state of R_1 first.
- Monotonic writes: writes cannot go back in time. After client issues W_1, any subsequent write must see and be working based off of W_1 first.
- Read my w rites: If a client issues W_1 and then issues R_1, that read must see the effect of the previous write. 
All these models are network partition tolerant.
Stronger then eventual consistency but weaker in consistency then say sequential.

## grading a trace
A trace is who did what when and at what value. Grading the trace allows you to under standard the tradeoff that the model being used is making, abaliability vs consistency.
lin --> SC --> causal --> session --> eventual
1. Real-Time Intervals. each operation is a bar. If A happened before B, sequential. If they overlap, concurrent.
2. PRogram order. each client has a list of ops in the order they where issued. These stay in order
3. Read-form. for every read that returned v, there is a pointer to the write that produced v
This leads to 5 questions being asked to understand the consistency of a model:
- Linearizable?             (is the program order organizated based on time operations recieved)
- Sequentially consistent?  (by definition, not concurrent)
- Casual?                   (no single move required)
- Session?                  (one client at a time, isolated)
- eventual                  (any return value legal?)