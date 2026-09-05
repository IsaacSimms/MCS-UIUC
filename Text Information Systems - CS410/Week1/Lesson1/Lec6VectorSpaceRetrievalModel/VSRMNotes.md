# Notes on the Vector Space Retrieval Model (VSRM)
**This is a continuation of the previous lecture on Vector Space Models. A particular approach to creating a ranking function. VSRM is the simplest Vector Space Model to implement**

## Note
Remember the theory of a "Vector Space Model" (VSM) is a framework with many things left undefined. It does not say:
    how to define demensions of the vector
    how to place a doc or query vector
    how to measure similarity between doc and query vectors (similarity function)
    the query or doc weights
To be able to successfully implement a VSM, these questions need to be defined and answered for the computer.

## How to implement VSM via VSRM

### Dimension Instantiation via Bag of Words (BOW)
Use each word that defines vocabulary (N) to define the deminsions of the vector space. Since there are N words in the vocab, there are N dimensions in the vector space.
This is the standard implementation of BOW
 
### Vector placement via Bit Vector
Bit vector represents both docs and queries. x = query and y = doc
x_i,y_i element of {0,1}
Each coordinate is only either present or absent.
1 if the term appears, 0 if it does not. just a "bit"

### Similarity instantiation via Dot Product
For each word, multiply query weight by doc weight and then add those products.
q   = the query vector
d   = the docs vector
x_i = query weight, generally (x_1 = the weight of the first instance of that vocab word in the doc, so on and so forth)
y_i = doc weight, generally   (y_1 = the weight of the first instance of that vocab word in the doc, so on and so forth)
N   = number of vocab words

**see DotProductEquation.png**
Put all these together and you have a ranking function. The pictured equation is that ranking function.

### See the lecture in coursera for an example in action

