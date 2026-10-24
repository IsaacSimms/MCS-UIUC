# Evaluating the performance of clustering
The success or failure of clustering is only meaningful relative to the stated *clustering bias*
- Any two objects can be similar depending on how you look at them. 
(could be as simple as if the bias is "docs are in the defined collection" then everyhing is similar at that point)
- This is, again, why the human in the look **must define perspective/bias** for assessing similarity in clustering

## Direct Evaluation
Humans are in the evaluation loop. 
- Humans examine the text objects in some capacity and produce an "ideal" clustering that affects the defined needs.
- The human defines how closeness can be quantified. (which could be from multiple perspectives)
Essentially, a human has defined a clustering bias.
- That human built cluster is then held as a gold standard. 
Anything the system outputs is measured against that gold standard to evaluate success.
That is done by quantifying the similarity between the system-generated clusters to the gold standard clusters.

## Indirect Evaluation
Measuring whether the clusters improve some external task or benchmark. A measurement of utility
Example: better browsing, retrieval, features, etc.
