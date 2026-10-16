# Two-component mixture of unigram language models to mine one topic
This topic to be mined from one document while factorin gout background words.

## The problem
A single unigram MLE on a document is going to assign a high probability to frequent words. 
Many frequent words are function words such as 'a' or 'the'. (these words dominate a distribution regardless of topic). This does not properly represent a topic.

## Solution
"The distribution does not need to explain all words/common words"
Use two unigram distribution models to account for the common words.
- Topic model (Theta_d):
Captures the document specific topical content.
Attempts to exemplify the content-carrying words that characterize the theme of 'd'.
- Background model (Theta_B):
Captures common, non-topical words shared across documents.
Exemplifies high frequency function words and gen vocab.
Usually fixed in advanced (estimated once on a large collection or assumed known). Then worked into many mining contexts.

## Generative process
For each word in d (the document):
1. Choose component with probability p(Theta_d) or p(Theta_B) (p(Theta_d) + p(Theta_B) = 1)
2. SAme the word from the chosen unigram

In english:
The model doesn't assign a single probability to a word. 
There are two possible sources for every word:
1. the topic distribution (theta_d)
2. the background distribution (theta_B)
Before any word is generated the model "flips a coin" (i.e. the "Topic choice") to decide which source will be used for that word.
Once the source is chosen, the word is drawn from that source’s unigram.
So the probability of seeing a particular word (say “the”) is the sum of the two mutually exclusive ways it could have been produced:

Chose topic and then drew “the” from theta_d
Chose background and then drew “the” from theta_B

That can be thought of as the following:
P("the") = p(theta_d)p("the" | theta_d) + p(Theta_B)p("the" | Theta_B)

P("the")
= 0.5 * 0.000001
+ 0.5 * 0.03
= 0.0000005 + 0.015
= 0.0150005