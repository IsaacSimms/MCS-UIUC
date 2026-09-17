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

To compute the probability of each query word in the doc: the probability of each word is the relative frequency of the word in the document. 
    The count of the query word in the document divided by the total number of words in the document

### Product logic problem
This is based on the assumption that the user has used terms from the documents in their queries.
If the user puts in multiple words into their query from a document, but has a word in the query that is not in the doc, now there is a multiply by zero in the likelihood equation.
This causes all the unigram query likelihood parts to get multiplied by a zero, zeroing out the whole situation.

## Sampling words from a doc model (fixes problem)
- An addition to the unigram query likelihood model
- Instead of document being looked at as a static list of words that is binary (either pulled from or not) the docs are a statistical language model like from lecture
- High value indicators such as "presidential" and "Campaign" from our recent example have higher weights in the statistical langauge model so tip the scales when the example query has them
- But, if a word is added to the query such as "Presidential Campaign update" does not break the equation simply because "update" is in the query but not at all in the document
    This is because "update" is still in te statistical langauge model so it will still get a number in the equation, although the weight in the statiscal language model is low comparatively

## Ranking function based on query likelihood
**see "Text Information Systems - CS410/Week4/Lesson 2 Statistical Language Model/RankingBasedOnQueryLikelihood.png"**

Line 1:
the query (q) is a sequence of n tokens (w_1,w_2...w_n)


Line 2:
This is the unigram assumption as defined elsewhere in this lecture.
- Every query token is an indpendent draw from the same document word statistical distribution
Terms:
- q            = the query (a sequence of tokens)
- d            = the document (who's language model (unigram statistical distribution) we are using as the generator)
- p(q | d)     = probability that this document emits the whole query (quantity that is used to rank)
- w_i          = the token in question (in position i)
**- p(w_i | d) = probability of drawing that token from the doc's unigram distribution**
- X....X       = joining together of clauses (n number) as a product

Line 3:
- Line 2 is probability but line three is turning that probability into a score that can rank
- add log to each probability to preserve order and the products of small proabilities to not disrupt the ranking
- use sum instead of X because you are using the a log identity now. 
- Outside of that, same bones as line 2