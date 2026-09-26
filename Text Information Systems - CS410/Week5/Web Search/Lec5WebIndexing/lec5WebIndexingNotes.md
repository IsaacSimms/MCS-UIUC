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

