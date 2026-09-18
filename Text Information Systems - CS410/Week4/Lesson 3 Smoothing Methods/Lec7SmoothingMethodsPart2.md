## Ranking Function with JM Smoothing
**See "Text Information Systems - CS410/Week4/Lesson 3 Smoothing Methods/RankingFunctionForJMSmoothing.png"**

- Line 1: Is a generic written query likelihood
- Line 2: Ranking function with JM definition.
This is what gets plugged in and alpha_d = lambda

- Line 3: algera after that plugin lambda for alpha_d

(because we are using Lambda to smooth by definition)
( Notice that you do not need the +log(alpha_d) after Lambda is subbed in. Lambda is the same for every doc)

Final Result: 
**(P_seen(w|d) / alpha_d P(w|C) = 1 + (1 - lambda) / lambda * c(w,d) / (|d|p(w|C))**

raw TF, divided by the doc length, divided by how common the word is in the collection. Essentially TF-IDF

- Line 4 subbing what we just built back into the ranking function
    - (|d|p(w|C) means the length of the document |d| multipled by the probability of the word given by the collection. The given count of a word.
    - This makes c(w,d) / (|d|p(w|C) give you the words relative frequency in a document divided by how common the word is in the collection.
        if the word is much more common in the document then in the rest of the collection, that will return larger then 1? vice versa, that value becomes less then 1

## Ranking function for Dirichlet Prior Smoothing
- Similar to same logic the flow of using JM smoothing in a ranking function
- **see "Text Information Systems - CS410/Week4/Lesson 3 Smoothing Methods/RankingFunctionWithDirichletPriorSmoothing.png"**
- Other then, much like previously discussed, mu is used in replacement to signify the use of baseline tokens
  

- Line 1: Is a generic written query likelihood
- Line 2: Ranking function with Dirichlet Prior definition.
This is what gets plugged in and alpha_d = mu

- Line 3: algera after that plugin mu for alpha_d. Final result:
**P_seen(w|d) / alpha_d P(w|C) = 1 + c(w,d) / mu p(w|C)**

- Line 4 subbing what we just built back into the ranking function
    - Note that with the subbing of alpha_d for mu, due to DP's logic the following must get subbed to replace alpha_d: mu / mu + |d|
        Therefore, in the final ranking function, the final + n log cannot be ignored and must look like n log(mu / mu + |d|)
