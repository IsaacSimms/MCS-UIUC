# Text Categorization Methods
There are two main methods. 

## Manual methods
Determine category based on some rules that are carefully designed. (External to the system)
Reflect the domain knowledge about the categorization problem.

Works well when:
- categories are well defined
- categories are easily distinguided based on surface features in text (things like keywords or punctuations are identified in text data easily)
- sufficient domain knowledge is available

Limitations:
- expensive
- doesn't scale
- labor intensive
- can't handle uncertainty well

## Machine-learning methods
### Human/agent/external system has to supply two things
- training data (a set of text objects labeled with correct categories) 
The training data is very important. Quality of training data is quality of text categorization system.
- a set of features that may help distinguish categories (words with unusual starting points, tags, phrases, special punctuation, etc.)

### ML then
learns *soft rules*. Figure out which category should be assigned to document, but not through a rule which is deterministic.
- instead of categorization in absolutes, probabilities or weights are used (this doc has x likelihood of being about sports)
- The ML architecture should figure out which features are most useful for seperatign different categories and optimally combining features to minimize errors.
- trained classifier must be able to be applies to new text object to probabilistically categorize object.

## generative classifiers
"learn what the data "looks" like in each category. 
Model the distribution fo text given in each category (and the prior categories) to obtain the probability of the category given the text.
- Naïve Bayes is an example
- objective function is likelihood, thus indirectly measuring training errors

## Discriminative classifiers
Directly model (or optimize) the mapping from features to category labels.
Objective focuses on separation rather then on generating the data.
- logistic regression, k-nearest neighbors, SVMs