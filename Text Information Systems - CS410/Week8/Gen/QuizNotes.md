- Understand Unigram langauge models and how you would find the value of P(w | Theta)
Multiply the P(w|Theta) values of each w together

- Understand mixture models
Mixture models assign high probability on different words beucase it gives an overall likelihood.
In a mixture model (e.g., mixture of unigrams), each component is a separate distribution over words. 
The training objective (typically EM) maximizes the likelihood of the observed documents.
If two components assign high probability to the same words, they are largely redundant.
Remember that in Unigram language models, a valid probability distribution must sum to 1.

- EM Algorithm (Expectation-Maximization)
An iterative algo for maximum-likelihood estimation when the model has latent variables.
It essentially alternates between two steps until convergence:
1. E-Step: given the current parameters, compute the posterior distribution over the latent variables.
(i.e. the soft assignment of each data point to each component)
2. M-step: given those posteriors, re-estimate the parameters to maximize the expected complete-data log-likelihood.

