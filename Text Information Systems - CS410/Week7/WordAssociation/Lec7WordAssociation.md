# How to mine associations between words from text
*Knowledge about the natural language*


## Definitions
- Paradigmatic relation: Two words can be substituted for each other without breaking the sentence.
Both a & b would belong to the same semantic or syntactic class
Examples: cat <--> dog or Monday <--> Tuesday

- Syntagmatic relation: Two words can be combines in a sentence
They are semantically related but not interchangable
Examles: cat + sit or car + drive

- These two relations are basic and complementary. The ideas generalize to any sequence data.

## Why it is useful
- Building relations provide direct knowledge about the language itself
- Improves the outcome of NLP tasks (particularly when lexical knowledge is needed)
- Supports grammer learning 
paradigmatic gives word classes. Syntagmatic gives how classes combine
- They are useful for applications of TR and mining
Text retrival: know and suggest word associations to anticipate variations of a query.
Automatic construction of topic maps. (words are nots and associations are edges)   
Compare and summarize opinions (are positive or negative words about 'battery' are present in reviews about new iphone.)

## How to mine word associations (basic idea, no algos)
- Statistical and context-based (word-sequence representations, seen in previous lectures)
- Paradigmatic: found by comparing context distributions. What woulds show up before, after, in the same sentence, etc.
Compare that between words. i.e. if the same words show up before and after the words "cat" and "dog" it is likely that those two words are paradigmatic. 
- Syntagmatic: found by measuring co-occurrence strength.
What words tend to occur to the left and right of word 'x'?