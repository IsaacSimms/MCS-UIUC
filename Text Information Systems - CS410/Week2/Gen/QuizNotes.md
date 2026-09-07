# Notes on what to take away from week 2 quiz

**Encoding d-gap to gamma code** Here is how you do that:
Let's say that the d-gap is 9
1. Binary of "9" 
    Remember, to convert a number to binary:
    divide the number by 2, record the remainder, repeat until the quotient (answer) is 0
    Remainders **bottom-to-top** are the bits
binary of 9 = **1001**
2. Drop the leftmost 1 (drop first bit = to 1) → offset, width "N".
1001 is now = to **001**
3. "N" ones + a single 0.
    Essentially however many bits you have, after the drop, that is how many ones you have. Then, add a zero on to the end.
    001 is 3 bits. So for this step, that is equal to 111... but then add a zero so:
the final answer is **1110**
4. Concatenate.
    Concatenate the results of steps 3 and 2, with step 3 proceeding step 2.
1110 + 001 = **1110001**

**Taking encoded gamma code  of term frequency and converting it into raw term frequency**
Weather you are looking at d-gap, term frequency, etc. it is still just taking ints and encoding it or decoding it via gamma code.
This is the same process as above, just flipped around. 
Let's say the given term frequency is 1110010
1. Read the ones until you get to the first zero. that is where you will break the concatenate
1110 | 010 
    (remember, left part is not part of the number. it tells you how many bits the number will still need. 010 is what we need)
2. Stick the leftmost one back on to the leftmost of the binary
010 = 1010
3. convert the binary to the int
    (remember, int to binary conversion involes dividing by 2 over and over.)
    You are essentially listing out the opposite of that, multiplications of 2, and adding up the places that have 1 in the binary
1 0 1 0
8 4 2 1
= 10
Therefore, the answer is **10**

Quiz touches on various theory topics such as:
    Importance of TF transformation
    Understanding BM25 formula architecture
    Document legnth normalization (pivoted and otherwise)
    Inverted Index knowledge at a high level
    Zipf's law
    Things like stop words and word segmentation

Dial in the complexities of inverted index. How document frequency contributes to things like disk space and accumulators
Note with accumulators:
An accumulator is a running score for a single document. 
When a query is getting scored over an inverted index, the score does not get allocated for every doc in the collection.
**One accumulator is allocated only when that document first appears in a query term's postings list**