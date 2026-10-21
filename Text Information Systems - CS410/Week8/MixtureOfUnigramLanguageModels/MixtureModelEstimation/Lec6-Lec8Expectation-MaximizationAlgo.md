# EM (Expectation-Maximization)
An iterative method for finding the maximum-likelihood parameters of a model when some of the data is hidden from it. 

In a mixture model the hidden part is which component (which distribution) generated each word in the end result. 
We cannot know those assignments before hand. The EM algo repeatedly guesses those assignments and then updates the parameters based on the guesses. 

## How it works
1. Start with a rough guess of the topic distribution
2. E-Step: For every word in the document, ask “how likely is it that this word came from the topic rather than the background?”
Use the current topic and background distributions to compute that probability (the word’s responsibility).
3. M-Step: Pretend those responsibilities are fractional counts. 
Recount the words, giving the topic only the fraction of each word that was assigned to it, and normalize to get a new topic distribution. 
4. Repeat steps 2 and 3. Each round makes the observed doc more probable under the model. Stop when the numbers stop changing. 