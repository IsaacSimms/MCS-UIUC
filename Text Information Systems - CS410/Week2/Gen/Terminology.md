# Some important termonology to understand

### VSM:
VSM is a scoring rule. It is a way to take a query and a set of documents, turn both in to a bag of words, and rank how much those documents and the query overlap.

### Term Frequency (TF):
     number of times a term occurs in a document.
It is a within-document count of those .

### Document Frequency (DF):
The number of documents that contain a specific term at least once.
A collection level statistic.

### Collection frequency:
how many times a term occurs in the entire collection. 

### Inverse Document Frequency (IDF):
IDF is a form of DF where terms that occur in documents with high frequency get down-weighted in the heuristic.
Rare terms get a high IDF.
Terms that occur in every doc get a near zero.
    log base does not change ranking IDF.

#### IDF equation
idf_t = log (N \ df_t)

where t is the term and N is the collection side

### TF Transformation
A function that gets applied to the raw tf. (In VSM, this occurs before multiplying by the IDF)
There are more then one version of this function depending on how VSM is getting implemented.

### Pivoted Length Normalization
A function that normalizes document size in the scoring heuristic. 
    A 1000 page doc is going to have more chances for a term to be included then a 200 page doc.
    Meaning without a normalization technique like this, that 1000 page doc could inappropriately score better in the metric if that metring was only scoring raw sum (bit-dot, raw TF-IDF, unnormalized cosine numerator)
    This function in the vector space model normalizes the documents so each doc has the same scoring potential within the weights. 

### BM25
A production grade VSM that is widely used today.
Packs shippable heuristics, some of which are discussed in this terminology notes, into something that can actually perform the modeling. 

### Inverted Index and postings
A data structure that operates so the scoring model can be scaled to encompass an entire collection of docs. 

#### sub data structures
Dictionary: has one entry per term. holds the term, a pointer to its list within the data structure (often IDF style)
Postings list: for each term defined in the dictionary, all of the documents that contain it. (usually sorted by a PK like docID)

Inverted index: the dictionary essentially.
Posting: a single instance of the postings list.

### Misc

d-gap: apart of the inverted index/postings architecture.  the difference between successive docIDs in a postings list, not the raw IDs themselves. Usually gets stored.
Binary Coding: Fixed-width in bits per integer  You pick a budget in bits for each int in advance
    Pro: trivially easy to encode and decode
    Bad: a d-gap of 1 costs the same as a d-gap of 200.
Unary Coding: The width of the bits for each integer grows with the size of that int.
    Pro: the encoding is proportional to the size of the int. Resource considerate. 
    Bad: large numbers ballon in resource consumption. 
Gamma: A hybrid approach to coding where the length is coded using unary and the value is coded using binary.

### Zipf's Law
Assumption:
    In the average pile of text, a few words are used constantly and almost every other word is rare relatively speaking.
The whole vocabulary gets ranked by how often each word appears. Rank 1 = common.

cf_i is proportional to 1 / i