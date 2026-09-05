# THE TF-IDF MODEL
# How to improve the instantiation (a specific instance or example) of the Vector Space Model (VSM)
# i.e. VSM continued


### Remember:
Example:
Query = news about presidential campaign
Doc 2: news about organic food campaign                         -- f(q,d2)=3
Doc 3: news of presidential campaign                            -- f(q,d3)=3
Doc 4: news of presidential campaign ... presidential candidate -- f(q,d4)=3

Under our original instantiaito of VSM all three of these docs would score the same against that query. 
But, Doc 4 should score higher then both of the other docs due to the use of the word "presidential", a high value word, twice. 
And, Doc 2 should not get the same bump to its score for having the word "about", a very common word, to a different doc that is using the word "presidential", word that is much less common and more likely to be a signal of doc --> query relevance

These problems occur largely because of assumptions on how the vectors in the vector space. 
We will solve these two problems in this lecture. To do this, we need to change how the vectors are placed in the Vector space. 

## Term Frequency Vector (TFV)(improvement by understanding how often term occurs)
note: a slot is a coordinate of the vector space. one slot = one term in the vocabulary. the vocabulary *is* the vector space.

In a TFV, the VSM document or query with raw counts in the slots instead of bits. **TFV promotes tracking term frequency**

In our previous heuristic from week 1, set membership was used to populate the weights:
    Tokenize the doc --> throw away order of words, just have a group of words --> keep a set of terms that occurred in that group --> slot x is 1 if the term is in the set, and 0 if it is not.
    that 1/0 are the bits. 

To get the counts, the same tokenization and general workflow occurs as previously described. However, you keep a multiset. And in that multiset, how many times that token was fired total is stored.
    This allows us to store the fact that the token "presidential" fires twice in Doc 4

### Term Frequency weighting (formula)
N = total size of vocabulary

q=(x_1,...x_N)
    q stands for the query in question
    x_i = the raw count of W_i in the query (how many times that specific token fired in q)

d=(y_=...y_N)
    d stands for the document in question
    y_i = the raw count of W_i in the doc (how many times that specific token fired in d)

Sim(q,d) = q.d = x_1 y_1 + ... + x_N y_N = summation ^ N _i=1 x_i y_i

## Inverse Document Frequency (IDF) (improvement by understanding the commonality of terms)
Fixes the problem with "stock" (common) words having weight in the similarity calculation that they should not have.
    (having teh word "the" in both the query and doc does not give you insight into if the doc and query are similar)

These stock words are common everywhere. Use global statistics of documents (in the whole collection)
    If almost all docs have the same term, that term is considered stock.
    If a small percentage of documents contain any one term, that term is considered rare.

Terms that are rare, meaning they do not appear in the collection very often, are rewarded with a high IDF score. They get more weight.
Terms that are stock words, which occur in almost every document, do not get a high IDF score and are downweighted. (examples include "the" or "of")

**IDF(W) = log((M+1)/df(w)**
    M = total number of documents in the collection
    df(w) = document frequency (total number of documents containing that specific term)

