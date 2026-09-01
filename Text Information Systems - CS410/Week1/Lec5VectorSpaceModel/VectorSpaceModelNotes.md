# Basic idea behind vector space model

##  Note
last lecture was about different types of text retrival models
This lecture, we are honing in on a specific modelm the vector space model

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
the docs that are closest to the query in vector space are likely to be the most relevant.

### VSM Framework 
**check VSMFramework.png**
VSM is a framework with the following assumptions:
    a doc and query are represented by a term vector
        term: basic concept (usually a word or phrase)
            each term defines a single demension of the vector
            with N terms, there are N dimensions in space
            Query Vector = the different terms in the query get weights, see slide for equation
            Doc Vector   = the different terms in the doc get weights, see slide for equation
            **these query and doc weights are really important, and play a meaningful role in the success of the system.**

### What VSM doesn't do / say
VSM does not define for you what the basic concept is. assumption: that is orthogonal (basic concept = term)
What the term weights actually are (and by extension, where to place a doc or query in vector space)
Note:
    term weight in query indicates how important that term is but in the doc, term weight indicates how well characterized that doc is.
**Similarity measure** is the description of what "near" means in the scoring of docs relevance. How do we compute what doc is closest to the query in vector space programmatically? That is the similarity measure.
*Basically, the VSM is the skelton and many of the definitions within that skeleton need to be dialed in by the engineer for that specific use case.*

