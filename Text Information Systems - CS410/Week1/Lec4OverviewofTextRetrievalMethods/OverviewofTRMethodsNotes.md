## Remember
We are talking about "Pull" text retrieval (TR) methods
Last lecture we discussed calculating the relevant of documents (R'(q)) i.e. when provided with a query, the set of documents returned that is actually relevant to the query.
There is document selection which is looking at an absolute relevance (yes / no) and there is document ranking which is looking at relative relevance
Relative relevance is the most common and best practice in a majority of use cases.
This lecture discusses different types of document ranking function.

## Designing a ranking function
**Look at the ranking function .png in this directory**
The queries (q) is a collection of words
The documents (d) is also a collection of words
The ranking function (f), if built well, should be taking q and d as arguments (f(q,d)) and return all ranked relevant docs on top of non-relevant ones.
**key**             = the function needs to measure the ***likelihood*** that the d is relevant to the q
**Retrieval model** = used to do the key. The model formalizes relevance by giving that metric a computational definition.

## Different type of retrieval models
**see RetrievalModels.png**
### Similarity based models
**f(q,d) = similarity(q,d)**
assumption = if one document is more similar to the query then another document, then that document which is more similar must be more relevant to the query
### Probabilistic models
**f(d,q) = p(R=1|d,q), where R *element-of* {0,1}**
assumption = queries and docs are observations from random variables.
R = binary random variable. Indicates if doc is relevant to query
A doc's relevance to a query is given by the probability that R is equal to 1
types:
    classic probabilistic model
    language model
    divergence-from-rnadomness model
### probabilistic inference model
**f(q,d) = p(d-->q)**
associate uncertainty to inference rules. 
quantify probability that we can show query follows from doc from that inference rule.
### Axiomatic model
**f(q,d)**
must satisfy a set of constraints to be determined as relevant

#### worth noting
The relevant set of docs returned for any one query is going to be similar accross all of these different models
and similar variables. Therefore:

## common ideas and form of state of the art retrieval models
### Note:
bag of words remains the most used model in search engines to this day.
And what will be used for this part of the lecture
### computed score
remember f(q,d)
lets say q = "presidential campaign news"
the score of a doc is going to be determined by looking at each word in q independently.
#### number of heuristics used in bag of words
Term Frequency     = How many times does "presidential" occur in d? c("presidential", d) more hits = more relevance
Document Length    = How long is d? |d| in general, if a term occurs many times in a document that is much longer it is NOT as significant as that same term occuring just as many times in a document that is much smaller.
Document Frequency = How often do we see "presidential" in the entire collection? df("presidential) P("presidential"|collection)

All of these are determining the popularity of a term in the collection. Accross all of them, matching a rare term from query to doc contriutes more to relevance factor then matching a common term.

## Commonly used models and which is best (considered state of the art)
Note: when truly optimized all of the below models tend to perform equally well
- Pivoted length normalization
- BM25 (most popular)
- Query likelihood
- PL2
