# Search engines (SE)
This lecture discusses how search engines work in detail.
### Pull
A search engine is one of the most common implementations of the pull mode of text access.

## Overview - three things discussed
Define text retrieval (TR)
TR vs Database Retrieval (DR)
Document selection va Document Ranking

### Test Retrieval "Search technology
Given              = collection of text (documents) exist
input at "runtime" = user provides query
Output             = the SE returns relevant docs
TR is a form of information retrieval. (not all information retrieval is text retrieval but all text retrieval is a form of information retrieval)

Note: Text retrival is still at the core of information retrieval at a broader scale. e.x. to search for videos, the companion text (metadata and tags and all that) is what actually gets searched in order to serve you the video that you are looking for. 

### TR vs Database Retrieval (DR)
TR = unstructured data and ambiguous
DR = structured data (with exceptions)... well defined semantics

TR = query is often ambagious and incomplete too, since its natural language just like what is being retrieved.
DR = query is very well defined semantics (SQL dominates) and outlines the complete specification of what is required when written well

TR = returns things that are determined relevant
DR = returns exact matched records to query

This lands TR as being empirical. There is no one mathematicall proof that one method is going to work better in every use case then another.
Success is often determined by evaluation involving users.

### What goes into TR formulation (see image)
Vocab (V)   = established syntax of the NL going into the TR (or langauges)
query       = Each q sub i (word in query) should be in V.
Document    = text data returned. usually much larger then the query but not always
Collection  = group of docs. Can be huge. (the whole web is a collection)

Set of relevant docs is generally unknown. Its user dependent. The user query is only a part of the information used to return result

Task        = **compute R'(q), an approximation of R(q)**... in laymen terms: we know that the relevant set is the set of docs that satisfies the query. But:
the system doesn't have a set like that handed to it on a silver platter. Different users could have different relevant sets from the same query. Therefore:
The task explains that unknown gap between the relevant set and where the system is currently at.
    R(q)  = set of docs that should come back from query (relevant set)
    R'(q) = the docs that the search engine actually returns.

#### How to compute R'(q)
##### Strat 1 = Document selection
A binary classification function is used. That function makes a yes or no decision on every document in the collection. If yes, the doc goes in R'(q) if no, then it stays out obviously. relevant noted as 1, not relevant noted as 0.
This is **absolute relevance**
##### Strat 2 = Document ranking
Here, value score is placed on each doc based on the likelyhood the doc is relevant to the query / how relevant the doc is.
There is a cutoff (theta) and all docs with a relevance score above that threshold is returned.
This is **relative relevance**... system only decides if a doc is more relevent then another.
###### Document ranking is preferred in most use cases
Some of the reasons for this is that the classifier is probably inaccurate:
    over-constrained query = no relevent docs
    under-constrained query = over delivery
    Finding the happy medium between the two extremes in Document Selection.
Let's say we are able to return all the relevant docs via doc selection so that problem does not exist. You still want to rank the docs. Relevance is a matter of degree.
You don't want to oversaturate the user, and hit them with something that is high value.

###### Probability Ranking Principle
This is a theoretical justification for ranking docs.
"Returning a ranked list of documents in descending order of probability that a document is relevant to the query is the optimal strategy under the followign two assumptions:
    the utility of that doc to a user is independent of the utility of any other doc served
    a user browses results sequentially
Neither of these are true in all results / use cases (but arguably relevant in many uses)