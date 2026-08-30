### Natural Language Content Analysis is the first step to processing data.
# Three things covered in this lecture
1: what is natural language processing? (NLP)
2: State of the art of Natural  language proccessing
3: NLP for Text Retrieval

Refer to TextDataProcessingWorkflowBasic.png... NLP is the first thing that happens to a big dataset of text in our workflow.
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
We can do this part pretty well, approx 97% accuracy
### Syntactic Analysis (parsing)
Figuring out the structure of the sentence. A and a dog does togother to form a "noun phrase"
See the carrots in the picture example in this directory. Noun phrase here in "A dog"... "is chasing" is a complex verb and "a boy" is a noun phrase, but those two things
get combined into a verb phrase. And the whole thing is getting combined into a sentence.
Parsers (a program) are doing this step
We can do partial parsing pretty well, about 90% accurate (by partial, we mean some portion of the phrase) But, complete parsing is incredibly difficult
### Semantic Analysis
Humans are mapping whe phrase to what we know in our knowledge base in our brains to develop understanding.
Computers are denoting the meaning of the phrase by assigning symbols to the pieces of it. (Dog = D1)
Precise and deep semantic analysis is very difficult. 


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
            Anaphora resolution is the process of finding what a referring expression points back to. "JOhn persuaded Bill to buy a TV for himself" Is himself john or bill?
            Presuppostion background information that is not referred to by the speaker, and is assumed already settled
        Inference is still difficult. Don't have complete semenatic understanding is a bottleneck.
The difficulties with NLP tends to leave modern, robust NLP able to process large amounts of text in a "shallow" way. But, analyzing text in a "deep" way does not work at almost any scale. Scaling can mean here in amount but largely means the complexity of the text itself. Has to do with ohw similar the text is to the
training data.

Use NLP by machines to:
Entity extraction:  finding spans in text that refer to real world things, their labeling and/or relationships. (some entities are harder then others)
Disambiguation:     Figure out if a specific word in a specific context has a certian meaning. (and may have a different meaning if the context where different)
Sentiment analysis: Figure out meaning of a phrase, in the total sense of the world, to determine if that phrase is positive, negative, sad, etc.

## NLP for Text Retrieval
**For NLP to work in text retrieval it needs to be general, robust, and efficient. Meaning, the NLP needs to be shallow (text is similar to training data)**

The **bag of words** (BOW) implementation of NLP is the common use case in text retrieval for search tasks. (there are others, but BOW is the simplest)
In BOW, order is thrown out. What matters to this process is which words occur and how often.
Makes it harder to understand the meaning of a phrase but lets say you are doing a search. If there are bunch of uses of a word in an article, same word the user
is asking about, chances are that article is what the user is asking for.
Search engines are using it.
Things like machine translation, that requires the structure, does not work with BOW.
### Some text reterival methodologies fix issues with basic NLP implementation
Looking at BOW again, and the word java, an ambiguity has arisen where it could not be understood if the user meant the coffee or the programming language. But
when compined with the word applet, which is a text retrival problem at that point, it becomes unambiguous the user meant the programming language. 
Relevance feedback: Couple different implementations but essentially, relevant / non-relevant hits of a query are accounted for and used to produce better semantic matching. 

### Complex NLP| for Text retrieval
Knowledge graph = at a basic level, it is a set of typed (in the programming style, although not literally) entities plus typed relations between those entities.
That set of entities and connections is then what is searched to produce a result to a query.