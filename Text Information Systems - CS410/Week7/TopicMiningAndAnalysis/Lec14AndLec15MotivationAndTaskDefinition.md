# Motivation of topic mining

## Topic Mining
Topic mining is a common major task after word association mining. 
A transition from individual word relations to discovering main themes that organize a collection of text. 
summarizing large collections, browsing, supporting tasks such as sentiment analysis or classification

## Tasks of Topics  mining
1. Disover what topics (k) are in a collection of N documents
2. Determine the coverage of each topic in each document (how much each document is about each topic)

### Formalization
Input: Collection C =d_1....d_N documents
Num of topics = k
Output:
k = (theta_1....theta_k)
And coverage values pi_ij for each document (d_i) and topic (theta_j), where pi_ij is the probability that d_i covers topic theta_j

## Topic (theta) = Term
Topic theta = a term such as "Sports, travel, science, etc." Some TR style operations are performed on collection of terms to extract topic.


1. Discover topics: Extract each candidate term from the collection.
So that good topics are frequent enough to be representative but no so frequent that they are stop words.
TF-IDF is a natural scoring function here.
    This is the scoring function design.
    - Favor representative term
    - Avoid words that are too frequent.
    - include domain heuristics. favoring title words, hashtags in tweets, etc.
Take the top 'k' terms as topics
1. Compute coverage: For each document, set pi_ij (the coverage of topic theta_j in document_i) according to the presence or relative frequencies of term j in that document.

### Limitations
- A single term is often too coarse or ambiguous to represent a real theme
- coverage can be too brittle
- no natural way to capture related words that belong to the same topic