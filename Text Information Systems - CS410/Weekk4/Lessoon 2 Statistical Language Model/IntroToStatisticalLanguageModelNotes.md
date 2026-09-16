# Statistical Language models
Modeling text data with probabilistic models (modeling query based on document)

## statistical langauge model
- "A probability distribution over a sequence of words"
- p = probability under this context
- Every possible string is assigned a numeric value for p.
- This value is **context-dependent** "order and neighboring words change probability"... the topic of the text and language used also are factors
- p("Today is Wednesday") is much more probably then p("Today Wednesday is")
    - p("Today is Wednesday") = 0.001         (approx values) (gramattically correct and common sequence of words)
    - p("Today Wednesday is") = 0.00000000001 (approx values) (grammatically incorrect)
    - p("The eigenvalue is positive") 0.00001 (approx values) (grammatically correct but less common phrase)
- This is a probabilistic model for "generating" text, (although crude)

### usefulness of language models
- ability to quantify uncertainties in natural language
- speech recognition and token prediction/generation
    - given that the first two words are "John" and "feels" what is the likelihood the next word is "happy" vs "habit. 
        - these two words are similar sounding, but these models can parse them and produce likely hood of one vs the other based on dataset
- language models are helpful in information retrieval as well

### Unigram LM (simplest language model)
- generates text by generating each word independently from each other
    - the probability of a sequence is the product of each word
    - p(w_1,w_2,w_3...w_n) = p(w_1)p(w_2)p(w_3)...p(w_n)
- Parameters: we have a probability for each word as a parameter, and all probabilites must sum to 1
    - {p(w_I)} p(w_1) + ... + p(w_n) = 1
- The text in question is drawn ("generated") are drawn according to the word distribution

#### Turning a document into a unigram LM using Maximum Likelihood Estimator (MLE)
- d                         = the document (w/ word count)
- c(w,d)                    = how many times w appears in d
- |d|                       = total tokens in d
- theta                     = the unigram model (one probability per vocab word)
- p (w | theta) or p(w | d) = estimated probability of drawing a word (w) from that document's model

**p(w | theta) = p(w | d) = c(w,d) / |d|**

### LMs for topic representation
Given a set of text input, the term likehood can be determined

Say the model is given general background english text:
- structural words will still rank the highest (the(0.03), a(0.02)...)
- then common words will rank next (food(0.003), computer (0.00001)...)
- Then uncommon words will get ranked much lower then all other words

But, you could also give the langauge model computer science papers as the dataset instead:
- structural words wills still rank the most commoon
- there will then be a block of common words. but, common words like computer(0.004) or software(0.0001) will rank much higher then other common words
- the distribution at the tail end of extremely uncommon words will still exist

### LMs for association analysis
Figuring out what words are semantically related to one another. 

Let's say you want to do this for the word "computer"
intake dataset is a collection of documents containing the word computer. The topic for the LM would be p(w|"computer")
- structural words are going to fall at the top of this distribution still, as they are closely associated with all words, since they are everywhere. 
- But, that middle section of the distribution will have comptuer's probability in that collection of docs (0.004)
- along with a group of common-to-uncommon words who's probability is associated with computer such as software(0.0001)
  
### using LMs to get rid of structural words in these analysis's
- A background english text model can be used to determine what words are common in general. filter out those words
- then you can take the model analyzing the dataset of documents containing the word computer
- take the ratio of these two probabilities. The words that you are looking for such as (computer) and (software) will be produced