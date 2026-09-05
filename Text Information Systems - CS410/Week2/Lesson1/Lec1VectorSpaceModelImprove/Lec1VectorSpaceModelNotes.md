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

## Term Frequency Vector (TFV)(improvement)
note: a slot is a coordinate of the vector space. one slot = one term in the vocabulary. the vocabulary *is* the vector space.

In a TFV, the VSM document or query with raw counts in the slots instead of bits. **TFV promotes tracking term frequency**

In our previous heuristic from week 1, set membership was used to populate the weights:
    Tokenize the doc --> throw away order of words, just have a group of words --> keep a set of terms that occurred in that group --> slot x is 1 if the term is in the set, and 0 if it is not.
    that 1/0 are the bits. 

To get the counts, the same tokenization and general workflow occurs as previously described. However, you keep a multiset. And in that multiset, how many times that token was fired total is stored.
    This allows us to store the fact that the token "presidential" fires twice in Doc 4
