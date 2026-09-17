# Begin discussion of smoothing as it relates to Statistical Language Models
Take another look at "Text Information Systems - CS410/Week4/Lesson 2 Statistical Language Model/RankingBasedOnQueryLikelihood.png"

### We want to know, how do you estimate p(w | d)
- Use the maximum likelihood estimate
Normalize the word frequencies in the document
p_ml(w | d) = c(w, d) / |d|
    c = word count

## Smoothing LM
In order to assign a non 0 probability to words that have not been observed in the document we have to take away some probability mass from the words that ARE observed in the document.
  - That extra probability mass is assigned to the words that would otherwise not have any
  - p(w | d) *even if* c(w,d) = 0

- Question becomes, what probability should be assigned to the unseen words?
    Let the probability of an unseen word be proportional to its probability given by a reference LM
        Common here: Reference LM = Collection LM
see "Text Information Systems - CS410/Week4/Lesson 2 Statistical Language Model/Smooth_A_LM.png"
    - a piecewise equation to act as a template. Two cases: the word occurred in d (p_seen(w | d)) or it did not (alpha_d p(w | C)

### Rewriting the ranking function with smoothing
substitute the piecewise p(w | d) into the ranking function and split the sum
"Text Information Systems - CS410/Week4/Lesson 2 Statistical Language Model/RewriteRankingFunctionWithSmoothing.png"
