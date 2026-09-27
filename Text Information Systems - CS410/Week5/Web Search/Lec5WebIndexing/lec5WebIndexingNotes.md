# Using Indexer to create inverted index of web pages
**Remember** Crawler takes the whole web and distilles down into cached pages. Those pages get processed by an **Indexer** to create inverted index. 
**Indexing**: Building a data structure the search engine uses to answer "which pages contain this term" without scanning the entire web.
Crawler gives you raw pages, indexer turns it into inverted index: term --> list of (doc, tf, extra payload)

## Overview of Web Indexing
- Standard information retrival methods are the basis, but insufficient due to scalability and efficiency issues
A primary problem is the corpus is so large that there is no way a web indexing proccess is going to fit into a single machine or single disc. Enter distributed computing.
- You'll see many distributed system technologies used in web indexing infrastructures such as:
1. Google file system (GFS)
2. MapReduce (software layer for parallel computation)
3. Hadoop (opensource MapReduce)

## GFS
GFS is a cluster filesystem used for huge files (including what you'd get with crawls/indexes).
- There is a client (which in this case is the job. MapReduce, indexing, etc.)
- There is one master server. Howles metadata (namespaces, chunk lists, logging, etc.) (includes checkpoint logic for restarts & failure)
- Then there are the ChunkServers. These are what hold the actual bytes on linux disks. 
A file is split into large chunks here, 64mb (each chunk gets a chuck ID) Chunks are replicated for fault tolerance.

Applicant/GFS sends file name/chunk index to GFS master (the request for data) -->
The GFS master returns a chunk handle/chunk locations (where in the whole system the data lives) -->
The GFS client send the specific Chunkserver which has the file system containing the data the chunk handle it wants, and the byte range it is looking for -->
The GFS chunkserver sends the requested chunk data back to the GFS client

## MapReduce
minimize programmer load for parallel processing tasks (important for distributed systems/public cloud)
- abstracts away some of the low level architecture (network and storage)
- built-in fault tolerance
- automatic load balancing

input is seperated into key-value pairs (these values can be processed in parallel) -->
The pairs are given to map functions -->
Map function processes pairs, giving them all a new key -->
values with the same key are grouped together -->
each group is handled to reduce function (each reduce function gets one group with one key) -->
reduce function processes values in order to create the data that the programmer wants. 

The programmer writes the map function and the reduce function based on what they are wanting the result to be.

### TR example in MapReduce
Let's say you are wanting to build and use an application which does word counting. Input = strings | Output = per word counts
(This is related to TR bc this kind of counting would be useful for accessing the popularity of a word in a large collection, an essential behavior for IDF weighting.)

In MapReduce, you could parallelize lines from the input file.
The input to the map function is a single line of the original input into the system. The output from the map function is each individual word, associated with a key.