# Document Length Normalization in the  Vector Space Model

### note
Come back to that query = "news about presidential campaign" example

If doc4 has "news, presidential, presidential, and campaign" over the course of 100 words
and doc6 has "campaign, campaign, news, news, presidential, and presidential" over the course of 5000 words
Then, the differences in doc size should be taken into consideration when determining the likeness score of each doc.
    doc6 has more likeness if you where to look at an TF-IDF function with not TF transformation or doc length normalization.
    Employing tf transformation (lec2) does help balance the likeness score, but still does not account for the fact that doc6 is much longer, and therefore had many more opprotunities to use like terms. 
        "In doc6, the length suggests that the use of campaign at the beginning of the doc may have nothing to do with the use of presidential at the end"
"If you where to generate an extremely long document attempting to contain all the words in a vocabulary, eventually you would match any query"

## Enter Document Length Normalization
- Given the above, we want to penalize long docs with a doc length normalizer
    But, you want to make sure to avoid over-penalization
- Framing: dissect why a doc is long:
    A doc is long because it uses more words  = more penalization 
        (an entire research paper is going to simply contain more words and not me more similar to the query then the abstract for that same paper)
    A doc is long because it has more content = less penalization
        (let's say a single doc is the concatenation of multiple abstracts from different papers)
- **Pivot length normalizer**:
    A method for navigating this problem.
    The pivot is the doc length at which you apply no length penalty and no length bonus to that document.
        Any doc longer then the pivot gets a penalty. Any doc smaller then the pivot gets a bonus.
    Generally, the average doc length in your collection.
    The normalizer(pivot) = 1

## State of the Art VSM Ranking Functions
Reference "Text Information Systems - CS410/Week2/Lesson1/Lec3DocLengthNormalization/VSMRankingFunctionsIncludingDocLengthNormalization.png"

### The pivoted Length Normalization VSM
after the c(w,q) you have a numerator and a denominator
    The numerator is the TF transformation function.
    The denominator is the document length normalization function
        If you take a look at "/home/isaacsimms/Desktop/MCS-UIUC/Text Information Systems - CS410/Week2/Lesson1/Lec3DocLengthNormalization/PivotedLengthNormalization.png"
        You will see that the doc length normalization function is controlled by b. 
            If b is set to zero, there will be no normalization that occurs.
            The larger b is as compared to zero, the more normalization will occur

### BM25 and comparison
As you compare BM25 ranking function to the Pivoted length normalization function you will notice that both of these functions have the same IDF function within them.
    log M + 1 / df(w)
And, they both have a raw count of the query
    c(w,q)

However, the TF transformation and the Doc length normalization functions are different in BM25 as compared to the pivoted length normalization VSM

Still, after c(w,q)
    The entire numerator "(k + 1)c(w,d)" and the first half of the demoninator "c(w,d) + k" act as the TF transformation function
    The rest of the demoninator "1 - b + b (|d|/avdl)"

## Further improvements to VSM
### Further improvement to the instantiation of the dimensions in VSM
Remember, up until now we have been using a "Bag of Words" instantiation where each word in the vocabulary is a dimension of the vector space.
Further dialing in of this practice could include things like:
    Stop word removal: removing stock words from the vector space all together
    Stemmed words
    using phrases to define vector space
    Latent semantic indexing: using word clusters to define vector space
    Use character n-grams: define vector space with a sequence of chracters rather then terms
**However it has been found that in practice,   bag of words is sufficient for a large majority of use cases.**
    But note: sometimes language specific or domain specific tokenization is required to ensure a well-weighted "normalization of terms"

### Further improvement to the instantiation of the similarity function
remember, up until now we have been using dot product as the similarity function.
    Note: dot product still seems to be the best practice core function to determine similarity. Especially when terms are weighted appropriately.
    This is partially because dot product is incredibly general, and terms can be weighted in different ways. 
Euclidean and cosine of angle between two vectors are possible additions.

### Further improvements to the BM25 function as a whole
#### BM25F
BM25 for docs with structures
Combines the frequency counts of terms in all fields then apply BM25 (instead of the other way around)
Avoids overcounting the first occurrence of a term. 
#### BM25+
Adds a small constant to the TF
Addresses the problem of over penalization of long documents.
Shown to be better then vanilla BM25 in a lot of ways. 

