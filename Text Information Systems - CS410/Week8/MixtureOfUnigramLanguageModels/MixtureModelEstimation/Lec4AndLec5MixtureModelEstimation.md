# Why Maximum-likelihood estimation works
Remember: 
There are two word distributions when using a Mixture model Estimation.
- A topic distribution (Topic words you are looking for)
- A fixed background distribution. (covers common words)

Goal: Adjust the topi9c distribution to make observed document as likely as possible.

## The interaction
- They collaborate: both contribute to explaining the words, so together they raise the likelihood.
- They compete: probability mass is limited (everything in a distribution must sum to 1). 
Giving mass to one word means taking it away from another.
Result: the topic ends up claiming the words the background explains poorly (content words) and avoids the words the background already covers well (function words). 
This is why common words get factored out.

## Data (word) frequency
If a word appears many more time sin the document, the topic is pulled to give it a higher probability.
This is because each occurrence mutliplies the likelihood. 
**HOWEVER**
That pull is limited by the competition between the two distributions. 
If the background distribution already explains that word well, the topic distribution does not raise the probability.

## Three core behaviors under this MAximum Likelihood Estimation (MLE) model
1. Every component tries to put high probability on frequent words in the data
2. Different components tend to specialize on different words
3. The mixing weight controls how strongly each component responds to the data