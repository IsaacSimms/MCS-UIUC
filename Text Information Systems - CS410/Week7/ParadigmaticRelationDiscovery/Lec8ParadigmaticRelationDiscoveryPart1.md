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

## Expected overlap of words in Context
*Basic similarity function used to comapre two context vectors*