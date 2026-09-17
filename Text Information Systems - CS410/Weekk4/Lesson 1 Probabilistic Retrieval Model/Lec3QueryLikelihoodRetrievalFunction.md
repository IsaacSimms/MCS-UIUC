# Query Likelihood Retrieval Function - a probabilistic model
- When a user likes a particular doc, what is the likelihood a specific query is going to be apposed
    The assumption being that if a user is thinking about a document which a bunch of specific terms in it, those same terms are going to be used to pose the query
        Each word becomes independent of the sample

## Unigram Query Likelihood
Rank the documents by p (q | d): This is th probability that document d's language model generates query q
Assumption made: 
- Every query word is generated independently
- order of phrases do not enter the score
Example:
q = "presidential campaign"

d = a document that contains those words

p(q | d) = p(“presidential” | d) * p(“campaign” | d)
 = c("presidentail", d) / |d| * c("campaign", d) / |d|
