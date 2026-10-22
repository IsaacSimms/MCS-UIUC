# Text Clustering
## What is text clustering?
Input into the system is a pile of unorganized text objects. Text clustering is architecture and workflows which put similar objects together into "piles" which reflect the underlying structure of the input.
- "Objects" can be documents, terms, passages, websites, etc.

## The clustering bias
Defining similar under this context is a difficult problem to solve. 
Two things can be similar or not depending on the viewpoint you choose.
A user/engineer must define the perspective for assessing similarity.
A clustering task is only well defined once the user declares the perspective (bias) that should be used. 
    **Remember**: The clustering bias makes it so that there is a uniquely correct answer. Without that perspective, there is no right answer.

## Examples
- One could cluster docs in a collection
- terms can be clustered accross docs to define things like concepts/themes/topics
- Cluster any selected text segment
- can cluster websites or based on metadata (example being all articles by a particular author)

