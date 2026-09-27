# Link Analysis in Web Search
You use the results of link analysis to improve search

## Ranking algorithms for web search
The information needs are different, docs have lots of info on the web, quality varies on web, etc.
- Standard IR models are applicable but insufficient to the needs of web search (but important foundational building blocks)
- This had lead to major extensions of traditional information retrieval to meet the needs of modern web search.
Using links to improve scoring.
Exploiting click throughs (analyzing what users click on and what they ignore) for implicit feedback.
Combining different methodologies through machine learning.

## Links
- Many links different pages together. (remember that wiki game? that can be played for portions of the web)
- Each link often has anchor text, which is a description of what that links. (query matches anchor text) (anchor text is a good reference for relvance of page the link is pointing to)
Types of pages as it relates to links:
- Authority: Lots of other pages point to it
- Hub:       Points to a lot of other pages
Assumption made about links:
Links are like citations in literature. If a page is cited often, it is expected to be more useful in general then a page that is never cited.

### PageRank
PageRank = a query-independent score of how much a *link graph* endoses a page. It is a ranking feature used with an inverted index. 
Essentially, a citation counting functionality that can be used with other IR behaviors. Accounts for things like indirect citation (a page being linked by a highly sited page will get some weight)
- Smooths citations (every page assumed to have a non-zero citaition count)

#### Random surfing model
At any page, there is some probability the surfer randomly jumps to another page or d factor probability it follows a link.
- d                 = damping factor, the probability the surfer follows an outlink instead of jumping
- Random Jumping    = with a probability of 1 - d the surfer ignores outlinks and teleports to a random page
- Transition Matrix = a matrix of values indicating how likely a surfer is to go from one page to another
M    = the **PageRank Matrix**. This is what you multiply by in power iteration
M_ij = the probability of going from d_i to d_j.

Random notes:
Pages with a lot of in links of a higher probability of being accessed.
The **Equilibrium Equation** computes the probability of reaching a page. That can be found in the PageRankAlgorithm.png.
**Normalization does not effect PageRank *ranking*, but it can effect total values, leading to variants in the formula**.
The zero-outlink problem p(di) doesn't sum to 1.