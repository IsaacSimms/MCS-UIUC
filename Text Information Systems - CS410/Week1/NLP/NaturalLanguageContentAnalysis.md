### Natural Language Content Analysis is the first step to processing data.
# Three things covered in this lecture
1: what is natural language processing? (NLP)
2: State of the art of Natural  language proccessing
3: NLP for Text Retrieval

## What is NLP?
Prof used anaology: think about if you came accross some text in a langue that you don't understand, and you need to do "processign" in order to understand that text
in a language that you understand. This is what computers are having to do.
"A dog is chasing a boy on the playground" - humans are going to be able to read and understand that without any issues.
But, a computer is going to has to do multiple steps to decipher what is going on. 
### Lexical analysis
I.e. it assigns tags to each phrase /token from a finite tagset.
It scores each word against patterns learned from human-labled text.
The computer is using something called an annoted corpora as the source of truth on this. A collection of text that humans have labeled with extra information outside
of just the raw text. (millions of tokens have been annoted in this way)
**"Part of speech tagging" is another word for this. Dog is a noun, chasing is a verb, etc. Syntactic categories**
### Syntactic Analysis (parsing)
Figuring out the structure of the sentence. A and a dog does togother to form a "noun phrase"
See the carrots in the picture example in this directory. Noun phrase here in "A dog"... "is chasing" is a complex verb and "a boy" is a noun phrase, but those two things
get combined into a verb phrase. And the whole thing is getting combined into a sentence.
PArsers (a program) are doing this step
### Semantic Analysis
Humans are mapping whe phrase to what we know in our knowledge base in our brains to develop understanding. 
Computers are denoting the meaning of the phrase by assigning symbols to the pieces of it. (Dog = D1)
### Inference
Once understanding of provided text is determined, making analysis and "inferring" more information about the content.
In the provided example, the boy is scared.
#### Pragmatic analysis
Analyzing the user, why this sentence was said / provided in the first place.
Could be inferred the user said this sentence to the owner of the dog in an attempt to get the owner to control their dog.

### NLP Notes
Humans have a large, "baked in" natural language knowledge base. Computers do not
Natural language is designed for making human to human communication efficient. this adds complexity/challenges for a system.
    word overloading is common and contextual in natural language
    common sense knowledge is often omitted.
    we keep and communicate ambiguities, with the assumption the receiver is able to quickly and effortlessly decipher them.
    Meaning: ambiguity can be a "Killer"
    reasoning about human common sense / cultural differences / etc. is required for a performant system.
    Examples:
        Word level:
        - "root" has many different meanings based on context
        - "design" can be a noun or a verb based on sentence structure
        Syntactic level:
        - Phrases can be interprated two completely different ways. There is "langauge processing that is natural" or "there is natural language that is processsing"
        - "A man say a boy with a telescope" who had the telescope? 
        Anaphora resolution
