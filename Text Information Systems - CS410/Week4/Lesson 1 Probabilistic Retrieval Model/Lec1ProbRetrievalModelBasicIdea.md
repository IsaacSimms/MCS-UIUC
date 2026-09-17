# The probabilistic retrieval model - much different then vector space models

- BM25 is a probabilistic model. (who's form is similar to a backwards space model and it is widely used, which is why it has been discussed previously)
- This lecture discusses a form of language model --> *query likelihood*
- PL2  is a "divergence-from randomness" model, which is one of the most high performant architectures to date.

## Assumptions
- R is an element of {0,1} and is introduced as a binary random variable.
- query and documents are observations from random variables (in a vector space model, they are assumed to be vectors)
- **Probabilistic models: f(d,q) = p(R = 1|d,q)** (again, given that R is an element of {0,1})

## Query Likelihood
In query likelihood, the assumption: the probability of relevance equation can be approximated by the probability of a query, given a document and that docs relevance.
(Solves: If a user likes doc d, what is the likelihood that user will enter query q in order to retrieve d)

**p(R = 1|d,q) = p(q|d,R = 1) (this is approx. not a true =)**

This esssentially means if we look at results and see q1 in the first column and d2 in the second column, what is the likelihood that 1 (meaning relevance) is in the R column.
Therefore, the equation can also be written as:

**count(q,d R = 1) / count(q,d)**