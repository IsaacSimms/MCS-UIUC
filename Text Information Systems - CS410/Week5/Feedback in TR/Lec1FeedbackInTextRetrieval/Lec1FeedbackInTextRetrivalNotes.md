# Feedback in Text Retrieval
Feedback: using evidence after the first ranking to rewrite the query (or the query model) then searching again in an iterative fashion.

## Relevance Feedback:
a form of TR feedback where users make explicit relevance judgement on the initial results.
(about which returned documents are relevant and not relevant)
The document collection and those judgement then go into a feedback module, then an updated query is created and fed back into the retrival engine.
Downside: extra effort on behalf of user. 

## Pseudo/blind/automatic feedback
Same general structure as relevance feedback but the top "k" initial results are assumed to be relevant.
Less reliable but less effort on behalf of the user.
This can be effective for adding words to the query but are associated with it still. Such as "software" being  indication that that doc is about "computer" bc those top doc judgement can be fed directly back into the query

## Implicit Feedback
Lives under the assumption that user-clicked docs are assumped to be relevant, and skipped docs are non-relevant.
Judgments aren't confidently reliable like in Relevance feedback, but it is not any extra work like from automatic feedback.
Follows the same feedback workflows as relevance feedback outside of what determines if a doc is relevant.

