# Implementing a text retrieval system from the systems perspective
There is a challenge in scale here. Every query needs responded to quickly, and there are many queries that need responded to concurrently.

## The typical architecture
see Text Information Systems - CS410/Week2/Lesson1/Lec4ImplementationOfTRSystems/SampleTRSystemArchitecture.png 

- 1: The docs are sent trough a **tokenizer**
    The tokenizer turns the raw character steams from the inputs and turns them into terms. 
    Typically, for english, the terms are split on whitespace or punctuation, are turned into all lowercase.
    The output ios a doc rep and a query rep respectively

The doc rep is a document specific term list post tockenization. Initially we looked at a bit vector doc rep. 
But, more sophisticated doc reps involve thinks like TF-IDF and BM25t weights.
- The doc rep is placed in an **indexer**
    The indexer consumes every doc rep and builds an **index**
        - The index is a data structure which actually answers the question "which docs have term T?"
        - The index is important because it means that every document in a collection does not need to be walked for every query. Only documents returned by the index need to be walked at query time.

        - The standard structure of an index is essentially two parts that each term gets placed in. The dictionary and the postings list.

        - An inverted Map from the terms to the documents that contain them. **for the dictionary**
        One entry per distint term with a variety of fields. Common fields include:
            term string (or termID) = the key the query must hit exactly
            df_t = how many documents contain t (the term) (this is used in IDF)
            pointer = byte offset (block ID on the postings list)

        - The postings list is structured as an actual list. 
        Every term in the index gets an entry into the postings list. Each entry has the term, and a sequence of document hits, sorted by docID. 
    

The query rep is a query specific term list post tockenization. Initially we looked at a bit vector query rep. 
But, more sophisticated query reps involve thinks like TF-IDF and BM25t weights.
- The query rep is placed directly into the scorer and the index feeds into the scorer as well. 
    