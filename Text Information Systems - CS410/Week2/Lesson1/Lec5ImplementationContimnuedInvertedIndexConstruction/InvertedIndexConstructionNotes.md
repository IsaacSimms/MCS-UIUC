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