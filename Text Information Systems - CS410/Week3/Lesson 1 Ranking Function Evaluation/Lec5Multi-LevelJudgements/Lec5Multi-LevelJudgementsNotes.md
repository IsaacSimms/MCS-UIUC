# Ranking Function Evaluation when there is multiple "Levels" of judgement
*Up until now this has been a discussion of binary judgement. A doc is either relevant or non relevant*

## Multi-Level Judgement
*Multi-Level in this context means that the relevance judgement iws a matter of degree. Some docs highly relevant, some docs moderately so,some docs not at all*

Precision and Recall both rely on binary judgement. For multi-level, we use **Gain**

### Gain
How much gain of relevant information a user can acquire by reviewing a document
A scale (with either tier being assigned a numeric value. So non-relevant = 1, moderately relevant = 2, very relevant = 3, etc.)

#### Cumulative gain
As you go down the ranked list, add up all the gain into a single value

cumulative gain at D1 is just its gain (3)
cumulative gain at D2 is D1 + D2 (3 + 2)
cumulative gain at D3 is D1 + D2 + D3 (3 + 2 + 2)
so on and so forth

#### Discounted Cumulative Gain (DCG)
Note: Cumulative gain does not take into consideration the position of documents
This fixes that problem and forces the position of the documents to be a factor on the end result.

D1 = the gain of that doc (3)
D2 = the gain on that doc divided by log 2 (2/log(2))
D3 = the gain on that doc divided by log 3 (1/log(3))
so on and so forth. 

You then add all those up, much like traditional cumulative gain
3 + (2/log(2)) + (1/log(3))...

#### The last step: Normalization (nDCG@k)
Normalize the DCG:

DCG@10
/
IdealDCG@10

- DCG is the actual ranked list result from the ranking function in question, as described above
- An "Ideal DCG" revolves around the concept that all highest rates docs in the collection are going to be at the very top of the ranked list
(If there are 9 highly relevant docs (3) in the collection and the cutoff is ten, D1-D9 will be three and D10 will be 2, in this example)

This compares the actual returned DCG values with the most optimal outcome. This will map the DCG values into a range between 0 and 1
    Highest (best) value is 1 (the ideal list)

We are wanting to evaluate these ranking functions accross multiple topics/queries to get an overall sense, not just one topic. 
    If you do not normalize the DCG in this way, different topics will return different DCG scales for each system.
    Another way to put it is that we don't want the results to be dominated by high (easy) values
        9 highly relevant docs is going to return a high DCG. But a query with only 2 highly relevant docs in the whole collection cannot return a high DCG
    This normalization solves that problem and has all queries/topics evaluated on an even playing field