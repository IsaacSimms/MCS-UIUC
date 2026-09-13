# The focus of this whole lecture series is ranking function evaluation
The ability to definitively judge weather a ranking function actually ranked documents based on true relevance to the query, as defined by what a human would consider relevant.

- used to assess the actual utility of a TR system
    this utility measurement should eval the useful nes to users in a real application
    common to do this judgement via user studies (interactive IR eval)
- used to compare different system and methods, determining which TR is best
    Only measure what is needed to correlate utility for actual users (doesn't have to be exact)
    Often times done through test collections (IR evaluation)

## What should be measured
- Effectiveness / accuracy = how accurate (relevant) are the search results
    ability of the system to rank relevant docs **on top** of nonrelevant ones
- Efficiency               = how quickly is the user able to get those results
    both space (memory / disk) and time overhead
- How useful is this system for real user tasks
    user studies are essential here

## Cranfield Evaluation Methodology
- This is the standard way to evaluate retrieval systems without a human in the loop
- **reusable** test collections and defined measures are apart of the methodlogy (same test collection used to compare different systems)
- Freezes three things (three things are fixed before systems are compared)
    a document collection
    a set of queries
    relevance judgement (for a query, ranked list of which docs are relevant to nonrelevant) (binaries)
- an ideal ranked list for the test collection is defined. The system's result is compared to that ideal list to quantify success
    note, that what an "ideal list" is, can very from use case to use case or user to user. 
        When comparing two systems, system A could produce less total docs, most of which are relevant, but it does not have every relevant doc
        system B could produce all relevant docs but could produce some docs that are not as relevant and rank them high, creating noise. 
        No one of these options is better than the other in all use cases. It depends on what that user population needs for that query
- for laboratory testing of system components, built in the 1960s originally.
