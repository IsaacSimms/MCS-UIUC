# Mining a single topic in probabilistic topic models

## Definition
The simplest topic model = one document and one topic. 
- you are only looking to discover the single word distribution (theta)
- Input = C = {d}, V 
- Output = {Theta}
A distribution p(w | Theta) over the vocab
- The doc is 100% covered by the one topic

## Language Model Setup
*The formal definition of the unigram language model which is the topic*
See Text Information Systems - CS410/Week8/ProbabilisticTopicModels/LanguageModelSetup.png
- Data = the document is a sequence of words from a mixed vocabulary
- Model = the topic (theta) is a set of probabilities p(w_i | theta) which sum to 1
- Likelihood = the probability of the document under is under that topic (product of the word probabilities)
- ML Estimation goal = finding the theta that maximizes that likelihood that the doc is under the topic (finding the topic that this doc is actually associated with)

## Computation of Maximum Likelihood Estimate
Remember, in single topic probabilistic topic models:
- we maximize the likelihood (or equivalently the log-likelihood) of the document under theta.
- The constraint is that the Theta_i sum to 1.
- The solution turns out to be normalized counts.