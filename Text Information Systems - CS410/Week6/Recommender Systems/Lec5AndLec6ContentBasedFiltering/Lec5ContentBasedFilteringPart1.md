# Recommender systems. Many methodologies used in search are applicable to recommendation systems
**Remember there are two different modes of text access, push and pull. Search engines are a pull access, where recommendation systems are a push access**

In push, the system takes the initiative when there is a stable information need or the system has a good understanding of the user's need.

## Recommendation system, a form of filtering system
- User has a stable and long term interest in a dynamic information source
- The system makes a delievery decision immediately as the document arrives. 

### The basic question: Will User (U) like item (X)
THere are two different ways to answer this question: 
- System looks at what the user likes. Then, checks to see if X is simliar to what the user already accesses.
- System looks at the users who already regularly interact with X, and then decide if user (U) is similar to those other users
*these can be combined for a hybrid system*

## Typical Content-based filtering system
**Recommends items by matching item content against a model of one particular user's interests. (does not use collective user behavior)**
- Core of the system is a *user interest profile*, which is a binary classifier/utility function. (has the knowledge on the user's interests)
"User profile text" is fed into the initialization stage, which is what feeds into the binary classifier. 
- Includes a learning module, which takes accumulated docs and feedback from the docs the user accepts, and feeds that back into the binary classifier

### Utility function
- Used to evaluate a content-based filtering system. (search ranking evaluation functions do not meet the needs for content evaluation functions)
- Utility function has a set of already labeled doc delieveres. It comapres that set to the set of docs the binary classifier returns as #good (a delievered document that the user treats as relevant) and #bad (a delievered document that the user treats as not relevant)
- A good binary classifier has a utility function which returns as many good docs as possible with as few docs as possible. 

### Three problems in content-based filtering
- making the filtering decision 
doc text w/ profile text --> yes/no
- Initialization
The filter getting initialized based on only profile text or a very few examples
- System must learn... from:
limited relevance judgement. 
A set of accumulated documents. 
- This must all be done with the ability to maximize the utility & utility for the user

### Extending a retrival system for information filtering
- retrieval techniques can be used to score documents, and that can be used to weight the filter
- implement a score threshold for filtering decisions
There are many approaches to threshold settings and ML
- use traditional feedback for improving scoring