# Paradigmatic relation discovery
*how to find paradigmatic relations*: when two words share similar context by having similar positions in text

*method*: collect the contexts of each candidate word **Pseudo document** --> 
represent each context as bag of words --> 
compute similarity between those context representations

## Context representation
- Known as *Pseudo document*
- The context of a single word can be defined in several ways within a pseudo doc:
    - Left1 = only collect one adjacent word left to candidate word
    - right1 = only collect one adjacent word right to candidate word
    - left1/right1 = collect one to the left and one to the right
    - Window8 (plus/minus 8) = look at a fixed window of 8 words on the left and right of the candidate word.
    - etc.

### measuring context similarity
Sim("Cat", "Dog") = Sim(Left1("cat"), Left1("dog"))
                  + Sim(Right1("cat"), Right1("dog"))
                  + …
                  + Sim(Window8("cat"), Window8("dog"))
- left1/right1 = tight syntactic and local semantic discovery
- window8 = captures broader topical relatedness
- ... = this is a spectrum

## Vector space model
**Each context view (bag of words) is itself a bag of words, turned into a vector, and compared with a similarity function**
- Each bag of words (pseudo doc) defines one dimension in the vector.
- Context = a vector whose components are frequencies/probability of context words. Meaning, similarity of two contexts is the similarity of their vectors. (this is the same vector-space idea used for docs/queries)

## Expected overlap of words in Context (EOWC)
*Basic similarity function used to comapre two context vectors*

1. How do you compute each vector?
x_i = c(w_i, d1) / |d1|
y_i = c(w_i, d2) / |d2|

- c(w_i,d) = raw count of word w_i in the given context
- |d| = total number of word occurrences in the context
- x_i = the probability that a randomly drawn word from contexr d1 is w_i

2. How do you compute the similarity?
Sim(d1, d2) = d1.d2 = x_1 y_1 + ... + x_n y_n

**Interpretation:** probability that a word is randomly picked from d1 and a word randomly picked from d2 are identical. High value means the two contexts contain similar words in similar proportions.

### Two problems with EOWC
- Frequency dominance: matching one high-count term contributes far more then matching several lower-count terms
- equal treatment of words: a stock word like 'the' receives the same weight as a content word

### fixes
*adding heuristics*
- sub-lienear TF transformation: fixes the frequency dominance problem. (BM25-style transform)
Replace raw counts of the words with a function that grows slow as num of words increases.
- IDF Weighting: Fixes equal treatment of words problem.
Multiple by inverse doc frequencies of the word so rare context words contribute more then common ones

#### TF transformation (BM25)
*down-weights terms that occur a lot*
- Start near-linear for small counts
- asymptotically approaches k + 1 as count grows
- 'k' controls the saturation point

**the BM25 curve**: y = (k + 1)x / x+ k

#### IDF weighting
*down-weights terms that appear in many docs*
IDF(w) = log((M + 1) / k)
- M = total number of docs (or pseudo docs) in collection
- k = number of docs that contain term
- when k = 1, IDF is maximal
- when k approaches M, IDF approaches 0

Therefore, the curve falls quickly then flattens. A term that occurs in every doc contributes almost nothing. 
A rare term contributes a large multiplier.

#### IDF Weighting and TF Transformation recap
- paradigmatic: comapre two vectors (Dot product). High similarity --> substitutable words
- Syntagmatic: look inside one vector. High-weighted terms --> words that co-occur with the target
- dual use of the same weighted context vector