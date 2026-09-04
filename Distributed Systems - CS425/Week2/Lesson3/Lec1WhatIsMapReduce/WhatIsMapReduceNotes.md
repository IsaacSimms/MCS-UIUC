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
Processes each indivial record (a play from shakespeare, or a chapter of a play, just some sort of division of the whole)
with the goal of **generating "intermediate" key/value pairs**

**look at MapTaskDivision.png**
Essentially, the "welcome" key is assigned the value of one because it was in countered once. (the second everyone is independent of the first one)
Note: Map is easy to parallelize because you can simply split (shard) the record set into two different tasks.