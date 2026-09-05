# Sublinear Term Frequency TRansformation (change weight based on term frequency)

### Note:
This is a continuation of the TF-IDF architecture.
    TF-IDF Scores alikeness on how many documents contain a term and weather that term was stock or not.
    Doing so solved a lot of problems. Documents that spam the key word 50 times are going to get  10x the weight as compared to a document that has that same key word 5 times. 
        However, documents that have a very rare key word 5 times is likely to be just as relevant to the document with the key word 50 times.

## Intro
take a look at "Text Information Systems - CS410/Week2/Lesson1/Lec2TFTransformationNotes.md/TF-IDFWeightedRankingFunction.png"
    **This is a ranking function with TF-IDF implemented but npt yet Term frequency Transformation**

Notice the "c(w,d)" section
    c = count (number of occurrences)
    w = word or the term in question)
    d = document in question

Together, c(w,d) means the raw count of that word in the document.
If a document had an uncommon term in it, the likeness score would go up the same amount with every additional instance of that term. Giving it an unfair ranking profile.
    The first instance of a term says *a lot* about the likeness of a document to a query. 
    However, the 100th instance of a term does not tell you anything about the likeness of that document that the other 99 instances of that term has not already described.

## Enter Tf Transformation
This function turns the raw count (c(w,d)) of a term in a document into a **term frequency weight** (TF(w,d))

In "Text Information Systems - CS410/Week2/Lesson1/Lec2TFTransformationNotes.md/TFTransformationGraph.png"
    The x axis is the raw count of the word.
    The y axis is the term frequency weight.

A bit Vector (remember week 1) is going to have a 0 or 1 weight. If the count is 0, the term has zero weight. If the count is 1, the weight is one. 
If we where going to use raw count for the TF-IDF ranking function, without TF transformation, as previously described, that would be a linear function with y = x. One instace of word gets one weight.

What we want for our term frequency part of our ranking function is something like this: **y = log(1 + x)**
Lowers the inference of really high weight but retains the inference of very low weight

If the use case in question required an even steeper bend to the curve you could use log on it twice: y = log(1+log(1+x))

### The BM25 Transformation
Current best practice / known function for Term Frequency Transformation (used in BM25)

**y = ((k + 1)*x / (x + k))**
remember,
    x is the raw count of the word
    y is the term frequency weight
k is the "saturation parameter"... meaning how quickly the weight curve flattens over time and how high it is allowed to go.
    Note: when this function is actually being used, k is a defined variable.
        If you set k = 0, you literally have a bit vector.
        When you set k to a very large number, you will get closer and closer to a linear function as that number increases.

if x(count) is zero, weight is still zero
If x is 1, weight is still one. 
However as x grows infinitely, the weight approaches k + 1 and eventually stops growing all together.