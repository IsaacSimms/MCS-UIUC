# Basic idea behind vector space model

##  Note
last lecture was about different types of text retrival models
This lecture, we are honing in on a specicfic modelm the vector space model

## Vector space model (VSM)
This model is a special type of similarity based model **f(q,d) = similarity(q,d)**
So relevance = similarity between doc and query

BUT to actually have the above mentioned assumption be true, we need to define what relevance is, in a way that can be implemented programatically
To do this, the core similarity model assumption stands

### VSM conceptually
**look at illustration .png in this direcotry**
Each term defines a dimension of the space defined
Assumption = all documents and queries are placed in that space.

Lets look at d1 in the illustration, that placement within the vector space means that doc is likely relevant to the terms presidential and library. But, doesn't talk about programming.
In this model, the document's representation in this vector space is the only thing that is looked at. (for example, the order of words is not looked at, as this is bag of words)

Then we look at d2, it lives in a different vector space and is likely relevant to the terms programming and library but not presidential.
But think, a doc that is strongly relevant to programming and library (likely meaning software library) but not relevant to presidential at all, 
could be misleading if you did not take into account at all the lack of relevance to the term presidential.

All the docs in the collection being queries somewhere in this vector -->
The query gets placed in this vector -->
