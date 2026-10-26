## Text categorization Evaluation
Compare a system's category assignments against a human/agent/external system labeled ground truth on a test collection.

## Evaluation methodology quick hits
- have humans create test collection with tags (ground truth)
- generate categorization results on text collection
- compare system categorization against ground truth

Higher similarity = better results.
- similarity can be measured from different perspectives
- not all categorization mistakes created equal. Different mistakes have different costs, and that depends on the perspective/use case.
- **Evaluation is a relative comparison of methods**

## Contingency table outcomes (per category)
Contingency table: 2×2 count of every system decision against the ground-truth label for a given category (or set of categories).

- True positive (TP): system and ground truth both say yes
- False positive (FP): system says yes, ground truth says no
- False negative (FN): system says no, ground truth says yes
- True negative (TN): Both system and ground truth say no

### Classification Accuracy calculations (percentage of correct decisions)
**Accuracy = (TP + TN) / total decisions**

A pro is this style of accuracy calculation is relatively easy to do. Metric works well when the training data is very good.

Con:
Class imbalance is one class is far more common than the others in the test data. System scores really well on that set but it may be more important to get decisions right on some docs or categories than others, and the system could miss the mark.
Email spam filtering is an example. Very bad to block a good, important email, much more so than letting one spam slip through. 

### Precision and Recall calculations
- **Precision = TP / (TP + FP)**
When the system says yes (blocks email as spam in the above example) how often is it correct?

- **Recall = TP / (TP+ FN)
Out of all the items that should have been yes, how many did the system catch? (How many spam emails did the system actually block)

Both can be computed per category or per document

### F-measure
**F_1 = 2 * ((Precision * Recall) / (Precision + Recall))**

Single number summary when you need to balance precision and recall.

## aggregating evaluations across many categories
You can get an accuracy, precision, and recall of each category. You need to be able to get one overall number.

### Macro-average
calculate the metric separate for each category. Then take arithmetic or geometric mean of those numbers.
Each category contributes equally regardless of how many docs

### Micro-average
throw every document-category decision into one giant contingency table and compute precision/recall once from the pooled count.
Larger categories dominate result.

