# RPCs (Remote Procedure Call) in distributed systems

## Defintion
RPC is an abstraction that lets a process invoke a function in another process (possible on a different host)
Uses the same programming model as a local procedure call.
Arguments and return values are passed over the network via stubs and marashalling (enables code reuse across distributed systems). Including cloud computing.

## LPC vs RPC
- LPC = "Local procedure call"... stays inside a single process. (exactly one set of semantics).
If process is alive, function executed once.
Arguments travel on the stack and/or within registers.
Objects reached by pointer or reference depending on language. 

- This differs from the previously define RPCs where a function call crosses a process boundray. 
Raw pointers or references become useless under this behavior due to different address spaces. 
Callee named by *global reference* (IP + port + procedure number)
Call isn't free but RPCs allow for code reuse without exposing the sockets as f form of communcation abstraction in distributed systems.

**Note with RPCs vs LPCs**: 
If function call is within the same process = LPC
If function call is from one process to another process *within the same host* then it is an RPC
AND
If a function call is from one host to another host, that is also an RPC (often involving a message over the network here)

## RPC call Semantics
*hard to guarantee "exactly-once" semantics under failures* bc the called function may not exectue if:
- request message is dropped
- return message is dropped
- Called process fails before executing
- called process fails after executing but before sending return
(Note its difficult for a caller process to distinguish *why* the RPC failed)

Function could also execute multiple times if the request message is duplicated in error.

### Practical semantics used in prod
- at least once (sun RPC as example). retransmit the request and re-execute function on every dup
- at most one (Java RMI as example). retransmit the request > filter duplicates at server > but the response is a cached reply, not a re-execution
- maybe/best-effort. no retransmission on duplicate messages

idepotent work = use at-least once. Otherwise demand at-most-once for most situations
(Idempotent means an operation can be executed multiple times and produces the same final result as if it had been executed once.)
Examples of Idempotent operations:
x = 1 &
x = *argument* y
no matter how many times these things execute, the answer is the same. at least once RPC architecture is fine here. 

Exampes of non-idempotent operations:
x = x + 1 
x = x * 2
The number of times those operations get executed effects the end state of the system. at most once is RPC architecture is required.

## RPC implementation and marshalling
Note: The network complexity in RPC architecture is abstracted away behind a thin layer of generated code, that way the programmer writes functions normally.

### The flow & implementation architecture
1. Caller (say, client process P1)
application code calls. Looks like a normal function. What the application dev writes.
2. Client stub
Intercepts the local application code call. Exact same sig as the remote function, so the caller code remains unchanged.
- Marshals the arguments into a platform-independent Common Data Representation (CDR) so endianness and data layout differences do not matter.
Marshalling converts arguments from client's native memory layout to the standardized (platform independent) byte stream (CDR).
Endianness = the order in which a computer stores the bytes of a multi-byte value
3. Client communcation module
Packages the marshalled request and sends it over the network to the server
4. server communication module
receives the request message
5. dispatcher
looks at procedure identifier and routes request to correct server stub
6. Server stub
Unmarshall the CDR arguments into the server's native format
7. callee (server process P2)
executes the "local" function body
8. Return path
Essentially the already outlined path but in reverse.
server stub marshels return value into CDR > communication modules ship reply > client stub unmarshall it > returns the result back to original caller


Note:
RPCs are the primitive transations (the next lecture) are the unit of work built from those RPCs. 
