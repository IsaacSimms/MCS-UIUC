# Notes from taking the quizzes in week 4

- Given a set of vocabulary, what are the probabilities of a fraction of the words given by unigram language model:
Remember, all probabilities sum to 1

So if you are given 3 words, text = .4 and mining = .2, research must = .4 (for each word's probability)

But, there's a unigram assumption that each word draw is independent of the others. So to figure out the probability, those values need to be multipled together:
.4 * .2 * .4 = **0.032**

Understand what happens when you add JM smoothing to this same type of question **(I need to review this)**

- maximum likelihood estimitations with and without smoothing
    understand that probability smoothing avoid assigning zero probabilities to terms and breaking equations.

- JM and Dirichlet Prior smoothing.
    What happenes when lambda or mu are increased/decreased in the respective assumptions
    Review what happens when words double in a document **(need to review this)**

- In scoring functions
  log is strictly increasing on (0,1]
  P(Q|D) and log(P(Q|D)) are going to produce the same RANKING in a list of documents because log controls numerical stability (product of tiny numbers) NOT the ranking order **only true of if P(Q|D) > 0**
  If P(Q|D) can equal zero (unsmoothed) then a scoring function without the log would give it zero and put it at the bottom. And, log(0) is not a real number.