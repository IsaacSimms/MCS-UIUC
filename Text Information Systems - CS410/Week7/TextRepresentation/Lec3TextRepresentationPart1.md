# Text representation
How natural language allows us to represent text in many different ways.
These different ways of text representations offer different levels of depth
- shallow (general and robust/reseliant)
- deeper (more analysis capabilities but more error prone, require more NLP, etc)

## Levels of representation shallow --> deep
- string of characters: most general, no semantic power (works for any language)
- Sequence of words: After word segmentation NLP. Words become the basic units of human communication.
enables counting, topic and sentiment identification, etc. Easy and reliable with languages like english.
- Sequence of words add part-of-speech tags: add syntactic category to words (noun, verb, etc). 
Enables things like noun-verb associations
- add Syntactic structure: a parse tree. Useful for style analysis and grammer checking.
- add Semantic analysis: entities and relations. (dog = animal, boy = person, chasing = relation)
- add Logical Representation: predicate and inference rules. Derived facts (mistakes common)
- add speech acts: intent of the text. 