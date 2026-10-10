# Text Representation and Enabled Analysis
Different representation layers enable different analyses.
- Word-sequence (BOW) representations are a practical sweet spot.genera enough, robust enough, and powerful enough for *most* tasks.

| Representation         | Generality / Robustness | Enabled analysis                               | Example applications                                                     |
| ---------------------- | ----------------------- | ---------------------------------------------- | ------------------------------------------------------------------------ |
| Character string       | Highest                 | Stream processing only                         | Compression                                                              |
| Sequence of words      | High                    | Word relations, topic analysis, sentiment      | Thesaurus discovery, topic mining, opinion mining, business intelligence |
| + Syntactic structure  | Medium                  | Graph analysis on parse trees                  | Stylistic analysis, authorship classification                            |
| + Entities & relations | Lower                   | Knowledge-graph / information-network analysis | Entity-centric knowledge aggregation, multi-source integration           |
| Logical predicates     | Lowest                  | Large-scale inference                          | Knowledge assistants                                                     |

**Note: This course is focusing on the "Sequence of words" level of text representation, which is the most common text representation in text mining.**

It is the workhorse because:
- Relatively easy and accurate
- minimal manual effort
- effective for a wide range of mining tasks
- statistical methods built on them generalize accross languages and domains.

