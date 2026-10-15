# Two-component mixture of unigram language models to mine one topic
This topic to be mined from one document while factorin gout background words.

## The problem
A single unigram MLE on a document is going to assign a high probability to frequent words. 
Many frequent words are function words such as 'a' or 'the'. (these words dominate a distribution regardless of topic). This does not properly represent a topic.

## Solution
"The distribution does not need to explain all words/common words"
Use two unigram distribution models to account for the common words.
- Topic model (Theta_d):
Caputes teh document specific topical content.
Attempts to exemplify the content-carrying words that characterize the theme of 'd'.
- Background model (Theta_B):
Captures common, non-topical words shared across documents.
Exemplifies high frequency function words and gen vocab.
Usually fixed in advanced (estimated once on a large collection or assumed known). Then worked into many mining contexts.