# Using similarity based approaches to do Text Clustering
- Similarity-based clustering = explicitly defining a similarity function between text objects and then partition them to maximize intra-cluster similarity while minimzing inter-cluster similarity.
    You are explicitly providing a view of what "you" as the user thinks are similar.
    Intra-group similarity = how similar objects *inside the same cluster* are to each other.
    Inter-group similarity = how similar objects *in different clusters* are to each other.
## There are two primary strategies for obtaining optimal clustering:

### Hierarchical: a tree of clusters is progressively built. 
- Agglomerative: start with every object as its own cluster and repeatedly merge the most similar paid until everything is in larger and larger groups.
Stops when stopping criterion has been met (such as number of clusters reached) or when a similarity requirement (weather that be intra-group or inter-group) has been met.
- Divisive: Start with one big cluster and repeatedly split it apart.
- Once you make a full hierarchy, you can cut the hierarchy off at different cluster levels for different use cases. (maybe you are topic mining on a specific set of key words so you only need certian clusters. Or you are browsing, so you need the whole hierarchy.)
- Three common ways to reduce pairwise similarities down to one number:
    1. single-link: similarity of *closest pair* of objects. 
    Groups are considered similar if any member of one is close to any member of another.
    As long as one object in each group are similar to each other, the clusters are linked.
    Tends to produce loose, long chain like clusters.
    2. Complete-link: similarity of *farthest pair* of objects
    Groups are considered similar if any member of one group is reasonably close to every member of the other.
    Every object in each group have to be similar to each other for the two clusters to get linked.
    Tends to produce compact, "spherical" clusters
    3. Average-link: average similarity of *all pairs* of objects.
    If objects are similar on average then the clusters will link.
    A compromise between the two extremes.

### Flat/partitional: start with a guess of what should be clustered (random or seeded) then iteratively improve a flat partition of K clusters.
- k-means clustering is a common form.
Represent each text object as a term vector adn assume a similarity function defined on two objects.
High level breakdown.
1. Choose the number of clusters (K) in advance
2. start with K initial centroids
3. Repeatedly:
- assign every document to its nearest centroid
Approx the **E-step** of the EM algorithm. The vector is what gets assigned.
- recompute each centroid as the average of the documents currently assigned to it (until the assignment stops changing)
Approx the **M-step** of the EM algorithm. each centroid is recomputed as average of the vectors now assigned to the given cluster.

Note: this is repeated until the similarity-based objective function converges.
