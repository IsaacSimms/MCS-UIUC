# CS 410 Practice Quiz – Week 10 (Text Clustering & Related)

## Question 1
**What is NOT a motivation for text clustering?**

Text clustering is an unsupervised technique that groups similar documents by content similarity without labels. Standard motivations are obtaining an overall picture of a large collection, linking near-duplicates, and creating navigable structure (e.g., for browsing). Removing spam from a small set of human-annotated examples is a supervised classification task, not clustering.

**Correct answer:** To remove spam documents based on a small collection of human annotated spam documents  
**Why:** This describes text categorization (supervised learning that uses labeled spam examples). The other options are classic motivations for unsupervised clustering.

## Question 2
**For the agglomerative clustering algorithm, which of the following is TRUE?**

Agglomerative clustering is a bottom-up hierarchical method. It starts with each item as its own cluster and repeatedly merges the two closest clusters according to a chosen similarity (or distance) measure and linkage criterion until a single cluster remains, producing a dendrogram. It is not top-down, and the hierarchy depth is not fixed at \(\log_2(N)\).

**Correct answer:** The user needs to specify a similarity measurement.  
**Why:** A similarity/distance function is required to decide which pair of clusters to merge at each step. The other two statements are false.

## Question 3
**Which evaluation method is more applicable for evaluating clustering results of a large collection of documents?**

Direct (external) evaluation compares cluster assignments against a full gold-standard labeling of the collection to compute metrics such as purity or NMI. For large collections this requires annotating every document, which is expensive. Indirect evaluation instead measures whether the clustering improves a downstream application (retrieval, browsing, etc.) with versus without the clusters.

**Correct answer:** Use the indirect evaluation method and test the performance with or without clustering for an application.  
**Why:** Full human annotation of a large collection is impractical; indirect evaluation via a downstream task scales without exhaustive labeling.

## Question 4
**Which category do Naive Bayes classifiers belong to?**

Discriminative classifiers model the decision boundary directly by estimating \(P(y \mid x)\). Generative classifiers model how the data are generated in each class by estimating \(P(x \mid y)\) and \(P(y)\), then apply Bayes’ rule. Naive Bayes is generative: under a feature-independence assumption it estimates class priors and class-conditional feature probabilities from counts, then classifies by maximizing the posterior.

**Correct answer:** Generative classifiers  
**Why:** Naive Bayes explicitly models the joint distribution via class-conditional densities and priors rather than learning a decision boundary directly.

## Question 5
**Which task is unsupervised in general?**

Text categorization (classification) assigns documents to predefined categories and requires labeled training examples. Text clustering groups documents by similarity without any predefined labels or training examples.

**Correct answer:** Text clustering  
**Why:** Clustering discovers groups from the data alone (unsupervised). Categorization needs human-annotated labels (supervised).

## Question 6
**Which variation of the hierarchical text clustering algorithm is least sensitive to outliers?**

In agglomerative hierarchical clustering the linkage criterion defines inter-cluster distance:
- Single-link uses the minimum pairwise distance (highly sensitive to outliers via chaining).
- Complete-link uses the maximum pairwise distance (less sensitive than single-link but still affected by extremes).
- Average-link uses the average of all pairwise distances (outliers have less influence).

**Correct answer:** Average-link  
**Why:** Averaging all pairs dilutes the effect of extreme points, making average-link the most robust of the three to outliers.

## Question 7
**Which algorithm involves a process that is close to an EM algorithm?**

EM (Expectation-Maximization) alternates an E-step (compute expected values of latent variables given current parameters) and an M-step (update parameters to maximize the expected complete-data likelihood). K-means can be viewed as a hard-assignment special case of EM for a mixture of spherical Gaussians: assignment is a hard E-step and centroid update is the corresponding M-step. Standard Naive Bayes training is a single-pass count-based MLE, and agglomerative clustering is a deterministic merge process.

**Correct answer:** K-means clustering  
**Why:** Its assignment + centroid-update loop is a hard-assignment approximation of EM. The other two algorithms do not involve an analogous iterative expectation-maximization process.