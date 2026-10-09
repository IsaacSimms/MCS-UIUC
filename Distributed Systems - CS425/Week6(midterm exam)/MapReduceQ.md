# Map reduce practice question

## Notes

- Map takes a portion of the raw dataset from the DFS and emits a (key, value) pair based on a defined set of parameters.
    - a map task cannot see the whole dataset. It is only ever going to see a split.
    - There can be multiple map tasks running on a dataset concurrently, one per split.
    - Those key value pairs are written to local disk on the machine that did the Map task. 
    - They are partitioned on the disk (partition function (hash(key) mod R) organizes the keys and picks which reducer will own those pairs, based on the key)

input (raw data):
value1, value2, value3, value4, value5, value6, value7, value8, value9, value10

output map1:
(key1, value1)
(key1, value3)
(key1, value5)

(key2, value2)
(key2, value4)

output map2:
(key1, value6)
(key1, value8)
(key1, value10)

(key2, value7)
(key2, value9)


- Shuffle: The reducer task is going to the local disk of each map task and pulling the specifc chunk that it is responsable for (the key that it is supposed to do the next computation on)
This may travel over network.
This is not a set of logic that gets written, 

input:
Each map task's local output file (listed above)

output:
at reducer1:
(key1, value1)
(key1, value3)
(key1, value5)
(key1, value6)
(key1, value8)
(key1, value10)

at reducer2:
(key2, value2)
(key2, value4)
(key2, value7)
(key2, value9)

- Reduce: Takes in the output of shuffle as input.**The reducer owns a partition, not a single key. Reducer function is called once per key** Performs a desired computation on it, outputs a key, value pair based on that computation back into that distributed file system. 
Output of reduce can often be a reduction of the data to a desired state. "Add each value of key x together and output result." "Concantante string values associated with key y and output result"

input: 
the result of shuffle (Listed above)

output (back into DFS):
reducer 1:
(key3, value X)

reducer 2:
(key4, value Y)

### general notes
- A record (a value from the original dataset) can emit zero, none, or many key, value pairs. Not always one. 
- R = the number of reducers for that job
- A reducer can take in multiple keys in a single pass
- many MapReduce goals are completed in more then one pass, having to do with physical constraints.

## Practice assessment MapReduce question:

You are given a social network log that captures information about all the posts on a
social network during the course of a day. Each line contains tuples (a, hh:mm:ss) where
a is a user id, and hh:mm:ss is the timestamp of a post made by the user. If a user has
multiple posts, they will appear as separate entries. The entries are not sorted in any
order.
Write a MapReduce program to find those 3 hours of day when the maximum,
minimum and median number of posts were made. Your output should be three
integers, each in the range 0-23.
You should have at least some parallelism. Ensure that your output does not
contain duplicates. You can set your key and value to arbitrary objects. You cannot
retain data at any of the machines from a task (Map or Reduce) for use in a later task.
Chaining MapReduces is allowed, as long as you don’t over-use chaining (where
parallelization could have helped instead). Each MapReduce in a chain can read the
dataset, but there is no other persistent memory across the chain. Pseudocode is
preferable, and it can be coarse-grained, e.g., you can say “get top k from this list by
field x”, “sort this list by key x”, etc.). Be clear and concise and don’t miss any steps.

### Answer:

#### try 1
Output requirements:
3 integers (max, min, median)
a missing hour = 0
ties = no duplicate hours

job 1:
map:
input = the raw data set (a, hh:mm:ss)
multiple map tasks are getting split of raw data

output = (key, value) being (key = each hour(hh)(0-23) , value = 1)
data is now list of instances associated with hour. 
Each map task is only going to output this for hours in its split.

reduce:
input: one or more sets of keys from the output of each map task

Output: (key, value) (hour of the day(hh), number of events in that hour)

job 2:
map:
input = (hour, count) key, value pairs (as built by the previous job)
output = (1, (hour,count)) key, value pairs. 

reduce:
Input: bc all key,value pairs from the map task of job 2 have the same key, all pairs are sent to a single reduce task. 
That reduce task is responsible for selecting the median, max, and min.

output: three integers (max, min, median)

#### try 2
Output requirements:
3 integers (max, min, median)
a missing hour = 0
ties = no duplicate hours

job 1: (counts posts per hour) (done in parallel)
Map:
input: raw data (a, hh::mm:ss) 
hour = hh                       # each map only gets one split
output: (hour, 1)               # each map only outputs hours present in its split

Framework partitions pairs by key (by hours)

Reduce:
input: (hour, values)          # values = 1, 1, 1, 1,...x
output: (hour, sum(values))    # hours that never had a post are not present (i.e. (hour, count))

Job 2: (picks three hours for answer) (input is job 1 output)
Map:
input: (hour, count)
output: (1, (hour, count))      # same key for every pair --> one reducer

Framework partitions pairs (groups all pairs to one group due to same key)

Reduce:
Input: (1, (hour, count))
Reduce:
array slots(0...23) = 0
foreach (hour, count) in (hour,count):
    slots(hour) = count
    array hours = (0, 1..23) 
    sort hours by (slots(hour) assending, ascending)
minHour = hours(0)
maxHour = hours(23)
medHour = hours(11)

emit(maxHour)
emit(minHour)
emit(medHour)