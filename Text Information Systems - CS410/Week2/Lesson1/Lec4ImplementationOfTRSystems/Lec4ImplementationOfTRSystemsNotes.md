# Implementing a text retrieval system from the systems perspective
There is a challenge in scale here. Every query needs responded to quickly, and there are many queries that need responded to concurrently.

## The typical architecture
see "Text Information Systems - CS410/Week2/Lesson1/Lec4ImplementationOfTRSystems/TRSystemArchitectureSample.png" 

### Tokenizer
- 1: The docs are sent trough a **tokenizer**
    The tokenizer turns the raw character steams from the inputs and turns them into terms. 
    Typically, for english, the terms are split on whitespace or punctuation, are turned into all lowercase.
    The output is a doc rep and a query rep respectively

    Normalize lexical units: Words with similar meanings get mapped to the same indexing term
    Stemming: Mapping all inflectional forms of words to the same root form. Example:
        - computer --> compute
        - computation --> compute
        - computing --> compute
        Helpful in most situations but not all


The doc rep is a document specific term list post tokenization. Initially we looked at a bit vector doc rep. 
But, more sophisticated doc reps involve thinks like TF-IDF and BM25t weights.
### Indexer / index
- The doc rep is placed in an **indexer**
    The indexer consumes every doc rep and builds an **index**
        - Indexing is a form of preprocessing
        - **Inverted Index** is the dominating method for indexing (in basic search algorithms) and what is described below
        - The index is a data structure which actually answers the question "which docs have term T?"
        - The index is important because it means that every document in a collection does not need to be walked for every query. Only documents returned by the index need to be walked at query time.

        - The standard structure of an inverted index is essentially two parts that each term gets placed in. The dictionary and the postings list.

#### Dictionary
        - An inverted Map from the terms to the documents that contain them. **for the dictionary**
        - Needs to be fast and accessed at random. In memory is preferred.
        - Hash table, B-tree, etc. are common structures.
        - One entry per distint term with a variety of fields. Common fields include:
            term string = the key the query must hit exactly (essential)
            df_t = how many documents contain t (the term) (this is used in IDF) (essential)
            total frequency: number of times that term appears in those docs
            pointer = byte offset (block ID on the postings list)

#### Postings List
        - The postings list is structured as an actual list.
        - Since sequential access to the postings list based on results of dictionary query is expected, the postings list can stay on disk and be compressed.
            Compression is favorable bc CPU processing is rarely the bottleneck, so decompression is not the bottleneck either. I/O is the bottleneck.
        Every term in the index gets an entry into the postings list. Each entry has the term, and a sequence of document hits, sorted by docID. 
    The Indexer/index process is inherently an offline process.

    The postings list can also store the "position". Helpful for checking if the query is a phrase of two or more words. (close position of terms = phrase)
        This represents the frequency of the term accross documents. For example:
        If term "news" appeared in three different docs one time:
            The Dictionary would show term = "news", num of docs = 3, frequency = 3
            The Postings shows docID = 1,Freq = 1 and docID = 2, feq = 1, and docID 3, freq = 1.
            But, the position is just going to show p1, p2, and p3 since the term is the first term in the Postings and only has a frequency of one across all docs.

        Let's now say that presidential shows up twice in a single doc:
            The dictionary is going to show term = "presidential", num of docs = 1, term frequency = 2
            The Postings shows docID = 3, feq = 2
            But the position shows P6 and P7 for presidential on the same entre since presidential only shows up on one doc but it shows up twice.


### Query rep / scorer
The query rep is a query specific term list post tokenization. Initially we looked at a bit vector query rep. 
But, more sophisticated query reps involve thinks like TF-IDF and BM25t weights.
- The query rep is placed directly into the scorer and the index feeds into the scorer as well. 
    The scorer contains the actual ranking function
    Again, input = query rep and index
    such as: score(q,d) = |q intersection d| where intersection means the number of terms that appear in both the query and document
    The query representation --> scorer is inherently an online process

### Results
- That intersection is served to the user as results

### Judgments / feedback
- The user will then provide judgments on which results from the ranking function where similar, and which ones where not.
That judgment is fed back into the scorer as feedback to improve the ranking function.
    The feedback could be explicit, meaning a research manually telling which ones are good and which ones are not.
    The feedback could be implicit, data on which docs where clicked on by end users is used as judgment
    This feedback loop could be an online or offline process depending on which method is used. 

## Search examples

### Single-term query:
Query gets run though this architecture as describes

### Multi-term boolean query

#### Match term "A" AND term "B"
get all the docs that match term A, get all the docs that match term B, return the intersection of those two results. 

#### Match term "A" OR term "B"
get all docs that match term and and get all docs that match term be and return the union of those results. 

### Multi-term keyword query
essentially the same logic as a disjunctive boolean query (A OR B)
However, aggregate the term weights

### Why inverted index is more efficient then sequentially scanning docs based on the query
Look at the web. An untenable amount of docs. Scanning every doc one by one at query time would take a very long time to return a result to the query
#### Empirical distribution of words
As previously discussed, this decrives stable language-independent patterns uin how people use natural language
Assumption: a few words (the, a, we, of, etc.) occur very frequently and are more closely associated with the structure of the langauge then they are a gage on similarity between doc and query
But, a majority of words in the language occur very rarely and are context specific
Structural (stock) words may be "corpus" specific... meaning they very from context to context

## Zipf's Law
The Empirical distribution of words phenomenon described above is characterized by Zipf's law.

**rank * frequency = constant**
(rank of the word multipled by the frequency of the word equals the constant
    Constant = the product of rank and frequency. Stays roughly the same for every word. However, stock words end up with a much higher constant then all over words.
High frequency words (structural words) = get a very low TF-IDF weight, often removed all together
Intermediate Frequency words            = occur in quite a few documents but they are not as common as structural words, and not as rare as the rare words.
    Used in queries commonly and get a solid TF-IDF weight
Rare words                              = do not occur in documents or queries very frequently. Still very useful for ranking and get a very high TF-IDF weight, if the user happens to query for one of them.
    There are many rare words.

