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
  
### MAP
MAP  = the *arithmetic* mean of average precision over a set of many queries
gMAP = the *geometric* mean of average precision over a set of many queries
