# How an Inverted Index is constructed

## Note
- Constructing an inverted index is relatively easy when the dataset is small
- Primary challenge is a huge index being made on a limited amount of memory
    Therefore, memory-based methods are often not usable on large collections

## Sort-Based Inversion
- So, when collection data cant fit on to memory (most datasets) there are multiple methods for sorting that data. Example:
    - collect local tubles (gather termID, docID, freq, for a small set of docs)
    - Sort local tubles to make runs. (sort those counts based on term to make a partial inverted index) (gets written to disk)
    - pair-wise merge runs (first two steps are done on all the data. Then they all get merged and put back on to disk piece by piece)
    - output inverted file

### First thing the Indexer does with the tokens: Lexicon
There is a term lexicon and a DocID lexicon.
A lexicon is a lookup table that turns strings into integers. They are used to create the IDs which identify each term in the doc, and each doc in the collection.
    - first, it produces a set of records for each term <termID, docID, freq>  sorted by docID
        Eventually, creating these records will run out of memory and you will need to write to disk.
            Before that happens, the records get reorganized to sort by term-ID
    - Next phase is a merge & sort
        All information about "term X" is in a specific group of the records

### Inverted Index Compression
Generally, for inverted index compression:
**leverage skewed distribution of values and use variable-length encoding.**

#### Term Frequency Compression (skewed distribution)
- use the assumption that small numbers tend to occur far more frequently then large numbers (zipf's law)
    Given that assumption, use fewer bits for small integers at the cost of more bits for large integers
#### Document ID compression
- **d-gap** = store the difference between documentID integers instead of the IDs themselves. Saves on space significantly
    Doc access is inherently sequential, making this a viable option

#### many different encoding methods
##### binary code
equal-length coding - every value uses the exact same amount of bits (so that defined number of bits needs to be able to hold the largest amount of bits possible)
appropriate for randomly distributed values
realtively simple

##### unary code
When x is greater than or equal to 1 it is coded as x-1 followed by a zero
(simply put, int x is coded as x number of ones plus a zero at the end, number of bits.)
3 --> 110 bits... 5 --> 11110 bits
Uses a huge amount of bits when the number is large, but uses a small amount of bits when the number is small.
Inefficient if there are large numbers possible but good for when there are only small numbers in the set getting compressed.

##### elias gamma code
look at the following slide for the math behind gamma coding "Text Information Systems - CS410/Week2/Lesson1/Lec5ImplementationContinuedInvertedIndexConstruction/IntegerCompressionMethods.png"
A combination of binary coding and unary coding. 
Code writes the integer in two pieces, how long is the number and leftover bits. 
Turn the number into binary and drop its leading 1.
What remains is the "leftover" and the length of the code is how many bits are present.
For example:
13 in binary = 1101
drop the leading 1 so the leftover is 101
To store 101 requires 3 bits.
Therefore, the length is 3
This is essentially using a unary prefix on the "leftover" in order to determine the length

Simple example:
“How many bits 5 uses” is 3 (101). Unary of 3 is 110. Stick leftover on the end:
110 + 01 = 11001     ← γ(5)

##### elias delta.
Delta coding uses the same "write number as bits, throw away leading 1, look at leftover for coding" methodology
However, instead of using unary coding on the leftover, it uses gamma coding on th leftover to produce the bits results.

### Uncompressing the inverted index
#### decode the encoded integers
- Unary decoding: count 1s until you see a zer
- gamma decoding
    k = how many leftover bits follow unary prefix
    First decode the unary section (this value = k+1)
    read k more bits, decode them as binary, let this value = r
    the decoded value of the encoded number is = to: **2^k + r

#### decode docIDs that where encoded using d-gap
Remember: d-gap encoded docIDs do not store the docIDs, they store the jumps between them. But, the first stored value *is* the first docID. 
Read the next integer (i.e. the gap) and add it to the value that you already have. 

Use sequential decoding (in this course at minimum)
The encoded ID list will be x1, x2, x3...
Decoding x1 obtains     docID 1... then decode x2 and add the recovered value to the doc that ID1 just obtained
Repeat this process to decode x3, x4, etc... add the recovered value to the docID that came immediately before it.
