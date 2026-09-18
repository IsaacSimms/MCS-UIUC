# Types of Smoothing
## how do you smooth p(w | d)?
To implement query likelihood function plus smoothing there are still two variables that need to be sorted out:
- P_seen (w | d) = ? (the probability that a specific word is in a document (exactly))
- alpha_d = ?        (the share of probability that is reserved for words that the document never uses) (technically reserved from the document's perspective)

### Using the Linear Interpolation (Jelinek-Mercer) Smoothing (LM Smoothing)
**see "Text Information Systems - CS410/Week4/Lesson 3 Smoothing Methods/LinearInterpolationSmoothing.png"**
-Finds Unigram LM p(w|d)

Remember, if a term is in a query but not in a doc at all, zero P_seen (w | d) would be allocated to the term without smoothing
- Use a collection LM (P(w|C)) to allocate a small probability to all terms in collection
    Smoothing Parameter (lambda) = between (0,1) and applied before (P(w|C))
    Short keyword queries want small lambda (trust the doc). Long/verbose queries want larger lambda (explain the glue words from the collection).

### Dirichlet Prior (Bayesian) Smoothing (DP Smoothing)
**see "Text Information Systems - CS410/Week4/Lesson 3 Smoothing Methods/DirichletPriorSmoothing.png"**
Much like the Linear Interpolation smoothing, you are going to use a Collection LM combined with a unigram LM to give high weight to key query words, but some probability to query words that are not in the document. 
- better on short, title queries (Linear Interpolation is better on long, verbose queries)

here mu is used. A way to think about it is the collection "donates" mu extra tokens for this document, for allocation to the probabilities of terms in the query but not in the doc. 
Mu is set to a constant. Every word gets this "sudo count" in their probability
    This meas that longer docs get less of a smoothing then shorter ones.
