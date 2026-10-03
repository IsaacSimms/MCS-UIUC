# Collaborative Filtering
**This is looking at the user similarity**
i.e Look at who likes X, and then check if U is similar

## Definition
Makes a filtering decision for one user from judgement of other users. Does not look at item content. 
- An individuals interests/preferences are inferred from that of similar users

### Assumptions
- Shared interests implies similar preferences (an interest in astronomy implies a preference for scientific research)
- Shared preferences implies similar interests (an interest in scientific research implies a shared interest in achedmic publishers)
- There are enough observed preferences to be able to make a judgement. 

#### Two instuitions
- user to user: If joe and jane like the same papers, if joe likes a new paper, jane probably will too. 
- item-item: If 90% of people who like start wars also like independence day, liking star wars is a predictor that you like independence day. 

### Collaborative filtering problem
A partially observed rating matrix is common. (illustrated as a box. Rows are users U, columns are objects O).
Filled cell is a known rating, an empty cell is where the prediction occurs. 
X_ij = f(u_i, o_j), where f maps U × O to real numbers.

# // == Lec 8 notes start here == //
**Take that collaborative filtering problem and describe how to fill in the missing cells in the matrix

##  Memory based approaches
Memory-based = keep raw rating matrix of item in memory. No model is fit. to fill the missing user_a rating on the object, find users similar to user_a and take the weighted average of their ratings.
    *user_a's rating of object_o is not taken into account here, that field is empty*
There are sub methods differing in the similar weights.
Not all users contribute the same amount to the metric. The weights control that inference. 
    If the recommendation system is pulling content for user_a, and user_i is more similar to user_a then all other users, then user_i is going to control the most weight.
Algo in Screenshot is the memory-based approach

## User Similarity Measures
User similarity is the weight w(a,i) in the memory-based predictor. The formula that answers the question: how much should user_i's rating of object_j count towards predicting user_'s missing value. 
The pearson correlation coefficient (in screenshot) is the equation here. Only sum over items both users have rated.
Cosine is another

## Recommendation summary
- Recommendation filtering is "easy" as compared to pull based information retrieval.
Expectation is low, any successful recommendation is generally better then none.-
- Filtering is "hard" bc the decision has to be immediate and binary.
Also difficult due to data sparseness (limited feedback).
And cold start (there is little user information at the beginning).
- Understand difference between content-based vs. collaborative filtering vs hybrid
- Recommendation is often combined with search for a push + pull architecture
