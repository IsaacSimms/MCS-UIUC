# Notes about how to unlock fast search invert index

## General scoring function 
Look at "Text Information Systems - CS410/Week2/Lesson1/Lec6FastSearchSystemImplementation/GenFormOfAScoringFunction.png"

VSM is techincally a type of scoring function, although there can be many types. 

a function (f) for query (q) and document (d)

f_a = a function that considers to adjustment factors
    f_d(d) and f_q(q)

Inside that f_a function, you have another function called h. 
    h is the scoring function
    g(...)... functions are what weight the matched query term in d
    h aggregates it.

Then the f functions do the final score adjustments

## General ranking function
Look at "Text Information Systems - CS410/Week2/Lesson1/Lec6FastSearchSystemImplementation/GenFormOFARankingFunction.png"
the same demarking on what each variable means and all that stands as compared to the generic scoring function previously discussed

f_d(d) and f_q(q) are pre-computed and ready to go at query time
A score accumulator is maintained for every d. that accumulator is used to compute h

For each query term t:
    fetch the inverted list (from the index)
    For each posting (d_j, f_j) on that list:
        compute g(t, d_j, q)
        add f into d_js accumulator
            If d_j does not have an accumulator, create one
        then incrementally build the running total in h off of that
    Adjust f_a and sort

**Note that only documents that are matched with a query term are processed**

### Accumulators
A note as it relates to accumulators:
- There is only one accumulator per document. Regardless of if there are multiple terms in that query.
- Let's say the query is multi word, something like "information security". 
- If a document contains just the word information or just the word security, it gets pulled into the ranking function and allocated an accumulator
- If the document contains both the words information and security, it still gets pulled into the ranking function and allocated a single accumulator
- Accumulators are going to get initialized to zero and filled with the weighted scoring of the terms relationship to the document.
    (if you are ranking based on raw TF sum, the accumulator is going to hold that raw count of how many times each term occurred in each doc)

## General efficiency improvements when doing ranking function BM25
Caching data (query results/recent queries, list of inverted index)
Keeping only the most promising accumulators
Parallel processing (required to scale up to web level datasets)