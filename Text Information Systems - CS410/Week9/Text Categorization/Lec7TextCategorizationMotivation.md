# Text categorization: A form of text data mining and analytics
Related to topic mining (analyzing based on predfined topics) and opinion/sentiment mining

## Definition
- Given a set of **predefined categories** (usually hierarchical) & a set of example text objects already labeled with those categories (as training data):
decide which category(s) a new, unlabeled text object would belong to.
- Clustering = what groups exist? categorization = which one of those known groups does this object belong to?
- system learns the decision rule from those labeled examples

## Why it is useful and forms
- adds a semantic layer on top of raw text for efficient organization, browsing, aggregation, etc. Very useful for huge collections.
- support tactile tasks such as news topic assignment or spam filtering or inbox filtering
- inference of external properties by treating metadata text as a sensor
- Adds another level to how text can be represented. (text can be represented by BOW key words, and categories under this context.)

### Internal
categories that characterize a text object. Categorization derived by the content of the object (topical, sentiment, etc.)

### External
categories that characterize an entity associated with that text object. Categorization derived by metadata. (What author write this article, etc.)

## Variants
- binary:            two categories. spam/not spam. relevant/not-relevant. 0/1 style.
- multi-class:       k amount of categories. There must be more then two mutually exclusive classes
- Hierarchical:      categories form a tree. decisions can be made level by level.
- multi-label/joint: an object can receive multiple labels/categories. Tasks can share information.