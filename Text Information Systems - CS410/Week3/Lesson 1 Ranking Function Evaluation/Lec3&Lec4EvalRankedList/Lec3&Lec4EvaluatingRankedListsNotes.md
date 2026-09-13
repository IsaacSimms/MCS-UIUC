# How to evaluate a ranked list output of a ranking function
Precision and Recall are the main ways to quantitively analyze a search result

## How to use precision and recall to analyze a ranked linked
**use precision and recall within different cutoffs** 
Generally, "where the user will stop browsing" is where we want to put those cutoffs. (common for 10 docs to be cutoff)
    For convienance/viability, common to assume that precision is 0 at all other documents beyond the cutoff
### Comparing two PR Curves
Think a line graph with points.
Precision is the Y axis
Recall is the X axis
Plot the points (each doc retrieved) on to the graph. Draw a line connecting all of the *relevant* docs retrieved.
    That is how you get a PR Curve

Do that same process for two different ranked lists from two different systems on the same graph. You can now use the curves on that graph to compare the precision and recall between the two systems.
    You are looking for "at the same point in recall, which system has better precision?" (Higher the curve is better)

One way to measure the precision-recall curve, look at all the same under the line on the graph. 
    Take a look at every recall point and then calculate average precision:
        Add up relevant docs precision metric: 1/1 + 2/2 + 3/5 + 4/8....    
        Divide by total number of docs (10)
    Using this average precision method is not only sensitive to precision based on recall, it is also sensitive to the order in which the docs where ranked

## Mean Average Precision (MAP)
### Precision
- The average of precision at every cutoff where a new relevant document is retrieved
- Normalizer = the total number of relevant docs in a collection
- Precision is sensitive to the rank of each relevant doc
- Looks at a single query, and the corresponding results
  
### MAP & gMAP
For both of these, you are still taking the average percision from many different ranked list results and "smashing" them together into a mean in some way.

MAP  = the *arithmetic* mean of average precision over a set of many queries
    This is the traditional way that you would find the mean of something. 
        Take all of the average precision values in question and add them together.
        then divide that new value by how many original values where added together.
    MAP is dominated by large values
        It means the query is easy, with a high average position
    If you are you are evaluating a ranking function hoping to improve it or analyze it for all types of queries, MAP is a better option

gMAP = the *geometric* mean of average precision over a set of many queries
    gMAP does end with a mean value, but you get there through a different methodlogy.
        Take all of the average precision values (Q) in question and *multiply* them together.
        then take the Q-th root of that value to find the gMAP
    gMAP is dominated by low values
        Poor performing queries with a low average position
    Therefore, if you are evaluating a ranking function with the hopes of attempting to improve the algorithm for poorly performing queries, gMAP is a better option.

### Special case, Mean Reciprocal Rank
This is when there is only one relevant document in the collection (known item search)
Average precision = Reciprocal Rank = 1/r
Mean average precision --> mean reciprocal rank
