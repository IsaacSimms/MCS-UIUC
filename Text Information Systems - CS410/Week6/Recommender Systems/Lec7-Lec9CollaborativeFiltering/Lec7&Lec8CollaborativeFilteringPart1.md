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
Algo in Screenshot is the memory-based approach
