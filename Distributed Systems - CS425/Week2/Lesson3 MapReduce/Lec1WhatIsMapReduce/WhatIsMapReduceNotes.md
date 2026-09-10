# MapReduce Overview
**Overall paradigm**

## What is MapReduce?
*the term MapReduce has been taken from functional languages*

"Map":
 Is a meta function that applies the function behavior to a list of inputs. Those inputs can be thought of as records
Each record is processed sequentially and independently.

"Reduce":
processes a set of all the records in batches

## The wordcount example
"lets say you where given the task to count all the instances of a word in all of shakespeare's text" 
*essentially just operation on large amount of data is the key*

### Map
Processes each individual record (a play from shakespeare, or a chapter of a play, just some sort of division of the whole)
with the goal of **generating "intermediate" key/value pairs**

**look at MapTaskDivision.png**
Essentially, the "welcome" key is assigned the value of one because it was in countered once. (the second everyone is independent of the first one)
Note: Map functions can be parallelized because you can simply split (shard) the record set into two different tasks.
Parallelization needs up the process

So now, we have a key/value pair for every word in the corpus, meaning we have some way to quantify those words, but we do not have the actual count of the words in the record. 

### Reduce
The reduce **processes and merges** the results of the intermediate values from the Map phase. The reduce function does so by looking at each value associated with each key *per key basis*.
Because the two "everyone" keys are the same they will get added together. Each of those values get processed independently from each other and grouped.
Note: Reduce functions can be parallelized. Assign each key to a single Reduce task and have more then one task processing the set of keys concurrently.

Popular architecture: Hash partitioning. This means that each key is assigned to reduce # = hashFunction(key)%number of reduce servers.
This leads to uniform load balancing of keys accross the tasks.

### Execution flow

Input is split into chunks. Each chunk is fed to a mapper.
Mappers emit intermediate key-value pairs.
The framework shuffles: all values for the same intermediate key go to the same reducer.
Reducers process each key’s value list and emit results.
Output is written (typically one file per reducer).